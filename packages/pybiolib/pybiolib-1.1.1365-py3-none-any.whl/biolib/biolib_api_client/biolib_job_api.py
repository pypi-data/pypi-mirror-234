import os
import time
from urllib.parse import urlparse

import requests

import biolib.api

from biolib import utils
from biolib.biolib_api_client.auth import BearerAuth
from biolib.biolib_api_client import BiolibApiClient, CloudJob, JobState
from biolib.biolib_errors import BioLibError, RetryLimitException, StorageDownloadFailed, JobResultPermissionError, \
    JobResultError, JobResultNotFound
from biolib.biolib_logging import logger
from biolib.utils import BIOLIB_PACKAGE_VERSION
from biolib.typing_utils import TypedDict, Optional, Literal, Dict


class PresignedS3UploadLinkResponse(TypedDict):
    presigned_upload_url: str


class PresignedS3DownloadLinkResponse(TypedDict):
    presigned_download_url: str


def _get_user_info() -> Optional[str]:
    if utils.BASE_URL_IS_PUBLIC_BIOLIB:
        return None

    enterprise_agent_info_opt_env_vars = ['DOMINO_STARTING_USERNAME', 'USER']

    for env_var in enterprise_agent_info_opt_env_vars:
        env_var_value = os.getenv(env_var)
        if env_var_value:
            return env_var_value

    return None


class BiolibJobApi:

    @staticmethod
    def create(
            app_version_id,
            app_resource_name_prefix=None,
            override_command=False,
            caller_job=None,
            machine='',
            experiment_uuid: Optional[str] = None,
            timeout: Optional[int] = None,
            notify: bool = False,
    ):
        data = {
            'app_version_id': app_version_id,
            'client_type': 'biolib-python',
            'notify': notify,
            'client_version': BIOLIB_PACKAGE_VERSION,
            'client_opt_user_info': _get_user_info(),
        }

        if app_resource_name_prefix:
            data.update({
                'app_resource_name_prefix': app_resource_name_prefix
            })

        if override_command:
            data.update({
                'arguments_override_command': override_command
            })

        if caller_job:
            data['caller_job'] = caller_job

        if machine:
            data.update({
                'requested_machine': machine
            })

        if experiment_uuid:
            data['experiment_uuid'] = experiment_uuid

        if timeout:
            data['requested_timeout_seconds'] = timeout

        response = biolib.api._client.post(path='/jobs/', data=data)  # pylint: disable=protected-access

        return response.json()

    @staticmethod
    def update_state(job_uuid: str, state: JobState) -> None:
        try:
            biolib.api.client.patch(path=f'/jobs/{job_uuid}/', data={'state': state.value})
        except BaseException as error:
            logger.error(f'Failed to update job "{job_uuid}" to state "{state.value}" due to {error}')

    @staticmethod
    def create_cloud_job(job_id: str, result_name_prefix: Optional[str]) -> CloudJob:
        response = None
        data = {'job_id': job_id}
        if result_name_prefix:
            data['result_name_prefix'] = result_name_prefix

        for retry in range(4):
            try:
                response = requests.post(
                    f'{BiolibApiClient.get().base_url}/api/jobs/cloud/',
                    json=data,
                    auth=BearerAuth(BiolibApiClient.get().access_token)
                )

                if response.status_code == 503:
                    raise RetryLimitException(response.content)
                # Handle possible validation errors from backend
                elif not response.ok:
                    raise BioLibError(response.text)

                break

            except RetryLimitException as retry_exception:  # pylint: disable=broad-except
                if retry > 3:
                    raise BioLibError('Reached retry limit for cloud job creation') from retry_exception
                time.sleep(1)

        if not response:
            raise BioLibError('Could not create new cloud job')

        cloud_job: CloudJob = response.json()
        return cloud_job

    @staticmethod
    def get_job_storage_download_url(
            job_uuid: str,
            job_auth_token: str,
            storage_type: Literal['input', 'results'],
    ) -> str:
        try:
            response = biolib.api.client.get(
                url=f'{BiolibApiClient.get().base_url}/api/jobs/{job_uuid}/storage/{storage_type}/download/',
                authenticate=True,
                headers={'Job-Auth-Token': job_auth_token}
            )
            presigned_s3_download_link_response: PresignedS3DownloadLinkResponse = response.json()
            presigned_download_url = presigned_s3_download_link_response['presigned_download_url']

            app_caller_proxy_job_storage_base_url = os.getenv('BIOLIB_CLOUD_JOB_STORAGE_BASE_URL', '')
            if app_caller_proxy_job_storage_base_url:
                # Done to hit App Caller Proxy when downloading result from inside an app
                parsed_url = urlparse(presigned_download_url)
                presigned_download_url = f'{app_caller_proxy_job_storage_base_url}{parsed_url.path}?{parsed_url.query}'

            return presigned_download_url

        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code
            if storage_type == 'results':
                if status_code == 401:
                    raise JobResultPermissionError('You must be signed in to get result of the job') from None
                elif status_code == 403:
                    raise JobResultPermissionError(
                        'Cannot get result of job. Maybe the job was created without being signed in?'
                    ) from None
                elif status_code == 404:
                    raise JobResultNotFound('Job result not found') from None
                else:
                    raise JobResultError('Failed to get result of job') from error
            else:
                raise StorageDownloadFailed(error.response.content) from error

        except Exception as error:  # pylint: disable=broad-except
            if storage_type == 'results':
                raise JobResultError('Failed to get result of job') from error
            else:
                raise StorageDownloadFailed('Failed to download from Job Storage') from error

    @staticmethod
    def create_job_with_data(
            app_version_uuid: str,
            app_resource_name_prefix: Optional[str],
            module_input_serialized: bytes,
            arguments_override_command: bool,
            experiment_uuid: Optional[str],
            requested_machine: Optional[str],
            result_name_prefix: Optional[str],
            caller_job_uuid: Optional[str] = None,
            requested_timeout_seconds: Optional[int] = None,
            notify: bool = False,
    ) -> Dict:
        job_dict: Dict = biolib.api.client.post(
            path='/jobs/create_job_with_data/',
            data=module_input_serialized,
            headers={
                'Content-Type': 'application/octet-stream',
                'app-version-uuid': app_version_uuid,
                'app-resource-name-prefix': app_resource_name_prefix,
                'arguments-override-command': str(arguments_override_command),
                'caller-job-uuid': caller_job_uuid,
                'client-opt-user-info': _get_user_info(),
                'client-type': 'biolib-python',
                'client-version': BIOLIB_PACKAGE_VERSION,
                'experiment-uuid': experiment_uuid,
                'requested-machine': requested_machine,
                'result-name-prefix': result_name_prefix,
                'requested-timeout-seconds': str(requested_timeout_seconds) if requested_timeout_seconds else None,
                'notify': 'true' if notify else 'false',
            }
        ).json()
        return job_dict
