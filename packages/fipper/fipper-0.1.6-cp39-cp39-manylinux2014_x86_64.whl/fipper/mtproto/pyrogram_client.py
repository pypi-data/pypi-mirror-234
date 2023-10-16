import json
from typing import Callable
from typing import Dict
from typing import Optional

import fipper
from fipper.raw.base import InputPeer
from fipper.raw.functions.channels import GetFullChannel
from fipper.raw.functions.messages import GetFullChat
from fipper.raw.functions.phone import EditGroupCallParticipant
from fipper.raw.functions.phone import GetGroupCall
from fipper.raw.functions.phone import GetGroupParticipants
from fipper.raw.functions.phone import JoinGroupCall
from fipper.raw.functions.phone import LeaveGroupCall
from fipper.raw.types import Channel
from fipper.raw.types import ChannelForbidden
from fipper.raw.types import Chat
from fipper.raw.types import ChatForbidden
from fipper.raw.types import DataJSON
from fipper.raw.types import GroupCall
from fipper.raw.types import GroupCallDiscarded
from fipper.raw.types import InputChannel
from fipper.raw.types import InputGroupCall
from fipper.raw.types import InputPeerChannel
from fipper.raw.types import MessageActionChatDeleteUser
from fipper.raw.types import MessageActionInviteToGroupCall
from fipper.raw.types import MessageService
from fipper.raw.types import PeerChat
from fipper.raw.types import UpdateChannel
from fipper.raw.types import UpdateGroupCall
from fipper.raw.types import UpdateGroupCallConnection
from fipper.raw.types import UpdateGroupCallParticipants
from fipper.raw.types import UpdateNewChannelMessage
from fipper.raw.types import UpdateNewMessage
from fipper.raw.types import Updates

from .bridged_client import BridgedClient
from .client_cache import ClientCache


