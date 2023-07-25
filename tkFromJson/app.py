import tkinter as tk
from tkinter import ttk
import json
import threading
import time
from Manager.manager import Manager
import datetime
class MainApp(tk.Tk):
    old_time = time.time() - 6
    modules_data = 0
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.get_perc()
        with open('tkFromJson/appSettings.json') as file:
            self.settings = json.load(file)
        self.place_modules()
        self.place_hyper()
        self.place_out()
        self.read_modules()
        self.one_sec_cheker()
        print(self.read_modules())
        print(self.hyper_data)
        self.mainloop()




    def get_perc(self):
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()


    def pX(self,ch):
        return int((self.screen_width/100)*ch)

    def pY(self,ch):
        return int((self.screen_height/100)*ch)



    def place_modules(self):
        how_many_in_row = 8
        window_width = int(self.screen_width/how_many_in_row)
        window_height = int(self.screen_height/9)
        self.dict_with_elements = {}
        self.modules_frame = tk.Frame(self)
        #creating elements
        volume_added = False
        for i,v in enumerate(self.settings['modules']):
            if v['type'] == 'swaps':
                if volume_added == False:
                    font_razmer1 = ("Arial", int(window_height / 5))
                    font_razmer2 = ("Arial", int(window_height / 7))
                    self.dict_with_elements['swaps_volume'] = {}
                    self.dict_with_elements['swaps_volume']['data'] = {'type':'swaps_volume'}
                    self.dict_with_elements['swaps_volume']['frame_object'] = tk.Frame(self.modules_frame)
                    self.dict_with_elements['swaps_volume']['name_label'] = tk.Label(
                        self.dict_with_elements['swaps_volume']['frame_object'], text='All swaps volume')
                    self.dict_with_elements['swaps_volume']['volume_label'] = tk.Label(
                        self.dict_with_elements['swaps_volume']['frame_object'], text='Volume $',font=font_razmer2)
                    self.dict_with_elements['swaps_volume']['volume_entry'] = tk.Entry(
                        self.dict_with_elements['swaps_volume']['frame_object'],font=font_razmer1,justify='center')

                    # self.dict_with_elements[v['name']]['frame_object'] = tk.Frame()
                    self.dict_with_elements['swaps_volume']['name_label'].place(x=0, width=window_width, y=0,
                                                                                  height=int(window_height / 2))
                    self.dict_with_elements['swaps_volume']['volume_label'].place(x=0, width=int(window_width / 2),
                                                                                   y=int(window_height / 2),
                                                                                   height=int(window_height / 2))
                    self.dict_with_elements['swaps_volume']['volume_entry'].place(x=int(window_width / 2),
                                                                                   width=window_width / 2,
                                                                                   y=int(window_height / 2),
                                                                                   height=int(window_height / 2))


                # md_name = v['module_name']
                font_razmer = ("Arial",int(window_height/4))
                font_razmer1 = ("Arial", int(window_height / 5))
                self.dict_with_elements[v['module_name']] = {}
                self.dict_with_elements[v['module_name']]['frame_object'] = tk.Frame(self.modules_frame)
                self.dict_with_elements[v['module_name']]['name_label'] = tk.Button(self.dict_with_elements[v['module_name']]['frame_object'],text=v['name'],bg='#F74A4A',font=('Arial',int((window_height*2)/len(v['name']))))
                self.dict_with_elements[v['module_name']]['swaps_label'] = tk.Label(self.dict_with_elements[v['module_name']]['frame_object'],text='Swaps',bg='#F74A4A',font=font_razmer1)
                self.dict_with_elements[v['module_name']]['swaps_entry'] = tk.Entry(self.dict_with_elements[v['module_name']]['frame_object'],bg='#F74A4A',font=font_razmer,justify='center')

                self.dict_with_elements[v['module_name']]['data'] = {'type':'swaps','activated':False}
                # self.dict_with_elements[v['name']]['frame_object'] = tk.Frame()
                def on_button_click(module):
                    if module['data']['activated'] == False:
                        color = '#CFF2FF'
                        module['data']['activated'] = True
                        module['name_label'].configure(bg=color)
                        module['swaps_label'].configure(bg=color)
                        module['swaps_entry'].configure(bg=color)
                        module['swaps_entry'].delete(0, tk.END)

                    elif module['data']['activated'] == True:
                        color = '#F74A4A'
                        module['data']['activated'] = False
                        module['name_label'].configure(bg=color)
                        module['swaps_label'].configure(bg=color)
                        module['swaps_entry'].configure(bg=color)
                        module['swaps_entry'].delete(0, tk.END)

                self.dict_with_elements[v['module_name']]['name_label'].configure(command=lambda mdl=self.dict_with_elements[v['module_name']]: on_button_click(mdl))

                self.dict_with_elements[v['module_name']]['name_label'].place(x=0,width=window_width,y=0,height=int(window_height/2))
                self.dict_with_elements[v['module_name']]['swaps_label'].place(x=0,width=int(window_width/2),y=int(window_height/2),height=int(window_height/2))
                self.dict_with_elements[v['module_name']]['swaps_entry'].place(x=int(window_width/2),width=window_width/2,y=int(window_height/2),height=int(window_height/2))
                volume_added = True
            if v['type'] == 'stake':
                self.dict_with_elements[v['module_name']] = {}
                self.dict_with_elements[v['module_name']]['frame_object'] = tk.Frame(self.modules_frame)
                self.dict_with_elements[v['module_name']]['name_label'] = tk.Button(self.dict_with_elements[v['module_name']]['frame_object'],text=v['name'],bg='#F74A4A')
                self.dict_with_elements[v['module_name']]['volume_label'] = tk.Label(self.dict_with_elements[v['module_name']]['frame_object'],text='Volume $',bg='#F74A4A')
                self.dict_with_elements[v['module_name']]['volume_entry'] = tk.Entry(self.dict_with_elements[v['module_name']]['frame_object'],bg='#F74A4A')
                self.dict_with_elements[v['module_name']]['borrow_label'] = tk.Label(self.dict_with_elements[v['module_name']]['frame_object'],text='Borrow %',bg='#F74A4A')
                self.dict_with_elements[v['module_name']]['borrow_entry'] = tk.Entry(self.dict_with_elements[v['module_name']]['frame_object'],bg='#F74A4A')
                self.dict_with_elements[v['module_name']]['data'] = {}
                # self.dict_with_elements[v['name']]['frame_object'] = tk.Frame()
                def on_button_click_stake(module):
                    if module['data']['borrow'] == True:
                        if module['data']['activated'] == False:
                            color = '#CFF2FF'
                            module['data']['activated'] = True
                            module['name_label'].configure(bg=color)
                            module['volume_label'].configure(bg=color)
                            module['volume_entry'].configure(bg=color)
                            module['borrow_label'].configure(bg=color)
                            module['borrow_entry'].configure(bg=color)
                            module['volume_entry'].delete(0, tk.END)
                            module['borrow_entry'].delete(0, tk.END)

                        elif module['data']['activated'] == True:
                            color = '#F74A4A'
                            module['data']['activated'] = False
                            module['name_label'].configure(bg=color)
                            module['volume_label'].configure(bg=color)
                            module['volume_entry'].configure(bg=color)
                            module['borrow_label'].configure(bg=color)
                            module['borrow_entry'].configure(bg=color)
                            module['volume_entry'].delete(0, tk.END)
                            module['borrow_entry'].delete(0, tk.END)
                    elif module['data']['borrow'] == False:
                        if module['data']['activated'] == False:
                            color = '#CFF2FF'
                            module['data']['activated'] = True
                            module['name_label'].configure(bg=color)
                            module['volume_label'].configure(bg=color)
                            module['volume_entry'].configure(bg=color)
                            # module['borrow_label'].configure(bg=color)
                            # module['borrow_entry'].configure(bg=color)
                            module['volume_entry'].delete(0, tk.END)
                            # module['borrow_entry'].delete(0, tk.END)

                        elif module['data']['activated'] == True:
                            color = '#F74A4A'
                            module['data']['activated'] = False
                            module['name_label'].configure(bg=color)
                            module['volume_label'].configure(bg=color)
                            module['volume_entry'].configure(bg=color)
                            # module['borrow_label'].configure(bg=color)
                            # module['borrow_entry'].configure(bg=color)
                            module['volume_entry'].delete(0, tk.END)
                            # module['borrow_entry'].delete(0, tk.END)

                self.dict_with_elements[v['module_name']]['name_label'].configure(command=lambda mdl=self.dict_with_elements[v['module_name']]: on_button_click_stake(mdl))
                if v['borrow'] == True:
                    self.dict_with_elements[v['module_name']]['volume_label'].configure(
                        font=('Arial', int(window_height / 7)))
                    self.dict_with_elements[v['module_name']]['name_label'].configure(font=('Arial',int((window_height*1.3)/len(v['name']))))
                    self.dict_with_elements[v['module_name']]['volume_entry'].configure(
                        font=('Arial', int(window_height / 7)), justify='center')
                    self.dict_with_elements[v['module_name']]['borrow_label'].configure(
                        font=('Arial', int(window_height / 7)))
                    self.dict_with_elements[v['module_name']]['borrow_entry'].configure(
                        font=('Arial', int(window_height / 7)), justify='center')
                    borrow_height = int(window_height/3)
                    self.dict_with_elements[v['module_name']]['data'] = {'type': 'stake', 'activated': False,'borrow': True}
                    self.dict_with_elements[v['module_name']]['name_label'].place(x=0,width=window_width,y=0,height=borrow_height)
                    self.dict_with_elements[v['module_name']]['volume_label'].place(x=0,width=int(window_width/2),y=borrow_height,height=borrow_height)
                    self.dict_with_elements[v['module_name']]['volume_entry'].place(x=int(window_width/2),width=window_width/2,y=borrow_height,height=borrow_height)
                    self.dict_with_elements[v['module_name']]['borrow_label'].place(x=0,width=int(window_width/2),y=borrow_height*2,height=borrow_height)
                    self.dict_with_elements[v['module_name']]['borrow_entry'].place(x=int(window_width/2),width=window_width/2,y=borrow_height*2,height=borrow_height)
                else:
                    self.dict_with_elements[v['module_name']]['name_label'].configure(
                        font=('Arial', int((window_height * 2   ) / len(v['name']))))
                    self.dict_with_elements[v['module_name']]['volume_label'].configure(font=('Arial',int(window_height/7)))
                    self.dict_with_elements[v['module_name']]['volume_entry'].configure(font=('Arial',int(window_height/5)),justify='center')
                    borrow_height = int(window_height / 2)
                    self.dict_with_elements[v['module_name']]['data'] = {'type': 'stake', 'activated': False,'borrow': False}

                    self.dict_with_elements[v['module_name']]['name_label'].place(x=0, width=window_width, y=0,height=borrow_height)
                    self.dict_with_elements[v['module_name']]['volume_label'].place(x=0, width=int(window_width / 2),y=borrow_height,height=borrow_height)
                    self.dict_with_elements[v['module_name']]['volume_entry'].place(x=int(window_width / 2),
                                                                                    width=window_width / 2,
                                                                                    y=borrow_height,
                                                                                    height=borrow_height)
        # placing elements
        chx = 0
        chy = 0
        # self.modules_frame = tk.Frame(self)
        for i,v in enumerate(self.dict_with_elements):
            self.dict_with_elements[v]['frame_object'].place(x=chx * window_width, y=chy*window_height, height=window_height, width=window_width)
            chx = chx + 1
            if how_many_in_row - chx == 0:
                chy = chy + 1
                chx = 0
        self.modules_frame.place(x=0,width=self.screen_width,y=self.pY(57),height=(chy+1)*window_height)

    def place_hyper(self):

        height = int(self.screen_height/20)
        per_one = self.screen_width/55


        self.hyper_elemnts_dict = {}
        self.hyper_elemnts_dict['frame_object'] = tk.Frame(self)

        style = ttk.Style(self.hyper_elemnts_dict['frame_object'])
        font_size = int(height/2)
        style.configure('TLabel', font=('Helvetica', font_size))
        style.configure('TButton', font=('Helvetica', font_size))
        style.configure('TLabel', anchor='center')
        style.configure('TLabel',background='#FFBDBD')
        style.configure('TEntry', font=('Helvetica', font_size))

        #3 на лейбл 4 на ввод = 7
        self.hyper_elemnts_dict['gas_label'] = ttk.Label(self.hyper_elemnts_dict['frame_object'],text='Gas')
        self.hyper_elemnts_dict['gas_entry'] = ttk.Entry(self.hyper_elemnts_dict['frame_object'], font=('Helvetica', font_size),justify='center')

        #8 на лейбл 4 на ввод = 12
        self.hyper_elemnts_dict['time_b_label'] = ttk.Label(self.hyper_elemnts_dict['frame_object'],text='Time between')
        self.hyper_elemnts_dict['time_b_entry'] = ttk.Entry(self.hyper_elemnts_dict['frame_object'], font=('Helvetica', font_size),justify='center')

        #15 на лейбл 4 на ввод = 19
        self.hyper_elemnts_dict['time_r_label'] = ttk.Label(self.hyper_elemnts_dict['frame_object'],text='Random time +- %')
        self.hyper_elemnts_dict['time_r_entry'] = ttk.Entry(self.hyper_elemnts_dict['frame_object'], font=('Helvetica', font_size),justify='center')

        #3 на лейбл
        self.new_required = False
        def new_button_activated():
            if self.new_required == False:
                self.new_required = True
                self.hyper_elemnts_dict['new_button'].configure(bg='#0790FA')
            elif self.new_required == True:
                self.new_required = False
                self.hyper_elemnts_dict['new_button'].configure(bg='#FF3B3E')
        self.hyper_elemnts_dict['new_button'] = tk.Button(self.hyper_elemnts_dict['frame_object'],text='New',bg='#FF3B3E',command=new_button_activated)

        self.hyper_elemnts_dict['start_button'] = ttk.Button(self.hyper_elemnts_dict['frame_object'], text='Check or Start')

        self.hyper_elemnts_dict['autor_label'] = ttk.Label(self.hyper_elemnts_dict['frame_object'],text = '  Swap&Stake\n@SwissScripts',font=('Helvetica', int(font_size/1.6)))
        self.hyper_elemnts_dict['use_autor_label'] = ttk.Label(self.hyper_elemnts_dict['frame_object'],
                                                           text=f"   Modules by\n{self.settings['autor']}",
                                                           font=('Helvetica', int(font_size / 1.6)))






        self.hyper_elemnts_dict['gas_label'].place(x=0,width=int(per_one*3),y=0,height=height)
        self.hyper_elemnts_dict['gas_entry'].place(x=int(per_one*3), width=int(per_one*4), y=0, height=height)

        self.hyper_elemnts_dict['time_b_label'].place(x=int(per_one*7), width=int(per_one * 8), y=0, height=height)
        self.hyper_elemnts_dict['time_b_entry'].place(x=int(per_one * 15), width=int(per_one * 4), y=0, height=height)

        self.hyper_elemnts_dict['time_r_label'].place(x=int(per_one*19), width=int(per_one * 10), y=0, height=height)
        self.hyper_elemnts_dict['time_r_entry'].place(x=int(per_one * 29), width=int(per_one * 4), y=0, height=height)

        self.hyper_elemnts_dict['new_button'].place(x=int(per_one * 33), width=int(per_one * 5), y=0, height=height)

        self.hyper_elemnts_dict['start_button'].place(x=int(per_one * 38), width=int(per_one * 8), y=0, height=height)

        self.hyper_elemnts_dict['autor_label'].place(x=int(per_one * 50),height=height,width=int(per_one * 5))
        self.hyper_elemnts_dict['use_autor_label'].place(x=int(per_one * 46),height=height,width=int(per_one *4.5))

        self.hyper_elemnts_dict['frame_object'].place(x=0,y=self.pY(51),width=self.screen_width,height=height)

        self.hyper_elemnts_dict['start_button'].bind("<Button-1>",self.final_button_pressed)

    def place_out(self):
        self.out_text_window = tk.Text()

        self.out_text_window.place(x=0,y=0,width=self.screen_width,height=self.pY(50))


    def read_modules(self):
        self.modules_data = {}
        for i,v in enumerate(self.dict_with_elements):
            # print(self.dict_with_elements[v])
            if self.dict_with_elements[v]['data']['type'] == 'swaps':
                self.modules_data[v] = {}
                self.modules_data[v]['type'] = 'swaps'
                self.modules_data[v]['activated'] = self.dict_with_elements[v]['data']['activated']
                self.modules_data[v]['swaps_entry'] = self.dict_with_elements[v]['swaps_entry'].get()
            elif self.dict_with_elements[v]['data']['type'] == 'stake':
                self.modules_data[v] = {}
                self.modules_data[v]['type'] = 'stake'
                self.modules_data[v]['activated'] = self.dict_with_elements[v]['data']['activated']
                self.modules_data[v]['volume_entry'] = self.dict_with_elements[v]['volume_entry'].get()
                if self.dict_with_elements[v]['data']['borrow'] == True:
                    self.modules_data[v]['borrow'] = True
                    self.modules_data[v]['borrow_entry'] = self.dict_with_elements[v]['borrow_entry'].get()
                else:
                    self.modules_data[v]['borrow'] = False
            elif self.dict_with_elements[v]['data']['type'] == 'swaps_volume':
                self.modules_data[v] = {}
                self.modules_data[v]['type'] = 'swaps_volume'
                self.modules_data[v]['volume_entry'] = self.dict_with_elements[v]['volume_entry'].get()
                if self.modules_data[v]['volume_entry'] == '':
                    self.modules_data[v]['activated'] = False
                else:
                    self.modules_data[v]['activated'] = True


        self.hyper_data = {}
        self.hyper_data['gas'] = {}
        self.hyper_data['time_b'] = {}
        self.hyper_data['time_r'] = {}

        self.hyper_data['new'] = self.new_required
        self.hyper_data['gas']['activated'] = False
        self.hyper_data['time_b']['activated'] = False
        self.hyper_data['time_r']['activated'] = False

        gas = self.hyper_elemnts_dict['gas_entry'].get()
        if gas != '':
            self.hyper_data['gas']['activated'] = True
            self.hyper_data['gas']['value'] = gas

        time_b = self.hyper_elemnts_dict['time_b_entry'].get()
        if time_b != '':
            self.hyper_data['time_b']['activated'] = True
            self.hyper_data['time_b']['value'] = time_b

        time_r = self.hyper_elemnts_dict['time_r_entry'].get()
        if time_r != '':
            self.hyper_data['time_r']['activated'] = True
            self.hyper_data['time_r']['value'] = time_r




        return self.modules_data


    def function_out(self,message):
        self.out_text_window.insert("1.0",f'{message}  time: {datetime.datetime.today()}')

    def one_sec_cheker(self):
        def is_float(ch):
            try:
                d = float(ch)
                if d <= 0:
                    return False
                return True
            except:
                return False
        def is_float0(ch):
            try:
                d = float(ch)
                if d < 0:
                    return False
                return True
            except:
                return False

        def is_int(ch):
            try:
                d = int(ch)
                if d <= 0:
                    return False
                return True
            except:
                return False

        def checker():
            while True:
                if time.time() - self.old_time > 5:
                    self.hyper_elemnts_dict['start_button'].configure(text='Check or Start')
                time.sleep(1)
                self.read_modules()
                for i in self.modules_data:
                    if self.modules_data[i]['type'] == 'swaps_volume':
                        # self.modules_data[i]['great'] = False
                        if self.modules_data[i]['activated'] == False:
                            self.modules_data[i]['great'] = False
                            self.dict_with_elements['swaps_volume']['volume_entry'].delete(0, tk.END)
                        if is_float(self.modules_data[i]['volume_entry']):
                            # self.modules_data[i]['great'] = False
                            if len(str(self.modules_data[i]['volume_entry']))>6:
                                self.dict_with_elements['swaps_volume']['volume_entry'].delete(6, tk.END)
                                self.modules_data[i]['great'] = False
                            else:
                                self.modules_data[i]['great'] = True
                        else:
                            self.dict_with_elements['swaps_volume']['volume_entry'].delete(0,tk.END)
                            self.modules_data[i]['great'] = False

                    if self.modules_data[i]['type'] == 'swaps':
                        if self.modules_data[i]['activated'] == False:
                            self.modules_data[i]['great'] = False
                            self.dict_with_elements[i]['swaps_entry'].delete(0, tk.END)
                        if is_int(self.modules_data[i]['swaps_entry']):
                            if len(self.modules_data[i]['swaps_entry']) > 3:
                                self.dict_with_elements[i]['swaps_entry'].delete(3, tk.END)
                                self.modules_data[i]['great'] = False
                            else:
                                self.modules_data[i]['great'] = True
                        else:
                            self.modules_data[i]['great'] = False
                            self.dict_with_elements[i]['swaps_entry'].delete(0,tk.END)

                    if self.modules_data[i]['type'] == 'stake':
                        self.modules_data[i]['great'] = False
                        if self.modules_data[i]['activated'] == False:
                            self.dict_with_elements[i]['volume_entry'].delete(0, tk.END)
                        if is_float(self.modules_data[i]['volume_entry']):
                            if len(self.modules_data[i]['volume_entry']) > 6:
                                self.dict_with_elements[i]['volume_entry'].delete(6, tk.END)
                            else:
                                self.modules_data[i]['great'] = True
                        else:
                            self.dict_with_elements[i]['volume_entry'].delete(0, tk.END)


                        if self.modules_data[i]['borrow'] == True:
                            # self.modules_data[i]['great'] = False
                            if self.modules_data[i]['activated'] == False:
                                self.dict_with_elements[i]['borrow_entry'].delete(0, tk.END)
                                self.modules_data[i]['great'] = False
                            if is_float(self.modules_data[i]['borrow_entry']):
                                if len(self.modules_data[i]['borrow_entry']) > 4:
                                    self.dict_with_elements[i]['borrow_entry'].delete(4, tk.END)
                                    self.modules_data[i]['great'] = True
                                if float(self.modules_data[i]['borrow_entry'])>70.:
                                    self.dict_with_elements[i]['borrow_entry'].delete(0, tk.END)
                                    self.dict_with_elements[i]['borrow_entry'].insert(0,'70')
                                    self.modules_data[i]['great'] = True
                            else:
                                self.dict_with_elements[i]['borrow_entry'].delete(0, tk.END)
                                self.modules_data[i]['great'] = False
                    if self.hyper_data['gas']['activated']:
                        if is_float0(self.hyper_data['gas']['value']):
                            if len(self.hyper_data['gas']['value'])>4:
                                self.hyper_elemnts_dict['gas_entry'].delete(4,tk.END)
                        else:
                            self.hyper_elemnts_dict['gas_entry'].delete(0, tk.END)

                    if self.hyper_data['time_b']['activated']:
                        if is_float(self.hyper_data['time_b']['value']):
                            if len(self.hyper_data['time_b']['value'])>5:
                                self.hyper_elemnts_dict['time_b_entry'].delete(5,tk.END)
                        else:
                            self.hyper_elemnts_dict['time_b_entry'].delete(0, tk.END)

                    if self.hyper_data['time_r']['activated']:
                        if is_float(self.hyper_data['time_r']['value']):
                            if len(self.hyper_data['time_r']['value'])>2:
                                self.hyper_elemnts_dict['time_r_entry'].delete(2,tk.END)
                        else:
                            self.hyper_elemnts_dict['time_r_entry'].delete(0, tk.END)


        proc = threading.Thread(target=checker)
        proc.start()

    def final_button_pressed(self,event):
        def func_out(message):
            self.out_text_window.insert("1.0",f'{message}  time: {datetime.datetime.today()}')

        if self.hyper_data['gas']['activated'] == False:
            self.function_out('\nEnter Gas field')
            return
        if self.hyper_data['time_b']['activated'] == False:
            self.function_out('\nEnter time beetwen field')
            return
        if self.hyper_data['time_r']['activated'] == False:
            self.function_out('\nEnter time random field')
            return
        if int(self.hyper_data['time_r']['value']) > 90:
            self.function_out('\nTime random field must be < 90')
            return
        est = False
        # sw = False
        for i in self.modules_data:
            if self.modules_data[i]['activated'] == True:
                # est = True
                if self.modules_data[i]['great'] == False:
                    self.function_out(f'\nModule {i} has filling errors')
                    return
                elif self.modules_data[i]['type'] == 'swaps':
                    est = True
                    if self.modules_data['swaps_volume']['great'] == False:
                        self.function_out('\nThere is no volume for swaps')
                        return
                elif self.modules_data[i]['type'] == 'stake':
                    est = True

                # if se
        if est == False:
            self.function_out(f'\nNo modules are selected')
            return

        to_write = {'hyper_data': self.hyper_data, 'modules_data': self.modules_data}
        to_write = str(to_write)
        to_write = to_write.replace('\'', '\"')
        to_write = to_write.replace('False', 'false')
        to_write = to_write.replace('True', 'true')
        with open('data.json', 'w') as file:
            file.write(to_write)
        if time.time() - self.old_time > 5:

            # print(self.modules_data)


            self.Manager = Manager(func_out)
            self.Manager.read_data_json()
            self.Manager.read_wallets_txt()
            self.Manager.prepare_data_for_raschet()
            self.Manager.check_if_can()
            self.old_time = time.time()
            self.hyper_elemnts_dict['start_button'].configure(text='press in 5 sec')

        elif time.time() - self.old_time < 5:
            self.Manager = Manager(func_out)
            self.Manager.read_data_json()
            self.Manager.read_wallets_txt()
            self.Manager.prepare_data_for_raschet()
            self.Manager.vipolnenie_for_all_accs()



# d = MainApp()