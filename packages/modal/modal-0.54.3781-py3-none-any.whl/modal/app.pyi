import google.protobuf.message
import modal._output
import modal.client
import modal.object
import typing
import typing_extensions

Tree = typing.TypeVar("Tree")

class _LocalApp:
    _tag_to_object_id: typing.Dict[str, str]
    _client: modal.client._Client
    _app_id: str
    _app_page_url: str
    _environment_name: str

    def __init__(self, client: modal.client._Client, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, stub_name: typing.Union[str, None] = None, environment_name: typing.Union[str, None] = None):
        ...

    @property
    def client(self) -> modal.client._Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    async def _create_all_objects(self, blueprint: typing.Dict[str, modal.object._Object], new_app_state: int, environment_name: str, shell: bool = False, output_mgr: typing.Union[modal._output.OutputManager, None] = None):
        ...

    async def disconnect(self):
        ...

    async def stop(self):
        ...

    def log_url(self):
        ...

    def __getitem__(self, tag: str) -> modal.object._Object:
        ...

    def __contains__(self, tag: str) -> bool:
        ...

    def __getattr__(self, tag: str) -> modal.object._Object:
        ...

    @staticmethod
    async def _init_existing(client: modal.client._Client, existing_app_id: str) -> _LocalApp:
        ...

    @staticmethod
    async def _init_new(client: modal.client._Client, description: typing.Union[str, None] = None, detach: bool = False, deploying: bool = False, environment_name: str = '') -> _LocalApp:
        ...

    @staticmethod
    async def _init_from_name(client: modal.client._Client, name: str, namespace, environment_name: str = ''):
        ...

    async def deploy(self, name: str, namespace, object_entity: str) -> str:
        ...

    async def spawn_sandbox(self, *args, **kwargs):
        ...

    @staticmethod
    async def _deploy_single_object(obj: modal.object._Object, type_prefix: str, client: modal.client._Client, label: str, namespace: int, environment_name: int):
        ...


class _ContainerApp:
    _client: typing.Union[modal.client._Client, None]
    _app_id: str
    _associated_stub: typing.Union[typing.Any, None]
    _environment_name: typing.Union[str, None]
    _tag_to_object_id: typing.Dict[str, str]
    _tag_to_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]

    def __init__(self, client: modal.client._Client, app_id: str, stub_name: str, environment_name: str, tag_to_object_id: typing.Dict[str, str], tag_to_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]):
        ...

    @property
    def client(self) -> modal.client._Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    def _associate_stub_container(self, stub):
        ...

    def __getitem__(self, tag: str) -> modal.object._Object:
        ...

    def __contains__(self, tag: str) -> bool:
        ...

    def __getattr__(self, tag: str) -> modal.object._Object:
        ...

    def _has_object(self, tag: str) -> bool:
        ...

    def _hydrate_object(self, obj, tag: str):
        ...

    def _get_pty(self) -> modal.object._Object:
        ...

    @staticmethod
    async def init_container(client: modal.client._Client, app_id: str, stub_name: str = '', environment_name: str = '') -> _ContainerApp:
        ...

    async def spawn_sandbox(self, *args, **kwargs):
        ...

    @staticmethod
    def _reset_container():
        ...


class LocalApp:
    _tag_to_object_id: typing.Dict[str, str]
    _client: modal.client.Client
    _app_id: str
    _app_page_url: str
    _environment_name: str

    def __init__(self, client: modal.client.Client, app_id: str, app_page_url: str, tag_to_object_id: typing.Union[typing.Dict[str, str], None] = None, stub_name: typing.Union[str, None] = None, environment_name: typing.Union[str, None] = None):
        ...

    @property
    def client(self) -> modal.client.Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    class ___create_all_objects_spec(typing_extensions.Protocol):
        def __call__(self, blueprint: typing.Dict[str, modal.object.Object], new_app_state: int, environment_name: str, shell: bool = False, output_mgr: typing.Union[modal._output.OutputManager, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _create_all_objects: ___create_all_objects_spec

    class __disconnect_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    disconnect: __disconnect_spec

    class __stop_spec(typing_extensions.Protocol):
        def __call__(self):
            ...

        async def aio(self, *args, **kwargs):
            ...

    stop: __stop_spec

    def log_url(self):
        ...

    def __getitem__(self, tag: str) -> modal.object.Object:
        ...

    def __contains__(self, tag: str) -> bool:
        ...

    def __getattr__(self, tag: str) -> modal.object.Object:
        ...

    class ___init_existing_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, existing_app_id: str) -> LocalApp:
            ...

        async def aio(self, *args, **kwargs) -> LocalApp:
            ...

    _init_existing: ___init_existing_spec

    class ___init_new_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, description: typing.Union[str, None] = None, detach: bool = False, deploying: bool = False, environment_name: str = '') -> LocalApp:
            ...

        async def aio(self, *args, **kwargs) -> LocalApp:
            ...

    _init_new: ___init_new_spec

    class ___init_from_name_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, name: str, namespace, environment_name: str = ''):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _init_from_name: ___init_from_name_spec

    class __deploy_spec(typing_extensions.Protocol):
        def __call__(self, name: str, namespace, object_entity: str) -> str:
            ...

        async def aio(self, *args, **kwargs) -> str:
            ...

    deploy: __deploy_spec

    class __spawn_sandbox_spec(typing_extensions.Protocol):
        def __call__(self, *args, **kwargs):
            ...

        async def aio(self, *args, **kwargs):
            ...

    spawn_sandbox: __spawn_sandbox_spec

    class ___deploy_single_object_spec(typing_extensions.Protocol):
        def __call__(self, obj: modal.object.Object, type_prefix: str, client: modal.client.Client, label: str, namespace: int, environment_name: int):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _deploy_single_object: ___deploy_single_object_spec


class ContainerApp:
    _client: typing.Union[modal.client.Client, None]
    _app_id: str
    _associated_stub: typing.Union[typing.Any, None]
    _environment_name: typing.Union[str, None]
    _tag_to_object_id: typing.Dict[str, str]
    _tag_to_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]

    def __init__(self, client: modal.client.Client, app_id: str, stub_name: str, environment_name: str, tag_to_object_id: typing.Dict[str, str], tag_to_handle_metadata: typing.Dict[str, typing.Union[google.protobuf.message.Message, None]]):
        ...

    @property
    def client(self) -> modal.client.Client:
        ...

    @property
    def app_id(self) -> str:
        ...

    def _associate_stub_container(self, stub):
        ...

    def __getitem__(self, tag: str) -> modal.object.Object:
        ...

    def __contains__(self, tag: str) -> bool:
        ...

    def __getattr__(self, tag: str) -> modal.object.Object:
        ...

    def _has_object(self, tag: str) -> bool:
        ...

    def _hydrate_object(self, obj, tag: str):
        ...

    def _get_pty(self) -> modal.object.Object:
        ...

    class __init_container_spec(typing_extensions.Protocol):
        def __call__(self, client: modal.client.Client, app_id: str, stub_name: str = '', environment_name: str = '') -> ContainerApp:
            ...

        async def aio(self, *args, **kwargs) -> ContainerApp:
            ...

    init_container: __init_container_spec

    class __spawn_sandbox_spec(typing_extensions.Protocol):
        def __call__(self, *args, **kwargs):
            ...

        async def aio(self, *args, **kwargs):
            ...

    spawn_sandbox: __spawn_sandbox_spec

    @staticmethod
    def _reset_container():
        ...


_container_app: _ContainerApp

container_app: ContainerApp

def is_local() -> bool:
    ...
