from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class CoinSwapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'COINSWAP'
        super().__init__()


class Coinswap(UniFactory):

    IDENTIFIER = 'CS'

    def __init__(self, w3_provider=None):
        super(Coinswap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x34DBe8E5faefaBF5018c16822e4d86F02d57Ec27')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xc2d8d27f3196d9989abf366230a47384010440c0')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return CoinSwapCache()

    def reserve_manager(self):
        return CoinSwapReserve()

    def __str__(self):
        return 'CoinSwap'


class CoinSwapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = CoinSwapCache()
        self.swap = Coinswap(w3_provider=self.w3)
        self.prefix = 'COINSWAP'
