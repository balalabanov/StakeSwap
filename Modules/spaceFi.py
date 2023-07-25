import random
import random
from web3 import Web3
import requests
import time
import json
def crypto_to_usd(asset = 'ETH'):
    toDo = 0
    while toDo < 3:
        try:
            url = f'https://min-api.cryptocompare.com/data/price?fsym={asset}&tsyms=USDT'
            response = requests.get(url)
            result = [response.json()]
            price = result[0]['USDT']
            return float(price)
        except:
            time.sleep(5)
            toDo = toDo + 1
    # print("\033[31m{}".format('Core -> Instruments -> Balance -> crypto_to_usd(asset) ERROR'))
    # print("\033[0m{}".format(' '))
    # return 'ERROR'
    raise Exception('Getiing Market Data Error')

def usd_to_zk_gas(usd=0.3):
    eth_price = crypto_to_usd('ETH')
    return int(Web3.to_wei(usd/eth_price,'ether')/250000000)

def check_token_balance(address, rpc='https://mainnet.era.zksync.io', token_address='0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4', ABI = None):
    toDo = 0
    while toDo<3:
        try:
            if ABI == None:

                with open('data/erc20.json') as jsonabi:
                    ABI = json.load(jsonabi)
                # ABI = approve_abi
                    # print(ABI)

            if True:
                web3 = Web3(Web3.HTTPProvider(rpc))
                token = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=ABI)
                token_balance = token.functions.balanceOf(web3.to_checksum_address(address)).call()
                return token_balance

        except:
            time.sleep(5)
            toDo = toDo + 1
    raise Exception('ERC20 Token Balance Error')

def check_tx_sucs(tx,rpc="https://mainnet.era.zksync.io"):
    time.sleep(10)
    toDo = 0
    while toDo<3:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc))
            txn = w3.eth.get_transaction_receipt(tx)
            status = txn['status']
            if status == 1:
                return True
            else:
                return False
        except:
            time.sleep(3)
            toDo = toDo + 1
    # print("\033[31m{}".format('Core -> Utils -> Tx -> check_tx_sucs(tx,rpc) ERROR'))
    # print("\033[37m{}".format(' '))
    raise Exception('Checking tx sucs Error')
def eth_usd(acc,function_out,volume_in_usd,gas=0.4):
    # abi = 'Swap Exact E T H For Tokens (Uint256, Address[], Address, Uint256)'
    try:
        with open('data/allAbi.json') as file:
            abi = json.load(file)
    except:
        function_out('\nCan not open abi for spaceFi eth_usd')
        return False

    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    # nonce = w3.eth.get_transaction_count(acc.address)
    value = Web3.to_wei(volume_in_usd/crypto_to_usd(),'ether')
    contract = w3.eth.contract(Web3.to_checksum_address('0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d'), abi=abi)
    # print(contract.decode_function_input('0x7ff36ab500000000000000000000000000000000000000000000000000000000001d1b640000000000000000000000000000000000000000000000000000000000000080000000000000000000000000e7a1d4e573bb648bcc63bccdd3ebb1828f4003e600000000000000000000000000000000000000000000000000000000649f992700000000000000000000000000000000000000000000000000000000000000020000000000000000000000005aea5775959fbc2557cc8789bc1bf90a239d9a910000000000000000000000003355df6d4c9c3035724fd0e3914de96a5a83aaf4'))
    args = [int(volume_in_usd * 0.95 * 10 ** 6),
            [Web3.to_checksum_address('0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91'),
             Web3.to_checksum_address('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4')], Web3.to_checksum_address(acc.address),
            int(time.time() + 60 * 20)]

    txn = contract.functions.swapExactETHForTokens(*args)

    builded_txn = txn.build_transaction({
        'chainId': 324,
        'from': Web3.to_checksum_address(acc.address),
        'value': value,
        'gas': usd_to_zk_gas(gas),
        'nonce': w3.eth.get_transaction_count(acc.address),
        'maxFeePerGas': 250000000,
        'maxPriorityFeePerGas': 250000000
    })

    signed_approve = w3.eth.account.sign_transaction(builded_txn, acc.key)
    txn_hash_approve = w3.eth.send_raw_transaction(signed_approve.rawTransaction)
    txn_approve_text = txn_hash_approve.hex()
    print(txn_approve_text)
    try:
        suc =  check_tx_sucs(txn_approve_text)
        if suc:
            return True
        else:
            function_out('\nError while swapping spaceFi eth_usd')
            return False
    except:
        return False


