from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class CafeCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'CAFE'
        super().__init__()


class Cafe(UniFactory):

    IDENTIFIER = 'CF'

    def __init__(self, w3_provider=None):
        super(Cafe, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x933DAea3a5995Fb94b14A7696a5F3ffD7B1E385A')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x3e708FdbE3ADA63fc94F8F61811196f1302137AD')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return CafeCache()

    def reserve_manager(self):
        return CafeReserve()

    def __str__(self):
        return 'Cafe'


class CafeReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = CafeCache()
        self.swap = Cafe(w3_provider=self.w3)
        self.prefix = 'CAFE'
