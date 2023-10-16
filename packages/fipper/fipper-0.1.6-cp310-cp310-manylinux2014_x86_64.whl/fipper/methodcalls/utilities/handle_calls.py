from fipper.xdcalls import Update
from fipper.xdcalls.groups import (
    GroupCallParticipant,
    JoinedGroupCallParticipant,
    LeftGroupCallParticipant,
    UpdatedGroupCallParticipant,
)
from fipper.viper import Viper


class ClientCallsHandler(Viper):
    async def _init_client_calls(self):
        if not self.is_connected:
            await self.start()
        self._my_id = await self.assistant.get_id()
        self._cache_local_peer = await self.assistant.resolve_peer(
            self._my_id,
        )

    def _handle_client_calls(self):
        @self.assistant.on_kicked()
        async def kicked_handler(chat_id: int):
            self._call_holder.remove_call(
                chat_id,
            )
            await self._binding.send({
                'action': 'leave_call',
                'chat_id': chat_id,
                'type': 'kicked_from_group',
            })
            await self._on_event_update.propagate(
                'KICK_HANDLER',
                self,
                chat_id,
            )
            self._cache_user_peer.pop(chat_id)

        @self.assistant.on_closed_voice_chat()
        async def closed_voice_chat_handler(chat_id: int):
            self._cache_user_peer.pop(chat_id)
            await self._binding.send({
                'action': 'leave_call',
                'chat_id': chat_id,
                'type': 'closed_voice_chat',
            })
            await self._on_event_update.propagate(
                'CLOSED_HANDLER',
                self,
                chat_id,
            )

        @self.assistant.on_receive_invite()
        async def receive_invite_handler(action):
            await self._on_event_update.propagate(
                'INVITE_HANDLER',
                self,
                action,
            )

        @self.assistant.on_left_group()
        async def left_handler(chat_id: int):
            await self._on_event_update.propagate(
                'LEFT_HANDLER',
                self,
                chat_id,
            )

        @self.assistant.on_participants_change()
        async def participants_handler(
            chat_id: int,
            participant: GroupCallParticipant,
            just_joined: bool,
            just_left: bool,
        ):
            if participant.user_id == self._my_id:
                return
            update_participant: Update = UpdatedGroupCallParticipant(
                chat_id,
                participant,
            )
            if just_joined:
                update_participant = JoinedGroupCallParticipant(
                    chat_id,
                    participant,
                )
            elif just_left:
                update_participant = LeftGroupCallParticipant(
                    chat_id,
                    participant,
                )
            await self._on_event_update.propagate(
                'PARTICIPANTS_LIST',
                self,
                update_participant,
            )
