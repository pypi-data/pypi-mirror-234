import modal._function_utils
import modal._output
import modal.app
import modal.client
import modal.cls
import modal.functions
import modal.gpu
import modal.image
import modal.mount
import modal.network_file_system
import modal.object
import modal.proxy
import modal.retries
import modal.sandbox
import modal.schedule
import modal.secret
import modal.volume
import os
import synchronicity.combined_types
import typing
import typing_extensions

class _LocalEntrypoint:
    _info: modal._function_utils.FunctionInfo
    _stub: _Stub

    def __init__(self, info, stub):
        ...

    def __call__(self, *args, **kwargs):
        ...

    @property
    def info(self) -> modal._function_utils.FunctionInfo:
        ...

    @property
    def stub(self) -> _Stub:
        ...


class LocalEntrypoint:
    _info: modal._function_utils.FunctionInfo
    _stub: Stub

    def __init__(self, info, stub):
        ...

    def __call__(self, *args, **kwargs):
        ...

    @property
    def info(self) -> modal._function_utils.FunctionInfo:
        ...

    @property
    def stub(self) -> Stub:
        ...


def check_sequence(items: typing.Sequence[typing.Any], item_type: typing.Type[typing.Any], error_msg: str):
    ...


CLS_T = typing.TypeVar("CLS_T", bound="typing.Type")

