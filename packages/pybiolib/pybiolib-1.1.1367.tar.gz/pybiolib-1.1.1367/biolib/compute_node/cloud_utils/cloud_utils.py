# pylint: disable=unsubscriptable-object
import base64
import json
import os
import subprocess
import time
from datetime import datetime
from socket import gethostbyname, gethostname
import requests

import biolib.api

from biolib import utils
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger_no_user_data
from biolib.typing_utils import Optional
from biolib.biolib_api_client import BiolibApiClient
from biolib.compute_node.webserver.webserver_types import WebserverConfig, ComputeNodeInfo, ShutdownTimes

def trust_ceritificates(certs_data):
    # cert path on amazon linux 2
    ca_directory = "/etc/pki/ca-trust/source/anchors/"

    if not os.path.exists(ca_directory):
        logger_no_user_data.error(f"Certificate path not found at {ca_directory}")
        return
    for idx, cert_data in enumerate(certs_data):
        with open(f"{ca_directory}bl-cert-{idx}.crt","w") as fcert:
            fcert.write(cert_data)

    result = subprocess.run(['update-ca-trust'], capture_output=True, check=False)
    logger_no_user_data.debug(result.stdout.decode())
    if result.returncode == 0:
        logger_no_user_data.info("Certificates added successfully!")
    else:
        logger_no_user_data.error(f"Failed to update certificates: {result.stderr.decode()}")


