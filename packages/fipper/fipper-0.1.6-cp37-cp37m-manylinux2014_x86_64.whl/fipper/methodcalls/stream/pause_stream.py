import asyncio

from fipper.exception import NodeJSNotRunning
from fipper.exception import ClientCallsNotSet
from fipper.exception import NotInGroupCallError
from fipper.xdcalls import NotInGroupCall
from fipper.xdcalls.session import Session
from fipper.viper import Viper


class PauseStream(Viper):
    async def pause_stream(
        self,
        chat_id: int,
    ):
        """Pause the playing stream

        This method allow to pause the streaming file

        Parameters:
            chat_id (``int``):
                Unique identifier (int) of the target chat.

        Raises:
            ClientCallsNotSet: In case you try
                to call this method without any MtProto client
            NodeJSNotRunning: In case you try
                to call this method without do
                :meth:`~fipper.PyTgCalls.start` before
            NotInGroupCallError: In case you try
                to leave a non-joined group call

        Returns:
            ``bool``:
            On success, true is returned if was paused

        Example:
            .. code-block:: python
                :emphasize-lines: 10-12

                from fipper import Client
                from fipper import idle
                ...

                app = PyTgCalls(client)
                app.start()

                ...  # Call API methods

                app.pause_stream(
                    -1001185324811,
                )

                idle()
        """
        if self.assistant is not None:
            if self._wait_until_run is not None:
                solver_id = Session.generate_session_id(24)

                async def internal_sender():
                    if not self._wait_until_run.done():
                        await self._wait_until_run
                    await self._binding.send({
                        'action': 'pause',
                        'chat_id': chat_id,
                        'solver_id': solver_id,
                    })
                active_call = self._call_holder.get_active_call(chat_id)
                asyncio.ensure_future(internal_sender())
                result = await self._wait_result.wait_future_update(
                    solver_id,
                )
                if isinstance(result, NotInGroupCall):
                    raise NotInGroupCallError()
                return active_call.status == 'playing'
            else:
                raise NodeJSNotRunning()
        else:
            raise ClientCallsNotSet()
