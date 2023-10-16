import fipper
from fipper import raw


class GroupCallsNotFound(Exception):
    def __init__(self, er: str):
        super().__init__(er)


class EditTitileGroupCall:
    async def title_group_call(
        self: 'fipper.Client',
        chat_id: int,
        title: str
    ):
        """
        Title group call
        """
        full_chat = await self.get_group_call(chat_id)

        if full_chat.call is None:
            raise GroupCallsNotFound('Chat Without a Voice Chats')

        await self.invoke(
            raw.functions.phone.EditGroupCallTitle(
                call=full_chat.call,
                title=title,
            )
        )