class _Stub:
    _name: typing.Union[str, None]
    _description: typing.Union[str, None]
    _blueprint: typing.Dict[str, modal.object._Object]
    _function_mounts: typing.Dict[str, modal.mount._Mount]
    _mounts: typing.Sequence[modal.mount._Mount]
    _secrets: typing.Sequence[modal.secret._Secret]
    _web_endpoints: typing.List[str]
    _local_entrypoints: typing.Dict[str, _LocalEntrypoint]
    _container_app: typing.Union[modal.app._ContainerApp, None]
    _local_app: typing.Union[modal.app._LocalApp, None]
    _all_stubs: typing.ClassVar[typing.Dict[str, typing.List[_Stub]]]

    def __init__(self, name: typing.Union[str, None] = None, *, image: typing.Union[modal.image._Image, None] = None, mounts: typing.Sequence[modal.mount._Mount] = [], secrets: typing.Sequence[modal.secret._Secret] = [], **blueprint: modal.object._Object) -> None:
        ...

    @property
    def name(self) -> typing.Union[str, None]:
        ...

    @property
    def app(self):
        ...

    @property
    def app_id(self) -> typing.Union[str, None]:
        ...

    @property
    def description(self) -> typing.Union[str, None]:
        ...

    def set_description(self, description: str):
        ...

    def _validate_blueprint_value(self, key: str, value: typing.Any):
        ...

    def _add_object(self, tag, obj):
        ...

    def __getitem__(self, tag: str):
        ...

    def __setitem__(self, tag: str, obj: modal.object._Object):
        ...

    def __getattr__(self, tag: str) -> modal.object._Object:
        ...

    def __setattr__(self, tag: str, obj: modal.object._Object):
        ...

    def get_objects(self) -> typing.List[typing.Tuple[str, modal.object._Object]]:
        ...

    def _uncreate_all_objects(self):
        ...

    def is_inside(self, image: typing.Union[modal.image._Image, None] = None) -> bool:
        ...

    def _set_local_app(self, app: modal.app._LocalApp) -> typing.AsyncContextManager[None]:
        ...

    def run(self, client: typing.Union[modal.client._Client, None] = None, stdout=None, show_progress: bool = True, detach: bool = False, output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> typing.AsyncContextManager[_Stub]:
        ...

    def _get_default_image(self):
        ...

    @property
    def _pty_input_stream(self):
        ...

    def _add_pty_input_stream(self):
        ...

    def _get_watch_mounts(self):
        ...

    def _add_function(self, function: modal.functions._Function):
        ...

    @property
    def registered_functions(self) -> typing.Dict[str, modal.functions._Function]:
        ...

    @property
    def registered_classes(self) -> typing.Dict[str, modal.functions._Function]:
        ...

    @property
    def registered_entrypoints(self) -> typing.Dict[str, _LocalEntrypoint]:
        ...

    @property
    def registered_web_endpoints(self) -> typing.List[str]:
        ...

    def local_entrypoint(self, _warn_parentheses_missing=None, *, name: typing.Union[str, None] = None) -> typing.Callable[[typing.Callable[..., typing.Any]], None]:
        ...

    def function(self, _warn_parentheses_missing=None, *, image: typing.Union[modal.image._Image, None] = None, schedule: typing.Union[modal.schedule.Schedule, None] = None, secret: typing.Union[modal.secret._Secret, None] = None, secrets: typing.Sequence[modal.secret._Secret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, mounts: typing.Sequence[modal.mount._Mount] = (), shared_volumes: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {}, network_file_systems: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {}, allow_cross_region_volumes: bool = False, volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume._Volume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy._Proxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, concurrency_limit: typing.Union[int, None] = None, allow_concurrent_inputs: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, timeout: typing.Union[int, None] = None, interactive: bool = False, keep_warm: typing.Union[int, None] = None, name: typing.Union[str, None] = None, is_generator: typing.Union[bool, None] = None, cloud: typing.Union[str, None] = None) -> typing.Callable[..., modal.functions._Function]:
        ...

    def cls(self, _warn_parentheses_missing=None, *, image: typing.Union[modal.image._Image, None] = None, secret: typing.Union[modal.secret._Secret, None] = None, secrets: typing.Sequence[modal.secret._Secret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, mounts: typing.Sequence[modal.mount._Mount] = (), shared_volumes: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {}, network_file_systems: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {}, allow_cross_region_volumes: bool = False, volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume._Volume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy._Proxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, concurrency_limit: typing.Union[int, None] = None, allow_concurrent_inputs: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, timeout: typing.Union[int, None] = None, interactive: bool = False, keep_warm: typing.Union[int, None] = None, cloud: typing.Union[str, None] = None, auto_snapshot_enabled: typing.Union[bool, None] = None) -> typing.Callable[[CLS_T], modal.cls._Cls]:
        ...

    def _get_deduplicated_function_mounts(self, mounts: typing.Dict[str, modal.mount._Mount]):
        ...

    async def spawn_sandbox(self, *entrypoint_args: str, image: typing.Union[modal.image._Image, None] = None, mounts: typing.Sequence[modal.mount._Mount] = (), secrets: typing.Sequence[modal.secret._Secret] = (), network_file_systems: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system._NetworkFileSystem] = {}, timeout: typing.Union[int, None] = None, workdir: typing.Union[str, None] = None, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, cloud: typing.Union[str, None] = None, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None) -> modal.sandbox._Sandbox:
        ...


class Stub:
    _name: typing.Union[str, None]
    _description: typing.Union[str, None]
    _blueprint: typing.Dict[str, modal.object.Object]
    _function_mounts: typing.Dict[str, modal.mount.Mount]
    _mounts: typing.Sequence[modal.mount.Mount]
    _secrets: typing.Sequence[modal.secret.Secret]
    _web_endpoints: typing.List[str]
    _local_entrypoints: typing.Dict[str, LocalEntrypoint]
    _container_app: typing.Union[modal.app.ContainerApp, None]
    _local_app: typing.Union[modal.app.LocalApp, None]
    _all_stubs: typing.ClassVar[typing.Dict[str, typing.List[Stub]]]

    def __init__(self, name: typing.Union[str, None] = None, *, image: typing.Union[modal.image.Image, None] = None, mounts: typing.Sequence[modal.mount.Mount] = [], secrets: typing.Sequence[modal.secret.Secret] = [], **blueprint: modal.object.Object) -> None:
        ...

    @property
    def name(self) -> typing.Union[str, None]:
        ...

    @property
    def app(self):
        ...

    @property
    def app_id(self) -> typing.Union[str, None]:
        ...

    @property
    def description(self) -> typing.Union[str, None]:
        ...

    def set_description(self, description: str):
        ...

    def _validate_blueprint_value(self, key: str, value: typing.Any):
        ...

    def _add_object(self, tag, obj):
        ...

    def __getitem__(self, tag: str):
        ...

    def __setitem__(self, tag: str, obj: modal.object.Object):
        ...

    def __getattr__(self, tag: str) -> modal.object.Object:
        ...

    def __setattr__(self, tag: str, obj: modal.object.Object):
        ...

    def get_objects(self) -> typing.List[typing.Tuple[str, modal.object.Object]]:
        ...

    def _uncreate_all_objects(self):
        ...

    def is_inside(self, image: typing.Union[modal.image.Image, None] = None) -> bool:
        ...

    class ___set_local_app_spec(typing_extensions.Protocol):
        def __call__(self, app: modal.app.LocalApp) -> synchronicity.combined_types.AsyncAndBlockingContextManager[None]:
            ...

        def aio(self, app: modal.app.LocalApp) -> typing.AsyncContextManager[None]:
            ...

    _set_local_app: ___set_local_app_spec

    class __run_spec(typing_extensions.Protocol):
        def __call__(self, client: typing.Union[modal.client.Client, None] = None, stdout=None, show_progress: bool = True, detach: bool = False, output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> synchronicity.combined_types.AsyncAndBlockingContextManager[Stub]:
            ...

        def aio(self, client: typing.Union[modal.client.Client, None] = None, stdout=None, show_progress: bool = True, detach: bool = False, output_mgr: typing.Union[modal._output.OutputManager, None] = None) -> typing.AsyncContextManager[Stub]:
            ...

    run: __run_spec

    def _get_default_image(self):
        ...

    @property
    def _pty_input_stream(self):
        ...

    def _add_pty_input_stream(self):
        ...

    def _get_watch_mounts(self):
        ...

    def _add_function(self, function: modal.functions.Function):
        ...

    @property
    def registered_functions(self) -> typing.Dict[str, modal.functions.Function]:
        ...

    @property
    def registered_classes(self) -> typing.Dict[str, modal.functions.Function]:
        ...

    @property
    def registered_entrypoints(self) -> typing.Dict[str, LocalEntrypoint]:
        ...

    @property
    def registered_web_endpoints(self) -> typing.List[str]:
        ...

    def local_entrypoint(self, _warn_parentheses_missing=None, *, name: typing.Union[str, None] = None) -> typing.Callable[[typing.Callable[..., typing.Any]], None]:
        ...

    def function(self, _warn_parentheses_missing=None, *, image: typing.Union[modal.image.Image, None] = None, schedule: typing.Union[modal.schedule.Schedule, None] = None, secret: typing.Union[modal.secret.Secret, None] = None, secrets: typing.Sequence[modal.secret.Secret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, mounts: typing.Sequence[modal.mount.Mount] = (), shared_volumes: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem] = {}, network_file_systems: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem] = {}, allow_cross_region_volumes: bool = False, volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume.Volume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy.Proxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, concurrency_limit: typing.Union[int, None] = None, allow_concurrent_inputs: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, timeout: typing.Union[int, None] = None, interactive: bool = False, keep_warm: typing.Union[int, None] = None, name: typing.Union[str, None] = None, is_generator: typing.Union[bool, None] = None, cloud: typing.Union[str, None] = None) -> typing.Callable[..., modal.functions.Function]:
        ...

    def cls(self, _warn_parentheses_missing=None, *, image: typing.Union[modal.image.Image, None] = None, secret: typing.Union[modal.secret.Secret, None] = None, secrets: typing.Sequence[modal.secret.Secret] = (), gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, serialized: bool = False, mounts: typing.Sequence[modal.mount.Mount] = (), shared_volumes: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem] = {}, network_file_systems: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem] = {}, allow_cross_region_volumes: bool = False, volumes: typing.Dict[typing.Union[str, os.PathLike], modal.volume.Volume] = {}, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None, proxy: typing.Union[modal.proxy.Proxy, None] = None, retries: typing.Union[int, modal.retries.Retries, None] = None, concurrency_limit: typing.Union[int, None] = None, allow_concurrent_inputs: typing.Union[int, None] = None, container_idle_timeout: typing.Union[int, None] = None, timeout: typing.Union[int, None] = None, interactive: bool = False, keep_warm: typing.Union[int, None] = None, cloud: typing.Union[str, None] = None, auto_snapshot_enabled: typing.Union[bool, None] = None) -> typing.Callable[[CLS_T], modal.cls.Cls]:
        ...

    def _get_deduplicated_function_mounts(self, mounts: typing.Dict[str, modal.mount.Mount]):
        ...

    class __spawn_sandbox_spec(typing_extensions.Protocol):
        def __call__(self, *entrypoint_args: str, image: typing.Union[modal.image.Image, None] = None, mounts: typing.Sequence[modal.mount.Mount] = (), secrets: typing.Sequence[modal.secret.Secret] = (), network_file_systems: typing.Dict[typing.Union[str, os.PathLike], modal.network_file_system.NetworkFileSystem] = {}, timeout: typing.Union[int, None] = None, workdir: typing.Union[str, None] = None, gpu: typing.Union[None, bool, str, modal.gpu._GPUConfig] = None, cloud: typing.Union[str, None] = None, cpu: typing.Union[float, None] = None, memory: typing.Union[int, None] = None) -> modal.sandbox.Sandbox:
            ...

        async def aio(self, *args, **kwargs) -> modal.sandbox.Sandbox:
            ...

    spawn_sandbox: __spawn_sandbox_spec


_default_image: modal.image._Image