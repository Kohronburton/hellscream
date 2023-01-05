from dex.dexmanager import DEXManager
from flashloan.cream import CREAMLending
import logging
import json
from multiprocessing import Process, Queue
from network.provider import random_local_provider
from network.redis import redis_connection
import random
from redis import Redis
import time
import web3
from web3.exceptions import ContractLogicError, BadFunctionCallOutput


def work(q):
    ew = ERC20_Worker()

    while True:
        res = q.get()
        if res == 'DONE':
            return

        try:
            ew.lookup_contract(res)
        except (OverflowError, ContractLogicError, BadFunctionCallOutput):
            logging.warning(f'Overflow error, blacklisting {res}')
            ew.blacklist_addr(res)


class ERC20_Worker:

    def __init__(self, w3_provider=None):

        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        self.erc20abi = json.load(open('abi/erc20.abi'))
        self.redis = redis_connection()

        # Multiprocessing Workers
        self.work_queues = []
        self.procs = []

        self.stablecoin_addresses = [
            web3.Web3.toChecksumAddress('0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'),   # Binance: BUSD Stablecoin
            web3.Web3.toChecksumAddress('0x55d398326f99059fF775485246999027B3197955'),   # BUSD-T Stablecoin
            web3.Web3.toChecksumAddress('0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d')    # USD Coin: USDC Token
        ]

        self.TOKEN_WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
        self.TOKEN_ETH = '0x2170Ed0880ac9A755fd29B2688956BD959F933F8'

    def balanceOf(self, token_contract: str, wallet_address: str) -> int:

        bep20Token = self.w3.eth.contract(address=token_contract, abi=self.erc20abi)
        amount = bep20Token.functions.balanceOf(wallet_address).call()

        return amount

    def stablecoins(self):
        tokens = []
        for addr in self.stablecoin_addresses:
            tokens.append(self.get_token(addr))

        return tokens

    def blacklist_addr(self, addr):
        self.redis.sadd('ERC20_BLACKLIST_ADDR', web3.Web3.toChecksumAddress(addr))

    def is_blacklisted(self, addr: str) -> bool:
        return self.redis.sismember('ERC20_BLACKLIST_ADDR', addr)

    def get_blacklist(self) -> set:
        bl = []
        for addr in self.redis.smembers('ERC20_BLACKLIST_ADDR'):
            bl.append(addr.decode('utf-8'))
        return set(bl)

    def queue_erc20_lookup(self, address):
        self.redis.sadd('ERC20_TO_FETCH', web3.Web3.toChecksumAddress(address))

    def get_queued_erc20(self):
        q = self.redis.smembers('ERC20_TO_FETCH')
        return [p.decode('utf-8') for p in q]

    def dequeue_erc20(self, address: str):
        self.redis.srem('ERC20_TO_FETCH', address)

    def _find_all_erc20_from_dexes(self) -> set:

        dm = DEXManager()
        all_erc20_contracts = []
        for dex in dm.dex_list:
            cache = dex.cache()
            all_erc20_contracts.extend(list(cache.pair_token0_addr.values()))
            all_erc20_contracts.extend(list(cache.pair_token1_addr.values()))

        cl = CREAMLending()
        all_erc20_contracts.extend(cl.addr_tkn.keys())
        all_erc20_contracts.extend(cl.token_fl_mapping().keys())
        all_erc20_contracts.extend(self.get_queued_erc20())

        blacklist = self.get_blacklist()

        return set(all_erc20_contracts) - blacklist

    def get_token(self, address):
        tk = {'name': self.redis.hget('ERC20_NAMES', address).decode('utf-8'),
              'address': address,
              'decimal': int(self.redis.hget('ERC20_DECIMALS', address)),
              'total_supply': self.redis.hget('ERC20_TOTALSUPPLY', address),
              'symbol': self.redis.hget('ERC20_SYMBOL', address).decode('utf-8'),
              }

        return tk

    def get_token_by_name(self, name):

        name_count = 0
        for address, token in self.all_tokens().items():
            if token['name'] == name:
                name_count += 1

        if name_count > 1:
            raise ValueError(f"Warning: name {name} is not unique among token database, found {name_count} matches")

        for address, token in self.all_tokens().items():
            if token['name'] == name:
                return token
        raise ValueError(f'Token {name} is not in system')

    def lookup_contract(self, contract_address):
        contract = self.w3.eth.contract(address=contract_address, abi=self.erc20abi)

        name = contract.functions.name().call()
        decimals = contract.functions.decimals().call()
        total_supply = contract.functions.totalSupply().call()
        symbol = contract.functions.symbol().call()

        self.redis.hset('ERC20_NAMES', contract_address, name)
        self.redis.hset('ERC20_DECIMALS', contract_address, decimals)
        self.redis.hset('ERC20_TOTALSUPPLY', contract_address, total_supply)
        self.redis.hset('ERC20_SYMBOL', contract_address, symbol)

        self.dequeue_erc20(contract_address)

        logging.info(f'Updated: {name: <20} {decimals: <6} {total_supply}')

    def all_tokens(self):
        names = self.redis.hgetall('ERC20_NAMES')
        decimals = self.redis.hgetall('ERC20_DECIMALS')
        total_supply = self.redis.hgetall('ERC20_TOTALSUPPLY')
        symbols = self.redis.hgetall('ERC20_SYMBOL')

        type_names = {}
        for token_addr, token_name in names.items():
            token_addr = token_addr.decode('utf-8')
            token_name = token_name.decode('utf-8')
            type_names[token_addr] = token_name
        names = type_names

        type_symbols = {}
        for token_addr, token_symb in symbols.items():
            token_addr = token_addr.decode('utf-8')
            token_symb = token_symb.decode('utf-8')
            type_symbols[token_addr] = token_symb
        symbols = type_symbols

        type_decimals = {}
        for token_addr, token_decimals in decimals.items():
            token_addr = token_addr.decode('utf-8')
            token_decimals = int(token_decimals)
            type_decimals[token_addr] = token_decimals
        decimals = type_decimals

        type_totalsupply = {}
        for token_addr, token_tsupply in total_supply.items():
            token_addr = token_addr.decode('utf-8')
            token_tsupply = int(token_tsupply)
            type_totalsupply[token_addr] = token_tsupply
        total_supply = type_totalsupply

        tokens = {}

        blacklist = self.get_blacklist()

        for add, name in names.items():
            if add not in blacklist:
                tokens[add] = {'name': name,
                               'address': add,
                               'decimal': decimals[add],
                               'total_supply': total_supply[add],
                               'symbol': symbols[add]}

        return tokens

    def mainloop_single_threaded(self):

        all_erc20_contracts = self._find_all_erc20_from_dexes()
        all_tokens = self.all_tokens()
        blacklist = self.get_blacklist()

        for contract in all_erc20_contracts:
            if contract not in all_tokens.keys() and contract not in blacklist:
                try:
                    self.lookup_contract(contract)
                except OverflowError:
                    logging.error('Overflow Error, blacklisting', contract)
                    self.blacklist_addr(contract)

    def mainloop(self):

        if len(self.procs) == 0:
            for _ in range(20):
                q = Queue()
                self.work_queues.append(q)
                p = Process(target=work, args=(q, ))
                self.procs.append(p)
            for p in self.procs:
                p.start()

        all_erc20_contracts = self._find_all_erc20_from_dexes()
        all_tokens = self.all_tokens()
        blacklist = self.get_blacklist()

        for contract in all_erc20_contracts:
            if contract not in all_tokens.keys() and contract not in blacklist:
                q = random.choice(self.work_queues)
                q.put(contract)
                logging.info(f'Put {contract}')

        done = False
        while not done:
            done = all([q.empty() for q in self.work_queues])
            time.sleep(1)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    logging.info('ERC20 Worker entering main loop')
    worker = ERC20_Worker()

    out_counter = 0
    while True:
        worker.mainloop()

        time.sleep(10)
        out_counter += 1
        if out_counter > 2:
            token_count = len(worker.all_tokens().keys())
            logging.info(f'ERC20 Worker, ALL OK {token_count} tokens in database')
            out_counter = 0
