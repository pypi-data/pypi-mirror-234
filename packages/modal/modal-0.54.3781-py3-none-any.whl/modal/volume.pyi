import asyncio.locks
import modal.object
import modal_proto.api_pb2
import pathlib
import typing
import typing_extensions

class _Volume(modal.object._Object):
    _lock: asyncio.locks.Lock

    def _initialize_from_empty(self):
        ...

    @staticmethod
    def new() -> _Volume:
        ...

    @staticmethod
    def persisted(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> _Volume:
        ...

    async def _do_reload(self, lock=True):
        ...

    async def commit(self):
        ...

    async def reload(self):
        ...

    def iterdir(self, path: str) -> typing.AsyncIterator[modal_proto.api_pb2.VolumeListFilesEntry]:
        ...

    async def listdir(self, path: str) -> typing.List[modal_proto.api_pb2.VolumeListFilesEntry]:
        ...

    def read_file(self, path: typing.Union[str, bytes]) -> typing.AsyncIterator[bytes]:
        ...

    async def _add_local_file(self, local_path: typing.Union[pathlib.Path, str], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None):
        ...

    async def _add_local_dir(self, local_path: typing.Union[pathlib.Path, str], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None):
        ...

    async def _upload_file(self, local_path: typing.Union[pathlib.Path, str], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> modal_proto.api_pb2.MountFile:
        ...


class Volume(modal.object.Object):
    _lock: asyncio.locks.Lock

    def __init__(self, *args, **kwargs):
        ...

    def _initialize_from_empty(self):
        ...

    @staticmethod
    def new() -> Volume:
        ...

    @staticmethod
    def persisted(label: str, namespace=1, environment_name: typing.Union[str, None] = None) -> Volume:
        ...

    class ___do_reload_spec(typing_extensions.Protocol):
        def __call__(self, lock=True):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _do_reload: ___do_reload_spec

    class __commit_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    commit: __commit_spec

    class __reload_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    reload: __reload_spec

    class __iterdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.Iterator[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

        def aio(self, path: str) -> typing.AsyncIterator[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

    iterdir: __iterdir_spec

    class __listdir_spec(typing_extensions.Protocol):
        def __call__(self, path: str) -> typing.List[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

        async def aio(self, *args, **kwargs) -> typing.List[modal_proto.api_pb2.VolumeListFilesEntry]:
            ...

    listdir: __listdir_spec

    class __read_file_spec(typing_extensions.Protocol):
        def __call__(self, path: typing.Union[str, bytes]) -> typing.Iterator[bytes]:
            ...

        def aio(self, path: typing.Union[str, bytes]) -> typing.AsyncIterator[bytes]:
            ...

    read_file: __read_file_spec

    class ___add_local_file_spec(typing_extensions.Protocol):
        def __call__(self, local_path: typing.Union[pathlib.Path, str], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _add_local_file: ___add_local_file_spec

    class ___add_local_dir_spec(typing_extensions.Protocol):
        def __call__(self, local_path: typing.Union[pathlib.Path, str], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _add_local_dir: ___add_local_dir_spec

    class ___upload_file_spec(typing_extensions.Protocol):
        def __call__(self, local_path: typing.Union[pathlib.Path, str], remote_path: typing.Union[str, pathlib.PurePosixPath, None] = None) -> modal_proto.api_pb2.MountFile:
            ...

        async def aio(self, *args, **kwargs) -> modal_proto.api_pb2.MountFile:
            ...

    _upload_file: ___upload_file_spec