class FipperClientCalls(BridgedClient):
    def __init__(
        self,
        cache_duration: int,
        client: 'fipper.Client',
    ):
        self.assistant: fipper.Client = client
        self._handler: Dict[str, Callable] = {}
        self._cache: ClientCache = ClientCache(
            cache_duration,
            self,
        )

        @self.assistant.on_raw_update()
        async def on_update(_, update, __, data2):
            if isinstance(
                update,
                UpdateGroupCallParticipants,
            ):
                participants = update.participants
                for participant in participants:
                    result = self._cache.set_participants_cache(
                        update.call.id,
                        self.chat_id(participant.peer),
                        participant.muted,
                        participant.volume,
                        participant.can_self_unmute,
                        participant.video is not None or
                        participant.presentation is not None,
                        participant.presentation is not None,
                        participant.video is not None,
                        participant.raise_hand_rating,
                        participant.left,
                    )
                    if result is not None:
                        if 'PARTICIPANTS_HANDLER' in self._handler:
                            await self._handler['PARTICIPANTS_HANDLER'](
                                self._cache.get_chat_id(update.call.id),
                                result,
                                participant.just_joined,
                                participant.left,
                            )
            if isinstance(
                update,
                UpdateGroupCall,
            ):
                chat_id = self.chat_id(data2[update.chat_id])
                if isinstance(
                    update.call,
                    GroupCall,
                ):
                    if update.call.schedule_date is None:
                        self._cache.set_cache(
                            chat_id,
                            InputGroupCall(
                                access_hash=update.call.access_hash,
                                id=update.call.id,
                            ),
                        )
                if isinstance(
                    update.call,
                    GroupCallDiscarded,
                ):
                    self._cache.drop_cache(chat_id)
                    if 'CLOSED_HANDLER' in self._handler:
                        await self._handler['CLOSED_HANDLER'](
                            chat_id,
                        )
            if isinstance(
                update,
                UpdateChannel,
            ):
                chat_id = self.chat_id(update)
                if len(data2) > 0:
                    if isinstance(
                        data2[update.channel_id],
                        ChannelForbidden,
                    ):
                        self._cache.drop_cache(chat_id)
                        if 'KICK_HANDLER' in self._handler:
                            await self._handler['KICK_HANDLER'](
                                chat_id,
                            )
            if isinstance(
                update,
                UpdateNewChannelMessage,
            ) or isinstance(
                update,
                UpdateNewMessage,
            ):
                if isinstance(
                    update.message,
                    MessageService,
                ):
                    if isinstance(
                        update.message.action,
                        MessageActionInviteToGroupCall,
                    ):
                        if 'INVITE_HANDLER' in self._handler:
                            await self._handler['INVITE_HANDLER'](
                                update.message.action,
                            )
                    if isinstance(
                        update.message.action,
                        MessageActionChatDeleteUser,
                    ):
                        if isinstance(
                            update.message.peer_id,
                            PeerChat,
                        ):
                            chat_id = self.chat_id(update.message.peer_id)
                            if isinstance(
                                data2[update.message.peer_id.chat_id],
                                ChatForbidden,
                            ):
                                self._cache.drop_cache(chat_id)
                                if 'KICK_HANDLER' in self._handler:
                                    await self._handler['KICK_HANDLER'](
                                        chat_id,
                                    )
            if isinstance(
                data2,
                Dict,
            ):
                for group_id in data2:
                    if isinstance(
                        update,
                        UpdateNewChannelMessage,
                    ) or isinstance(
                        update,
                        UpdateNewMessage,
                    ):
                        if isinstance(
                            update.message,
                            MessageService,
                        ):
                            if isinstance(
                                data2[group_id],
                                Channel,
                            ) or isinstance(
                                data2[group_id],
                                Chat,
                            ):
                                chat_id = self.chat_id(data2[group_id])
                                if data2[group_id].left:
                                    self._cache.drop_cache(
                                        chat_id,
                                    )
                                    if 'LEFT_HANDLER' in self._handler:
                                        await self._handler['LEFT_HANDLER'](
                                            chat_id,
                                        )
            raise fipper.ContinuePropagation()

    def on_closed_voice_chat(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            if self is not None:
                self._handler['CLOSED_HANDLER'] = func
            return func
        return decorator

    def on_kicked(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            if self is not None:
                self._handler['KICK_HANDLER'] = func
            return func
        return decorator

    def on_receive_invite(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            if self is not None:
                self._handler['INVITE_HANDLER'] = func
            return func
        return decorator

    def on_left_group(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            if self is not None:
                self._handler['LEFT_HANDLER'] = func
            return func
        return decorator

    def on_participants_change(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            if self is not None:
                self._handler['PARTICIPANTS_HANDLER'] = func
            return func
        return decorator

    async def get_call(
        self,
        chat_id: int,
    ) -> Optional[InputGroupCall]:
        chat = await self.assistant.resolve_peer(chat_id)
        if isinstance(chat, InputPeerChannel):
            input_call = (
                await self.assistant.invoke(
                    GetFullChannel(
                        channel=InputChannel(
                            channel_id=chat.channel_id,
                            access_hash=chat.access_hash,
                        ),
                    ),
                )
            ).full_chat.call
        else:
            input_call = (
                await self.assistant.invoke(
                    GetFullChat(chat_id=chat.chat_id),
                )
            ).full_chat.call
        if input_call is not None:
            call: GroupCall = (
                await self.assistant.invoke(
                    GetGroupCall(
                        call=input_call,
                        limit=-1,
                    ),
                )
            ).call
            if call.schedule_date is not None:
                return None
        return input_call

    async def get_group_call_participants(
        self,
        chat_id: int,
    ):
        return await self._cache.get_participant_list(
            chat_id,
        )

    async def get_participants(
        self,
        input_call: InputGroupCall,
    ):
        return [
            {
                'user_id': self.chat_id(participant.peer),
                'muted': participant.muted,
                'volume': participant.volume,
                'can_self_unmute': participant.can_self_unmute,
                'video': participant.video,
                'presentation': participant.presentation,
                'raise_hand_rating': participant.raise_hand_rating,
                'left': participant.left,
            } for participant in (
                await self.assistant.invoke(
                    GetGroupParticipants(
                        call=input_call,
                        ids=[],
                        sources=[],
                        offset='',
                        limit=500,
                    ),
                )
            ).participants
        ]

    async def join_group_call(
        self,
        chat_id: int,
        json_join: dict,
        invite_hash: str,
        have_video: bool,
        join_as: InputPeer,
    ) -> dict:
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            result: Updates = await self.assistant.invoke(
                JoinGroupCall(
                    call=chat_call,
                    params=DataJSON(data=json.dumps(json_join)),
                    muted=False,
                    join_as=join_as,
                    video_stopped=have_video,
                    invite_hash=invite_hash,
                ),
            )
            for update in result.updates:
                if isinstance(
                    update,
                    UpdateGroupCallParticipants,
                ):
                    participants = update.participants
                    for participant in participants:
                        self._cache.set_participants_cache(
                            update.call.id,
                            self.chat_id(participant.peer),
                            participant.muted,
                            participant.volume,
                            participant.can_self_unmute,
                            participant.video is not None or
                            participant.presentation is not None,
                            participant.presentation is not None,
                            participant.video is not None,
                            participant.raise_hand_rating,
                            participant.left,
                        )
                if isinstance(update, UpdateGroupCallConnection):
                    transport = json.loads(update.params.data)[
                        'transport'
                    ]
                    return {
                        'transport': {
                            'ufrag': transport['ufrag'],
                            'pwd': transport['pwd'],
                            'fingerprints': transport['fingerprints'],
                            'candidates': transport['candidates'],
                        },
                    }
        return {'transport': None}

    async def leave_group_call(
        self,
        chat_id: int,
    ):
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            await self.assistant.invoke(
                LeaveGroupCall(
                    call=chat_call,
                    source=0,
                ),
            )

    async def change_volume(
        self,
        chat_id: int,
        volume: int,
        participant: InputPeer,
    ):
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            await self.assistant.invoke(
                EditGroupCallParticipant(
                    call=chat_call,
                    participant=participant,
                    muted=False,
                    volume=volume * 100,
                ),
            )

    async def set_video_call_status(
        self,
        chat_id: int,
        stopped_status: Optional[bool],
        paused_status: Optional[bool],
        participant: InputPeer,
    ):
        chat_call = await self._cache.get_full_chat(chat_id)
        if chat_call is not None:
            await self.assistant.invoke(
                EditGroupCallParticipant(
                    call=chat_call,
                    participant=participant,
                    muted=False,
                    video_stopped=stopped_status,
                    video_paused=paused_status,
                ),
            )

    async def get_full_chat(self, chat_id: int):
        return await self._cache.get_full_chat(chat_id)

    async def resolve_peer(
        self,
        user_id: int,
    ) -> InputPeer:
        return await self.assistant.resolve_peer(user_id)

    async def get_id(self) -> int:
        return (await self.assistant.get_me()).id

    def is_connected(self) -> bool:
        return self.assistant.is_connected

    async def start(self):
        await self.assistant.start()
