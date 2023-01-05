from dex.dexmanager import DEXManager

dm = DEXManager()

for dex in dm.dex_list:

    print(dex, dex.ROUTER_ADDRESS)
    cache = dex.cache()

    print('Num pairs:', len(cache.pair_tokens))
    print()
