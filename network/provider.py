from web3 import Web3
import time

# Peer List: https://gist.github.com/rfikki
# https://docs.binance.org/smart-chain/developer/fullnode.html


L_PROVIDER1 = 'http://127.0.0.1:8745'


def random_local_provider():
    w3_1 = Web3(Web3.HTTPProvider(L_PROVIDER1))

    return w3_1


def remote_provider():
    return Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))


if __name__ == '__main__':

    w3_1 = Web3(Web3.HTTPProvider(L_PROVIDER1))
    while True:
        print(w3_1.eth.syncing)
        time.sleep(1)
