from core.basic0.curency_erc20 import crypto_to_usd
from web3 import Web3

def usd_to_zk_gas(usd=0.3):
    eth_price = crypto_to_usd('ETH')
    return int(Web3.to_wei(usd/eth_price,'ether')/250000000)
