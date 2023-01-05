from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class JustLiquidityCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'JUSTLIQ'
        super().__init__()


class JustLiquidity(UniFactory):

    IDENTIFIER = 'JL'

    def __init__(self, w3_provider=None):
        super(JustLiquidity, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xbd67d157502A23309Db761c41965600c2Ec788b2')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x553990F2CBA90272390f62C5BDb1681fFc899675')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return JustLiquidityCache()

    def reserve_manager(self):
        return JustLiquidityReserve()

    def __str__(self):
        return 'JustLiquidity'


class JustLiquidityReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = JustLiquidityCache()
        self.swap = JustLiquidity(w3_provider=self.w3)
        self.prefix = 'JUSTLIQ'
