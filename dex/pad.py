from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class PadCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'PAD'
        super().__init__()


class Pad(UniFactory):

    IDENTIFIER = 'PA'

    def __init__(self, w3_provider=None):
        super(Pad, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x76437234D29f84D9A12820A137c6c6A719138C24')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xb836017acf10b8a7c6c6c9e99efe0f5b0250fc45')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return PadCache()

    def reserve_manager(self):
        return PadReserve()

    def __str__(self):
        return 'Pad'


class PadReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = PadCache()
        self.swap = Pad(w3_provider=self.w3)
        self.prefix = 'PAD'