def usd_eth(acc, function_out, volume_in_usd, gas=0.4):
    volume_in_usd = (check_token_balance(acc.address)- random.randint(1, 20)) / (10 ** 6)
    # abi = 'Swap Exact E T H For Tokens (Uint256, Address[], Address, Uint256)'
    try:
        with open('data/allAbi.json') as file:
            abi = json.load(file)
    except:
        function_out('\nCan not open abi for spaceFi usd_eth')
        return False

    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    # nonce = w3.eth.get_transaction_count(acc.address)
    # value = Web3.to_wei(volume_in_usd / crypto_to_usd(), 'ether')
    contract = w3.eth.contract(Web3.to_checksum_address('0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d'), abi=abi)

    args = [int(volume_in_usd *  (10 ** 6)),Web3.to_wei(0.95*(volume_in_usd/crypto_to_usd()),'ether'),
            [Web3.to_checksum_address('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4'),
             Web3.to_checksum_address('0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91')], Web3.to_checksum_address(acc.address),
            int(time.time() + 60 * 20)]

    txn = contract.functions.swapExactTokensForETH(*args)

    builded_txn = txn.build_transaction({
        'chainId': 324,
        'from': Web3.to_checksum_address(acc.address),
        'value': Web3.to_wei(0,'ether'),
        'gas': usd_to_zk_gas(gas),
        'nonce': w3.eth.get_transaction_count(acc.address),
        'maxFeePerGas': 250000000,
        'maxPriorityFeePerGas': 250000000
    })

    signed_approve = w3.eth.account.sign_transaction(builded_txn, acc.key)
    txn_hash_approve = w3.eth.send_raw_transaction(signed_approve.rawTransaction)
    txn_approve_text = txn_hash_approve.hex()

    try:
        suc = check_tx_sucs(txn_approve_text)
        if suc:
            return True
        else:
            function_out('\nError while swapping spaceFi usd_eth')
            return False
    except:
        return False

def approve(acc,function_out,gas=0.3):
    try:
        with open('data/allAbi.json') as file:
            abi = json.load(file)
    except:
        function_out('\nCan not open abi for spaceFi approve')
        return False

    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    # nonce = w3.eth.get_transaction_count(acc.address)
    # value = Web3.to_wei(volume_in_usd / crypto_to_usd(), 'ether')
    contract = w3.eth.contract(Web3.to_checksum_address('0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4'), abi=abi)

    args = [Web3.to_checksum_address('0xbE7D1FD1f6748bbDefC4fbaCafBb11C6Fc506d1d'),2**256-1]
    txn = contract.functions.approve(*args)

    builded_txn = txn.build_transaction({
        'chainId': 324,
        'from': Web3.to_checksum_address(acc.address),
        'value': Web3.to_wei(0,'ether'),
        'gas': usd_to_zk_gas(gas),
        'nonce': w3.eth.get_transaction_count(acc.address),
        'maxFeePerGas': 250000000,
        'maxPriorityFeePerGas': 250000000
    })

    signed_approve = w3.eth.account.sign_transaction(builded_txn, acc.key)
    txn_hash_approve = w3.eth.send_raw_transaction(signed_approve.rawTransaction)
    txn_approve_text = txn_hash_approve.hex()

    try:
        suc = check_tx_sucs(txn_approve_text)
        if suc:
            time.sleep(71)
            return True
        else:
            function_out('\nError while approving spaceFi usdc')
            return False
    except:
        return False