import asyncio
import logging
import sys
from traceback import format_exc

from fipper.exception import ClientCallsAlreadyRunning
from fipper.viper import Viper

logs = logging.getLogger(__name__)


class Start(Viper):
    async def start(self):
        """Start the client.

        This method start and then connects to the NodeJS core.

        Raises:
            PyTgCallsAlreadyRunning: In case you try
                to start an already started client.

        Example:
            .. code-block:: python
                :emphasize-lines: 5

                from pytgcalls import Client
                from pytgcalls import idle
                ...
                app = Client(client)
                app.start()

                ...  # Call API methods

                idle()
        """
        try:
            if not self._is_running:
                self._is_running = True
                loop = asyncio.get_running_loop()
                self._wait_until_run = loop.create_future()
                await self._init_client_calls()
                self._handle_client_calls()
                await self._start_binding()
        except BaseException:
            logs.info(f'INFO START - {str(format_exc())}')
            logs.error(f'ERROR START - {str(format_exc())}')
            sys.exit()
