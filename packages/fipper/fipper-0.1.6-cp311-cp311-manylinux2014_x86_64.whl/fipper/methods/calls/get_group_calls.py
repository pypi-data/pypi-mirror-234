from typing import Optional, Union

import fipper
from fipper import raw


class GetGroupCall:
    async def get_group_call(
        self: "fipper.Client",
        chat_id: Union[int, str],
        limit: int = -1
    ) -> Optional[raw.types.InputGroupCall]:
        """
        Get group call
        """
        peer = await self.resolve_peer(chat_id)
        
        if isinstance(peer, raw.types.InputPeerChannel):
            full_chat = (await self.invoke(
                raw.functions.channels.GetFullChannel(
                    channel=raw.types.InputChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash,
                    )
                ))).full_chat
        else:
            if isinstance(peer, raw.types.InputPeerChat):
                full_chat = (await self.invoke(
                    raw.functions.messages.GetFullChat(
                        chat_id=peer.chat_id
                    ))).full_chat

        if full_chat.call is not None:
            call: raw.types.GroupCall = (
                raw.functions.phone.GetGroupCall(
                    call=full_chat.call,
                    limit=limit,
                )
            ).call

        return full_chat
