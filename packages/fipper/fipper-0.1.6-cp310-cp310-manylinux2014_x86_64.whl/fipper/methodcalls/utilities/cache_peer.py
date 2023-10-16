from fipper.viper import Viper


class CachePeer(Viper):
    @property
    def cache_peer(self):
        return self._cache_local_peer
