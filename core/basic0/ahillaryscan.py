import requests
import time


def get_txs(account_address: str, offset: int, limit: int = 100, direction: str = 'older'):
    params = {
        'limit': limit,
        'direction': direction,
        'accountAddress': account_address,
        'offset': offset
    }
    ch = 0
    while ch<2:
        try:
            dad = requests.get('https://zksync2-mainnet-explorer.zksync.io/transactions', params=params)
            return dad.json()
        except:
            ch = ch + 1
            time.sleep(30)
    raise Exception('l0 ahillaryscan error')