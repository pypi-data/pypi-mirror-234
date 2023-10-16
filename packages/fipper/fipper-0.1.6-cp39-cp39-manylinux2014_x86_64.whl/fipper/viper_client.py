import atexit
from typing import Any

from .binding import Binding
from .handlers import HandlersHolder
from .methodcalls import MethodCalls
from .mtproto import MtProtoClient
from .xdcalls import CacheCalls
from .xdcalls.call_holder import CallHolder
from .xdcalls.update_solver import UpdateSolver
from .viper import Viper


class ViperCalls(MethodCalls, Viper):
    """PyTgCalls Client, the main means
    for interacting with Group Calls.

    Attributes:
        active_calls (List of :obj:`~fipper.types.GroupCall`):
            Get a list of active (Playing / Paused) group calls
        calls (List of :obj:`~fipper.types.GroupCall`):
            Get a list of existent group calls
        cache_peer (`InputPeer (P)`_ | `InputPeer (T)`_):
            Get current Telegram user
        ping (``int``):
            Ping of NodeJS core
        is_connected (``bool``):
            Check if is alive the NodeJS connection

    Parameters:
        app (`Client`_ | `TelegramClient`_):
            Pass the MtProto Client

        cache_duration (``int``):
            Cache duration of Full Chat query

        overload_quiet_mode (``bool``):
            Disable overload cpu messages by setting true

        multi_thread (``bool``):
            This will use NodeJS on Multi Thread mode, not
            suggested on production code (Is really buggy,
            is just an experimental mode)

    Raises:
        InvalidMtProtoClient: You set an invalid MtProto client

    """

    def __init__(
        self,
        assistant: Any,
        cache_duration: int = 120,
        overload_quiet_mode: bool = False,
        # BETA SUPPORT, BY DEFAULT IS DISABLED
        multi_thread: bool = False,
    ):
        super().__init__()
        self.assistant = MtProtoClient(
            cache_duration,
            assistant,
        )
        self._is_running = False
        self._call_holder = CallHolder()
        self._cache_user_peer = CacheCalls()
        self._wait_result = UpdateSolver()
        self._on_event_update = HandlersHolder()
        self._binding = Binding(
            overload_quiet_mode,
            multi_thread,
        )

        def cleanup():
            if self._async_core is not None:
                self._async_core.cancel()
        atexit.register(cleanup)
