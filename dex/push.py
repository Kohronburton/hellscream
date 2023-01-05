from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class PushCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'PUSH'
        super().__init__()


class Push(UniFactory):

    IDENTIFIER = 'PU'

    def __init__(self, w3_provider=None):
        super(Push, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x1380BF99ba8d0fEA3A82d0e28A7D10F430239190')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x7Ee498aE1e4e14d5a31BCd5a9215f58216d701BE')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return PushCache()

    def reserve_manager(self):
        return PushReserve()

    def __str__(self):
        return 'Push'


class PushReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = PushCache()
        self.swap = Push(w3_provider=self.w3)
        self.prefix = 'PUSH'
