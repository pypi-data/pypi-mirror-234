import os

import requests

from biolib import utils
from biolib.biolib_api_client import BiolibApiClient, CreatedJobDict
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.biolib_logging import logger_no_user_data
from biolib.utils.multipart_uploader import get_chunk_iterator_from_file_object


class JobStorage:
    module_output_file_name = 'module-output.bbf'

    @staticmethod
    def upload_module_input(job: CreatedJobDict, module_input_serialized: bytes) -> None:
        base_url = BiolibApiClient.get().base_url
        job_uuid = job['public_id']
        headers = {'Job-Auth-Token': job['auth_token']}

        multipart_uploader = utils.MultiPartUploader(
            start_multipart_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/input/start_upload/',
                headers=headers
            ),
            get_presigned_upload_url_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/input/presigned_upload_url/',
                headers=headers
            ),
            complete_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/input/complete_upload/',
                headers=headers
            ),
        )

        multipart_uploader.upload(
            payload_iterator=utils.get_chunk_iterator_from_bytes(module_input_serialized),
            payload_size_in_bytes=len(module_input_serialized),
        )

    @staticmethod
    def upload_module_output(job_uuid: str, job_temporary_dir: str) -> None:
        logger_no_user_data.debug(f'Job "{job_uuid}" uploading result...')
        module_output_path = os.path.join(job_temporary_dir, JobStorage.module_output_file_name)
        module_output_size = os.path.getsize(module_output_path)

        with open(module_output_path, mode='rb') as module_output_file:
            module_output_iterator = get_chunk_iterator_from_file_object(module_output_file)
            multipart_uploader = JobStorage._get_module_output_uploader(job_uuid)
            multipart_uploader.upload(
                payload_iterator=module_output_iterator,
                payload_size_in_bytes=module_output_size,
            )

        logger_no_user_data.debug(f'Job "{job_uuid}" result uploaded successfully')

    @staticmethod
    def _get_module_output_uploader(job_uuid: str) -> utils.MultiPartUploader:
        base_url = BiolibApiClient.get().base_url
        config = CloudUtils.get_webserver_config()
        compute_node_auth_token = config['compute_node_info']['auth_token']  # pylint: disable=unsubscriptable-object
        headers = {'Compute-Node-Auth-Token': compute_node_auth_token}

        return utils.MultiPartUploader(
            start_multipart_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/start_upload/',
                headers=headers,
            ),
            get_presigned_upload_url_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/presigned_upload_url/',
                headers=headers,
            ),
            complete_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/complete_upload/',
                headers=headers,
            ),
        )

    @staticmethod
    def get_module_input(job: CreatedJobDict) -> bytes:
        job_uuid = job['public_id']
        logger_no_user_data.debug(f'Job "{job_uuid}" downloading module input...')
        presigned_download_url = BiolibJobApi.get_job_storage_download_url(
            job_uuid=job_uuid,
            job_auth_token=job['auth_token'],
            storage_type='input',
        )
        response = requests.get(url=presigned_download_url)
        response.raise_for_status()
        data: bytes = response.content
        logger_no_user_data.debug(f'Job "{job_uuid}" module input downloaded')
        return data
