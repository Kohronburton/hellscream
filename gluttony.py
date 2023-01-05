from dex.dexmanager import DEXManager
from erc20_worker import ERC20_Worker
import json
from multiprocessing import Process, Queue
from network.redis import redis_connection
import random
from scipy.optimize import minimize_scalar


class ProfitOptimizer:

    def __init__(self, s_dex, d_dex, s_token, d_token, starting_amount, verbose=False):
        self.s_dex = s_dex
        self.d_dex = d_dex
        self.s_token = s_token
        self.d_token = d_token
        self.starting_amount = starting_amount
        self.optimization_path = []
        self.verbose = verbose

    def get_profit(self, amount):

        if amount == 0:
            return 0

        amount_out = self.s_dex.router_contract.functions.getAmountsOut(int(amount), [self.s_token['address'],
                                                                                      self.d_token['address']]).call()

        amount_out_dest_dex = self.d_dex.router_contract.functions.getAmountsOut(amount_out[-1],
                                                                                 [self.d_token['address'],
                                                                                 self.s_token['address']]).call()
        profit = amount_out_dest_dex[-1] - amount

        self.optimization_path.append([amount, profit])

        if self.verbose:
            print('Amount In:', amount, 'Profit:', profit)

        # We have to return *negative 1* times profit because the optimization algorithm
        # in scipy is a minimizer, not a maximiser, and doesn't appear to be configurable
        # through a setting :/, nevermind, in the words of the wise Missy Elliott
        # I put my thing down, flip it and reverse it.
        return -1 * profit


def analytics(work_queue, thread_cnt):

    dm = DEXManager()
    erc = ERC20_Worker()
    tokens = erc.all_tokens()
    r = redis_connection()

    print(f'Thread {thread_cnt} entering main loop')

    while True:

        print(f'Thread {thread_cnt} queue length:', work_queue.qsize())

        pkt = work_queue.get()
        print(pkt)
        if pkt == 'DONE':
            return

        source_token = tokens[pkt['source_token']]
        dest_token = tokens[pkt['dest_token']]

        po = ProfitOptimizer(s_dex=dm.get_dex_by_ident(pkt['source_dex']),
                             d_dex=dm.get_dex_by_ident(pkt['dest_dex']),
                             s_token=source_token,
                             d_token=dest_token,
                             starting_amount=pkt['source_base'],
                             verbose=False)

        try:
            res = minimize_scalar(po.get_profit,
                                  method='bounded',
                                  bounds=[po.starting_amount * 0.00001, po.starting_amount * 100000])
        except OverflowError:
            print('Overflow Error, Python optimizer shit itself')
            continue

        pkt['optimizer_success'] = res.success
        pkt['optimizer_amount_in'] = res.x
        pkt['optimizer_profit'] = -1 * res.fun
        pkt['optimizer_amount_in_display'] = res.x / (1 * pow(10, source_token['decimal']))
        pkt['optimizer_profit_display'] = -1 * res.fun / (1 * pow(10, source_token['decimal']))

        if pkt['optimizer_success']:
            print('Optimizer Success:', pkt['optimizer_amount_in'], pkt['optimizer_profit'])
        else:
            print('Optimizer Ended:', pkt['optimizer_amount_in'], pkt['optimizer_profit'])

        r.publish('executioner', json.dumps(pkt))


def main_loop():

    procs = []
    queues = []

    cnt = 0
    for i in range(12):
        cnt += 1
        q = Queue()
        p = Process(target=analytics, args=(q, cnt))

        queues.append(q)
        procs.append(p)

        p.start()

    r = redis_connection()
    pub_sub = r.pubsub()
    pub_sub.subscribe('hellscream')

    try:
        while True:
            msg = pub_sub.get_message(timeout=5)
            if msg is None:
                continue
            else:
                # This is the initialization message
                if type(msg['data']) == int:
                    print(msg)
                else:
                    msg_dec = json.loads(msg['data'].decode('utf-8'))
                    q = random.choice(queues)
                    q.put(msg_dec)
    except KeyboardInterrupt:
        for q in queues:
            q.put('DONE')

        for p in procs:
            p.join()


if __name__ == '__main__':

    main_loop()
