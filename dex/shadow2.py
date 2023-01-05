from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class ShadowDEX2Cache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'SHADOWDEX2'
        super().__init__()


class ShadowDEX2(UniFactory):

    IDENTIFIER = 'SD2'

    def __init__(self, w3_provider=None):
        super(ShadowDEX2, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x5164b689eBECf0F5186969D410919092620C1F1f')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x2ba75f08fAE6Fa6C2b09C7f2D3cFe9a9E6d3167f')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return ShadowDEX2Cache()

    def reserve_manager(self):
        return ShadowDEX2Reserve()

    def __str__(self):
        return 'ShadowDEX2'


class ShadowDEX2Reserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = ShadowDEX2Cache()
        self.swap = ShadowDEX2(w3_provider=self.w3)
        self.prefix = 'ShadowDEX2'
