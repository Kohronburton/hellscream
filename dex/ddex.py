from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class dDEXCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'dDEX'
        super().__init__()


class dDEX(UniFactory):

    IDENTIFIER = 'DD'

    def __init__(self, w3_provider=None):
        super(dDEX, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x0c7146a55f976E9A7157F8a832BD4B751e0E6A13')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xceb15eCa4Fe2120043D9498D0147B8665c1DA925')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return dDEXCache()

    def reserve_manager(self):
        return dDEXReserve()

    def __str__(self):
        return 'dDEX'


class dDEXReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = dDEXCache()
        self.swap = dDEX(w3_provider=self.w3)
        self.prefix = 'dDEX'
