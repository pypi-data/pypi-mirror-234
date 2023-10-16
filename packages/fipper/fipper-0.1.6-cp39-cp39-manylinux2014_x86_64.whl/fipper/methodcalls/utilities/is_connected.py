from fipper.viper import Viper


class IsConnected(Viper):
    @property
    def is_connected(self):
        return self._binding.is_alive()