class CloudUtils:
    _webserver_config: Optional[WebserverConfig] = None

    @staticmethod
    def initialize() -> None:
        logger_no_user_data.info('Reporting availability...')
        CloudUtils._report_availability()

    @staticmethod
    def get_webserver_config() -> WebserverConfig:
        if CloudUtils._webserver_config:
            return CloudUtils._webserver_config

        CloudUtils._webserver_config = WebserverConfig(
            compute_node_info=ComputeNodeInfo(
                auth_token=CloudUtils._get_environment_variable_or_fail('BIOLIB_COMPUTE_NODE_AUTH_TOKEN'),
                ip_address=os.environ.get('BIOLIB_COMPUTE_NODE_CUSTOM_IP', default=gethostbyname(gethostname())),
                public_id=CloudUtils._get_environment_variable_or_fail('BIOLIB_COMPUTE_NODE_PUBLIC_ID'),
                pybiolib_version=utils.BIOLIB_PACKAGE_VERSION,
            ),
            base_url=CloudUtils._get_environment_variable_or_fail('BIOLIB_BASE_URL'),
            s3_general_storage_bucket_name=CloudUtils._get_environment_variable_or_fail(
                'BIOLIB_S3_GENERAL_STORAGE_BUCKET_NAME',
            ),
            is_dev=os.environ.get('BIOLIB_DEV') == 'TRUE',
            shutdown_times=ShutdownTimes(
                auto_shutdown_time_in_seconds=CloudUtils._get_environment_variable_as_int(
                    'BIOLIB_CLOUD_AUTO_SHUTDOWN_TIME_IN_SECONDS'
                ),
            )
        )

        return CloudUtils._webserver_config

    @staticmethod
    def deregister_and_shutdown() -> None:
        logger_no_user_data.debug('Deregistering...')

        if utils.IS_RUNNING_IN_CLOUD:
            config = CloudUtils.get_webserver_config()
            try:
                response = requests.post(url=f'{config["base_url"]}/api/jobs/deregister/', json={
                    'auth_token': config["compute_node_info"]["auth_token"],
                    'public_id': config["compute_node_info"]["public_id"],
                })

                if not response.ok:
                    response_content = response.content.decode()
                    logger_no_user_data.error(
                        f'Failed to deregister got status {response.status_code} and response {response_content}'
                    )

            except Exception as error:  # pylint: disable=broad-except
                logger_no_user_data.error(f'Failed to deregister got error: {error}')

            logger_no_user_data.debug('Waiting 10 seconds and shutting down...')
            # Sleep for 10 seconds to ensure logs are written
            time.sleep(10)
            logger_no_user_data.debug('Shutting down...')
            try:
                subprocess.run(['sudo', 'shutdown', 'now'], check=True)
            except Exception as error:  # pylint: disable=broad-except
                logger_no_user_data.error(f'Failed to shutdown got error: {error}')

        else:
            logger_no_user_data.error("Not deregistering as environment is not cloud")

    @staticmethod
    def finish_cloud_job(cloud_job_id: str, system_exception_code: Optional[int], exit_code: Optional[int]) -> None:
        if not cloud_job_id:
            logger_no_user_data.error(
                'Finish cloud job was called but no cloud job was supplied. '
                f'System exception code: {system_exception_code}'
            )
            return

        config = CloudUtils.get_webserver_config()

        for _ in range(100):
            try:
                response = requests.post(
                    url=f'{config["base_url"]}/api/jobs/cloud/finish/',
                    json={
                        'auth_token': config["compute_node_info"]["auth_token"],
                        'cloud_job_id': cloud_job_id,
                        'system_exception_code': system_exception_code,
                        'exit_code': exit_code
                    },
                    timeout=10,
                )

                response.raise_for_status()

                opt_error_string = f' with error code {system_exception_code}' if system_exception_code else ''
                logger_no_user_data.debug(
                    f'Cloud Job "{cloud_job_id}" was reported as finished' + opt_error_string
                )
                return

            except Exception as error:  # pylint: disable=broad-except
                logger_no_user_data.debug(
                    f'Could not finish cloud job "{cloud_job_id}" due to {error}, retrying...'
                )
                time.sleep(10)


    @staticmethod
    def _report_availability() -> None:
        try:
            config = CloudUtils.get_webserver_config()
            compute_node_info = config['compute_node_info']
            api_client = BiolibApiClient.get()
            logger_no_user_data.debug(
                f'Registering with {compute_node_info} to host {api_client.base_url} at {datetime.now()}'
            )

            response: Optional[requests.Response] = None
            max_retries = 5
            for retry_count in range(max_retries):
                try:
                    response = requests.post(
                        url=f'{api_client.base_url}/api/jobs/report_available/',
                        json=compute_node_info,
                    )
                    break
                except Exception as error:  # pylint: disable=broad-except
                    logger_no_user_data.error(f'Self-registering failed with error: {error}')
                    if retry_count < max_retries - 1:
                        seconds_to_sleep = 1
                        logger_no_user_data.info(f'Retrying self-registering in {seconds_to_sleep} seconds')
                        time.sleep(seconds_to_sleep)

            if not response:
                raise BioLibError('Failed to register. Max retry limit reached')

            if response.status_code != 201:
                raise Exception("Non 201 error code")
            else:
                logger_no_user_data.info("Compute node registered!")
                response_data = response.json()
                logger_no_user_data.info(f"Got data on register: {json.dumps(response_data)}")
                certs = []
                for federation in response_data["federation"]:
                    for cert_b64 in federation["certs_b64"]:
                        certs.append(base64.b64decode(cert_b64).decode())
                trust_ceritificates(certs)

        except Exception as exception:  # pylint: disable=broad-except
            logger_no_user_data.error(f'Shutting down as self register failed due to: {exception}')
            if not utils.IS_DEV:
                CloudUtils.deregister_and_shutdown()

    @staticmethod
    def _get_environment_variable_or_fail(key: str) -> str:
        value = os.environ.get(key)
        # Purposely loose falsy check (instead of `is not None`) as empty string should fail
        if not value:
            raise Exception(f'CloudUtils: Missing environment variable "{key}"')

        return value

    @staticmethod
    def _get_environment_variable_as_int(key: str) -> int:
        return int(CloudUtils._get_environment_variable_or_fail(key))

    @staticmethod
    def write_utilization_metric_sample(
            job_auth_token: str,
            compute_node_auth_token: str,
            data: dict,
    ):
        response = biolib.api._client.post(  # pylint: disable=protected-access
            path='/utilization_metrics/',
            headers={
                'Job-Auth-Token': job_auth_token,
                'Compute-Node-Auth-Token': compute_node_auth_token
            },
            data=data
        )  # pylint: disable=protected-access

        return response
