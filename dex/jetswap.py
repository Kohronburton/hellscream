from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class JetswapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'JETSWAP'
        super().__init__()


class Jetswap(UniFactory):

    IDENTIFIER = 'JS'

    def __init__(self, w3_provider=None):
        super(Jetswap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xBe65b8f75B9F20f4C522e0067a3887FADa714800')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x0eb58e5c8aa63314ff5547289185cc4583dfcbd5')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return JetswapCache()

    def reserve_manager(self):
        return JetswapReserve()

    def __str__(self):
        return 'JetSwap'


class JetswapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = JetswapCache()
        self.swap = Jetswap(w3_provider=self.w3)
        self.prefix = 'JETSWAP'
