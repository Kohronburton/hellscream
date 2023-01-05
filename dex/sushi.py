from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class SushiCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'SUSHI'
        super().__init__()


class Sushi(UniFactory):

    IDENTIFIER = 'SH'

    def __init__(self, w3_provider=None):
        super(Sushi, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xc35dadb65012ec5796536bd9864ed8773abc74c4')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return SushiCache()

    def reserve_manager(self):
        return SushiReserve()

    def __str__(self):
        return 'SushiSwap'


class SushiReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = SushiCache()
        self.swap = Sushi(w3_provider=self.w3)
        self.prefix = 'SUSHI'
