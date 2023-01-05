from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class DefinixCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'DEFINIX'
        super().__init__()


class Definix(UniFactory):

    IDENTIFIER = 'DF'

    def __init__(self, w3_provider=None):
        super(Definix, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x151030a9Fa62FbB202eEe50Bd4A4057AB9E826AD')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x43ebb0cb9bd53a3ed928dd662095ace1cef92d19')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return DefinixCache()

    def reserve_manager(self):
        return DefinixReserve()

    def __str__(self):
        return 'Definix'


class DefinixReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = DefinixCache()
        self.swap = Definix(w3_provider=self.w3)
        self.prefix = 'DEFINIX'
