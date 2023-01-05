Hellscream : A DeFi crypto trading bot experiment
====

Note: I wrote this for myself, and it was profitable between 2020 - 2021, at the end of 2021 profitability slowly dropped as others did this too.

Components:
```
dexhunter:
    Automatically discover distributed exchanges by scanning the blockchain mempool and then checking each address for ABI compatibility.

hellscream:
    Search Currency Pairs and put into worker queue

gluttony:
    - Pull from hellscream queue
    - Optimize the amount using an optimization algorithm
      - Optimization selection pressure:
        - Too low - Left money on the table
        - Too high - Slippage
    - Push profitable trades to executioner queue
    
executioner:
    - Make sure amount is still viable (i.e. enough liquidity)
    - Estimate GAS and compute final profitability
    - Execute the trade
    
hellscribe:
    Write everything to the database for analysis
