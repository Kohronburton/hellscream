from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class AleCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'ALE'
        super().__init__()


class Ale(UniFactory):

    IDENTIFIER = 'AL'

    def __init__(self, w3_provider=None):
        super(Ale, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xBfBCc27fC5eA4c1D7538e3e076c79A631Eb2beA6')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x731d91Dd835330cb2BeeAFB9a1672e3177B7168f')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return AleCache()

    def reserve_manager(self):
        return AleReserve()

    def __str__(self):
        return 'Ale'


class AleReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = AleCache()
        self.swap = Ale(w3_provider=self.w3)
        self.prefix = 'ALE'
