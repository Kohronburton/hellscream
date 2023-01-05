from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class BiSwapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'BISWAP'
        super().__init__()


class BiSwap(UniFactory):

    IDENTIFIER = 'BI'

    def __init__(self, w3_provider=None):
        super(BiSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x3a6d8cA21D1CF76F653A67577FA0D27453350dD8')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x858E3312ed3A876947EA49d572A7C42DE08af7EE')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return BiSwapCache()

    def reserve_manager(self):
        return BiSwapReserve()

    def __str__(self):
        return 'BiSwap'


class BiSwapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = BiSwapCache()
        self.swap = BiSwap(w3_provider=self.w3)
        self.prefix = 'BISWAP'
