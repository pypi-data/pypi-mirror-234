from .group_call_participant import GroupCallParticipant
from ..update import Update


class UpdatedGroupCallParticipant(Update):
    """A participant have changed
    him status

    Attributes:
        chat_id (``int``):
            Unique identifier of chat.
        participant (:obj:`~fipper.types.GroupCallParticipant()`):
            Info about a group call participant

    Parameters:
        chat_id (``int``):
            Unique identifier of chat.
        participant (:obj:`~fipper.types.GroupCallParticipant()`):
            Info about a group call participant
    """

    def __init__(
        self,
        chat_id: int,
        participant: GroupCallParticipant,
    ):
        super().__init__(chat_id)
        self.participant = participant
