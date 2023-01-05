from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class ShadowDEX3Cache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'SHADOWDEX3'
        super().__init__()


class ShadowDEX3(UniFactory):

    IDENTIFIER = 'SD3'

    def __init__(self, w3_provider=None):
        super(ShadowDEX3, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x26234882C1D95fCaDA4553a655045c35cffC9dAD')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xB836017ACf10b8A7c6c6C9e99eFE0f5B0250FC45')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return ShadowDEX3Cache()

    def reserve_manager(self):
        return ShadowDEX3Reserve()

    def __str__(self):
        return 'ShadowDEX3'


class ShadowDEX3Reserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = ShadowDEX3Cache()
        self.swap = ShadowDEX3(w3_provider=self.w3)
        self.prefix = 'ShadowDEX3'
