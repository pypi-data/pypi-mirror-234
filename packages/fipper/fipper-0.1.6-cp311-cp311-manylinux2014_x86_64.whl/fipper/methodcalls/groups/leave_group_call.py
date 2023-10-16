import asyncio

from fipper.exception import NoActiveGroupCall
from fipper.exception import NodeJSNotRunning
from fipper.exception import ClientCallsNotSet
from fipper.exception import NotInGroupCallError
from fipper.xdcalls import NotInGroupCall
from fipper.xdcalls.session import Session
from fipper.viper import Viper



class LeaveGroupCall(Viper):
    async def leave_group_call(
        self,
        chat_id: int,
    ):
        """Leave a group call

        This method allow to leave a Group Call

        Parameters:
            chat_id (``int``):
                Unique identifier (int) of the target chat.

        Raises:
            ClientCallsNotSet: In case you try
                to call this method without any MtProto client
            NodeJSNotRunning: In case you try
                to call this method without do
                :meth:`~fipper.PyTgCalls.start` before
            NoActiveGroupCall: In case you try
                to edit a not started group call
            NotInGroupCallError: In case you try
                to leave a non-joined group call

        Example:
            .. code-block:: python
                :emphasize-lines: 10-12

                from fipper import Client
                from fipper import idle
                ...

                app = PyTgCalls(client)
                app.start()

                ...  # Call API methods

                app.leave_group_call(
                    -1001185324811,
                )

                idle()
        """
        if self.assistant is not None:
            if self._wait_until_run is not None:
                chat_call = await self.assistant.get_full_chat(
                    chat_id,
                )
                if chat_call is not None:
                    solver_id = Session.generate_session_id(24)

                    async def internal_sender():
                        if not self._wait_until_run.done():
                            await self._wait_until_run
                        await self._binding.send({
                            'action': 'leave_call',
                            'chat_id': chat_id,
                            'type': 'requested',
                            'solver_id': solver_id,
                        })
                    asyncio.ensure_future(internal_sender())
                    result = await self._wait_result.wait_future_update(
                        solver_id,
                    )
                    if isinstance(result, NotInGroupCall):
                        raise NotInGroupCallError()
                else:
                    raise NoActiveGroupCall()
            else:
                raise NodeJSNotRunning()
        else:
            raise ClientCallsNotSet()
