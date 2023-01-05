from dex.dexmanager import DEXManager
import redis
from multiprocessing import Process, Queue
from network.redis import redis_connection
import random
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput


def work(dex_ident, queue):

    dm = DEXManager()

    dex = dm.get_dex_by_ident(dex_ident)
    if dex is None:
        print(f'Unable to get DEX by ident: {dex_ident}')
        return

    dex_cache = dex.cache()

    red = redis_connection()

    while True:
        res = queue.get()

        if res in ['DONE', None]:
            return

        try:
            get_pair(res, dex, red, dex_cache.REDIS_PREFIX)
        except (ValueError, OverflowError, BadFunctionCallOutput) as e:
            print('Exception:', str(e))
            red.sadd(f'{dex_cache.REDIS_PREFIX}_ADDR_BLACKLIST', res)


def get_pair(pair_index: int, dex, red, redis_prefix):

    pair_address = Web3.toChecksumAddress(dex.factory_contract.functions.allPairs(pair_index).call())
    pair = dex.pair_contract(pair_address)

    try:
        pair_name = pair.functions.name().call()
    except BadFunctionCallOutput:
        pair_name = f'{redis_prefix} pair {pair_index}'

    try:
        pair_symbol = pair.functions.symbol().call()
    except BadFunctionCallOutput:
        pair_symbol = f'{redis_prefix}_pair_{pair_index}'

    token0_address = Web3.toChecksumAddress(pair.functions.token0().call())
    token1_address = Web3.toChecksumAddress(pair.functions.token1().call())

    token0_contract = dex.erc20_contract(token0_address)
    token1_contract = dex.erc20_contract(token1_address)

    token0_name = token0_contract.functions.name().call()
    token1_name = token1_contract.functions.name().call()

    print('Index:', '{0: <10}'.format(pair_index),
          'Pair:', '{0: <15}'.format(pair_name),
          'Symbol:', '{0: <15}'.format(pair_symbol),
          'Token0:', '{0: <25}'.format(token0_name),
          'Token1:', '{0: <25}'.format(token1_name))

    red.hset(f'{redis_prefix}_IDX_ADDR', key=pair_index, value=pair_address)
    red.hset(f'{redis_prefix}_IDX_NAME', key=pair_index, value=pair_name)
    red.hset(f'{redis_prefix}_IDX_SYMBOL', key=pair_index, value=pair_symbol)
    red.hset(f'{redis_prefix}_IDX_TOKEN0_ADDR', key=pair_index, value=token0_address)
    red.hset(f'{redis_prefix}_IDX_TOKEN0_NAME', key=pair_index, value=token0_name)
    red.hset(f'{redis_prefix}_IDX_TOKEN1_ADDR', key=pair_index, value=token1_address)
    red.hset(f'{redis_prefix}_IDX_TOKEN1_NAME', key=pair_index, value=token1_name)


def fetch_dex_pairs(dex):
    red = redis_connection()

    num_threads = 32
    work_queues = []
    procs = []

    for i in range(num_threads):

        q = Queue()
        p = Process(target=work, args=(dex.IDENTIFIER, q))

        work_queues.append(q)
        procs.append(p)

    # What do we still need to fetch?

    dex_pair_cache = dex.cache()

    all_pairs_length = dex.all_pairs_length()
    cached_indicies = dex_pair_cache.all_indicies()
    for i in range(all_pairs_length):
        if i in cached_indicies:
            print(dex.IDENTIFIER, 'Already have index', i)
        else:
            if red.sismember(f'{dex_pair_cache.REDIS_PREFIX}_ADDR_BLACKLIST', i):
                print(dex.IDENTIFIER, 'Ignoring Blacklisted', i)
            else:
                print(dex.IDENTIFIER, 'Need to fetch index', i)
                q = random.choice(work_queues)
                q.put(i)

    for q in work_queues:
        q.put('DONE')

    for p in procs:
        p.start()

    for p in procs:
        p.join()


if __name__ == '__main__':

    dm = DEXManager()

    for dex in dm.dex_list:
        fetch_dex_pairs(dex)
