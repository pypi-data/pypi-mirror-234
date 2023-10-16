from .raw_update_handler import RawUpdateHandler
from .stream_ended_handler import StreamEndedHandler


class HandlerCalls(
    RawUpdateHandler,
    StreamEndedHandler,
):
    pass
