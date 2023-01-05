from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class BabyCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'BABY'
        super().__init__()


class Baby(UniFactory):

    IDENTIFIER = 'BB'

    def __init__(self, w3_provider=None):
        super(Baby, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x325E343f1dE602396E256B67eFd1F61C3A6B38Bd')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x86407bEa2078ea5f5EB5A52B2caA963bC1F889Da')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return BabyCache()

    def reserve_manager(self):
        return BabyReserve()

    def __str__(self):
        return 'BabySwap'


class BabyReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = BabyCache()
        self.swap = Baby(w3_provider=self.w3)
        self.prefix = 'BABY'
