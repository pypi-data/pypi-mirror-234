from fipper.viper import Viper


class ActiveCalls(Viper):
    @property
    def active_calls(self):
        return self._call_holder.active_calls
