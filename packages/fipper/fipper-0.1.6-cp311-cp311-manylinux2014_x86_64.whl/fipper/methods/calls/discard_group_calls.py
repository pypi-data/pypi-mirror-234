from typing import Union

import fipper
from fipper import raw


class GroupCallsNotFound(Exception):
    def __init__(self, er: str):
        super().__init__(er)


class DiscardGroupCall:
    async def discard_group_call(
        self: "fipper.Client",
        chat_id: Union[int, str]
    ) -> "fipper.raw.base.Updates":
        """ Discard group call
        """
        call = await self.get_group_call(chat_id)

        if call.call is None:
            raise GroupCallsNotFound('Chat Without a Voice Chats')

        return await self.invoke(
            raw.functions.phone.DiscardGroupCall(
                call=call.call
            )
        )
