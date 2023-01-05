from dex.dexmanager import DEXManager
from erc20_worker import ERC20_Worker
from hellscream_const import *
import json
from network.provider import random_local_provider
from web3 import Web3


def drain_contract():

    w3 = random_local_provider()
    bi_exchange_abi = json.load(open('sol_biexchange/build/contracts/BiExchange.json'))['abi']
    erc20_abi = json.load(open('sol_biexchange/build/contracts/IERC20.json'))['abi']

    bi_ex_contract = w3.eth.contract(address=BI_EXCHANGE_CONTRACT, abi=bi_exchange_abi)

    tkns = [
        Web3.toChecksumAddress('0x55d398326f99059ff775485246999027b3197955'),  # Binance-Peg BSC-USD (BSC-USD)
        Web3.toChecksumAddress('0xe9e7cea3dedca5984780bafc599bd69add087d56'),  # Binance-Peg BUSD Token (BUSD)
        Web3.toChecksumAddress('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'),  # WBNB
    ]

    for tkn in tkns:

        tkn_contract = w3.eth.contract(address=tkn, abi=erc20_abi)

        balance = tkn_contract.functions.balanceOf(BI_EXCHANGE_CONTRACT).call()
        if balance > 0:
            nonce = w3.eth.getTransactionCount(ME)
            tx = bi_ex_contract.functions.drain(Web3.toChecksumAddress(tkn), ME).buildTransaction({
                 'chainId': 56, 'gas': 1000000, 'gasPrice': w3.toWei('10', 'gwei'), 'nonce': nonce
            })
            sign_tx = w3.eth.account.signTransaction(tx, private_key=ME_PRIVATE)
            res = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
            print(res.hex())
            w3.eth.waitForTransactionReceipt(res.hex(), timeout=10000)

    nonce = w3.eth.getTransactionCount(ME)
    tx = bi_ex_contract.functions.drainETH(ME).buildTransaction({
         'chainId': 56, 'gas': 1000000, 'gasPrice': w3.toWei('10', 'gwei'), 'nonce': nonce
    })
    sign_tx = w3.eth.account.signTransaction(tx, private_key=ME_PRIVATE)
    res = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
    print(res.hex())
    w3.eth.waitForTransactionReceipt(res.hex(), timeout=10000)


if __name__ == '__main__':
    drain_contract()
