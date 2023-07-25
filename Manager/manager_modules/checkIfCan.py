from core.basic0.curency_erc20 import crypto_to_usd
from core.basic0.zk_eth_balance import eth_zk_balance
from web3 import Web3


class CheckIfCan:


    def check_if_can(self):
        curency = crypto_to_usd()
        summ_required = 0

        for i in self.raschet_data:
            summ_required = summ_required + self.raschet_data[i]

        for i, v in enumerate(self.account_list):
            eth_in_usd_balance = float(Web3.from_wei(eth_zk_balance(v.address),'ether'))*curency
            if eth_in_usd_balance-summ_required*0.9<0:
                self.function_out(f'\naddress {v.address} have not enough ether for tasks. Required:{round(summ_required,2)} usd, Balance:{round(eth_in_usd_balance,2)} usd')
            else:
                self.function_out(
                    f'\naddress {v.address} gg')