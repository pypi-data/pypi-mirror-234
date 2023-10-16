import sys
import click

from biolib import biolib_errors, utils
from biolib.app import BioLibApp
from biolib.typing_utils import Tuple


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_interspersed_args=False),
    help='Run an application on BioLib',
)
@click.option('--local', is_flag=True, required=False, help='Run the application locally')
@click.argument('uri', required=True)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def run(local: bool, uri: str, args: Tuple[str]) -> None:
    try:
        app = BioLibApp(uri=uri)
    except biolib_errors.BioLibError as error:
        print(f'An error occurred:\n {error.message}', file=sys.stderr)
        exit(1)

    def _get_stdin():
        stdin = None
        if not sys.stdin.isatty() and not utils.IS_DEV:
            stdin = sys.stdin.read()
        return stdin

    job = app.cli(args=list(args), stdin=_get_stdin(), files=None, machine=('local' if local else ''))
    job.save_files('biolib_results')

    # Write stdout and stderr if it has not been streamed (Markdown is not streamed)
    if app.version.get('stdout_render_type') == 'markdown' or not sys.stdout.isatty():
        sys.stdout.buffer.write(job.get_stdout())
        sys.stderr.buffer.write(job.get_stderr())

    exit(job.get_exit_code())
