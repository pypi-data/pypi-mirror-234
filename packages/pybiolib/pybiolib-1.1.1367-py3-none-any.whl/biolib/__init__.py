# Imports to hide
import os

from biolib import typing_utils as _typing_utils
from biolib.app import BioLibApp as _BioLibApp
# TODO: Fix ignore of type
from biolib.app.search_apps import search_apps  # type: ignore
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger as _logger, logger_no_user_data as _logger_no_user_data
from biolib.experiments.experiment import Experiment
from biolib.biolib_api_client import BiolibApiClient as _BioLibApiClient, App
from biolib.jobs import Job as _Job
from biolib import user as _user
from biolib.typing_utils import List, Optional

import biolib.api
import biolib.app
import biolib.cli
import biolib.utils


# ------------------------------------ Function definitions for public Python API ------------------------------------

def call_cli() -> None:
    biolib.cli.cli()


def load(uri: str) -> _BioLibApp:
    return _BioLibApp(uri)


def search(
        search_query: Optional[str] = None,
        team: Optional[str] = None,
        count: int = 100
    ) -> List[str]:
    apps: List[str] = search_apps(search_query, team, count)
    return apps


def get_job(job_id: str) -> _Job:
    return _Job.create_from_uuid(uuid=job_id)


def fetch_jobs(count: int = 25) -> List[_Job]:
    return _Job.fetch_jobs(count)


def get_experiment(name: str) -> Experiment:
    return Experiment(name)


def show_jobs(count: int = 25) -> None:
    _Job.show_jobs(count=count)


def show_experiments(count: int = 25) -> None:
    Experiment.show_experiments(count=count)


def sign_in() -> None:
    _user.sign_in()


def sign_out() -> None:
    _user.sign_out()


def login() -> None:
    sign_in()


def logout() -> None:
    sign_out()


def set_api_base_url(api_base_url: str) -> None:
    _BioLibApiClient.initialize(base_url=api_base_url)
    biolib.utils.BIOLIB_BASE_URL = api_base_url
    biolib.utils.BASE_URL_IS_PUBLIC_BIOLIB = api_base_url.endswith('biolib.com') or (
            os.environ.get('BIOLIB_ENVIRONMENT_IS_PUBLIC_BIOLIB', '').upper() == 'TRUE'
    )


def set_base_url(base_url: str) -> None:
    return set_api_base_url(base_url)


def set_api_token(api_token: str) -> None:
    api_client = _BioLibApiClient.get()
    api_client.sign_in_with_api_token(api_token)


def set_log_level(level: _typing_utils.Union[str, int]) -> None:
    _logger.setLevel(level)
    _logger_no_user_data.setLevel(level)


def _configure_requests_certificates():
    if os.getenv('REQUESTS_CA_BUNDLE'):
        return  # don't change REQUESTS_CA_BUNDLE if manually configured

    certs_to_check = [
        '/etc/ssl/certs/ca-certificates.crt',
        '/etc/pki/tls/certs/ca-bundle.crt',
        '/etc/ssl/ca-bundle.pem',
        '/etc/pki/tls/cacert.pem',
        '/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem',
        '/etc/ssl/cert.pem',
    ]

    for cert in certs_to_check:
        if os.path.exists(cert):
            os.environ['REQUESTS_CA_BUNDLE'] = cert
            return


# -------------------------------------------------- Configuration ---------------------------------------------------
__version__ = biolib.utils.BIOLIB_PACKAGE_VERSION
_DEFAULT_LOG_LEVEL = 'INFO' if biolib.utils.IS_RUNNING_IN_NOTEBOOK else 'WARNING'
_logger.configure(default_log_level=_DEFAULT_LOG_LEVEL)
_logger_no_user_data.configure(default_log_level=_DEFAULT_LOG_LEVEL)
_configure_requests_certificates()

set_api_base_url(biolib.utils.BIOLIB_BASE_URL)
