from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class DollaremonCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'DOLLAREMON'
        super().__init__()


class Dollaremon(UniFactory):

    IDENTIFIER = 'DL'

    def __init__(self, w3_provider=None):
        super(Dollaremon, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xa871F514C70dC3399aB9605258eFF5c78d5a95Ae')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xcb4ee9910811edb5ff3fe0e3ce3a8ced25e24079')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return DollaremonCache()

    def reserve_manager(self):
        return DollaremonReserve()

    def __str__(self):
        return 'Dollaremon'


class DollaremonReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = DollaremonCache()
        self.swap = Dollaremon(w3_provider=self.w3)
        self.prefix = 'DOLLAREMON'
