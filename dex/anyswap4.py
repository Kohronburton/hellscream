from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class Anyswap4Cache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'ANYSWAP4'
        super().__init__()


class Anyswap4(UniFactory):

    IDENTIFIER = 'A4'

    def __init__(self, w3_provider=None):
        super(Anyswap4, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xd1C5966f9F5Ee6881Ff6b261BBeDa45972B1B5f3')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xc35dadb65012ec5796536bd9864ed8773abc74c4')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return Anyswap4Cache()

    def reserve_manager(self):
        return Anyswap4Reserve()

    def __str__(self):
        return 'Anyswap4'


class Anyswap4Reserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = Anyswap4Cache()
        self.swap = Anyswap4(w3_provider=self.w3)
        self.prefix = 'ANYSWAP4'
