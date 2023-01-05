from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class SmartSwapCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'SMARTSWAP'
        super().__init__()


class SmartSwap(UniFactory):

    IDENTIFIER = 'SM'

    def __init__(self, w3_provider=None):
        super(SmartSwap, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xf78234E21f1F34c4D8f65faF1BC82bfc0fa24920')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x655333a1cd74232c404049af9d2d6cf1244e71f6')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return SmartSwapCache()

    def reserve_manager(self):
        return SmartSwapReserve()

    def __str__(self):
        return 'SmartSwap'


class SmartSwapReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = SmartSwapCache()
        self.swap = SmartSwap(w3_provider=self.w3)
        self.prefix = 'SMARTSWAP'
