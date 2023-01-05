from dex.aleswap import Ale, AleCache
from dex.anyswap4 import Anyswap4, Anyswap4Cache
from dex.ape import Ape, ApeCache
from dex.baby import Baby, BabyCache
from dex.bakery import Bakery, BakeryCache
from dex.biswap import BiSwap, BiSwapCache
from dex.borgswap import BorgSwap, BorgCache
from dex.burger import Burger, BurgerCache
from dex.cafe import Cafe, CafeCache
from dex.cheeseswap import CheeseSwap, CheeseCache
from dex.coinswap import Coinswap, CoinSwapCache
from dex.ddex import dDEX, dDEXCache
from dex.definix import Definix, DefinixCache
from dex.dino import Dino, DinoCache
from dex.dollaremon import Dollaremon, DollaremonCache
from dex.fatanimal import FatAnimal, FatAnimalCache
from dex.foodcourt import FoodCourt, FoodCourtCache
from dex.jetswap import Jetswap, JetswapCache
from dex.mdex import MDEX, MDEXCache
from dex.moondoge import MoonDoge, MoonDogeCache
from dex.pad import Pad, PadCache
from dex.pactswap import Pactswap, PactswapCache
from dex.pancake import Pancake, PancakeCache
from dex.panther import Panther, PantherCache
from dex.planet import Planet, PlanetCache
from dex.push import Push, PushCache
from dex.shadow1 import ShadowDEX1, ShadowDEX1Cache
from dex.shadow2 import ShadowDEX2, ShadowDEX2Cache
from dex.shadow3 import ShadowDEX3, ShadowDEX3Cache
from dex.slime import Slime, SlimeCache
from dex.smartswap import SmartSwap, SmartSwapCache
from dex.stablex import StableX, StableXCache
from dex.sushi import Sushi, SushiCache
from dex.tat import Tat, TatCache
from dex.twindex import TwindexSwap, TwindexSwapCache
from dex.valueliquid import ValueLiquid, ValueLiquidCache
from dex.wardenswap import WardenSwap, WardenSwapCache
from dex.waultswap import WaultSwap, WaultSwapCache


class DEXManager:

    def __init__(self, w3_provider=None):
        self.ale = Ale(w3_provider)
        self.any4 = Anyswap4(w3_provider)
        self.ape = Ape(w3_provider)
        self.baby = Baby(w3_provider)
        self.bakery = Bakery(w3_provider)
        self.biswap = BiSwap(w3_provider)
        self.borg = BorgSwap(w3_provider)
        # self.burger = Burger()  # Currently Paused after hack
        self.cafe = Cafe()
        self.cheese = CheeseSwap(w3_provider)
        self.coinswap = Coinswap(w3_provider)
        self.ddex = dDEX(w3_provider)
        self.definix = Definix(w3_provider)
        self.dino = Dino(w3_provider)
        self.dollaremon = Dollaremon(w3_provider)
        self.fatanimal = FatAnimal(w3_provider)
        self.foodcourt = FoodCourt(w3_provider)
        self.jetswap = Jetswap(w3_provider)
        self.mdex = MDEX(w3_provider)
        self.moondoge = MoonDoge(w3_provider)
        self.pad = Pad(w3_provider)
        self.pact = Pactswap(w3_provider)
        self.pancake = Pancake(w3_provider)
        self.panther = Panther(w3_provider)
        self.planet = Planet(w3_provider)
        self.push = Push(w3_provider)
        self.shadowdex1 = ShadowDEX1(w3_provider)
        self.shadowdex2 = ShadowDEX2(w3_provider)
        self.shadowdex3 = ShadowDEX3(w3_provider)
        self.slime = Slime(w3_provider)
        self.smart = SmartSwap(w3_provider)
        self.stablex = StableX(w3_provider)
        self.sushi = Sushi(w3_provider)
        self.tat = Tat(w3_provider)
        self.twindex = TwindexSwap(w3_provider)
        self.valliquid = ValueLiquid(w3_provider)
        self.wardenswap = WardenSwap(w3_provider)
        self.wault = WaultSwap(w3_provider)

        self.ale_cache = AleCache()
        self.any4_cache = Anyswap4Cache()
        self.ape_cache = ApeCache()
        self.baby_cache = BabyCache()
        self.bakery_cache = BakeryCache()
        self.biswap_cache = BiSwapCache()
        self.borg_cache = BorgCache()
        # self.burger_cache = BurgerCache()  # Currently Paused after hack
        self.cafe_cache = CafeCache()
        self.cheese_cache = CheeseCache()
        self.coinswap_cache = CoinSwapCache()
        self.ddex_cache = dDEXCache()
        self.definix_cache = DefinixCache()
        self.dino_cache = DinoCache()
        self.dollaremon_cache = DollaremonCache()
        self.fatanimal_cache = FatAnimalCache()
        self.foodcourt_cache = FoodCourtCache()
        self.jetswap_cache = JetswapCache()
        self.mdex_cache = MDEXCache()
        self.moondoge_cache = MoonDogeCache()
        self.pad_cache = PadCache()
        self.pact_cache = PactswapCache()
        self.pancake_cache = PancakeCache()
        self.panther_cache = PantherCache()
        self.planet_cache = PlanetCache()
        self.push_cache = PushCache()
        self.shadowdex1_cache = ShadowDEX1Cache()
        self.shadowdex2_cache = ShadowDEX2Cache()
        self.shadowdex3_cache = ShadowDEX3Cache()
        self.slime_cahce = SlimeCache()
        self.smart_cache = SmartSwapCache()
        self.stablex_cache = StableXCache()
        self.sushi_cache = SushiCache()
        self.tat_cache = TatCache()
        self.twindex_cache = TwindexSwapCache()
        self.valliquid_cache = ValueLiquidCache()
        self.wardenswap_cache = WardenSwapCache()
        self.waultswap_cache = WaultSwapCache()

        self.dex_list = [self.ale, self.any4, self.ape, self.baby, self.bakery, self.borg, self.cafe, self.cheese,
                         self.coinswap,
                         self.ddex, self.definix, self.dino, self.dollaremon, self.fatanimal,
                         self.foodcourt, self.jetswap, self.mdex,
                         self.moondoge, self.pad, self.pancake, self.panther, self.planet, self.push, self.shadowdex1,
                         self.shadowdex2,
                         self.shadowdex3, self.slime, self.smart, self.stablex, self.sushi, self.tat, self.twindex,
                         self.wardenswap, self.wault]

        self.cache_list = []
        for d in self.dex_list:
            self.cache_list.append(d.cache())

    def dex_router_address(self, identifier:str):
        for dex in self.dex_list:
            if dex.IDENTIFIER == identifier:
                return dex.ROUTER_ADDRESS

    def get_dex_by_ident(self, identifier: str):
        for d in self.dex_list:
            if d.IDENTIFIER == identifier:
                return d

    def get_pair_cache_by_indent(self, identifier: str):

        for i, dex in enumerate(self.dex_list):
            if dex.IDENTIFIER == identifier:
                return self.cache_list[i]

        raise NotImplemented(f'No pair cache for identifier {identifier}')

    def dex_factory_addr_by_ident(self, identifier: str) -> str:
        for d in self.dex_list:
            if d.IDENTIFIER == identifier:
                return d.ROUTER_ADDRESS

    def dex_by_address(self, address: str):
        for d in self.dex_list:
            if d.ROUTER_ADDRESS == address:
                return d

            if d.FACTORY_ADDRESS == address:
                return d
