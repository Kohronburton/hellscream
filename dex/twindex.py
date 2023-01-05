from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class TwindexSwapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'TWINDEX'
        super().__init__()


class TwindexSwap(UniFactory):

    IDENTIFIER = 'TW'

    def __init__(self, w3_provider=None):
        super(TwindexSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x6B011d0d53b0Da6ace2a3F436Fd197A4E35f47EF')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x4e66fda7820c53c1a2f601f84918c375205eac3e')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return TwindexSwapCache()

    def reserve_manager(self):
        return TwindexSwapReserve()

    def __str__(self):
        return 'TWINDEX'


class TwindexSwapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = TwindexSwapCache()
        self.swap = TwindexSwap(w3_provider=self.w3)
        self.prefix = 'TWINDEX'
