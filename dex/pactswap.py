from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class PactswapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'PACTSWAP'
        super().__init__()


class Pactswap(UniFactory):

    IDENTIFIER = 'PT'

    def __init__(self, w3_provider=None):
        super(Pactswap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xf542194C48729406983868443ccC10Cb7f9d1799')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x4cBAF01d645a233D11CD5A19939387A94d7f2f02')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return PactswapCache()

    def reserve_manager(self):
        return PactswapReserve()

    def __str__(self):
        return 'Pactswap'


class PactswapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = PactswapCache()
        self.swap = Pactswap(w3_provider=self.w3)
        self.prefix = 'PACTSWAP'
