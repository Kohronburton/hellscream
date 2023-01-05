import json
from network.provider import random_local_provider
import os
from web3 import Web3

FLASH_LOAN_CONTRACT = '0x02x'

ME = os.environ.get('PUBLIC_KEY')
ME_PRIVATE = os.environ.get('PRIVATE_KEY')

w3 = random_local_provider()

abi = json.load(open('floan/build/contracts/FLoan.json'))['abi']
floan_contract = w3.eth.contract(address=FLASH_LOAN_CONTRACT, abi=abi)


amount = 10 * pow(10, 8)
nonce = w3.eth.getTransactionCount(ME)
tx = floan_contract.functions.doFlashloan('0x39x', amount).buildTransaction({
     'chainId': 56, 'gas': 1000000, 'gasPrice': w3.toWei('10', 'gwei'), 'nonce': nonce
})
sign_tx = w3.eth.account.signTransaction(tx, private_key=ME_PRIVATE)
res = w3.eth.sendRawTransaction(sign_tx.rawTransaction)
print(res)

# Example
# LINK: 2.719180234462059735
# Borrow: 1000
#    Fee: 0.3
