from network.redis import redis_connection


class PairCache:

    def __init__(self):
        self.r = redis_connection()

        self.pair_idx_addr = {}
        self.pair_idx_name = {}
        self.pair_idx_symbol = {}

        self.pair_token0_addr = {}
        self.pair_token0_name = {}
        self.pair_token1_addr = {}
        self.pair_token1_name = {}

        self.pair_tokens = []

        self.refresh_all()

    def _load_dict(self, redis_keyname):
        res = {}
        for k, v in self.r.hgetall(redis_keyname).items():
            res[int(k)] = v.decode('utf-8')
        return res

    def find_index_for_pair(self, tokenA, tokenB):
        for idx in self.pair_token0_addr.keys():

            if self.pair_token0_addr[idx] == tokenA and self.pair_token1_addr[idx] == tokenB:
                return idx

            if self.pair_token1_addr[idx] == tokenA and self.pair_token0_addr[idx] == tokenB:
                return idx

    def addr_for_index(self, index: int) -> str:
        addr = self.r.hget(f'{self.REDIS_PREFIX}_IDX_ADDR', index)
        return addr.decode('utf-8') if addr is not None else None

    def refresh_all(self):
        self.pair_idx_addr = self._load_dict(f'{self.REDIS_PREFIX}_IDX_ADDR')
        self.pair_idx_name = self._load_dict(f'{self.REDIS_PREFIX}_IDX_NAME')
        self.pair_idx_symbol = self._load_dict(f'{self.REDIS_PREFIX}_IDX_SYMBOL')
        self.pair_token0_addr = self._load_dict(f'{self.REDIS_PREFIX}_IDX_TOKEN0_ADDR')
        self.pair_token0_name = self._load_dict(f'{self.REDIS_PREFIX}_IDX_TOKEN0_NAME')
        self.pair_token1_addr = self._load_dict(f'{self.REDIS_PREFIX}_IDX_TOKEN1_ADDR')
        self.pair_token1_name = self._load_dict(f'{self.REDIS_PREFIX}_IDX_TOKEN1_NAME')

        for idx in self.pair_idx_name.keys():
            pair_address_1 = self.pair_token0_addr[idx]
            pair_address_2 = self.pair_token1_addr[idx]

            self.pair_tokens.append({pair_address_1, pair_address_2})

    def all_indicies(self) -> set:
        return set(self.pair_idx_addr.keys())

    def pair_addresses(self) -> set:
        return set(self.pair_idx_addr.values())

    def all_tradable_tokens(self) -> set:
        return set(list(self.pair_token0_addr.values()) + list(self.pair_token1_addr.values()))
