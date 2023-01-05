from dex.dexmanager import DEXManager
import json
import os
import requests
import time


def writeout_code(dex_name, api_result):

    dex_code_dir = f'st_analysis/dex_code/{dex_name}'

    if not os.path.exists(dex_code_dir):
        os.mkdir(dex_code_dir)

    source_filename = f'{dex_name}.sol'
    abi_filename = f'{dex_name}.abi'

    with open(f'{dex_code_dir}/{source_filename}', 'w') as f:
        f.write(api_result['SourceCode'])

    with open(f'{dex_code_dir}/{abi_filename}', 'w') as f:
        f.write(api_result['ABI'])


def go():
    dm = DEXManager()

    for dex in dm.dex_list:

        API_URL = 'https://api.bscscan.com/api?module=contract&action=getsourcecode&address=XXX' \
                  '&apikey=X'.replace('XXX', dex.ROUTER_ADDRESS)

        print(API_URL)
        r = requests.get(API_URL)
        api_resp = json.loads(r.text)
        source = api_resp['result'][0]

        writeout_code(str(dex), source)
        time.sleep(10)


if __name__ == '__main__':
    go()
