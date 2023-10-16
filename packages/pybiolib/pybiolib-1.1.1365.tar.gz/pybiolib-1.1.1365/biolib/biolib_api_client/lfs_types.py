from biolib.typing_utils import TypedDict


class LargeFileSystemVersion(TypedDict):
    presigned_download_url: str
    size_bytes: int
    uri: str
    uuid: str


class LargeFileSystem(TypedDict):
    uri: str
    uuid: str
