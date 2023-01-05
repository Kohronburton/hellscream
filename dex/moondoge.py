from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class MoonDogeCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'MOONDOGE'
        super().__init__()


class MoonDoge(UniFactory):

    IDENTIFIER = 'MD'

    def __init__(self, w3_provider=None):
        super(MoonDoge, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xBFEBd871ddE8cD22999aC9C5679Dfc8248884fCe')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x5a67d6d1e1c36dca265ca9b9bda0e3eb5af9b634')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return MoonDogeCache()

    def reserve_manager(self):
        return MoonDogeReserve()

    def __str__(self):
        return 'MoonDoge'


class MoonDogeReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = MoonDogeCache()
        self.swap = MoonDoge(w3_provider=self.w3)
        self.prefix = 'MOONDOGE'
