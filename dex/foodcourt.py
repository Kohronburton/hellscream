from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class FoodCourtCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'FOODCOURT'
        super().__init__()


class FoodCourt(UniFactory):

    IDENTIFIER = 'FC'

    def __init__(self, w3_provider=None):
        super(FoodCourt, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x0F4610aB02920a99f639F675085A5d3e24b0D7ae')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xc801c7980c8c7900bc898b1f38392b235ff64097')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return FoodCourtCache()

    def reserve_manager(self):
        return FoodCourtReserve()

    def __str__(self):
        return 'FoodCourt'


class FoodCourtReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = FoodCourtCache()
        self.swap = FoodCourt(w3_provider=self.w3)
        self.prefix = 'BURGER'
