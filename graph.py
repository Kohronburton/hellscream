from decimal import Decimal
from erc20_worker import ERC20_Worker


d997 = Decimal(997)
d1000 = Decimal(1000)


def getAmountOut(amountIn, reserveIn, reserveOut):
    amountInWithFee = Decimal(amountIn) * Decimal(997)
    numerator = amountInWithFee * reserveOut
    demominator = (reserveIn * Decimal(1000) + amountInWithFee)
    amountOut = numerator / demominator
    return float(amountOut)


def toInt(n):
    return Decimal(int(n))


def getEaEb(tokenIn, pairs):
    Ea = None
    Eb = None
    idx = 0
    tokenOut = tokenIn.copy()
    for pair in pairs:
        if idx == 0:
            if tokenIn['address'] == pair['tokenA']['address']:
                tokenOut = pair['tokenB']
            else:
                tokenOut = pair['tokenA']
        if idx == 1:
            Ra = pairs[0]['reserveA']
            Rb = pairs[0]['reserveB']
            if tokenIn['address'] == pairs[0]['tokenB']['address']:
                temp = Ra
                Ra = Rb
                Rb = temp
            Rb1 = pair['reserveA']
            Rc = pair['reserveB']
            if tokenOut['address'] == pair['tokenB']['address']:
                temp = Rb1
                Rb1 = Rc
                Rc = temp
                tokenOut = pair['tokenA']
            else:
                tokenOut = pair['tokenB']
            Ea = toInt(d1000*Ra*Rb1/(d1000*Rb1+d997*Rb))
            Eb = toInt(d997*Rb*Rc/(d1000*Rb1+d997*Rb))
        if idx > 1:
            Ra = Ea
            Rb = Eb
            Rb1 = pair['reserveA']
            Rc = pair['reserveB']
            if tokenOut['address'] == pair['tokenB']['address']:
                temp = Rb1
                Rb1 = Rc
                Rc = temp
                tokenOut = pair['tokenA']
            else:
                tokenOut = pair['tokenB']
            Ea = toInt(d1000*Ra*Rb1/(d1000*Rb1+d997*Rb))
            Eb = toInt(d997*Rb*Rc/(d1000*Rb1+d997*Rb))
        idx += 1
    return Ea, Eb


def sortTrades(trades, newTrade):
    trades.append(newTrade)
    return sorted(trades, key = lambda x: x['profit'])


def findTrades(pairs, tokenIn, tokenOut, amountIn, maxHops, currentPairs, path, bestTrades, count=4):
    for i in range(len(pairs)):
        newPath = path.copy()
        pair = pairs[i]
        if not pair['tokenA']['address'] == tokenIn['address'] and not pair['tokenB']['address'] == tokenIn['address']:
            continue
        if pair['reserveA'] / pow(10, pair['tokenA']['decimal']) < 1 or pair['reserveB']/pow(10, pair['tokenB']['decimal']) < 1:
            continue
        if tokenIn['address'] == pair['tokenA']['address']:
            tempOut = pair['tokenB']
        else:
            tempOut = pair['tokenA']
        newPath.append(tempOut)
        if tempOut['address'] == tokenOut['address'] and len(path) > 2:
            # get virtual reserves through path           
            Ea, Eb = getEaEb(tokenOut, currentPairs + [pair])
            newTrade = {'route': currentPairs + [pair], 'path': newPath, 'Ea': Ea, 'Eb': Eb}
            if Ea and Eb and Ea < Eb:
                ## add amount optimization here
                newTrade['amountOut'] = getAmountOut(amountIn, Ea, Eb)
                newTrade['profit'] = newTrade['amountOut'] - amountIn
                newTrade['p'] = int(newTrade['profit'])/pow(10, tokenOut['decimal'])
                bestTrades = sortTrades(bestTrades, newTrade)
                bestTrades.reverse()
                bestTrades = bestTrades[:count]
        elif maxHops > 1 and len(pairs) > 1:
            pairsExcludingThisPair = pairs[:i] + pairs[i+1:]
            bestTrades = findTrades(pairsExcludingThisPair, tempOut, tokenOut, amountIn, maxHops-1, currentPairs + [pair], newPath, bestTrades, count)
    return bestTrades


def update_reserves(pair_list, dex):

    manager = dex.reserve_manager()
    reserves = manager.get_reserves()
    for pair in pair_list:
        try:
            pair['reserveA'] = reserves[pair['address']][0]
            pair['reserveB'] = reserves[pair['address']][1]
        except KeyError as e:
            print('Warning, KeyError on update_reserves', str(e))


def build_pair_list(dex, limit=None, start=0):
    pairs = {}
    cache = dex.cache()

    erc20 = ERC20_Worker()
    tokens = erc20.all_tokens()

    for idx, pair_address in cache.pair_idx_addr.items():

        token0_addr = cache.pair_token0_addr[idx]
        token1_addr = cache.pair_token1_addr[idx]

        try:
            pair = {
                'address': pair_address,
                'tokenA': tokens[token0_addr],
                'tokenB': tokens[token1_addr],
                'reserveA': 0,
                'reserveB': 0
            }
            pairs[pair_address] = pair
        except KeyError:
            continue

    pairs_list = []
    for pair in pairs:
        pairs_list.append(pairs[pair])

    if limit is not None:
        return pairs_list[start: start + limit]
    else:
        return pairs_list
