from dex.dexmanager import DEXManager


if __name__ == '__main__':

    dm = DEXManager()

    for dex in dm.dex_list:

        procs = []
        queues = []

        reserve = dex.reserve_manager()

        done = False
        while not done:
            pair = reserve.find_due_pair()

            if pair is None:
                done = True
                continue

            reserve.fetch_pair_data(pair[0])

            if reserve.quick_drain is False:
                done = True
