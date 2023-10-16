import logging
from typing import Optional

import click

from biolib.biolib_logging import logger, logger_no_user_data
from biolib.biolib_push import push_application


@click.command(help='Push an application to BioLib')
@click.argument('uri')
@click.option('--path', default='.', required=False)
@click.option('--copy-images-from-version', required=False)
@click.option('--dev', is_flag=True, default=False, required=False)
def push(uri, path: str, copy_images_from_version: Optional[str], dev: bool) -> None:
    logger.configure(default_log_level=logging.INFO)
    logger_no_user_data.configure(default_log_level=logging.INFO)
    push_application(
        app_path=path,
        app_uri=uri,
        app_version_to_copy_images_from=copy_images_from_version,
        is_dev_version=dev,
    )
