from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class WardenSwapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'WARDENSWAP'
        super().__init__()


class WardenSwap(UniFactory):

    IDENTIFIER = 'WA'

    def __init__(self, w3_provider=None):
        super(WardenSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x71ac17934b60A4610dc58b715B61e45DCBdE4054')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x3657952d7ba5a0a4799809b5b6fdff9ec5b46293')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return WardenSwapCache()

    def reserve_manager(self):
        return WardenSwapReserve()

    def __str__(self):
        return 'WardenSwap'


class WardenSwapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = WardenSwapCache()
        self.swap = WardenSwap(w3_provider=self.w3)
        self.prefix = 'WARDENSWAP'
