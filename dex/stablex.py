from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class StableXCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'STABLEX'
        super().__init__()


class StableX(UniFactory):

    IDENTIFIER = 'SX'

    def __init__(self, w3_provider=None):
        super(StableX, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x8f2A0d8865D995364DC6843D51Cf6989001f989e')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x918d7e714243F7d9d463C37e106235dCde294ffC')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return StableXCache()

    def reserve_manager(self):
        return StableXReserve()

    def __str__(self):
        return 'SushiSwap'


class StableXReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = StableXCache()
        self.swap = StableX(w3_provider=self.w3)
        self.prefix = 'STABLEX'
