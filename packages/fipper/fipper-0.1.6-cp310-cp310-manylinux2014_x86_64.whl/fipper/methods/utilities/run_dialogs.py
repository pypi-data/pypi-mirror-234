
import fipper
from fipper.errors.exceptions import BotMethodInvalid


class RunDialogs:
    async def run_dialogs(self: 'fipper.Client'):
        if not self.is_connected:
            raise ConnectionError("Can't get dialogs a disconnected client")

        if self.me.is_bot:
            raise BotMethodInvalid('BotMethodInvalid for run_dialogs client')

        async for x in self.get_dialogs():
            self._dialogs.append(x)
