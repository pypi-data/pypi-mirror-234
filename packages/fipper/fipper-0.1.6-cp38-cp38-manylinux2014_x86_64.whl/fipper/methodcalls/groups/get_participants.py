from typing import List
from typing import Optional

from fipper.viper import Viper
from fipper.xdcalls.groups.group_call_participant import GroupCallParticipant


class GetParticipants(Viper):
    async def get_participants(
        self,
        chat_id: int,
    ) -> Optional[List[GroupCallParticipant]]:
        """Get list of participants from a group call

        This method return the list of participants on a group call
        using MtProto APIs

        Parameters:
            chat_id (``int``):
                Unique identifier (int) of the target chat.

        Returns:
            List of :obj:`~fipper.types.GroupCallParticipant()`:
            On success, a list of participants is returned

        Example:
            .. code-block:: python
                :emphasize-lines: 10-12

                from fipper import Client
                from fipper import idle
                ...

                app = PyTgCalls(client)
                app.start()

                ...  # Call API methods

                app.get_participants(
                    -1001185324811,
                )

                idle()
        """
        self._call_holder.get_call(
            chat_id,
        )
        return await self.assistant.get_group_call_participants(
            chat_id,
        )
