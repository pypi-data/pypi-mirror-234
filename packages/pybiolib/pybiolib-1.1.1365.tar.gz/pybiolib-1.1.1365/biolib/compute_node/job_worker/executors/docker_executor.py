import json
import tempfile
import time
import tarfile
import zipfile
import os
import io
import re
import shlex
from copy import copy
from datetime import datetime

import docker  # type: ignore
import docker.types  # type: ignore

from docker.errors import ImageNotFound  # type: ignore
from docker.models.containers import Container  # type: ignore

from biolib import utils
from biolib.biolib_binary_format import ModuleInput, ModuleOutputV2
from biolib.biolib_docker_client import BiolibDockerClient
from biolib.biolib_errors import DockerContainerNotFoundDuringExecutionException, BioLibError
from biolib.biolib_logging import logger, logger_no_user_data
from biolib.compute_node import utils as compute_node_utils
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.compute_node.job_worker.docker_image_cache import DockerImageCache
from biolib.biolib_binary_format.file_in_container import FileInContainer
from biolib.compute_node.job_worker.executors.docker_types import DockerDiffKind
from biolib.compute_node.job_worker.executors.types import StatusUpdate, LocalExecutorOptions
from biolib.compute_node.job_worker.mappings import Mappings, path_without_first_folder
from biolib.compute_node.job_worker.utils import ComputeProcessException
from biolib.compute_node.job_worker.utilization_reporter_thread import UtilizationReporterThread
from biolib.compute_node.utils import SystemExceptionCodes
from biolib.typing_utils import List, Dict, Optional


