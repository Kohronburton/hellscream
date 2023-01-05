from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class MDEXCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'MDEX'
        super().__init__()


class MDEX(UniFactory):

    IDENTIFIER = 'MX'

    def __init__(self, w3_provider=None):
        super(MDEX, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x7DAe51BD3E3376B8c7c4900E9107f12Be3AF1bA8')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x3CD1C46068dAEa5Ebb0d3f55F6915B10648062B8')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return MDEXCache()

    def reserve_manager(self):
        return MDEXReserve()

    def __str__(self):
        return 'MDEX'


class MDEXReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = MDEXCache()
        self.swap = MDEX(w3_provider=self.w3)
        self.prefix = 'MDEX'
