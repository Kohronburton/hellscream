from network.provider import random_local_provider
from dex.abstract.paircache import PairCache
from dex.abstract.reserve import Reserve
from dex.abstract.unifactory import UniFactory
from web3 import Web3


class PlanetCache(PairCache):

    def __init__(self):
        self.REDIS_PREFIX = 'PLANET'
        super().__init__()


class Planet(UniFactory):

    IDENTIFIER = 'PL'

    def __init__(self, w3_provider=None):
        super(Planet, self).__init__(w3_provider=w3_provider)
        self.ROUTER_ADDRESS = Web3.toChecksumAddress('0x9F088377BcdC220CB0E1Ad15aE6Bc75074beE9F6')
        self.FACTORY_ADDRESS = Web3.toChecksumAddress('0xa053582601214feb3778031a002135cbbb7dba18')
        self.factory_contract = self.factory()
        self.router_contract = self.router()

    def cache(self):
        return PlanetCache()

    def reserve_manager(self):
        return PlanetReserve()

    def __str__(self):
        return 'Planet'


class PlanetReserve(Reserve):

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        super().__init__(w3_provider=self.w3)
        self.cache = PlanetCache()
        self.swap = Planet(w3_provider=self.w3)
        self.prefix = 'PLANET'