class DockerExecutor:

    def __init__(self, options: LocalExecutorOptions):
        self._options: LocalExecutorOptions = options
        self._is_cleaning_up = False

        # TODO: Move this to shared class
        ##########
        if self._options['root_job_id'] == utils.RUN_DEV_JOB_ID:
            self._image_uri = self._options['module']['image_uri']
        else:
            absolute_container_image_uri = self._options['module']['absolute_image_uri']
            if absolute_container_image_uri:
                self._image_uri = str(absolute_container_image_uri)
            else:
                error_msg = 'absolute_image_uri was not supplied by backend'
                logger_no_user_data.error(error_msg)
                raise Exception(error_msg)

        self._send_system_exception = options['send_system_exception']
        self._send_stdout_and_stderr = options['send_stdout_and_stderr']

        federated_job_uuid: Optional[str] = self._options['job'].get('federated_job_uuid')
        if options['compute_node_info'] is not None and not federated_job_uuid:
            compute_node_public_id = options['compute_node_info']['public_id']
            compute_node_auth_token = options['compute_node_info']['auth_token']
            # Use "|" to separate the fields as this makes it easy for the ECR proxy to split
            ecr_proxy_auth_token = f'cloud-{compute_node_public_id}|{compute_node_auth_token}'
        else:
            ecr_proxy_auth_token = options['access_token']

        docker_auth_job_id = federated_job_uuid or self._options['job']['public_id']
        self._docker_auth_config = {'username': 'AWS', 'password': f'{ecr_proxy_auth_token},{docker_auth_job_id}'}

        self._random_docker_id = compute_node_utils.random_string(15)
        #########

        if utils.IS_RUNNING_IN_CLOUD:
            self._compute_process_dir = os.getenv('BIOLIB_USER_DATA_PATH')
            if not self._compute_process_dir:
                raise Exception('Environment variable BIOLIB_USER_DATA_PATH is not set')
            if not os.path.isdir(self._compute_process_dir):
                raise Exception(f'User data directory {self._compute_process_dir} does not exist')

        else:
            self._compute_process_dir = os.path.dirname(os.path.realpath(__file__))

        user_data_tar_dir = f'{self._compute_process_dir}/tars'
        os.makedirs(user_data_tar_dir, exist_ok=True)

        self._docker_container: Optional[Container] = None
        self._runtime_tar_path = f'{user_data_tar_dir}/runtime_{self._random_docker_id}.tar'
        self._input_tar_path = f'{user_data_tar_dir}/input_{self._random_docker_id}.tar'

        if utils.IS_RUNNING_IN_CLOUD and not utils.BIOLIB_SECRETS_TMPFS_PATH:
            error_message = 'Running in cloud but no TMPFS path has been set for secrets'
            logger_no_user_data.error(error_message)
            raise BioLibError(error_message)

        # If BIOLIB_SECRETS_TMPFS_PATH is set create the temporary directory there
        self._tmp_secrets_dir = tempfile.TemporaryDirectory(dir=utils.BIOLIB_SECRETS_TMPFS_PATH or None)
        os.chmod(self._tmp_secrets_dir.name, 0o755)

    @property
    def _container(self) -> Container:
        if self._docker_container is None:
            raise Exception('Docker container was None')
        return self._docker_container

    def execute_module(self, module_input_serialized: bytes, module_output_path: str) -> None:
        try:
            job_uuid = self._options['job']['public_id']
            send_status_update = self._options['send_status_update']
            module_input = ModuleInput(module_input_serialized).deserialize()

            send_status_update(StatusUpdate(progress=55, log_message='Pulling images...'))

            self._pull()

            send_status_update(StatusUpdate(progress=70, log_message='Computing...'))
            start_time = time.time()

            logger_no_user_data.debug(f'Starting execution of {job_uuid}.')
            try:
                self._execute_helper(module_input, module_output_path)
            except docker.errors.NotFound as docker_error:
                raise DockerContainerNotFoundDuringExecutionException from docker_error
            except Exception as exception:
                raise ComputeProcessException(
                    exception,
                    SystemExceptionCodes.FAILED_TO_RUN_COMPUTE_CONTAINER.value,
                    self._send_system_exception,
                ) from exception
            logger_no_user_data.debug(f'Completed execution of {job_uuid}.')
            logger_no_user_data.debug(f'Compute time: {time.time() - start_time}')
        finally:
            try:
                self.cleanup()
            except Exception:  # pylint: disable=broad-except
                logger_no_user_data.error('DockerExecutor failed to clean up container')

    def _pull(self):
        try:
            start_time = time.time()
            if utils.IS_RUNNING_IN_CLOUD:
                DockerImageCache().get(
                    image_uri=self._image_uri,
                    estimated_image_size_bytes=self._options['module']['estimated_image_size_bytes'],
                    pull_auth_config=self._docker_auth_config,
                    job_id=self._options['job']['public_id']
                )
            else:
                docker_client = BiolibDockerClient.get_docker_client()
                try:
                    docker_client.images.get(self._image_uri)
                except ImageNotFound:
                    docker_client.images.pull(self._image_uri, auth_config=self._docker_auth_config)
            logger_no_user_data.debug(f'Pulled image in: {time.time() - start_time}')

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_PULL_DOCKER_IMAGE.value,
                self._send_system_exception,
                may_contain_user_data=False
            ) from exception

    def _execute_helper(self, module_input, module_output_path: str) -> None:
        job_uuid = self._options['job']['public_id']
        logger_no_user_data.debug(f'Initializing container for {job_uuid}.')
        self._initialize_docker_container(module_input)

        if self._options['runtime_zip_bytes']:
            self._map_and_copy_runtime_files_to_container(self._options['runtime_zip_bytes'], module_input['arguments'])

        logger_no_user_data.debug(f'_map_and_copy_input_files_to_container for {job_uuid}.')
        self._map_and_copy_input_files_to_container(module_input['files'], module_input['arguments'])

        docker_api_client = BiolibDockerClient.get_docker_client().api
        logger_no_user_data.debug(f'Starting Docker container for {job_uuid}')

        stdout_and_stderr_stream = docker_api_client.attach(
            container=self._container.id,
            stderr=True,
            stdout=True,
            stream=True,
        )

        pre_start_diff = self._container.diff()
        self._container.start()

        if utils.IS_RUNNING_IN_CLOUD:
            webserver_config = CloudUtils.get_webserver_config()
            UtilizationReporterThread(
                container=self._container,
                job_uuid=job_uuid,
                job_access_token=self._options['access_token'],
                compute_node_info=webserver_config['compute_node_info']  # pylint: disable=unsubscriptable-object
            ).start()

        if self._options['job']['app_version'].get('stdout_render_type') != 'markdown':
            for stdout_and_stderr in stdout_and_stderr_stream:
                # Default messages to empty bytestring instead of None
                stdout_and_stderr = stdout_and_stderr if stdout_and_stderr is not None else b''

                self._send_stdout_and_stderr(stdout_and_stderr)

        exit_code = docker_api_client.wait(self._container.id)['StatusCode']
        # 137 is the error code from linux OOM killer (Should catch 90% of OOM errors)
        if exit_code == 137:
            raise ComputeProcessException(
                MemoryError(),
                SystemExceptionCodes.OUT_OF_MEMORY.value,
                self._send_system_exception
            )

        logger_no_user_data.debug(f'Docker container exited with code {exit_code} for {job_uuid}')

        full_stdout = docker_api_client.logs(self._container.id, stdout=True, stderr=False)
        full_stderr = docker_api_client.logs(self._container.id, stdout=False, stderr=True)

        self._write_module_output_to_file(
            arguments=module_input['arguments'],
            exit_code=exit_code,
            module_output_path=module_output_path,
            stderr=full_stderr,
            stdout=full_stdout,
            pre_start_diff=pre_start_diff,
        )

    def cleanup(self):
        # Don't clean up if already in the process of doing so, or done doing so
        if self._is_cleaning_up:
            return
        else:
            self._is_cleaning_up = True

        tar_time = time.time()
        for path_to_delete in [self._input_tar_path, self._runtime_tar_path]:
            if os.path.exists(path_to_delete):
                os.remove(path_to_delete)
        logger_no_user_data.debug(f"Deleted tars in: {time.time() - tar_time}")

        container_time = time.time()
        if self._docker_container:
            self._docker_container.remove(force=True)

        if utils.IS_RUNNING_IN_CLOUD:
            DockerImageCache().detach_job(
                image_uri=self._image_uri,
                job_id=self._options['job']['public_id']
            )

        logger_no_user_data.debug(f"Deleted compute container in: {time.time() - container_time}")
        self._tmp_secrets_dir.cleanup()

    # TODO: type this method
    def _initialize_docker_container(self, module_input):
        try:
            module = self._options['module']
            logger.debug(f"Initializing docker container with command: {module['command']}")

            docker_volume_mounts = [lfs.docker_mount for lfs in self._options['large_file_systems'].values()]

            internal_network = self._options['internal_network']
            extra_hosts: Dict[str, str] = {}

            biolib_system_secret = {
                'version': '1.0.0',
                'job_uuid': self._options['job']['public_id'],
                'job_auth_token': self._options['job']['auth_token'],
            }
            secrets: Dict[str, str] = dict(
                **module.get('secrets', {}),
                biolib_system_secret=json.dumps(biolib_system_secret, indent=4),
            )
            docker_volume_mounts.append(self._create_secrets_mount(secrets))

            environment_vars = {}

            # Include secrets and job info as env vars for app versions created before 20/11/2022
            app_version_created_at = datetime.strptime(
                self._options['job']['app_version']['created_at'],
                '%Y-%m-%dT%H:%M:%S.%fZ',
            )
            if app_version_created_at < datetime(2022, 11, 30, 0, 0):
                environment_vars = module.get('secrets', {})
                environment_vars.update({
                    'BIOLIB_JOB_UUID': self._options['job']['public_id'],
                    'BIOLIB_JOB_AUTH_TOKEN': self._options['job']['auth_token']
                })

            if utils.IS_RUNNING_IN_CLOUD and self._options['cloud_job']:
                environment_vars.update({
                    'BIOLIB_JOB_MAX_RUNTIME_IN_SECONDS': self._options['cloud_job']['max_runtime_in_seconds'],
                })

            for proxy in self._options['remote_host_proxies']:
                proxy_ip = proxy.get_ip_address_on_network(internal_network)
                if proxy.is_app_caller_proxy:
                    logger_no_user_data.debug('Found app caller proxy, setting both base URLs in compute container')
                    environment_vars.update({
                        'BIOLIB_BASE_URL': f'http://{proxy_ip}',
                        'BIOLIB_CLOUD_BASE_URL': f'http://{proxy_ip}',
                        # This should be removed eventually, but will break apps calling apps on older versions
                        'BIOLIB_CLOUD_RESULTS_BASE_URL': f'http://{proxy_ip}',
                        'BIOLIB_CLOUD_JOB_STORAGE_BASE_URL': f'http://{proxy_ip}',
                        # Inform container if we are targeting public biolib as we change the BIOLIB_BASE_URL
                        'BIOLIB_ENVIRONMENT_IS_PUBLIC_BIOLIB': bool(utils.BASE_URL_IS_PUBLIC_BIOLIB)
                    })
                else:
                    extra_hosts[proxy.hostname] = proxy_ip

            create_container_args = {
                'environment': environment_vars,
                'extra_hosts': extra_hosts,
                'image': self._image_uri,
                'mounts': docker_volume_mounts,
                'network': internal_network.name,
                'working_dir': module['working_directory'],
            }

            if self._options['job'].get('arguments_override_command'):
                # In this case, arguments contains a user specified command to run in the app
                create_container_args.update({
                    'command': module_input['arguments'],
                    'entrypoint': ''
                })

            else:
                create_container_args.update({
                    'command': shlex.split(module['command']) + module_input['arguments']
                })

            app_version = self._options['job']['app_version']
            if app_version.get('main_output_file') or app_version.get('stdout_render_type') == 'text':
                create_container_args['tty'] = True

            if utils.IS_RUNNING_IN_CLOUD:
                cloud_job = self._options["cloud_job"]
                create_container_args['mem_limit'] = f'{cloud_job["reserved_memory_in_bytes"]}b'
                create_container_args['nano_cpus'] = cloud_job["reserved_cpu_in_nano_shares"]

                biolib_identity_user_email: Optional[str] = cloud_job.get('biolib_identity_user_email')
                if biolib_identity_user_email:
                    create_container_args['environment'].update({
                        'BIOLIB_IDENTITY_USER_EMAIL': biolib_identity_user_email
                    })

            docker_runtime = os.getenv('BIOLIB_DOCKER_RUNTIME')
            if docker_runtime is not None:
                create_container_args['runtime'] = docker_runtime

            self._docker_container = BiolibDockerClient.get_docker_client().containers.create(
                **create_container_args
            )

            logger_no_user_data.debug('Finished initializing docker container')
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_START_COMPUTE_CONTAINER.value,
                self._send_system_exception
            ) from exception

    def _add_file_to_tar(self, tar, current_path, mapped_path, data):
        if current_path.endswith('/'):
            # Remove trailing slash as tarfile.addfile appends it automatically
            tarinfo = tarfile.TarInfo(name=mapped_path[:-1])
            tarinfo.type = tarfile.DIRTYPE
            tar.addfile(tarinfo)

        else:
            tarinfo = tarfile.TarInfo(name=mapped_path)
            file_like = io.BytesIO(data)
            tarinfo.size = len(file_like.getvalue())
            tar.addfile(tarinfo, file_like)

    def _make_input_tar(self, files, arguments: List[str]):
        module = self._options['module']
        input_tar = tarfile.open(self._input_tar_path, 'w')
        input_mappings = Mappings(module['input_files_mappings'], arguments)
        for path, data in files.items():
            # Make all paths absolute
            if not path.startswith('/'):
                path = '/' + path

            mapped_file_names = input_mappings.get_mappings_for_path(path)
            for mapped_file_name in mapped_file_names:
                self._add_file_to_tar(tar=input_tar, current_path=path, mapped_path=mapped_file_name, data=data)

        input_tar.close()

    def _make_runtime_tar(self, runtime_zip_data, arguments: List[str], remove_root_folder=True):
        module = self._options['module']
        runtime_tar = tarfile.open(self._runtime_tar_path, 'w')
        runtime_zip = zipfile.ZipFile(io.BytesIO(runtime_zip_data))
        source_mappings = Mappings(module['source_files_mappings'], arguments)

        for zip_file_name in runtime_zip.namelist():
            # Make paths absolute and remove root folder from path
            if remove_root_folder:
                file_path = '/' + path_without_first_folder(zip_file_name)
            else:
                file_path = '/' + zip_file_name
            mapped_file_names = source_mappings.get_mappings_for_path(file_path)
            for mapped_file_name in mapped_file_names:
                file_data = runtime_zip.read(zip_file_name)
                self._add_file_to_tar(
                    tar=runtime_tar,
                    current_path=zip_file_name,
                    mapped_path=mapped_file_name,
                    data=file_data,
                )

        runtime_tar.close()

    def _map_and_copy_input_files_to_container(self, files, arguments: List[str]):
        try:
            if self._docker_container is None:
                raise Exception('Docker container was None')

            self._make_input_tar(files, arguments)
            input_tar_bytes = open(self._input_tar_path, 'rb').read()
            BiolibDockerClient.get_docker_client().api.put_archive(self._docker_container.id, '/', input_tar_bytes)
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_COPY_INPUT_FILES_TO_COMPUTE_CONTAINER.value,
                self._send_system_exception
            ) from exception

    def _map_and_copy_runtime_files_to_container(self, runtime_zip_data, arguments: List[str], remove_root_folder=True):
        try:
            if self._docker_container is None:
                raise Exception('Docker container was None')

            self._make_runtime_tar(runtime_zip_data, arguments, remove_root_folder)
            runtime_tar_bytes = open(self._runtime_tar_path, 'rb').read()
            BiolibDockerClient.get_docker_client().api.put_archive(self._docker_container.id, '/', runtime_tar_bytes)
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_COPY_RUNTIME_FILES_TO_COMPUTE_CONTAINER.value,
                self._send_system_exception
            ) from exception

    def _write_module_output_to_file(
            self,
            arguments: List[str],
            exit_code: int,
            module_output_path: str,
            stderr: bytes,
            stdout: bytes,
            pre_start_diff: List[Dict],
    ) -> None:
        mapped_files: List[FileInContainer] = []
        try:
            mappings = Mappings(mappings_list=self._options['module']['output_files_mappings'], arguments=arguments)
            changed_files: List[FileInContainer] = self._get_changed_files_in_docker_container(pre_start_diff)

            for file in changed_files:
                if file.is_file():
                    for mapped_path in mappings.get_mappings_for_path(file.path):
                        mapped_output_file = copy(file)
                        mapped_output_file.path = mapped_path
                        mapped_files.append(mapped_output_file)

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_RETRIEVE_AND_MAP_OUTPUT_FILES.value,
                self._send_system_exception,
            ) from exception

        try:
            ModuleOutputV2.write_to_file(
                exit_code=exit_code,
                files=mapped_files,
                output_file_path=module_output_path,
                stderr=stderr,
                stdout=stdout,
            )
        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_SERIALIZE_AND_SEND_MODULE_OUTPUT.value,
                self._send_system_exception,
            ) from exception

    def _get_changed_files_in_docker_container(self, pre_start_diff: List[Dict]) -> List[FileInContainer]:
        from_mappings = [mapping['from_path'] for mapping in self._options['module']['output_files_mappings']]
        pre_start_diff_paths = [obj['Path'] for obj in pre_start_diff]
        post_run_diff = self._container.diff()
        run_diff_paths: List[str] = [
            obj['Path'] for obj in post_run_diff if
            obj['Kind'] in (DockerDiffKind.CHANGED.value, DockerDiffKind.ADDED.value) and
            obj['Path'] not in pre_start_diff_paths
        ]

        known_directories = set()
        for path in run_diff_paths:
            parent_folders = path.split('/')[:-1]
            for idx in range(len(parent_folders)):
                if idx == 0:
                    continue  # always skip root

                folder = '/' + '/'.join(parent_folders[1:idx + 1])
                known_directories.add(folder)

        def path_is_included_in_from_mappings(path: str) -> bool:
            for from_mapping in from_mappings:
                if path.startswith(from_mapping):
                    return True
            return False

        overlay_upper_dir_path = self._container.attrs['GraphDriver']['Data']['UpperDir']
        if not os.path.exists(overlay_upper_dir_path):
            overlay_upper_dir_path = None
            logger_no_user_data.debug(
                'Docker Overlay2 UpperDir not available. Falling back to container.get_archive() for file extraction'
            )

        logger.debug(f'overlay_upper_dir_path={overlay_upper_dir_path}')

        files_and_empty_dirs: List[FileInContainer] = []
        for path in run_diff_paths:
            if path not in known_directories and path_is_included_in_from_mappings(path):
                files_and_empty_dirs.append(FileInContainer(
                    container=self._container,
                    overlay_upper_dir_path=overlay_upper_dir_path,
                    path_in_container=path,
                ))

        return files_and_empty_dirs

    def _create_secrets_mount(self, secrets: Dict[str, str]) -> docker.types.Mount:
        job_uuid = self._options['job']['public_id']

        for key, value in secrets.items():
            if re.match(r'^[a-zA-Z0-9-_]+$', key):
                with open(f'{self._tmp_secrets_dir.name}/{key}', 'w') as secret_file:
                    secret_file.write(value)
            else:
                logger_no_user_data.warning(f'Job {job_uuid} uses secret with a key not matching validation regex')

        return docker.types.Mount(
            read_only=True,
            source=f'{self._tmp_secrets_dir.name}/',
            target='/biolib/secrets/',
            type='bind',
        )
