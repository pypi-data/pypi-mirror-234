from abc import ABC, abstractmethod
import io
import time

import requests
from requests import Response

from biolib.biolib_logging import logger
from biolib.typing_utils import Optional, Dict


class RemoteEndpoint(ABC):
    @abstractmethod
    def get_remote_url(self):
        pass


class IndexableBuffer(ABC):

    def __init__(self):
        self.pointer = 0

    @abstractmethod
    def get_data(self, start: int, length: int) -> bytes:
        pass

    def get_data_as_string(self, start: int, length: int) -> str:
        return self.get_data(start=start, length=length).decode()

    def get_data_as_int(self, start: int, length: int) -> int:
        return int.from_bytes(bytes=self.get_data(start=start, length=length), byteorder='big')

    def get_data_with_pointer(self, length: int) -> bytes:
        data = self.get_data(start=self.pointer, length=length)
        self.pointer += length
        return data

    def get_data_with_pointer_as_int(self, length: int) -> int:
        data = self.get_data_as_int(start=self.pointer, length=length)
        self.pointer += length
        return data

    def get_data_with_pointer_as_string(self, length: int) -> str:
        data = self.get_data_as_string(start=self.pointer, length=length)
        self.pointer += length
        return data


def _get_request_with_retries_for_timeout(
        url: str,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
) -> Response:
    retries = 10
    for retry_count in range(retries):
        if retry_count > 0:
            time.sleep(5 * retry_count)
            logger.debug('Retrying HTTP GET request...')

        try:
            response = requests.get(
                headers=headers,
                stream=stream,
                timeout=120,
                url=url,
            )
        except requests.exceptions.ReadTimeout:
            logger.debug('Got read timeout of HTTP GET request')
            continue

        if response.status_code == 502:
            logger.debug('Got 502 status for HTTP GET')
            continue

        if response.status_code == 400:
            logger.error(
                f'GET request for "{url}" got response with status {response.status_code} and '
                f'content: {response.content.decode()}'
            )

        if not response.ok:
            raise Exception(f'GET request for "{url}" got response with status {response.status_code}')

        return response

    raise Exception(f'Failed to complete HTTP GET request for "{url}" after {retries} retries')


class LocalFileIndexableBuffer(IndexableBuffer):

    def __init__(self, filename: str):
        super().__init__()
        self._filehandle = open(filename, 'rb')

    def get_data(self, start: int, length: int) -> bytes:
        if length < 0:
            raise Exception('get_data length must be positive')

        if length == 0:
            return bytes(0)

        self._filehandle.seek(start)
        data: bytes = self._filehandle.read(length)

        if len(data) != length:
            raise Exception(f'get_data got response of unexpected length. Got {len(data)} expected {length}.')

        return data


class RemoteIndexableBuffer(IndexableBuffer):

    def __init__(self, endpoint: RemoteEndpoint):
        super().__init__()
        self._endpoint = endpoint

    def get_data(self, start: int, length: int) -> bytes:
        if length < 0:
            raise Exception('get_data length must be positive')

        if length == 0:
            return bytes(0)

        end = start + length - 1
        response = _get_request_with_retries_for_timeout(
            url=self._endpoint.get_remote_url(),
            headers={'range': f'bytes={start}-{end}'},
        )

        data: bytes = response.content
        if len(data) != length:
            raise Exception(f'get_data got response of unexpected length. Got {len(data)} expected {length}.')

        return data


class InMemoryIndexableBuffer(IndexableBuffer):

    def __init__(self, data: bytes):
        super().__init__()
        self._buffer = data
        self._length_bytes = len(data)

    def get_data(self, start: int, length: int) -> bytes:
        end = start + length
        return self._buffer[start:end]

    def __len__(self):
        return self._length_bytes


class LazyLoadedFile:

    def __init__(self, path: str, buffer: IndexableBuffer, start: int, length: int):
        self._path = path
        self._buffer = buffer
        self._start = start
        self._length = length

    def __repr__(self) -> str:
        return f'File "{self._path}" with size of {self._length} bytes'

    @property
    def path(self) -> str:
        return self._path

    @property
    def start(self) -> int:
        return self._start

    @property
    def length(self) -> int:
        return self._length

    def get_file_handle(self) -> io.BufferedIOBase:
        return io.BytesIO(self.get_data())

    def get_data(self) -> bytes:
        return self._buffer.get_data(start=self._start, length=self._length)
