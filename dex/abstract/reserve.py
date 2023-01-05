from multiprocessing import Queue, Process
from network.provider import random_local_provider
from network.redis import redis_connection
from time import time, sleep


class Reserve:

    def __init__(self, w3_provider=None):
        if w3_provider is None:
            self.w3 = random_local_provider()
        else:
            self.w3 = w3_provider

        self.redis = redis_connection()

        self.cache = None  # BorgCache()
        self.swap = None  # BorgSwap(w3_provider=self.w3)
        self.prefix = ''  # 'BORG'

        self.quick_drain = False

        # Reserves are stored in redis like this:
        # {self.prefix}_RESERVE_UPDATED = {'<PAIR_ADDRESS>' : <1620957065 BLOCK_TIME>}
        # {self.prefix}_RESERVE_AMOUNTS = {'<PAIR_ADDRESS>' : <TOKEN_0_RESERVE>,<TOKEN_1_RESERVE>

    def get_reserves_for_pair(self, address):
        reserves = self.redis.hget(f'{self.prefix}_RESERVE_AMOUNTS', address)
        if reserves is None:
            return reserves
        else:
            updated = self.redis.hget(f'{self.prefix}_RESERVE_UPDATED', address)
            reserves = reserves.decode('utf-8').split(',')
            return [float(updated.decode('utf-8')), [float(reserves[0]), float(reserves[1])]]

    def get_reserves(self):
        reserves = {}
        for pair_address, reserve_str in self.redis.hgetall(f'{self.prefix}_RESERVE_AMOUNTS').items():
            pair_address = pair_address.decode('utf-8')
            reserve_str = reserve_str.decode('utf-8')

            reserves[pair_address] = [int(k) for k in reserve_str.split(',')]

        return reserves

    def find_due_pair(self, batch_size=1):
        reserve_updated = self.redis.hgetall(f'{self.prefix}_RESERVE_UPDATED')
        pair_addresses = set([k.decode('utf-8') for k in reserve_updated.keys()])
        all_known_pair_addr = self.cache.pair_addresses()
        not_done_addresses = all_known_pair_addr - pair_addresses

        if len(not_done_addresses) > 0:
            self.quick_drain = True
            print('%s_Reserve - Not done addresses:' % self.prefix, len(not_done_addresses), '/', len(all_known_pair_addr))
            if batch_size > 1:
                return list(not_done_addresses)[0:min(batch_size, len(not_done_addresses))]
            else:
                return [not_done_addresses.pop(), ]
        else:
            self.quick_drain = False

            reserve_times = sorted(reserve_updated.items(), key=lambda x: float(x[1]))

            now = time()

            if batch_size > 1:
                addresses = []
                for add_time in reserve_times[0:min(batch_size, len(reserve_times))]:
                    if now - float(add_time[1]) > 3600:
                        addresses.append(add_time[0].decode('utf-8'))

                return addresses
            else:
                if len(reserve_times) == 0:
                    return None
                else:
                    return [reserve_times[0][0].decode('utf-8')]

    def fetch_pair_data(self, pair_add_due, verbose=True):
        pair_contract = self.swap.pair_contract(pair_add_due)
        token0_reserve, token1_reserve, block_time = pair_contract.functions.getReserves().call()

        self.redis.hset(f'{self.prefix}_RESERVE_UPDATED',
                        pair_add_due,
                        str(time()))

        previous_reserves = self.redis.hget(f'{self.prefix}_RESERVE_AMOUNTS', pair_add_due)

        if previous_reserves is not None:
            previous_reserves = previous_reserves.decode('utf-8')

            token0_prev, token1_prev = previous_reserves.split(',')
            token0_curr, token1_curr = [str(token0_reserve), str(token1_reserve)]

            if token0_prev != token0_curr:
                delta = float(token0_curr) - float(token0_prev)
                if verbose:
                    print(f'{pair_add_due} Token0 Reserve change: {token0_prev} {token0_curr}, delta: {delta}')

            if token1_prev != token1_curr:
                delta = float(token1_curr) - float(token1_prev)
                if verbose:
                    print(f'{pair_add_due} Token1 Reserve change: {token1_prev} {token1_curr}, delta: {delta}')

        self.redis.hset(f'{self.prefix}_RESERVE_AMOUNTS',
                        pair_add_due,
                        '%s,%s' % (str(token0_reserve), str(token1_reserve)))

        if verbose:
            print(f'{pair_add_due} updated reserves', str(token0_reserve), str(token1_reserve))

    def worker(self):
        while True:
            pair_add_due = self.find_due_pair()

            self.fetch_pair_data(pair_add_due)

            if not self.quick_drain:
                sleep(6)
