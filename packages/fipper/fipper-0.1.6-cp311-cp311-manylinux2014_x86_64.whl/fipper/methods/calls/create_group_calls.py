from typing import Union, Optional
from datetime import datetime

import fipper
from fipper import raw


class GroupCallsAlready(Exception):
    def __init__(self, er: str):
        super().__init__(er)


class CreateGroupCall:
    async def create_group_call(
        self: "fipper.Client",
        chat_id: Union[int, str],
        title: Optional[str] = None,
        schedule_date: datetime = None
    ) -> "fipper.raw.base.Updates":
        """
        Create group call
        """
        peer = await self.resolve_peer(chat_id)
        call = await self.get_group_call(chat_id)

        if call.call:
            raise GroupCallsAlready("GroupCall Already Started.")

        await self.invoke(
            raw.functions.phone.CreateGroupCall(
                peer=raw.types.InputPeerChannel(
                    channel_id=peer.channel_id,
                    access_hash=peer.access_hash,
                ),
                random_id=self.rnd_id() // 9000000000,
                title=title,
                schedule_date=schedule_date
            )
        )
