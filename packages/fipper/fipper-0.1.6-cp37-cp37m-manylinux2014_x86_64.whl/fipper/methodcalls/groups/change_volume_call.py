from fipper.exception import NoActiveGroupCall
from fipper.exception import NodeJSNotRunning
from fipper.exception import ClientCallsNotSet
from fipper.viper import Viper


class ChangeVolumeCall(Viper):
    async def change_volume_call(self, chat_id: int, volume: int):
        """Change the volume of the playing stream

        This method change the output volume of the userbot
        using MtProto APIs

        Parameters:
            chat_id (``int``):
                Unique identifier (int) of the target chat.
            volume (``int``)
                Volume to set to the stream

        Raises:
            ClientCallsNotSet: In case you try
                to call this method without any MtProto client
            NodeJSNotRunning: In case you try
                to call this method without do
                :meth:`~fipper.PyTgCalls.start` before
            NoActiveGroupCall: In case you try
                to edit a not started group call

        Example:
            .. code-block:: python
                :emphasize-lines: 10-13

                from fipper import Client
                from fipper import idle
                ...

                app = PyTgCalls(client)
                app.start()

                ...  # Call API methods

                app.change_volume_call(
                    -1001185324811,
                    175,
                )

                idle()
        """
        if self.assistant is not None:
            if self._wait_until_run is not None:
                if not self._wait_until_run.done():
                    await self._wait_until_run
                chat_call = await self.assistant.get_full_chat(
                    chat_id,
                )
                if chat_call is not None:
                    await self.assistant.change_volume(
                        chat_id,
                        volume,
                        self._cache_user_peer.get(chat_id),
                    )
                else:
                    raise NoActiveGroupCall()
            else:
                raise NodeJSNotRunning()
        else:
            raise ClientCallsNotSet()
