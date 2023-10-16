import logging
import sys

import click

from biolib import biolib_errors
from biolib.biolib_logging import logger_no_user_data, logger
from biolib.lfs import push_large_file_system, create_large_file_system, describe_large_file_system, prune_lfs_cache
from biolib.typing_utils import Optional


@click.group(help='Manage Large File Systems')
def lfs() -> None:
    pass


@lfs.command(help='Create a Large File System')
@click.argument('uri', required=True)
def create(uri: str) -> None:
    logger.configure(default_log_level=logging.INFO)
    logger_no_user_data.configure(default_log_level=logging.INFO)
    create_large_file_system(lfs_uri=uri)


@lfs.command(help='Push a new version of a Large File System')
@click.argument('uri', required=True)
@click.option('--path', required=True, type=click.Path(exists=True))
@click.option('--chunk-size', default=None, required=False, type=click.INT, help='The size of each chunk (In MB)')
def push(uri: str, path: str, chunk_size: Optional[int]) -> None:
    logger.configure(default_log_level=logging.INFO)
    logger_no_user_data.configure(default_log_level=logging.INFO)
    try:
        push_large_file_system(lfs_uri=uri, input_dir=path, chunk_size_in_mb=chunk_size)
    except biolib_errors.BioLibError as error:
        print(f'An error occurred:\n{error.message}', file=sys.stderr)
        exit(1)


@lfs.command(help='Describe a Large File System')
@click.argument('uri', required=True)
@click.option('--json', is_flag=True, default=False, required=False, help='Format output as JSON')
def describe(uri: str, json: bool) -> None:
    describe_large_file_system(lfs_uri=uri, output_as_json=json)


@lfs.command(help='Prune LFS cache', hidden=True)
@click.option('--dry-run', type=click.BOOL, default=True, required=False)
def prune_cache(dry_run: bool) -> None:
    logger.configure(default_log_level=logging.INFO)
    logger_no_user_data.configure(default_log_level=logging.INFO)
    prune_lfs_cache(dry_run)
