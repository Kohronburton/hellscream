from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class DinoCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'DINO'
        super().__init__()


class Dino(UniFactory):

    IDENTIFIER = 'DN'

    def __init__(self, w3_provider=None):
        super(Dino, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xc2a88eCE6B6321819D947c9EadEABBa699c16349')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x35E9455c410EacD6B4Dc1D0ca3144031f6251Dc2')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return DinoCache()

    def reserve_manager(self):
        return DinoReserve()

    def __str__(self):
        return 'DinoSwap'


class DinoReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = DinoCache()
        self.swap = Dino(w3_provider=self.w3)
        self.prefix = 'DINO'
