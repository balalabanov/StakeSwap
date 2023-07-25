from web3 import Account
from web3 import Web3
import json
import random
from Manager.manager_modules.checkIfCan import CheckIfCan
import time
Account.enable_unaudited_hdwallet_features()
from core.basic0.curency_erc20 import crypto_to_usd
import threading
class Manager(CheckIfCan):

    def __init__(self,function_out):
        self.function_out = function_out

    def read_data_json(self):
        with open('data.json') as file:
            self.data_json = json.load(file)

    def read_wallets_txt(self):
        try:
            with open('wallets.txt') as file:
                wallets = file.readlines()

        except:
            self.function_out('\ncan not open wallets.txt')
            return

        if len(wallets) == 0:
            self.function_out('\nwallets.txt is empty')
            return

        for i,v in enumerate(wallets):
            wallets[i] = v.replace('\n','')
        self._wallets = wallets
        self.account_list = []
        for i,v in enumerate(wallets):
            try:
                try:
                    obj = Account.from_key(v)
                    self.account_list.append(obj)

                except:
                    obj = Account.from_mnemonic(v)
                    self.account_list.append(obj)
            except:
                self.function_out(f'\ncan not read wallet on row {i+1}')
        self.function_out(f'\nGot {len(self.account_list)} accounts')

    def prepare_data_for_raschet(self):
        self._activated_modules = {}
        self.raschet_data = {'swaps_price':0,'stake_price':0,'stake_borrow_price':0}
        gas = float(self.data_json['hyper_data']['gas']['value'])
        modules = self.data_json['modules_data']
        for i,v in enumerate(modules):
            if modules[v]['activated'] == True:
                self._activated_modules[v] = modules[v]
                if modules[v]['type'] == 'swaps':
                    self.raschet_data['swaps_price'] = self.raschet_data['swaps_price'] + float(modules[v]['swaps_entry'])*gas*0.75*2

                if modules[v]['type'] == 'stake':
                    if modules[v]['borrow'] == False:
                        self.raschet_data['stake_price'] = self.raschet_data['stake_price'] + float(modules[v]['volume_entry']) + gas

                    if modules[v]['borrow'] == True:
                        self.raschet_data['stake_borrow_price'] = self.raschet_data['stake_borrow_price'] + float(modules[v]['volume_entry'])*((100-float(modules[v]['borrow_entry']))/100) + gas*2


    def form_random_tasks(self,black_list = []):

        tasks_eth = {}
        tasks_usd = {}
        # tasks_stake = {}
        # task_colvo = []
        modules = self._activated_modules
        vsego = 0
        for i,v in enumerate(modules):
            if v in black_list:
                continue
            if modules[v]['type'] == 'swaps':
                tasks_eth[v] = {'type':'swaps','value':modules[v]['swaps_entry']}
                tasks_usd[v] = {'type':'swaps','value':modules[v]['swaps_entry']}
                vsego = vsego + int(modules[v]['swaps_entry'])*2
            elif modules[v]['type'] == 'stake':
                tasks_eth[v] = {'type':'stake','value':1}
                vsego = vsego + 1

        zadanie = []
        eth = True
        for i in range(vsego):
            if eth:
                summ = 0
                for j in tasks_eth:
                    summ = summ + int(tasks_eth[j]['value'])
                if summ == 0:
                    break

                wrong = True
                while wrong:
                    a = random.choice(list(tasks_eth))

                    if tasks_eth[a]['value'] != 0 and tasks_eth[a]['type'] == 'swaps':
                        tasks_eth[a]['value'] = int(tasks_eth[a]['value']) - 1
                        zadanie.append(f'{a}.eth')
                        wrong = False
                        eth = False
                    elif tasks_eth[a]['value'] != 0 and tasks_eth[a]['type'] == 'stake':
                        tasks_eth[a]['value'] = int(tasks_eth[a]['value']) - 1
                        zadanie.append(f'{a}.eth')
                        wrong = False
                        # eth = False
            if eth == False:
                summ = 0
                for j in tasks_usd:
                    summ = summ + int(tasks_usd[j]['value'])

                if summ == 0:
                    break

                wrong = True
                while wrong:
                    a = random.choice(list(tasks_usd))
                    if tasks_usd[a]['value'] != 0:
                        tasks_usd[a]['value'] = int(tasks_usd[a]['value']) - 1
                        zadanie.append(f'{a}.usd')
                        wrong = False
                        eth = True

        return zadanie


    def vipolnenie(self,acc,zadanie,black_list=[]):
        if len(zadanie) == 0:
            self.function_out(f'\nzadanie for {acc.address} is empty')
            return
        activated_modules = self._activated_modules
        eth_marker = True
        usd_approved = {}

        for i in zadanie:
            usd_approved[i[:-4]] = False

        done_with_sucs = 0
        while len(zadanie) != 0:
            self.function_out(f'\n{str(zadanie)}')
            for i,v in enumerate(zadanie):
                if v[-3:] == 'eth':
                    if activated_modules[v[:-4]]['type'] == 'swaps':

                        module_path = f"Modules.{v[:-4]}"

   
                        module = __import__(module_path, fromlist=["eth_usd"])

                        tx_is_ok = module.eth_usd(acc,self.function_out,float(activated_modules['swaps_volume']['volume_entry']),float(self.data_json['hyper_data']['gas']['value']))

                        if tx_is_ok:
                            # zadanie.pop(i)
                            done_with_sucs = done_with_sucs + 1
                            eth_marker = False
                        else:
                            black_list.append(v[:-4])
                            zadanie = self.form_random_tasks(black_list)
                            try:
                                zadanie = zadanie[:-done_with_sucs]
                            except:
                                zadanie = []

                                break

                    elif activated_modules[v[:-4]]['type'] == 'stake':
                        module_path = f"Modules.{v[:-4]}"

     
                        module = __import__(module_path, fromlist=["perform"])
                        if activated_modules[v[:-4]]['borrow'] == True:
                            tx_is_ok = module.perform(acc, self.function_out, float(activated_modules[v[:-4]]['volume_entry']),float(activated_modules[v[:-4]]['borrow_entry']),float(self.data_json['hyper_data']['gas']['value']))
                        else:
                            tx_is_ok = module.perform(acc, self.function_out,  float(activated_modules[v[:-4]]['volume_entry']))

                        if tx_is_ok:
                            done_with_sucs = done_with_sucs + 1
                            # zadanie.pop(i)
                            eth_marker = True
                        else:
                            black_list.append(v[:-4])
                            zadanie = self.form_random_tasks(black_list)
                            try:
                                zadanie = zadanie[:-done_with_sucs]
                            except:
                                zadanie = []

                                break


                if v[-3:] == 'usd':
                    if activated_modules[v[:-4]]['type'] == 'swaps':
                        # Определите полный путь до модуля
                        module_path = f"Modules.{v[:-4]}"

                      
                        module = __import__(module_path, fromlist=["usd_eth", "approve"])
                        if usd_approved[v[:-4]] == True:
                            print('Huy')
                        else:
                            tx_approved_is_ok = module.approve(acc,self.function_out)
                            if tx_approved_is_ok:
                                usd_approved[v[:-4]] = True

                            else:
                                black_list.append(v[:-4])
                                zadanie = self.form_random_tasks(black_list)
                                for ind, cn in enumerate(zadanie):
                                    if cn[-3:] == 'usd':
                                        zadanie = zadanie[ind:]
                                        break
                                    else:
                                        self.function_out(f'\nCan not generate tasks for {acc.address}')
                                        # zadanie = []
                                        return

                                try:
                                    zadanie = zadanie[:-done_with_sucs]
                                except:
                                    # print('huy')
                                    zadanie = []
                                    break

                        # if usd_approved[v[:-4]] == True:
                        tx_is_ok = module.usd_eth(acc, self.function_out,float(activated_modules['swaps_volume']['volume_entry']))

                        if tx_is_ok:
                            # zadanie.pop(i)
                            done_with_sucs = done_with_sucs + 1
                            eth_marker = True
                        else:
                            black_list.append(v[:-4])
                            zadanie = self.form_random_tasks(black_list)
                            for ind, cn in enumerate(zadanie):
                                if cn[-3:] == 'usd':
                                    zadanie = zadanie[ind:]
                                    break
                                else:
                                    self.function_out(f'\nCan not generate tasks for {acc.address}')

                            try:
                                zadanie = zadanie[:-done_with_sucs]
                            except:
                                print('huy')

                            break

                time.sleep(float(self.data_json['hyper_data']['time_b']['value'])*60+random.randint(0,int((float(self.data_json['hyper_data']['time_b']['value'])/100)*float(self.data_json['hyper_data']['time_b']['value'])*60)))
        self.function_out(f'\nDone with {acc.address}')
        return
    def vipolnenie_for_all_accs(self):
        for i in self.account_list:
            th = threading.Thread(target=self.vipolnenie,args=(i,self.form_random_tasks()))
            th.start()
