from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class FatAnimalCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'FANIMAL'
        super().__init__()


class FatAnimal(UniFactory):

    IDENTIFIER = 'FA'

    def __init__(self, w3_provider=None):
        super(FatAnimal, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x3181460954E2c590a0314B948a2e529777cc89A2')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xaba5cA9729294C2a49Cb6e741f2B97b988e80407')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return FatAnimalCache()

    def reserve_manager(self):
        return FatAnimalReserve()

    def __str__(self):
        return 'FatAnimal'


class FatAnimalReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = FatAnimalCache()
        self.swap = FatAnimal(w3_provider=self.w3)
        self.prefix = 'FANIMAL'
