from multiprocessing import Queue, Process
from dex.dexmanager import DEXManager
from dex.pancake import Pancake, PancakeCache
from erc20_worker import ERC20_Worker
from eth_abi.exceptions import InsufficientDataBytes
import json
from network.provider import random_local_provider
from network.redis import redis_connection
import random
import time
from web3.exceptions import BadFunctionCallOutput, ContractLogicError


class ProcWorker:

    def __init__(self):
        self.dm = DEXManager(w3_provider=random_local_provider())
        self.erc = ERC20_Worker()

        self.profit_redis = redis_connection()

        self.all_tokens = self.erc.all_tokens()

        self.PRINT_LOSSES = True

        # Work Statistics
        self.profits = 0
        self.losses = 0
        self.exceptions = 0
        self.num_work_packets = 0
        self.no_price_info = 0

        self.pancake = Pancake()
        self.pancake_cache = PancakeCache()

    def get_amount_token_usd(self, token_address, usd_amount=100):
        # find all stablecoin pairs
        stablecoins = self.erc.stablecoins()

        for st in stablecoins:

            #                       WBNB
            route = [st['address'], '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', token_address]

            stable_in = 100 * (1 * pow(10, st['decimal']))

            try:
                amount_out_pancake = self.pancake.router_contract.functions.getAmountsOut(stable_in, route).call()
                return amount_out_pancake[-1]
            except (BadFunctionCallOutput, OverflowError) as e:
                continue

    def get_amount_token_bnb(self, token_address, WBNB_amount=0.2):
        route = ['0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c', token_address]

        amount_in = WBNB_amount * (1 * pow(10, 18))

        try:
            amount_out_pancake = self.pancake.router_contract.functions.getAmountsOut(amount_in, route).call()
            return amount_out_pancake[-1]
        except (BadFunctionCallOutput, OverflowError) as e:
            return None

    def process_work_packet(self, work):
        if self.num_work_packets > 100:
            print('Thread Stats:',
                  'Profits:', self.profits,
                  'Losses:', self.losses,
                  'Exceptions:', self.exceptions,
                  'No price:', self.no_price_info)
            self.profits = 0
            self.losses = 0
            self.exceptions = 0
            self.num_work_packets = 0
            self.no_price_info = 0

        self.num_work_packets += 1

        frm = work['source_token']
        to = work['dest_token']

        src_cache = dm.get_pair_cache_by_indent(work['source_dex'])
        dst_cache = dm.get_pair_cache_by_indent(work['dest_dex'])

        if src_cache.find_index_for_pair(frm, to) is None:
            return

        work['source_base'] = self.get_amount_token_usd(frm)

        if work['source_base'] is None:
            self.no_price_info += 1
            return

        try:
            amount_in_src_dex = work['source_base']
            source_dex = self.dm.get_dex_by_ident(work['source_dex'])
            amount_out_src_dex = source_dex.router_contract.functions.getAmountsOut(amount_in_src_dex, [frm, to]).call()

            dest_dex = self.dm.get_dex_by_ident(work['dest_dex'])
            amount_out_dest_dex = dest_dex.router_contract.functions.getAmountsOut(amount_out_src_dex[-1], [to, frm]).call()

            amount_out = amount_out_dest_dex[-1]
            profit = amount_out - amount_in_src_dex
        except (BadFunctionCallOutput, InsufficientDataBytes, ContractLogicError, OverflowError) as e:
            self.exceptions += 1
            print(e)
            return

        profit_display = profit / pow(10, all_tokens[frm]['decimal'])

        if profit > 0:
            self.profits += 1
            print(str(source_dex.IDENTIFIER).ljust(5),
                  ' - ',
                  str(dest_dex.IDENTIFIER).ljust(5),
                  'PROFIT:'.ljust(10),
                  self.all_tokens[frm]['name'].ljust(20),
                  self.all_tokens[to]['name'].ljust(20),
                  '%f' % profit_display)

            work['profit'] = profit
            work['profit_display'] = profit_display

            self.profit_redis.publish('hellscream', json.dumps(work))
        else:
            self.losses += 1
            if self.PRINT_LOSSES:
                print(str(source_dex.IDENTIFIER).ljust(5),
                      ' - ',
                      str(dest_dex.IDENTIFIER).ljust(5),
                      'LOSS:'.ljust(10),
                      self.all_tokens[frm]['name'].ljust(20),
                      self.all_tokens[to]['name'].ljust(20),
                      '%f' % profit_display)


def worker(work_queue):

    pw = ProcWorker()

    while True:

        # Work:
        # {'source_dex'   : CHAR(2) Dex.IDENTIFIER,
        #  'dest_dex'     : CHAR(2) Dex.IDENTIFIER,
        #  'source_token' : '0x...',
        #  'source_base'  : BIGINT,
        #  'dest_token'   : '0x...',
        #  }
        work = work_queue.get()

        if work == 'DONE':
            print('Thread Stats:', 'Profits:', pw.profits, 'Losses:', pw.losses, 'Exceptions:', pw.exceptions)
            return

        pw.process_work_packet(work)


if __name__ == '__main__':

    erc20 = ERC20_Worker()
    all_tokens = erc20.all_tokens()
    dm = DEXManager()

    # WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
    # ETH = '0x2170Ed0880ac9A755fd29B2688956BD959F933F8'
    # XRP = '0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE'
    # DOT = '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402'
    # DAI = '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3'
    # LINK = '0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD'
    # TWT = '0x4B0F1812e5Df2A09796481Ff14017e6005508003'
    # LTC = '0x4338665CBB7B2485A8855A139b75D5e34AB0DB94'
    # CAKE = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'
    # BUSD = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
    # USDT = '0x55d398326f99059fF775485246999027B3197955'
    # BTCB = '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c'
    # AMOUNT = 100
    # fromTokens = CREAMLending.token_fl_mapping().keys()
    # toTokens = [DAI, USDT, WBNB, ETH, XRP, DOT, LINK, TWT, LTC, CAKE, BUSD, BTCB]

    num_procs = 12
    queues = []
    procs = []

    for i in range(num_procs):
        q = Queue()
        queues.append(q)

        p = Process(target=worker, args=(q, ))
        procs.append(p)
        p.start()

    for src_dex in dm.dex_list:
        for dst_dex in dm.dex_list:

            src_dex_ident = src_dex.IDENTIFIER
            dst_dex_ident = dst_dex.IDENTIFIER

            if src_dex_ident == dst_dex_ident:
                continue

            s_a = dm.get_pair_cache_by_indent(src_dex_ident).all_tradable_tokens()
            s_b = dm.get_pair_cache_by_indent(dst_dex_ident).all_tradable_tokens()

            common_tokens = s_a.intersection(s_b)

            if len(common_tokens) == 0:
                continue

            for aa in common_tokens:

                for bb in common_tokens:

                    if aa == bb:
                        continue

                    work = {'source_dex': src_dex_ident,
                            'source_token': aa,
                            'dest_dex': dst_dex_ident,
                            'dest_token': bb,
                            'timestamp': time.time()}

                    ''' MULTI-PROCESS '''
                    q = random.choice(queues)
                    q.put(work)

                    ''' SINGLE PROCESS '''
                    #pw = ProcWorker()
                    #pw.process_work_packet(work)

    for q in queues:
        q.put('DONE')

    for p in procs:
        p.join()
