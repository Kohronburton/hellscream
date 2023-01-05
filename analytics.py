from erc20_worker import ERC20_Worker
from network.redis import redis_connection
from redis import Redis


def starting_tokens():
    tokens = {
        '0x2170Ed0880ac9A755fd29B2688956BD959F933F8': 'Ethereum Token',
        '0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE': 'XRP Token',
        '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402': 'Polkadot Token',
        '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3': 'Dai Token',
        '0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD': 'ChainLink Token',
        '0x4B0F1812e5Df2A09796481Ff14017e6005508003': 'Trust Wallet',
        '0x4338665CBB7B2485A8855A139b75D5e34AB0DB94': 'Litecoin Token',
        '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82': 'PancakeSwap Token',
        '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c': 'Wrapped BNB',
        '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56': 'BUSD Token',
        '0x55d398326f99059fF775485246999027B3197955': 'Tether USD',
        '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c': 'BTCB Token'
    }

    return tokens


def find_common_tokens():

    redis = redis_connection()

    pcake_set = set()
    for k in ['PCAKE_IDX_TOKEN1_ADDR', 'PCAKE_IDX_TOKEN0_ADDR']:
        for index, token_address in redis.hgetall(k).items():
            token_address = token_address.decode('utf-8')
            pcake_set.add(token_address)

    borg_set = set()
    for k in ['BORG_IDX_TOKEN1_ADDR', 'BORG_IDX_TOKEN0_ADDR']:
        for index, token_address in redis.hgetall(k).items():
            token_address = token_address.decode('utf-8')
            borg_set.add(token_address)

    bsc_set = set()
    for k in ['BSCSCAN_IDX_TOKEN1_ADDR', 'BSCSCAN_IDX_TOKEN0_ADDR']:
        for index, token_address in redis.hgetall(k).items():
            token_address = token_address.decode('utf-8')
            bsc_set.add(token_address)

    cheese_set = set()
    for k in ['CHEESE_IDX_TOKEN1_ADDR', 'CHEESE_IDX_TOKEN0_ADDR']:
        for index, token_address in redis.hgetall(k).items():
            token_address = token_address.decode('utf-8')
            cheese_set.add(token_address)

    tokens_on_all_dexes = pcake_set.intersection(borg_set).intersection(bsc_set).intersection(cheese_set)
    worker = ERC20_Worker()
    for t in tokens_on_all_dexes:
        token = worker.get_token(t)
        print(token['address'], token['name'])


def cli():
    e = ERC20_Worker()
    tokens = e.all_tokens()
    for address, token in tokens.items():
        if '.finance' in token['name']:
            print(address, token['name'])


if __name__ == '__main__':
    cli()
