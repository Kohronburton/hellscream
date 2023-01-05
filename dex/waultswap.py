from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class WaultSwapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'WAULTSWAP'
        super().__init__()


class WaultSwap(UniFactory):

    IDENTIFIER = 'WS'

    def __init__(self, w3_provider=None):
        super(WaultSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xD48745E39BbED146eEC15b79cBF964884F9877c2')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xb42e3fe71b7e0673335b3331b3e1053bd9822570')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return WaultSwapCache()

    def reserve_manager(self):
        return WaultSwapReserve()

    def __str__(self):
        return 'WaultSwap'


class WaultSwapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = WaultSwapCache()
        self.swap = WaultSwap(w3_provider=self.w3)
        self.prefix = 'WAULTSWAP'
