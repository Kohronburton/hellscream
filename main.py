from erc20_worker import ERC20_Worker
from graph import build_pair_list, update_reserves, findTrades
from network.provider import random_local_provider
import os
import time
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput


PUBLIC = os.environ.get('PUBLIC_KEY')
PRIVATE = os.environ.get('PRIVATE_KEY')


def validate_path_reserves(pairs, path, verbose=True):

    got_reserves = True

    for i in range(len(path) - 1):
        token0_addr = path[i]['address']
        token0_name = path[i]['name']
        token1_addr = path[i + 1]['address']
        token1_name = path[i + 1]['name']

        # Now find the pair contract so we can find it's reserves
        reserves = None
        for p in pairs:
            if p['tokenA']['address'] == token0_addr and p['tokenB']['address'] == token1_addr:
                reserves = (p['reserveA'], p['reserveB'])

        if reserves is not None:
            if verbose:
                print('Pair %s' % str(i))
                print('\t%s..%s' % (token0_addr[0:5], token0_addr[-3:]),
                      token0_name.ljust(40),
                      str(reserves[0]).rjust(20))

                print('\t%s..%s' % (token1_addr[0:5], token1_addr[-3:]),
                      token1_name.ljust(40),
                      str(reserves[1]).rjust(20))
        else:
            got_reserves = False

            if verbose:
                print('Pair %s' % str(i))
                print('\t%s..%s' % (token0_addr[0:5], token0_addr[-3:]),
                      token0_name.ljust(40),
                      'NO RESERVES'.rjust(20))

                print('\t%s..%s' % (token1_addr[0:5], token1_addr[-3:]),
                      token1_name.ljust(40),
                      'NO RESERVES'.rjust(20))

    return got_reserves


def approve(tokenAddress, contractAddress, myAddress, amount):
    w3 = random_local_provider()
    erc20 = ERC20_Worker()

    bep20Token = w3.eth.contract(address=tokenAddress, abi=erc20.erc20abi)
    approved_amount = bep20Token.functions.allowance(myAddress, contractAddress).call()
    if approved_amount >= amount:
        return True
    try:
        tx = bep20Token.functions.approve(contractAddress, 2**256-1).buildTransaction({
            'from': myAddress,
            'value': 0,
            'gasPrice': int(20e9),
            'gas': 1500000,
            "nonce": w3.eth.getTransactionCount(myAddress),
            })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE)
        txhash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print('approving... ', txhash.hex())
        w3.eth.waitForTransactionReceipt(txhash.hex(), timeout=10000)
    except Exception as e:
        print('exception:', e)
        return False
    return True


def main2(pairs, dex, in_token):
    update_reserves(pairs, dex)

    current_pairs = []
    best_trades = []
    amount_in = 200 * pow(10, in_token['decimal'])

    trades = findTrades(pairs,
                        tokenIn=in_token,
                        tokenOut=in_token,
                        amountIn=amount_in,
                        maxHops=5,
                        currentPairs=current_pairs,
                        path=[in_token, ],
                        bestTrades=best_trades,
                        count=2)

    w3 = random_local_provider()

    for trade in trades:
        profit = trade['profit'] / pow(10, in_token['decimal'])

        if profit > 0:
            addr_path = [Web3.toChecksumAddress(x['address']) for x in trade['path']]
            print(addr_path, profit)

            try:
                amount_out_path = dex.router_contract.functions.getAmountsOut(amount_in, addr_path).call()
            except (BadFunctionCallOutput, OverflowError) as e:
                print('Exception computing profit on path', str(e))
                continue

            # Make sure there's sufficient output amount directly from the dex query
            if amount_out_path[-1] < amount_in:
                print('Insufficient Output Amount')
                continue

            '''
            UNCOMMENT THIS CODE TO ACTUALLY EXECUTE TRADES
            '''
            approve(addr_path[0], dex.ROUTER_ADDRESS, Web3.toChecksumAddress(PUBLIC), amount_in)

            tx = dex.router_contract.functions.swapExactTokensForTokens(amount_in,
                                                                   amount_in,
                                                                   addr_path,
                                                                   Web3.toChecksumAddress(PUBLIC),
                                                                   int(time.time() + 2000)).buildTransaction({
                'from': Web3.toChecksumAddress(PUBLIC),
                'value': 0,
                'gasPrice': int(10e9),
                'gas': 1500000,
                'nonce': w3.eth.getTransactionCount(Web3.toChecksumAddress(PUBLIC))
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE)
            try:
                txhash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
                print(txhash.hex())
            except:
                return None

            print('====================================')
            print('Maximum Profit: %f' % profit)
            print('\t', [x['name'] for x in trade['path']])
            print('\t', addr_path)
            print('\n')
            print(amount_in / pow(10, in_token['decimal']),
                  '->',
                  str(float(amount_out_pancake[-1] / pow(10, in_token['decimal']))))
            print('====================================')


if __name__ == '__main__':

    from dex.dexmanager import DEXManager

    dm = DEXManager()

    for dex in dm.dex_list:
        if dex.IDENTIFIER != 'MX':
            continue

        p = dex
        print(p)
        pairs = build_pair_list(p, limit=25000)
        '''
        print_most_common_tokens(pairs)
    
        21429 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c Wrapped BNB
        1719  0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56 BUSD Token
        404   0x55d398326f99059fF775485246999027B3197955 Tether USD
        214   0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82 PancakeSwap Token
        100   0x2170Ed0880ac9A755fd29B2688956BD959F933F8 Ethereum Token
        69    0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c BTCB Token
        44    0x547CBE0f0c25085e7015Aa6939b28402EB0CcDAC Elastic BNB
        43    0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402 Polkadot Token
        41    0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d USD Coin
        39    0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3 Dai Token
    
        '''
        erc20_manager = ERC20_Worker()

        '''
        for tk in ['0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
                   '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56',
                   '0x55d398326f99059fF775485246999027B3197955',
                   '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82',
                   '0x2170Ed0880ac9A755fd29B2688956BD959F933F8',
                   '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c',
                   '0x547CBE0f0c25085e7015Aa6939b28402EB0CcDAC',
                   '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402',
                   '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d',
                   '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3']:
        '''
        tk = Web3.toChecksumAddress('0x55d398326f99059ff775485246999027b3197955')
        token = erc20_manager.get_token(tk)
        print('|')
        print('+---', '%s..%s' % (tk[:5], tk[-3:]), '-', token['name'])
        main2(pairs, p, token)
