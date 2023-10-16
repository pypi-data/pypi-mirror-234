from fipper.viper import Viper


class Ping(Viper):
    @property
    async def ping(self) -> float:
        return round(await self._binding.ping, 5)
