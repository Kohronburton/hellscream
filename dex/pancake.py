from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class PancakeCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'PCAKE'
        super().__init__()


class Pancake(UniFactory):

    IDENTIFIER = 'PK'

    def __init__(self, w3_provider=None):
        super(Pancake, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x10ED43C718714eb63d5aA57B78B54704E256024E')
                              #  0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F router v1
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xBCfCcbde45cE874adCB698cC183deBcF17952812')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return PancakeCache()

    def reserve_manager(self):
        return PancakeReserve()

    def __str__(self):
        return 'PancakeSwap'


class PancakeReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = PancakeCache()
        self.swap = Pancake(w3_provider=self.w3)
        self.prefix = 'PCAKE'


