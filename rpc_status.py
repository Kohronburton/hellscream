from network.provider import random_local_provider
from pprint import pprint
import time

w3 = random_local_provider()

while True:

    if w3.eth.syncing == False:
        print(time.time(), ' Chain Synced')
    else:
        pprint(w3.eth.syncing)

    time.sleep(2)
