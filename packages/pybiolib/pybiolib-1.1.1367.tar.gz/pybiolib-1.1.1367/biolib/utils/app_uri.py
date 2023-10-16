import re

from biolib.biolib_errors import BioLibError
from biolib.typing_utils import TypedDict, Optional


class SemanticVersion(TypedDict):
    major: int
    minor: int
    patch: int


class AppUriParsed(TypedDict):
    account_handle_normalized: str
    app_name_normalized: str
    resource_name_prefix: Optional[str]
    version: Optional[SemanticVersion]


def normalize(string):
    return string.replace('-', '_').lower()


# Mainly copied from backend
def parse_app_uri(uri: str) -> AppUriParsed:
    uri_regex = r'^(@(?P<resource_name_prefix>[\w._-]+)/)?(?P<account_handle>[\w-]+)(/(?P<app_name>[\w-]+))?' \
                r'(:(?P<version>(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)))?$'

    uri_without_trailing_asterisk_version = uri[:-2] if uri.endswith(':*') else uri
    matches = re.search(uri_regex, uri_without_trailing_asterisk_version)
    if matches is None:
        raise BioLibError(f"Could not parse app uri '{uri}', uri did not match regex")

    resource_name_prefix: Optional[str] = matches.group('resource_name_prefix')
    account_handle_normalized: str = normalize(matches.group('account_handle'))
    app_name: Optional[str] = matches.group('app_name')

    # Default to account_handle if app_name is not supplied
    app_name_normalized = normalize(app_name) if app_name is not None else account_handle_normalized

    return AppUriParsed(
        resource_name_prefix=resource_name_prefix.lower() if resource_name_prefix is not None else 'biolib.com',
        account_handle_normalized=account_handle_normalized,
        app_name_normalized=app_name_normalized,
        version=None if not matches.group('version') else SemanticVersion(
            major=int(matches.group('major')),
            minor=int(matches.group('minor')),
            patch=int(matches.group('patch')),
        )
    )
