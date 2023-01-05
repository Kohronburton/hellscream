import json
from network.provider import random_local_provider


class UniFactory:

    def __init__(self, w3_provider=None):

        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        self.ROUTER_ADDRESS = None
        self.FACTORY_ADDRESS = None

        self.factoryABI = json.load(open('abi/IUniswapV2Factory.json'))['abi']
        self.pairABI = json.load(open('abi/IUniswapV2Pair.json'))['abi']
        self.routerABI = json.load(open('abi/IUniswapV2Router02.json'))['abi']
        self.erc20abi = json.load(open('abi/erc20.abi'))

        self.factory_contract = None
        self.router_contract = None

    def router(self):
        return self.w3.eth.contract(address=self.ROUTER_ADDRESS, abi=self.routerABI)

    def factory(self):
        return self.w3.eth.contract(address=self.FACTORY_ADDRESS, abi=self.factoryABI)

    def all_pairs_length(self):
        return self.factory_contract.functions.allPairsLength().call()

    def pair_contract(self, pair_address: str):
        return self.w3.eth.contract(address=pair_address, abi=self.pairABI)

    def erc20_contract(self, contract_address: str):
        return self.w3.eth.contract(address=contract_address, abi=self.erc20abi)
