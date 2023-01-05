from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class BorgCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'BORG'
        super().__init__()


class BorgSwap(UniFactory):

    IDENTIFIER = 'BO'

    def __init__(self, w3_provider=None):
        super(BorgSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xb3eEb69945D278Fe6f755830316a6A43eeB09Bd5')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x40dFC2f530469452D5A9bB33356B071Be0758c4c')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return BorgCache()

    def reserve_manager(self):
        return BorgReserve()

    def __str__(self):
        return 'BorgSwap'


class BorgReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = BorgCache()
        self.swap = BorgSwap(w3_provider=self.w3)
        self.prefix = 'BORG'
