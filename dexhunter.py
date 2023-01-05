from dex.dexmanager import DEXManager
import json
import logging
from network.provider import random_local_provider
from network.redis import redis_connection
import web3
from web3.exceptions import BadFunctionCallOutput


class DexHunter:

    def __init__(self):

        self.uni_router_abi = json.loads(open('abi/IUniswapV2Router02.json', 'r').read())
        self.redis = redis_connection()
        self.dex_addresses = []
        self.w3 = random_local_provider()

        self.dm = DEXManager()

        for dex in self.dm.dex_list:
            self.dex_addresses.append(dex.ROUTER_ADDRESS)

        self.pair_addresses = []
        for pc in self.dm.cache_list:
            self.pair_addresses.extend(pc.pair_addresses())

    def is_known_dex_address(self, address: str) -> bool:
        return address in self.dex_addresses

    def is_known_nondex_address(self, address: str) -> bool:
        if self.redis.sismember('DEXHUNTER_NONDEX_ADDRESSES', address):
            return True
        else:
            if address in self.pair_addresses:
                return True
        return False

    def set_is_not_dex(self, address):
        self.redis.sadd('DEXHUNTER_NONDEX_ADDRESSES', address)

    def set_maybe_dex(self, address):
        self.redis.sadd('DEXHUNTER_MAYBE_DEX', address)

    def check_address(self, address) -> bool:
        contract = self.w3.eth.contract(address=address, abi=self.uni_router_abi['abi'])
        try:
            factory = contract.functions.factory().call()
            self.set_maybe_dex(address)
            return True
        except (BadFunctionCallOutput, ValueError, TypeError):
            self.set_is_not_dex(address)
            return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    w3 = random_local_provider()
    dh = DexHunter()

    while True:
        txpool = w3.geth.txpool.content()
        pending = w3.geth.txpool.content().pending

        addresses = []
        for addr in list(pending.keys()):
            for nonce in list(pending[addr].keys()):
                addresses.append(pending[addr][nonce]['to'])

        addresses = list(set(addresses))

        print(len(addresses), 'in pending mempool')

        known_dexes = 0
        non_dexes = 0
        maybe_dexes = 0

        for addr in addresses:

            if addr is None:
                continue

            addr = web3.Web3.toChecksumAddress(addr)

            if dh.is_known_dex_address(addr):
                known_dexes += 1
                print('KNOWN DEX')
            else:
                if dh.is_known_nondex_address(addr):
                    non_dexes += 1
                    print('KNOWN NONDEX')
                else:
                    result = dh.check_address(addr)
                    if result:
                        maybe_dexes += 1
                        print('MAYBE DEX')
                    else:
                        non_dexes += 1
                        print('NONDEX')

        print('Known Dexes:', known_dexes)
        print('Non Dexes:', non_dexes)
        print('Maybe Dexes:', maybe_dexes)
        print()

    # pending = dict
    # keys = '0xaaaabbbb' : {AttributeDict({'1': AttributeDict({'blockHash': None,
    #   'blockNumber': None,
    #   'from': '0x8251ca3b5cf664944ef5877d9ada28f096308a9b',
    #   'gas': '0x5209',
    #   'gasPrice': '0x3b9aca00',
    #   'hash': '0xd0c0481a2f45205e0398903469e89b12702e69d28c39ca3e6e4550a8d1d06249',
    #   'input': '0x',
    #   'nonce': '0x1',
    #   'to': '0x54a936ffd2be2b3e307aad33bd79e612b9b7b88d',
    #   'transactionIndex': None,
    #   'value': '0x2fe831af73200',
    #   'v': '0x93',
    #   'r': '0xb03a95ba82ac8f9a67350fde47f8f2f7e2efb107ba5812d88b99dcde1371df18',
    #   's': '0x2e558424dfa684a961cce73442df7faad2fc7fde694d655356fd556a41549d66'})})
    #   }
