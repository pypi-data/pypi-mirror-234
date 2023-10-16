import math
import multiprocessing
import multiprocessing.pool
import os
import time
from urllib.parse import urlparse

import requests

from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.auth import BearerAuth
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger, logger_no_user_data
from biolib.typing_utils import TypedDict, List, Iterator, Tuple, Optional, Dict


def get_chunk_iterator_from_bytes(byte_buffer: bytes, chunk_size_in_bytes: int = 50_000_000) -> Iterator[bytes]:
    chunk_count = math.ceil(len(byte_buffer) / chunk_size_in_bytes)
    for chunk_number in range(chunk_count):
        start = chunk_size_in_bytes * chunk_number
        stop = start + chunk_size_in_bytes
        yield byte_buffer[start:stop]


def get_chunk_iterator_from_file_object(file_object, chunk_size_in_bytes: int = 50_000_000) -> Iterator[bytes]:
    while True:
        data = file_object.read(chunk_size_in_bytes)
        if not data:
            break
        yield data


class RequestOptions(TypedDict):
    headers: Optional[Dict[str, str]]
    requires_biolib_auth: bool
    url: str


class _PartMetadata(TypedDict):
    ETag: str
    PartNumber: int


_UploadChunkInputType = Tuple[int, bytes]
_UploadChunkReturnType = Tuple[_PartMetadata, int]


