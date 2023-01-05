from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class SlimeCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'SLIME'
        super().__init__()


class Slime(UniFactory):

    IDENTIFIER = 'SL'

    def __init__(self, w3_provider=None):
        super(Slime, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x34766241a5DF0483545A52AB1DBd5eC88E251dD3')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xcbe7425662bf0edf164abf12c881ced6fdafe75e')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return SlimeCache()

    def reserve_manager(self):
        return SlimeReserve()

    def __str__(self):
        return 'SlimeRouter'


class SlimeReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = SlimeCache()
        self.swap = Slime(w3_provider=self.w3)
        self.prefix = 'SLIME'
