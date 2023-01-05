from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class ValueLiquidCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'VALUELIQUID'
        super().__init__()


class ValueLiquid(UniFactory):

    IDENTIFIER = 'VL'

    def __init__(self, w3_provider=None):
        super(ValueLiquid, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0xb7e19a1188776f32E8C2B790D9ca578F2896Da7C')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0x1B8E12F839BD4e73A47adDF76cF7F0097d74c14C')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return ValueLiquidCache()

    def reserve_manager(self):
        return ValueLiquidReserve()

    def __str__(self):
        return 'ValueLiquid'


class ValueLiquidReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = ValueLiquidCache()
        self.swap = ValueLiquid(w3_provider=self.w3)
        self.prefix = 'VALUELIQUID'