class MultiPartUploader:

    def __init__(
            self,
            complete_upload_request: RequestOptions,
            get_presigned_upload_url_request: RequestOptions,
            start_multipart_upload_request: Optional[RequestOptions] = None,
    ):
        self._complete_upload_request = complete_upload_request
        self._get_presigned_upload_url_request = get_presigned_upload_url_request
        self._start_multipart_upload_request = start_multipart_upload_request
        self._bytes_uploaded: int = 0

    def upload(self, payload_iterator: Iterator[bytes], payload_size_in_bytes: int) -> None:
        parts: List[_PartMetadata] = []

        iterator_with_index: Iterator[_UploadChunkInputType] = enumerate(payload_iterator, 1)  # type: ignore
        logger_no_user_data.debug(f'Starting multipart upload of payload with size {payload_size_in_bytes} bytes')

        if self._start_multipart_upload_request:
            requires_biolib_auth = self._start_multipart_upload_request['requires_biolib_auth']
            start_multipart_upload = requests.post(
                auth=BearerAuth(BiolibApiClient.get().access_token) if requires_biolib_auth else None,
                headers=self._start_multipart_upload_request['headers'],
                timeout=30,
                url=self._start_multipart_upload_request['url'],
            )
            if start_multipart_upload.ok:
                logger_no_user_data.debug('Multipart upload started')
            else:
                logger_no_user_data.debug(
                    f'Failed to start multipart upload got response status: {start_multipart_upload.status_code}'
                )
                raise Exception('Failed to start multipart upload')

        # if multiprocessing start method is spawn or we are running in a daemon process,
        # multiprocessing.Pool may fail when called from script
        if multiprocessing.get_start_method() == 'spawn' or multiprocessing.current_process().daemon:
            logger_no_user_data.debug('Uploading multipart from main process...')
            for chunk in iterator_with_index:
                upload_chunk_response = self._upload_chunk(chunk)
                self._update_progress_bar_and_parts(
                    upload_chunk_response=upload_chunk_response,
                    parts=parts,
                    payload_size_in_bytes=payload_size_in_bytes
                )
        else:
            # use 16 cores, unless less is available
            process_pool = multiprocessing.pool.ThreadPool(processes=min(16, multiprocessing.cpu_count() - 1))
            try:
                response: _UploadChunkReturnType
                for response in process_pool.imap(self._upload_chunk, iterator_with_index):
                    self._update_progress_bar_and_parts(
                        upload_chunk_response=response,
                        parts=parts,
                        payload_size_in_bytes=payload_size_in_bytes
                    )
            finally:
                logger_no_user_data.debug('Multipart upload closing process pool...')
                process_pool.close()

        requires_biolib_auth = self._complete_upload_request['requires_biolib_auth']
        if requires_biolib_auth:
            BiolibApiClient.refresh_auth_token()

        logger_no_user_data.debug(f'Uploaded {len(parts)} parts, now calling complete upload...')
        for index in range(3):
            try:
                complete_upload_response = requests.post(
                    auth=BearerAuth(BiolibApiClient.get().access_token) if requires_biolib_auth else None,
                    headers=self._complete_upload_request['headers'],
                    json={'parts': parts, 'size_bytes': self._bytes_uploaded},
                    timeout=30,
                    url=self._complete_upload_request['url'],
                )
                if complete_upload_response.ok:
                    logger_no_user_data.debug('Multipart upload completed returning')
                    return

                logger_no_user_data.warning(
                    f'Failed to complete multipart upload got response status {complete_upload_response.status_code}. '
                    f'Retrying...'
                )

            except Exception as error:  # pylint: disable=broad-except
                logger_no_user_data.warning('Encountered error when completing multipart upload. Retrying...')
                logger.debug(f'Multipart complete error: {error}')
                time.sleep(index * index + 2)

        raise BioLibError('Max retries hit, when completing multipart upload')

    def _upload_chunk(self, _input: _UploadChunkInputType) -> _UploadChunkReturnType:
        part_number, chunk = _input
        requires_biolib_auth = self._get_presigned_upload_url_request['requires_biolib_auth']

        for index in range(20):  # will fail after approximately sum_i(i^2+2) = 41 min if range (20)
            if requires_biolib_auth:
                BiolibApiClient.refresh_auth_token()

            logger_no_user_data.debug(f'Uploading part number {part_number} with size {len(chunk)} bytes...')
            try:
                logger_no_user_data.debug(f'Getting upload URL for chunk {part_number}...')
                get_url_response = requests.get(
                    auth=BearerAuth(BiolibApiClient.get().access_token) if requires_biolib_auth else None,
                    headers=self._get_presigned_upload_url_request['headers'],
                    params={'part_number': part_number},
                    timeout=30,
                    url=self._get_presigned_upload_url_request['url'],
                )
                if not get_url_response.ok:
                    raise Exception(
                        f'Failed to get upload URL for part {part_number} got response status code '
                        f'{get_url_response.status_code}'
                    )

                presigned_upload_url = get_url_response.json()['presigned_upload_url']

                app_caller_proxy_job_storage_base_url = os.getenv('BIOLIB_CLOUD_JOB_STORAGE_BASE_URL', '')
                if app_caller_proxy_job_storage_base_url:
                    # Done to hit App Caller Proxy when uploading result from inside an app
                    parsed_url = urlparse(presigned_upload_url)
                    presigned_upload_url = \
                        f'{app_caller_proxy_job_storage_base_url}{parsed_url.path}?{parsed_url.query}'

                put_chunk_response = requests.put(url=presigned_upload_url, data=chunk, timeout=300)

                if put_chunk_response.ok:
                    return _PartMetadata(PartNumber=part_number, ETag=put_chunk_response.headers['ETag']), len(chunk)
                else:
                    logger_no_user_data.warning(
                        f'Got response with status {put_chunk_response.status_code} when uploading part {part_number}. '
                        'Retrying...'
                    )
                    logger.debug(f'Response content: {put_chunk_response.content.decode()}')

            except Exception as error:  # pylint: disable=broad-except
                logger_no_user_data.warning(f'Encountered error when uploading part {part_number}. Retrying...')
                logger.debug(f'Upload error: {error}')

            time.sleep(index * index + 2)

        logger_no_user_data.debug(f'Max retries hit, when uploading part {part_number}. Exiting...')
        raise BioLibError(f'Max retries hit, when uploading part {part_number}. Exiting...')

    def _update_progress_bar_and_parts(
        self,
        upload_chunk_response: _UploadChunkReturnType,
        parts: List[_PartMetadata],
        payload_size_in_bytes: int,
    ) -> None:
        part_metadata, chunk_byte_length = upload_chunk_response
        part_number = part_metadata['PartNumber']

        parts.append(part_metadata)
        self._bytes_uploaded += chunk_byte_length

        approx_progress_percent = min(self._bytes_uploaded / (payload_size_in_bytes + 1) * 100, 100)
        approx_rounded_progress = round(approx_progress_percent, 2)
        logger_no_user_data.debug(
            f'Uploaded part number {part_number} with size {chunk_byte_length} bytes, '
            f'the approximate progress is {approx_rounded_progress}%'
        )
