from .core import Core
from .decorators import Decorators
from .groups import Groups
from .handler import HandlerCalls
from .stream import Stream
from .utilities import Utilities


class MethodCalls(
    Core,
    Decorators,
    Groups,
    HandlerCalls,
    Stream,
    Utilities,
):
    pass
