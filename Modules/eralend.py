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


def perform(acc,function_out,volume_in_usd,return_percent,gas=0.5):
    try:
        with open('data/allAbi.json') as file:
            abi = json.load(file)
    except:
        function_out('\nCan not open abi for eralend perform')
        return False


    w3 = Web3(Web3.HTTPProvider('https://mainnet.era.zksync.io'))
    # nonce = w3.eth.get_transaction_count(acc.address)
    value = Web3.to_wei(volume_in_usd/crypto_to_usd(),'ether')
    contract = w3.eth.contract(Web3.to_checksum_address('0x1BbD33384869b30A323e15868Ce46013C82B86FB'), abi=abi)

    txn = contract.functions.mint()

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
            time.sleep(30)
            # return True
        else:
            function_out('\nError while staking eth eralend perform')
            return False
    except:
        function_out('\nError while staking eth eralend deep error(check tx sucs)')
        return False

    if return_percent == 0:
        return suc


    contract = w3.eth.contract(Web3.to_checksum_address('0x0171cA5b372eb510245F5FA214F5582911934b3D'),abi=abi)
    txn = contract.functions.enterMarkets([Web3.to_checksum_address('0x1BbD33384869b30A323e15868Ce46013C82B86FB')])

    builded_txn = txn.build_transaction({
        'chainId': 324,
        'from': Web3.to_checksum_address(acc.address),
        'value': Web3.to_wei(0,'ether'),
        'gas': usd_to_zk_gas(gas*1.5),
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
            time.sleep(60)
            # return True
        else:
            function_out('\nError while entering markets eth eralend perform')
            return False
    except:
        function_out('\nError while entering markets eth eralend deep error(check tx sucs)')
        return False

    contract = w3.eth.contract(Web3.to_checksum_address('0x1BbD33384869b30A323e15868Ce46013C82B86FB'),abi=abi)
    txn = contract.functions.borrow(int((return_percent/100)*value-1))

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
    print(txn_approve_text)

    try:
        suc =  check_tx_sucs(txn_approve_text)
        if suc:
            return True
        else:
            function_out('\nError while borrowing eth reactor perform')
            return False
    except:
        function_out('\nError while borrowing eth reactor deep error(check tx sucs)')
        return False
