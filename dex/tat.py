from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class TatCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'TAT'
        super().__init__()


class Tat(UniFactory):

    IDENTIFIER = 'TT'

    def __init__(self, w3_provider=None):
        super(Tat, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x53C309a523316599F9dAd3797860e625dA62F66e')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xa8d01b70ae1dc9ac201b56a81bea4c03298ffe0c')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return TatCache()

    def reserve_manager(self):
        return TatReserve()

    def __str__(self):
        return 'Tat'


class TatReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = TatCache()
        self.swap = Tat(w3_provider=self.w3)
        self.prefix = 'TAT'
