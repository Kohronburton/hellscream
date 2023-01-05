from borgswap import BorgCache
from bscscan import BSCScanCache
from cheeseswap import CheeseCache
import matplotlib.pyplot as plt
import networkx as nx
from pancake import PancakeCache


class DeFiPairVis:

    def __init__(self):
        pass

    def draw_defi_pairs(self, dex_cache, output_filename):

        pairs = []
        keys = dex_cache.pair_token0_addr.keys()
        for k in keys:
            pairs.append([dex_cache.pair_token0_addr[k],
                          dex_cache.pair_token1_addr[k]])

        dg = nx.DiGraph()
        dg.add_edges_from(pairs)

        plt.figure(1, figsize=(24, 24))

        nx.draw(dg)
        pos = nx.fruchterman_reingold_layout(dg)

        nx.draw_networkx_nodes(dg, pos)
        plt.savefig(output_filename)


if __name__ == '__main__':

    defi_res = DeFiPairVis()

    print('Drawing Borg')
    borg_res = BorgCache()
    defi_res.draw_defi_pairs(dex_cache=borg_res,
                             output_filename='visualizations/borgswap.png')

    print('BSCScan Borg')
    bsc_cache = BSCScanCache()
    defi_res.draw_defi_pairs(dex_cache=bsc_cache,
                             output_filename='visualizations/bscscan.png')

    print('Drawing Cheese')
    cheese_cache = CheeseCache()
    defi_res.draw_defi_pairs(dex_cache=cheese_cache,
                             output_filename='visualizations/cheese.png')

    print('Drawing Pancake')
    pcake_res = PancakeCache()
    defi_res.draw_defi_pairs(dex_cache=pcake_res,
                             output_filename='visualizations/pancake.png')
