import asyncio

import fipper
from fipper.xdcalls.call_holder import CallHolder
from fipper.xdcalls.groups import JoinedVoiceChat, LeftVoiceChat
from fipper.xdcalls.object import Object
from fipper.xdcalls.stream import ChangedStream, PausedStream, ResumedStream, StreamDeleted


class RawUpdateHandler:
    async def _raw_update_handler(
        self: 'fipper.Client',
        data: dict,
    ):
        obj = Object.from_dict(data)
        solved_update = False
        if 'solver_id' in data:
            solved_update = self._wait_result.resolve_future_update(
                data['solver_id'],
                obj,
            )
        if isinstance(obj, PausedStream):
            self._call_holder.set_status(
                obj.chat_id,
                CallHolder.PAUSED,
            )
        elif isinstance(obj, ResumedStream) or\
                isinstance(obj, ChangedStream) or\
                isinstance(obj, JoinedVoiceChat):
            self._call_holder.set_status(
                obj.chat_id,
                CallHolder.PLAYING,
            )
        elif isinstance(obj, LeftVoiceChat):
            self._call_holder.remove_call(
                obj.chat_id,
            )
        elif isinstance(obj, StreamDeleted):
            self._call_holder.remove_call(
                obj.chat_id,
            )
            asyncio.ensure_future(
                self._binding.send({
                    'action': 'leave_call',
                    'chat_id': obj.chat_id,
                    'type': 'file_deleted',
                }),
            )
        if not solved_update:
            await self._on_event_update.propagate(
                'RAW_UPDATE_HANDLER',
                self,
                obj,
            )
        return {
            'result': 'OK',
        }
