from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class PantherCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'PANTHER'
        super().__init__()


class Panther(UniFactory):

    IDENTIFIER = 'PR'

    def __init__(self, w3_provider=None):
        super(Panther, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x24f7c33ae5f77e2a9eceed7ea858b4ca2fa1b7ec')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x670f55c6284c629c23bae99f585e3f17e8b9fc31')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return PantherCache()

    def reserve_manager(self):
        return PantherReserve()

    def __str__(self):
        return 'PantherSwap'


class PantherReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = PantherCache()
        self.swap = Panther(w3_provider=self.w3)
        self.prefix = 'PANTHER'
