from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class CheeseCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'CHEESE'
        super().__init__()


class CheeseSwap(UniFactory):

    IDENTIFIER = 'CH'

    def __init__(self, w3_provider=None):
        super(CheeseSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x3047799262d8D2EF41eD2a222205968bC9B0d895')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xdd538E4Fd1b69B7863E1F741213276A6Cf1EfB3B')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return CheeseCache()

    def reserve_manager(self):
        return CheeseReserve()

    def __str__(self):
        return 'CheeseSwap'


class CheeseReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = CheeseCache()
        self.swap = CheeseSwap(w3_provider=self.w3)
        self.prefix = 'CHEESE'


