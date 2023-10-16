import base64
from datetime import datetime, timedelta
import sys
import time
from pathlib import Path
from collections import OrderedDict
from urllib.parse import urlparse

import requests
from biolib import api, utils
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_binary_format import LazyLoadedFile, ModuleOutputV2, ModuleInput
from biolib.biolib_binary_format.stdout_and_stderr import StdoutAndStderr
from biolib.biolib_errors import BioLibError, CloudJobFinishedError
from biolib.biolib_logging import logger, logger_no_user_data
from biolib.compute_node.utils import SystemExceptionCodeMap, SystemExceptionCodes
from biolib.jobs.job_result import JobResult
from biolib.jobs.types import JobDict, CloudJobStartedDict, CloudJobDict
from biolib.tables import BioLibTable
from biolib.typing_utils import Optional, List, cast, Dict
from biolib.utils import IS_RUNNING_IN_NOTEBOOK


class Job:
    # Columns to print in table when showing Job
    table_columns_to_row_map = OrderedDict({
        'ID': {'key': 'uuid', 'params': {'width': 36}},
        'Application': {'key': 'app_uri', 'params': {}},
        'Status': {'key': 'state', 'params': {}},
        'Started At': {'key': 'started_at', 'params': {}},
    })

    def __init__(self, job_dict: JobDict):
        self._uuid: str = job_dict['uuid']
        self._auth_token: str = job_dict['auth_token']

        self._job_dict: JobDict = job_dict
        self._job_dict_last_fetched_at: datetime = datetime.utcnow()
        self._result: Optional[JobResult] = None

    def __str__(self):
        return f"Job for {self._job_dict['app_uri']} created at {self._job_dict['created_at']} ({self._uuid})"

    def __repr__(self):
        return f'Job: {self._uuid}'

    @property
    def id(self) -> str:  # pylint: disable=invalid-name
        return self._uuid

    @property
    def result(self) -> JobResult:
        if not self._result:
            if self.get_status() == "completed":
                self._result = JobResult(job_uuid=self._uuid, job_auth_token=self._auth_token)
            else:
                raise BioLibError(f"Result is not available for {self._uuid}: status is {self._job_dict['state']}.")

        return self._result

    @property
    def stdout(self) -> bytes:
        logger.warning("The property .stdout is deprecated, please use .get_stdout()")
        return self.result.get_stdout()

    @property
    def stderr(self) -> bytes:
        logger.warning("The property .stderr is deprecated, please use .get_stderr()")
        return self.result.get_stderr()

    @property
    def exitcode(self) -> int:
        logger.warning("The property .exitcode is deprecated, please use .get_exit_code()")
        return self.result.get_exit_code()

    def is_finished(self) -> bool:
        if self._job_dict['ended_at']:
            return True

        self._refetch_job_dict()
        return bool(self._job_dict['ended_at'])

    def to_dict(self) -> Dict:
        # Construct user facing dict with friendly named keys
        return dict(
            app_uri=self._job_dict['app_uri'],
            created_at=self._job_dict['created_at'],
            finished_at=self._job_dict['ended_at'],
            job_id=self._job_dict['uuid'],
            started_at=self._job_dict['started_at'],
            state=self._job_dict['state'],
        )

    def list_output_files(self, *args, **kwargs) -> List[LazyLoadedFile]:
        return self.result.list_output_files(*args, **kwargs)

    def get_output_file(self, *args, **kwargs) -> LazyLoadedFile:
        return self.result.get_output_file(*args, **kwargs)

    def load_file_as_numpy(self, *args, **kwargs):
        try:
            import numpy  # type: ignore # pylint: disable=import-outside-toplevel,import-error
        except:  # pylint: disable=raise-missing-from
            raise Exception("Failed to import numpy, please make sure it is installed.")
        file_handle = self.result.get_output_file(*args, **kwargs).get_file_handle()
        return numpy.load(file_handle, allow_pickle=False)  # type: ignore

    def get_stdout(self) -> bytes:
        return self.result.get_stdout()

    def get_stderr(self) -> bytes:
        return self.result.get_stderr()

    def get_exit_code(self) -> int:
        return self.result.get_exit_code()

    def save_input_files(self, output_dir: str) -> None:
        self._refetch_job_dict()
        logger.info('Downloading input files...')
        try:
            presigned_download_url = BiolibJobApi.get_job_storage_download_url(
                job_uuid=self._job_dict['uuid'],
                job_auth_token=self._job_dict['auth_token'],
                storage_type='input',
            )
            response = requests.get(url=presigned_download_url)
            response.raise_for_status()
            module_input_serialized: bytes = response.content
        except Exception as error:
            # TODO: Improve error handling and messages
            raise error

        try:
            module_input = ModuleInput(module_input_serialized).deserialize()
        except Exception as error:
            # TODO: Improve error handling and messages
            raise error

        files = module_input['files'].items()
        logger.info(f'Saving input {len(files)} files to "{output_dir}"...')
        for path, data in files:
            # Remove leading slash of file_path
            destination_file_path = Path(output_dir) / Path(path.lstrip('/'))
            if destination_file_path.exists():
                destination_file_path.rename(f'{destination_file_path}.biolib-renamed.{time.strftime("%Y%m%d%H%M%S")}')

            dir_path = destination_file_path.parent
            if dir_path:
                dir_path.mkdir(parents=True, exist_ok=True)

            with open(destination_file_path, mode='wb') as file_handler:
                file_handler.write(data)

            logger.info(f'  - {destination_file_path}')

    def save_files(self, *args, **kwargs) -> None:
        self.result.save_files(*args, **kwargs)

    def get_status(self) -> str:
        self._refetch_job_dict()
        return self._job_dict['state']

    def wait(self):
        logger.info(f'Waiting for job {self.id} to finish...')
        while not self.is_finished():
            time.sleep(2)
        logger.info(f'Job {self.id} has finished.')

    def _get_cloud_job(self) -> CloudJobDict:
        self._refetch_job_dict(force_refetch=True)
        if self._job_dict['cloud_job'] is None:
            raise BioLibError(f'Job {self._uuid} did not register correctly. Try creating a new job.')

        return self._job_dict['cloud_job']

    def _set_result_module_output(self, module_output: ModuleOutputV2) -> None:
        self._result = JobResult(job_uuid=self._uuid, job_auth_token=self._auth_token, module_output=module_output)

    @staticmethod
    def fetch_jobs(count: int) -> List['Job']:
        job_dicts = Job._get_job_dicts(count)
        return [Job(job_dict) for job_dict in job_dicts]

    @staticmethod
    def show_jobs(count: int = 25) -> None:
        job_dicts = Job._get_job_dicts(count)
        BioLibTable(
            columns_to_row_map=Job.table_columns_to_row_map,
            rows=job_dicts,
            title='Jobs'
        ).print_table()

    @staticmethod
    def _get_job_dicts(count: int) -> List['JobDict']:
        job_dicts: List['JobDict'] = api.client.get(
            url='/jobs/',
            params={
                'page_size': str(count)
            }
        ).json()['results']
        return job_dicts

    @staticmethod
    def _get_job_dict(uuid: str, auth_token: Optional[str] = None) -> JobDict:
        job_dict: JobDict = api.client.get(
            url=f'/jobs/{uuid}/',
            headers={'Job-Auth-Token': auth_token} if auth_token else None,
        ).json()

        return job_dict

    @staticmethod
    def create_from_uuid(uuid: str, auth_token: Optional[str] = None) -> 'Job':
        job_dict = Job._get_job_dict(uuid=uuid, auth_token=auth_token)
        return Job(job_dict)

    @staticmethod
    def print_logs_packages(stdout_and_stderr_packages_b64):
        for stdout_and_stderr_package_b64 in stdout_and_stderr_packages_b64:
            stdout_and_stderr_package = base64.b64decode(stdout_and_stderr_package_b64)
            stdout_and_stderr = StdoutAndStderr(stdout_and_stderr_package).deserialize()

            sys.stdout.write(stdout_and_stderr.decode())
            if not IS_RUNNING_IN_NOTEBOOK:  # for some reason flushing in jupyter notebooks breaks \r handling
                sys.stdout.flush()
        # flush after having processed all packages
        sys.stdout.flush()

    def show(self) -> None:
        self._refetch_job_dict()
        BioLibTable(
            columns_to_row_map=Job.table_columns_to_row_map,
            rows=[self._job_dict],
            title=f'Job: {self._uuid}'
        ).print_table()

    def stream_logs(self) -> None:
        self._stream_logs()

    def _stream_logs(self, enable_print: bool = True) -> None:
        try:
            cloud_job = self._get_cloud_job_awaiting_started()
        except CloudJobFinishedError:
            logger.info(f'--- The job {self.id} has already completed (no streaming will take place) ---')
            logger.info('--- The stdout log is printed below: ---')
            sys.stdout.flush()
            print(self.get_stdout().decode(), file=sys.stdout)
            sys.stdout.flush()
            logger.info('--- The stderr log is printed below: ---')
            print(self.get_stderr().decode(), file=sys.stderr)
            sys.stderr.flush()
            logger.info(f'--- The job {self.id} has already completed. Its output was printed above. ---')
            return

        compute_node_url = cloud_job['compute_node_url']
        logger_no_user_data.debug(f'Using compute node URL "{compute_node_url}"')

        if utils.BIOLIB_CLOUD_BASE_URL:
            compute_node_url = utils.BIOLIB_CLOUD_BASE_URL + str(urlparse(compute_node_url).path)
            logger_no_user_data.debug(f'Using cloud proxy URL from env var BIOLIB_CLOUD_BASE_URL: {compute_node_url}')

        if enable_print:
            self._print_full_logs(node_url=compute_node_url)

        final_status_messages: List[str] = []
        while True:
            time.sleep(2)
            status_json = self._get_job_status_from_compute_node(compute_node_url)
            job_is_completed = status_json['is_completed']
            for status_update in status_json['status_updates']:
                # If the job is completed, print the log messages after all stdout and stderr has been written
                if job_is_completed:
                    final_status_messages.append(status_update['log_message'])
                else:
                    # Print the status before writing stdout and stderr
                    logger.info(f'Cloud: {status_update["log_message"]}')

            if 'stdout_and_stderr_packages_b64' and enable_print:
                self.print_logs_packages(status_json['stdout_and_stderr_packages_b64'])

            if 'error_code' in status_json:
                error_code = status_json['error_code']
                error_message = SystemExceptionCodeMap.get(error_code, f'Unknown error code {error_code}')

                raise BioLibError(f'Cloud: {error_message}')

            if job_is_completed:
                break

        # Print the final log messages after stdout and stderr has been written
        for message in final_status_messages:
            logger.info(f'Cloud: {message}')

        self.wait()  # Wait for compute node to tell the backend that the job is finished

    def _print_full_logs(self, node_url: str) -> None:
        try:
            response = requests.get(f'{node_url}/v1/job/{self._uuid}/status/?logs=full')
            if not response.ok:
                raise BioLibError(response.content)
        except Exception as error:
            logger.error(f'Could not get full streamed logs due to: {error}')
            raise BioLibError from error

        for status_update in response.json().get('previous_status_updates', []):
            logger.info(f'Cloud: {status_update["log_message"]}')

        self.print_logs_packages(response.json()['streamed_logs_packages_b64'])

    def _get_cloud_job_awaiting_started(self) -> CloudJobStartedDict:
        while True:
            cloud_job = self._get_cloud_job()

            if cloud_job['finished_at']:
                raise CloudJobFinishedError()

            if cloud_job and cloud_job['started_at']:
                if not cloud_job['compute_node_url']:
                    raise BioLibError(f'Failed to get URL to compute node for job {self._uuid}')

                return cast(CloudJobStartedDict, cloud_job)

            logger.info('Cloud: The job has been queued. Please wait...')
            time.sleep(10)

    def _get_job_status_from_compute_node(self, compute_node_url):
        for _ in range(15):
            try:
                response = requests.get(f'{compute_node_url}/v1/job/{self._uuid}/status/')
                if not response.ok:
                    raise BioLibError(response.content)
                return response.json()

            except Exception:  # pylint: disable=broad-except
                cloud_job = self._get_cloud_job()
                logger.debug("Failed to get status from compute node, retrying...")
                if cloud_job['finished_at']:
                    logger.debug("Job no longer exists on compute node, checking for error...")
                    if cloud_job['error_code'] != SystemExceptionCodes.COMPLETED_SUCCESSFULLY.value:
                        error_message = SystemExceptionCodeMap.get(
                            cloud_job['error_code'],
                            f'Unknown error code {cloud_job["error_code"]}'
                        )
                        raise BioLibError(f'Cloud: {error_message}') from None
                    else:
                        logger.info(f'The job {self._uuid} is finished. Get its output by calling `.result()`')
                        return

                time.sleep(2)

        raise BioLibError(
            'Failed to stream logs, did you lose internet connection?\n'
            'Call `.stream_logs()` on your job to resume streaming logs.'
        )

    def _refetch_job_dict(self, force_refetch: Optional[bool] = False) -> None:
        if not force_refetch and self._job_dict_last_fetched_at > datetime.utcnow() - timedelta(seconds=2):
            return

        self._job_dict = self._get_job_dict(self._uuid, self._auth_token)
        self._job_dict_last_fetched_at = datetime.utcnow()
