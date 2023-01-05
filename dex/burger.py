from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class BurgerCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'BURGER'
        super().__init__()


class Burger(UniFactory):

    IDENTIFIER = 'BG'

    def __init__(self, w3_provider=None):
        super(Burger, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x9ef4f7afa7cea1d1b29808a534db43f96051be6e')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x8a1E9d3aEbBBd5bA2A64d3355A48dD5E9b511256')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return BurgerCache()

    def reserve_manager(self):
        return BurgerReserve()

    def __str__(self):
        return 'Burger'


class BurgerReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = BurgerCache()
        self.swap = Burger(w3_provider=self.w3)
        self.prefix = 'BURGER'
