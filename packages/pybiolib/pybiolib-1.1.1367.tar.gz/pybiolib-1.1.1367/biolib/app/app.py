import glob
import os
import io
import random
import json
import string

from pathlib import Path
from biolib import utils
from biolib.compute_node.job_worker.job_storage import JobStorage
from biolib.compute_node.job_worker.job_worker import JobWorker
from biolib.experiments.experiment import Experiment
from biolib.jobs import Job
from biolib.typing_utils import Optional, cast
from biolib.biolib_api_client import CreatedJobDict, JobState
from biolib.jobs.types import JobDict
from biolib.biolib_api_client.app_types import App, AppVersion
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_api_client.biolib_app_api import BiolibAppApi
from biolib.biolib_binary_format import ModuleInput
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger
from biolib.utils.app_uri import parse_app_uri


class BioLibApp:

    def __init__(self, uri: str):
        app_response = BiolibAppApi.get_by_uri(uri)
        self._app: App = app_response['app']
        self._app_uri = app_response['app_uri']
        self._app_version: AppVersion = app_response['app_version']

        logger.info(f'Loaded project {self._app_uri}')

    def __str__(self) -> str:
        return self._app_uri

    @property
    def uuid(self) -> str:
        return self._app['public_id']

    @property
    def version(self) -> AppVersion:
        return self._app_version

    def cli(
            self,
            args=None,
            stdin=None,
            files=None,
            override_command=False,
            machine='',
            blocking: bool = True,
            experiment_id: Optional[str] = None,
            result_prefix: Optional[str] = None,
            timeout: Optional[int] = None,
            notify: bool = False,
    ) -> Job:
        if not experiment_id:
            experiment = Experiment.get_experiment_in_context()
            experiment_id = experiment.uuid if experiment else None

        module_input_serialized = self._get_serialized_module_input(args, stdin, files)

        if machine == 'local':
            if not blocking:
                raise BioLibError('The argument "blocking" cannot be False when running locally')

            if experiment_id:
                logger.warning('The argument "experiment_id" is ignored when running locally')

            if result_prefix:
                logger.warning('The argument "result_prefix" is ignored when running locally')

            return self._run_locally(module_input_serialized)

        job = self._start_in_cloud(
            experiment_id=experiment_id,
            machine=machine,
            module_input_serialized=module_input_serialized,
            notify=notify,
            override_command=override_command,
            result_prefix=result_prefix,
            timeout=timeout,
        )
        if blocking:
            # TODO: Deprecate utils.STREAM_STDOUT and always stream logs by simply calling job.stream_logs()
            if utils.IS_RUNNING_IN_NOTEBOOK:
                utils.STREAM_STDOUT = True

            enable_print = bool(
                utils.STREAM_STDOUT and
                (self._app_version.get('main_output_file') or self._app_version.get('stdout_render_type') == 'text')
            )
            job._stream_logs(enable_print=enable_print)  # pylint: disable=protected-access

        return job

    def exec(self, args=None, stdin=None, files=None, machine=''):
        return self.cli(args, stdin, files, override_command=True, machine=machine)

    def __call__(self, *args, **kwargs):
        if not args and not kwargs:
            self.cli()

        else:
            raise BioLibError('''
Calling an app directly with app() is currently being reworked.
To use the previous functionality, please call app.cli() instead. 
Example: "app.cli('--help')"
''')

    @staticmethod
    def _get_serialized_module_input(args=None, stdin=None, files=None) -> bytes:
        if args is None:
            args = []

        if stdin is None:
            stdin = b''

        if isinstance(args, str):
            args = list(filter(lambda p: p != '', args.split(' ')))

        if not isinstance(args, list):
            raise Exception('The given input arguments must be list or str')

        if isinstance(stdin, str):
            stdin = stdin.encode('utf-8')

        if files is None:
            files = []

        files_dict = {}
        for idx, arg in enumerate(args):
            if isinstance(arg, str):
                if os.path.isfile(arg) or os.path.isdir(arg):
                    files.append(arg)
                    args[idx] = arg.rstrip('/').split('/')[-1]

                # support --myarg=file.txt
                elif os.path.isfile(arg.split("=")[-1]) or os.path.isdir(arg.split("=")[-1]):
                    files.append(arg.split("=")[-1])
                    args[idx] = arg.split("=")[0] + '=' + arg.split("=")[-1].rstrip('/').split('/')[-1]
                else:
                    pass  # a normal string arg was given
            else:
                filename = f'input_{"".join(random.choices(string.ascii_letters + string.digits, k=7))}'
                if isinstance(arg, io.StringIO):
                    file_data = arg.getvalue().encode()
                elif isinstance(arg, io.BytesIO):
                    file_data = arg.getvalue()
                else:
                    raise Exception(f"Unexpected type of argument: {arg}")
                files_dict[f'/{filename}'] = file_data
                args[idx] = filename

        cwd = os.getcwd()

        if isinstance(files, list):
            for file in files:
                path = file
                if not file.startswith('/'):
                    # make path absolute
                    path = cwd + '/' + file

                # Recursively add data from files if dir
                if os.path.isdir(path):
                    for filename in glob.iglob(path + '**/**', recursive=True):
                        if os.path.isdir(filename):
                            continue
                        file = open(filename, 'rb')
                        relative_path = '/' + Path(path).stem + '/' + os.path.relpath(filename, start=path)
                        files_dict[relative_path] = file.read()
                        file.close()

                # Add file data
                else:
                    arg_split = path.split('/')
                    file = open(path, 'rb')
                    path = '/' + arg_split[-1]

                    files_dict[path] = file.read()
                    file.close()

        elif isinstance(files, dict):
            files_dict.update(files)
        else:
            raise Exception('The given files input must be list or dict or None')

        module_input_serialized: bytes = ModuleInput().serialize(
            stdin=stdin,
            arguments=args,
            files=files_dict,
        )
        return module_input_serialized

    def _start_in_cloud(
            self,
            module_input_serialized: bytes,
            override_command: bool = False,
            machine: Optional[str] = None,
            experiment_id: Optional[str] = None,
            result_prefix: Optional[str] = None,
            timeout: Optional[int] = None,
            notify: bool = False,
    ) -> Job:
        if len(module_input_serialized) < 500_000:
            _job_dict = BiolibJobApi.create_job_with_data(
                app_resource_name_prefix=parse_app_uri(self._app_uri)['resource_name_prefix'],
                app_version_uuid=self._app_version['public_id'],
                arguments_override_command=override_command,
                experiment_uuid=experiment_id,
                module_input_serialized=module_input_serialized,
                notify=notify,
                requested_machine=machine,
                requested_timeout_seconds=timeout,
                result_name_prefix=result_prefix,
            )
            return Job(cast(JobDict, _job_dict))

        job_dict: CreatedJobDict = BiolibJobApi.create(
            app_resource_name_prefix=parse_app_uri(self._app_uri)['resource_name_prefix'],
            app_version_id=self._app_version['public_id'],
            experiment_uuid=experiment_id,
            machine=machine,
            notify=notify,
            override_command=override_command,
            timeout=timeout,
        )
        JobStorage.upload_module_input(job=job_dict, module_input_serialized=module_input_serialized)
        cloud_job = BiolibJobApi.create_cloud_job(job_id=job_dict['public_id'], result_name_prefix=result_prefix)
        logger.debug(f"Cloud: Job created with id {cloud_job['public_id']}")
        return Job(cast(JobDict, job_dict))

    def _run_locally(self, module_input_serialized: bytes) -> Job:
        job_dict = BiolibJobApi.create(
            app_version_id=self._app_version['public_id'],
            app_resource_name_prefix=parse_app_uri(self._app_uri)['resource_name_prefix']
        )
        job = Job(job_dict)

        try:
            BiolibJobApi.update_state(job.id, JobState.IN_PROGRESS)
            module_output = JobWorker().run_job_locally(job_dict, module_input_serialized)
            job._set_result_module_output(module_output)  # pylint: disable=protected-access
            BiolibJobApi.update_state(job.id, JobState.COMPLETED)
        except BaseException as error:
            BiolibJobApi.update_state(job.id, JobState.FAILED)
            raise error

        return job

    def run(self, **kwargs) -> Job:
        args = []
        biolib_kwargs = {}
        for key, value in kwargs.items():
            if key.startswith('biolib_'):
                biolib_kwarg_key = key.replace('biolib_', '')
                biolib_kwargs[biolib_kwarg_key] = value
                continue

            if isinstance(value, dict):
                value = io.StringIO(json.dumps(value))

            if not key.startswith('--'):
                key = f'--{key}'

            args.extend([key, value])

        return self.cli(args, **biolib_kwargs)

    def start(self, **kwargs) -> Job:
        return self.run(biolib_blocking=False, **kwargs)
