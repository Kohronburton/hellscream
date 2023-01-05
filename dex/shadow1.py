from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class ShadowDEX1Cache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'SHADOWDEX1'
        super().__init__()


class ShadowDEX1(UniFactory):

    IDENTIFIER = 'SD1'

    def __init__(self, w3_provider=None):
        super(ShadowDEX1, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x5eD3C9089Ed0355bc77CF439Dc2eD28c4054C8c4')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xEeFa8Ca24dd1D573882277b917720953e999734D')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return ShadowDEX1Cache()

    def reserve_manager(self):
        return ShadowDEX1Reserve()

    def __str__(self):
        return 'ShadowDEX1'


class ShadowDEX1Reserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = ShadowDEX1Cache()
        self.swap = ShadowDEX1(w3_provider=self.w3)
        self.prefix = 'ShadowDEX1'
