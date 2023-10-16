import io
import os.path
import tarfile

from docker.models.containers import Container  # type: ignore

from biolib.typing_utils import Iterable, Optional


class FileInContainer:
    def __init__(self, container: Container, path_in_container: str, overlay_upper_dir_path: Optional[str]):
        self._container: Container = container
        self._path_on_disk: Optional[str] = overlay_upper_dir_path + path_in_container if overlay_upper_dir_path \
            else None

        self._path_in_container: str = path_in_container
        self._path: str = path_in_container
        self._buffered_file_data: Optional[bytes] = None

    def __repr__(self) -> str:
        return f'FileInContainer({self.path})'

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    def is_file(self) -> bool:
        if self._path_on_disk:
            return os.path.isfile(self._path_on_disk)
        else:
            return self._get_file_data_from_container_via_tar() is not None

    def get_data_size_in_bytes(self) -> int:
        if self._path_on_disk:
            return os.path.getsize(self._path_on_disk)
        else:
            file_data = self._get_file_data_from_container_via_tar()
            return len(file_data) if file_data else 0

    def get_data_stream(self) -> Iterable[bytes]:
        if self._path_on_disk:
            with open(self._path_on_disk, mode='rb') as file:
                while True:
                    chunk = file.read(1_024)
                    if not chunk:
                        return

                    yield chunk
        else:
            yield self._get_file_data_from_container_via_tar() or bytes()

    def _get_file_data_from_container_via_tar(self) -> Optional[bytes]:
        if not self._buffered_file_data:
            with io.BytesIO() as tmp_io:
                stream, _ = self._container.get_archive(path=self._path_in_container)
                for chunk in stream:
                    tmp_io.write(chunk)

                tmp_io.seek(0)
                with tarfile.open(fileobj=tmp_io) as tar:
                    members = tar.getmembers()
                    file_members = [member for member in members if member.isfile()]
                    if not file_members:
                        # Path was not a file
                        return None

                    assert len(file_members) == 1
                    file_obj = tar.extractfile(member=file_members[0])
                    if not file_obj:
                        # Path was not a file
                        return None

                    self._buffered_file_data = file_obj.read()

        return self._buffered_file_data
