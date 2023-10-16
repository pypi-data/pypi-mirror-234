from .cache_peer import CachePeer
from .get_max_voice_chat import GetMaxVoiceChat
from .handle_calls import ClientCallsHandler
from .is_connected import IsConnected
from .ping import Ping
from .run import Run
from .start import Start


class Utilities(
    CachePeer,
    GetMaxVoiceChat,
    ClientCallsHandler,
    IsConnected,
    Ping,
    Run,
    Start,
):
    pass
