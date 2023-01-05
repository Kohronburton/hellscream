from dex.dexmanager import DEXManager
from erc20_worker import ERC20_Worker
from flashloan.cream import CREAMLending
from hellscream_const import BI_EXCHANGE_CONTRACT, ME, ME_PRIVATE
import json
from network.redis import redis_connection
from network.provider import random_local_provider
from web3.exceptions import BadFunctionCallOutput


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def dot_aligned(seq):
    snums = [str(n) for n in seq]
    dots = []
    for s in snums:
        p = s.find('.')
        if p == -1:
            p = len(s)
        dots.append(p)
    m = max(dots)
    return [' '*(m - d) + s for s, d in zip(snums, dots)]


class Executioner:

    NOT_ENOUGH_PROFIT = 0
    DIRECT_CAPITAL_TRADE = 1
    NO_CODE_PATH = 2
    FLASHLOAN = 3
    ACQUIRING_TRADE = 4

    def __init__(self):
        self.erc = ERC20_Worker()
        self.dm = DEXManager()

        self.compat_cap_sources = []
        self.compat_cap_sources.extend(self.erc.stablecoin_addresses)
        self.compat_cap_sources.extend(CREAMLending.token_fl_mapping().keys())

        self.packets = []
        self.r = redis_connection()

    def my_balance_of(self, address: str) -> int:
        return self.erc.balanceOf(address, wallet_address=BI_EXCHANGE_CONTRACT)

    def find_most_viable_routes(self, pkt):

        target_token = pkt['source_token']
        target_amount = pkt['optimizer_amount_in']

        # Available stablecoins
        available_capital = {}  # ERC_TOKEN_ADDR -> Amount

        # Stablecoin checking commented out for now, because execute_acquiring_trade finds "lowest" amount
        #
        #for stbl in self.erc.stablecoin_addresses:
        #    balance = self.my_balance_of(stbl)
        #    if balance > 0:
        #        available_capital[stbl] = balance

        # Available WBNB
        wbnb_balance = 2 * (1 * pow(10, 18))  # self.my_balance_of(self.erc.TOKEN_WBNB)
        if wbnb_balance > 0:
            available_capital[self.erc.TOKEN_WBNB] = wbnb_balance

        if len(available_capital.keys()) == 0:
            print('Acquiring Capital Trades: No available capital')
            return None

        # Find which DEX's have this token
        dexs_available = []
        for dex in self.dm.dex_list:
            cache = dex.cache()
            if target_token in cache.pair_token0_addr.values() or target_token in cache.pair_token1_addr.values():
                dexs_available.append(dex)

        if len(dexs_available) == 0:
            return None

        # Find all possible acquisition routes
        acquisition_routes = {}  # DEX -> {'path': [], 'starting_addr': '0x', 'starting_amt': 12.3}
        for dex in dexs_available:

            if dex.IDENTIFIER in [pkt['source_dex'], pkt['dest_dex']]:
                continue

            for stbl in available_capital.keys():
                try:
                    amount_stbl_in = dex.router_contract.functions.getAmountsIn(int(target_amount),
                                                                                [stbl, target_token]).call()
                except (BadFunctionCallOutput, OverflowError) as e:
                    continue

                if available_capital[stbl] >= amount_stbl_in[0]:
                    acquisition_routes[dex] = {'path': [stbl, target_token],
                                               'starting_addr': stbl,
                                               'trade_path_amounts': amount_stbl_in}
        if len(acquisition_routes.keys()) == 0:
            print('No Acquisition Routes')
            return None

        # Find the cheapest acquisition route
        def find_lowest_acq(acq_routes):
            lowest_dex = None
            lowest_path = None

            for dex, path_info in acq_routes.items():

                if lowest_dex is None:
                    lowest_dex = dex
                    lowest_path = path_info

                if path_info['trade_path_amounts'] < lowest_path['trade_path_amounts']:
                    lowest_dex = dex
                    lowest_path = path_info

            return lowest_dex, lowest_path
        acq_dex, acq_routes = find_lowest_acq(acquisition_routes)

        # Find an exit route
        exit_routes = {}  # DEX -> {'path': [], 'starting_addr': '0x', 'starting_amt': 12.3}
        for dex in dexs_available:

            if dex.IDENTIFIER in [pkt['source_dex'], pkt['dest_dex'], acq_dex.IDENTIFIER]:
                continue

            for stbl in available_capital.keys():
                try:
                    amount_stbl_out = dex.router_contract.functions.getAmountsOut(int(pkt['optimizer_amount_in']),
                                                                                [target_token, stbl]).call()
                except (BadFunctionCallOutput, OverflowError) as e:
                    continue

                exit_routes[dex] = {'path': [target_token, stbl],
                                    'starting_addr': stbl,
                                    'trade_path_amounts': amount_stbl_out}
        if len(exit_routes.keys()) == 0:
            print('No exit routes')
            return None

        # Find the exit route with the greatest return
        def find_highest_exit(ex_routes):
            highest_dex = None
            highest_path = None

            for dex, path_info in ex_routes.items():

                if highest_dex is None:
                    highest_dex = dex
                    highest_path = path_info

                if path_info['trade_path_amounts'] > highest_path['trade_path_amounts']:
                    highest_dex = dex
                    highest_path = path_info

            return highest_dex, highest_path
        exit_dex, exit_routes = find_highest_exit(exit_routes)

        return acq_dex, acq_routes, exit_dex, exit_routes

    def execute_direct_trade(self, pkt):
        w3 = random_local_provider()
        abi = json.load(open('sol_biexchange/build/contracts/BiExchange.json'))['abi']
        contract = w3.eth.contract(address=BI_EXCHANGE_CONTRACT, abi=abi)
        nonce = w3.eth.getTransactionCount(ME)

        amount = int(pkt['optimizer_amount_in'])

        tx = contract.functions.biExchangeArb(self.dm.dex_router_address(pkt['source_dex']),
                                              self.dm.dex_router_address(pkt['source_dex']),
                                              pkt['source_token'],
                                              pkt['dest_token'],
                                              pkt['dest_token'],
                                              pkt['source_token'],
                                              amount).buildTransaction({
            'chainId': 56, 'gas': 1000000, 'gasPrice': w3.toWei('10', 'gwei'), 'nonce': nonce
        })

        sign_tx = w3.eth.account.signTransaction(tx, private_key=ME_PRIVATE)
        res = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
        return res.hex()

    def publish_result(self, pkt):
        self.r.publish('hellscribe', json.dumps(pkt))

    def execute_acquiring_trade(self, pkt, viable_routes):
        w3 = random_local_provider()
        abi = json.load(open('sol_biexchange/build/contracts/BiExchange.json'))['abi']
        contract = w3.eth.contract(address=BI_EXCHANGE_CONTRACT, abi=abi)
        nonce = w3.eth.getTransactionCount(ME)

        amount = int(viable_routes[1]['trade_path_amounts'][0])

        src_dex = self.dm.get_dex_by_ident(pkt['source_dex'])
        dst_dex = self.dm.get_dex_by_ident(pkt['dest_dex'])

        tx = contract.functions.acqTrade(viable_routes[0].ROUTER_ADDRESS,
                                         src_dex.ROUTER_ADDRESS,
                                         dst_dex.ROUTER_ADDRESS,
                                         viable_routes[2].ROUTER_ADDRESS,
                                         pkt['source_token'],
                                         pkt['dest_token'],
                                         amount).buildTransaction({
            'chainId': 56, 'gas': 1000000, 'gasPrice': w3.toWei('10', 'gwei'), 'nonce': nonce
        })

        sign_tx = w3.eth.account.signTransaction(tx, private_key=ME_PRIVATE)
        res = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
        return res.hex()

    def process_work_packet(self, pkt):

        src_dex = self.dm.get_dex_by_ident(pkt['source_dex'])
        dst_dex = self.dm.get_dex_by_ident(pkt['dest_dex'])
        source_token = self.erc.get_token(pkt['source_token'])
        dest_token = self.erc.get_token(pkt['dest_token'])

        print()
        print(f'{src_dex} -> {dst_dex}')
        i = 0
        profit_percent = pkt['optimizer_profit_display'] / pkt['optimizer_amount_in_display'] * 100
        print('Token  :', source_token['name'], '->', dest_token['name'])
        for s in dot_aligned([pkt['optimizer_amount_in_display'], pkt['optimizer_profit_display'], profit_percent]):
            if i == 0:
                print('Opt Amt:', s)
                i += 1
            elif i == 1:
                print('Opt Pft:', s)
                i += 1
            elif i == 2:
                if profit_percent >= 10:
                    print('Prf pct', Bcolors.OKGREEN, s, Bcolors.ENDC)
                else:
                    print('Prf pct', Bcolors.WARNING, s, Bcolors.ENDC)

        if profit_percent < 5:
            pkt['EXECUTIONER_RESULT'] = Executioner.NOT_ENOUGH_PROFIT
            print(Bcolors.FAIL, '✕', Bcolors.ENDC, 'Not enough profit')
            self.publish_result(pkt)
            return

        # Types of trades:
        #   - Direct Capital       (self capital, have path_0 token)
        #   - Direct Capital Swap  (StableCoin -> path_0 token)
        #   - Flashloan            (Flashloan  -> Swap -> Repay Loan)

        # Is direct Capital possible?
        available_funds = self.my_balance_of(source_token['address'])

        if available_funds >= pkt['optimizer_amount_in']:
            print('DIRECT_CAPITAL:', Bcolors.OKGREEN, '✔', Bcolors.ENDC)
            transaction_id = self.execute_direct_trade(pkt)

            pkt['EXECUTIONER_RESULT'] = Executioner.DIRECT_CAPITAL_TRADE
            pkt['EXECUTIONER_DIRECT_CAPITAL_TRANS_ID'] = transaction_id
            pkt['EXECUTIONER_DIRECT_CAPITAL_AVAILABLE'] = available_funds
            self.publish_result(pkt)
            return
        else:
            print('DIRECT_CAPITAL:', Bcolors.FAIL, '✕', Bcolors.ENDC)

        # Is direct Capital Swap Possible
        viable_routes = self.find_most_viable_routes(pkt)
        if viable_routes is not None:
            print('ACQUIRING_TRADE:', Bcolors.OKGREEN, '✔', Bcolors.ENDC)

            from pprint import pprint
            pprint(pkt)
            pprint(viable_routes)

            transaction_id = self.execute_acquiring_trade(pkt, viable_routes)
            pkt['EXECUTIONER_RESULT'] = Executioner.ACQUIRING_TRADE
            pkt['EXECUTIONER_ACQUIRING_TRADE_TRANS_ID'] = transaction_id
            print(Bcolors.OKGREEN, 'ACQUIRING_TRADE SUCCESS', Bcolors.ENDC, transaction_id)
            ser_viable_routes = (viable_routes[0].IDENTIFIER,
                                 viable_routes[1],
                                 viable_routes[2].IDENTIFIER,
                                 viable_routes[3])

            pkt['viable_routes'] = ser_viable_routes
            self.publish_result(pkt)
            return
        else:
            print('ACQUIRING_TRADE:', Bcolors.FAIL, '✕', Bcolors.ENDC)

        # Can we flashloan?
        if source_token['address'] in CREAMLending.token_fl_mapping().keys():
            print('FLASHLOAN:', Bcolors.OKGREEN, '✔', Bcolors.ENDC)
            pkt['EXECUTIONER_RESULT'] = Executioner.FLASHLOAN
            self.publish_result(pkt)
            return

        pkt['EXECUTIONER_RESULT'] = Executioner.NO_CODE_PATH
        self.publish_result(pkt)


def main_loop():

    r = redis_connection()
    pub_sub = r.pubsub()
    pub_sub.subscribe('executioner')

    exec = Executioner()

    try:
        print('Executioner Ready.')
        while True:
            msg = pub_sub.get_message(timeout=5)
            if msg is None:
                continue
            else:
                # This is the initialization message
                if type(msg['data']) == int:
                    print(msg)
                else:
                    msg_dec = json.loads(msg['data'].decode('utf-8'))
                    exec.process_work_packet(msg_dec)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':

    main_loop()
