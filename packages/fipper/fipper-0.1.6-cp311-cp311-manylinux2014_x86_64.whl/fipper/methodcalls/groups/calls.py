from fipper.viper import Viper


class Calls(Viper):
    def calls(self):
        return self._call_holder.calls
