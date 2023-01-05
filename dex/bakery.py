from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class BakeryCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'BAKERY'
        super().__init__()


class Bakery(UniFactory):

    IDENTIFIER = 'BK'

    def __init__(self, w3_provider=None):
        super(Bakery, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xCDe540d7eAFE93aC5fE6233Bee57E1270D3E330F')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x01bF7C66c6BD861915CdaaE475042d3c4BaE16A7')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return BakeryCache()

    def reserve_manager(self):
        return BakeryReserve()

    def __str__(self):
        return 'Bakery'


class BakeryReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = BakeryCache()
        self.swap = Bakery(w3_provider=self.w3)
        self.prefix = 'BAKERY'
