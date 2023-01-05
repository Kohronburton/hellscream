from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class ApeCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'APE'
        super().__init__()


class Ape(UniFactory):

    IDENTIFIER = 'AE'

    def __init__(self, w3_provider=None):
        super(Ape, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xC0788A3aD43d79aa53B09c2EaCc313A787d1d607')
                                # 0xcF0feBd3f17CEf5b47b0cD257aCf6025c5BFf3b7

        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x0841bd0b734e4f5853f0dd8d7ea041c241fb0da6')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return ApeCache()

    def reserve_manager(self):
        return ApeReserve()

    def __str__(self):
        return 'Ape'


class ApeReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = ApeCache()
        self.swap = Ape(w3_provider=self.w3)
        self.prefix = 'APE'
