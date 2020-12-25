#!/usr/bin/env python
# coding: utf-8

# In[2]:


# import tkinter as tk
# from tkinter import ttk

import openpyxl
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

import numpy as np
import os
import datetime

import json
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.exceptions import V20Error

# 1:アジア、2：ヨーロッパ、３：南米
area = [1, 2, 3]

def dollar_calc():    
    accountID = "101-009-16992901-001"
    access_token = "f7e364ea7596211439220a01ec9b075d-3fe7aa8f160f2beaa88d423b81457594"
    api = API(access_token=access_token, environment="practice")

    params = { "instruments": "USD_JPY" }
    pricing_info = PricingInfo(accountID=accountID, params=params)

    try:
        api.request(pricing_info)
        response = pricing_info.response

        dollar = float(response["prices"][0]["bids"][0]["price"])

    except V20Error as e:
        print("Error: {}".format(e))

    return dollar

dollar = dollar_calc()
paypal = 3.9
fxfee = 3
ebay = 9.15

# 仕入れ
item_id=1 
buy=1000
# 販売価格
sell=20
# 重量
weight=100
# 保存
switch='off'
# バイヤー地域
area=1
# 目標売価
target=300

basic = {
        0:530,
    
        1:580,
        2:630,
        3:700,
        4:770,
        5:840,
        6:910,
        7:980,
        8:1050,
        9:1120,
        10:1290,
        11:1560,
        12:1780,
        13:2000
}

eu = {
        0:20,
        1:40,
        2:60,
        3:80,
        4:100,
        5:120,
        6:140,
        7:160,
        8:180,
        9:200,
        10:250,
        11:300,
        12:350,
        13:400
}

sa = {
        0:40,
        1:80,
        2:120,
        3:160,
        4:200,
        5:240,
        6:280,
        7:320,
        8:360,
        9:400,
        10:500,
        11:600,
        12:700,
        13:800
}



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.my_color = '#fff'
        
        self.title('ProfitSum')
        self.geometry('660x560')
        self.option_add('*font', ('FixedSys', 14))
        self['bg'] = '#fff'
        self.wm_attributes('-topmost', True)
        
        self.s = ttk.Style()
        self.s.configure('My.TFrame')
        
        self.ifreme = ttk.Frame(self, style='My.TFrame')
        self.ifreme.pack(expand=True, fill=tk.BOTH, padx=16, pady=16)
        
        # バリデータの設定
        self.vcmd = (self.register(self.validate_input_items), "%S")
        
        ### 左フレーム
        self.frame_left = ttk.Frame(self.ifreme, padding=10, height=100, style='My.TFrame')
        self.frame_left.grid(column=0, row=0)
        
        
        # 仕入価格
        self.buy_lb = tk.Label(self.frame_left, text='仕入価格（円）', width=29, anchor="w")
        self.buy_lb.grid(column=0, row=0, pady=(10, 1))
        self.buy = tk.Entry(self.frame_left, width=30, validate="key", validatecommand=self.vcmd)
        self.buy.grid(column=0, row=1, padx=(25, 10), pady=(5, 10), ipady=5)
        self.buy.bind("<KeyRelease>", self.all_sum00)
        
        # 販売価格
        self.sell_lb = tk.Label(self.frame_left, text='販売価格（ドル）', width=29, anchor="w")
        self.sell_lb.grid(column=0, row=2, pady=(10, 1))
        self.sell = tk.Entry(self.frame_left, width=30)
        self.sell.grid(column=0, row=3, padx=(25, 10), pady=(5, 10), ipady=5)
        self.sell.bind("<KeyRelease>", self.all_sum01)
        
        # 重量
        self.weight_lb = tk.Label(self.frame_left, text='重量（グラム）', width=29, anchor="w")
        self.weight_lb.grid(column=0, row=4, pady=(10, 1))
        self.weight = tk.Entry(self.frame_left, width=30)
        self.weight.grid(column=0, row=5, padx=(25, 10), pady=(5, 10), ipady=5)
        self.weight.bind("<KeyRelease>", self.all_sum02)
        
        
        # 商品名
        self.item_name_lb = tk.Label(self.frame_left, text='商品名', width=29, anchor="w")
        self.item_name_lb.grid(column=0, row=6, pady=(10, 1))
        self.item_name = tk.Entry(self.frame_left, width=30)
        self.item_name.grid(column=0, row=7, padx=(25, 10), pady=(3, 5), ipady=5)
#         self.item_name.bind("<KeyRelease>", self.all_sum03)
        
        # 商品URL
        self.item_url_lb = tk.Label(self.frame_left, text='商品URL', width=29, anchor="w")
        self.item_url_lb.grid(column=0, row=8, pady=(10, 1))
        self.item_url = tk.Entry(self.frame_left, width=30)
        self.item_url.grid(column=0, row=9, padx=(25, 10), pady=(3, 5), ipady=5)
#         self.item_URL.bind("<KeyRelease>", self.all_sum04)
        
        # アイテムID
        self.itemid_lb = tk.Label(self.frame_left, text='アイテムID', width=29, anchor="w")
        self.itemid_lb.grid(column=0, row=10, pady=(10, 1))
        self.itemid = tk.Entry(self.frame_left, width=30)
        self.itemid.grid(column=0, row=11, padx=(25, 10), pady=(3, 5), ipady=5)
#         self.itemid.bind("<KeyRelease>", self.all_sum05)
        
        
        ### 右フレーム
        self.frame_fight = ttk.Frame(self.ifreme, padding=10, style='My.TFrame')
        self.frame_fight.grid(column=1, row=0, sticky=tk.N + tk.S)
        
        # 計算内訳
        self.progress = tk.LabelFrame(self.frame_fight, text='計算内訳', width=280, height=260, labelanchor=tk.N)
        self.progress.propagate(False)
        self.progress.grid(column=0, row=0, padx=10, pady=(15, 0))

        text_list = ['利益　　：', '利益率　：', '目標売価：', '販売価格：', '仕入価格：', '発送料　：', '手数料　：']
        
        self.text_00 = tk.StringVar()
        self.text_00.set(text_list[0])

        self.text_01 = tk.StringVar()
        self.text_01.set(text_list[1])
        
        self.text_02 = tk.StringVar()
        self.text_02.set(text_list[2])
        
        self.text_03 = tk.StringVar()
        self.text_03.set(text_list[3])
        
        self.text_04 = tk.StringVar()
        self.text_04.set(text_list[4])
        
        self.text_05 = tk.StringVar()
        self.text_05.set(text_list[5])

        self.text_06 = tk.StringVar()
        self.text_06.set(text_list[6])

        tk.Label(self.progress, textvariable=self.text_00).pack(padx=5, pady=5, anchor="w")
        tk.Label(self.progress, textvariable=self.text_01).pack(padx=5, pady=5, anchor="w")
        tk.Label(self.progress, textvariable=self.text_02, fg='#4CAF50').pack(padx=5, pady=5, anchor="w")
        tk.Label(self.progress, textvariable=self.text_03).pack(padx=5, pady=5, anchor="w")
        tk.Label(self.progress, textvariable=self.text_04).pack(padx=5, pady=5, anchor="w")
        tk.Label(self.progress, textvariable=self.text_05).pack(padx=5, pady=5, anchor="w")
        tk.Label(self.progress, textvariable=self.text_06).pack(padx=5, pady=5, anchor="w")

        
        ### 右子フレーム
        self.frame_fight_child = ttk.Frame(self.frame_fight, padding=10, style='My.TFrame')
        self.frame_fight_child.grid(column=0, row=1, sticky=tk.N + tk.S)

        # 発送地域のプルダウン
        self.area_lb = tk.Label(self.frame_fight_child, text="発送地域", width=10, anchor="w")
        self.area_lb.grid(column=0, row=1, pady=(10, 5))
        self.area_combo = ttk.Combobox(self.frame_fight_child, state='readonly', width=10)
        self.area_combo['values'] = ('アジア', '欧州', '南米')
        self.area_combo.current(1)
        self.area_combo.grid(column=1, row=1, padx=(10, 0), pady=(20, 10), ipady=2)
        self.area_combo.bind('<<ComboboxSelected>>', self.ship_area)
    
        # 為替の定義
        self.fx_lb = tk.Label(self.frame_fight_child, text="為替相場", width=10, anchor="w")
        self.fx_lb.grid(column=0, row=2, pady=(0, 5))
        self.fx_var = tk.IntVar(value=0)
        self.fx_var.set(dollar)
        self.fx_box = tk.Entry(self.frame_fight_child, width=12, textvariable=self.fx_var)
        self.fx_box.grid(column=1, row=2, padx=(15, 0), ipady=4)
        self.fx_box.bind("<KeyRelease>", self.fx_calc)
        
        # 目標利益
        self.target_lb = tk.Label(self.frame_fight_child, text="目標利益", width=10, anchor="w")
        self.target_lb.grid(column=0, row=3, pady=(5, 5))
        self.target_var = tk.IntVar(value=0)
        self.target_var.set(target)
        self.target = tk.Entry(self.frame_fight_child, width=12, textvariable=self.target_var)
        self.target.grid(column=1, row=3, padx=(15, 0), ipady=4)
        self.target.bind("<KeyRelease>", self.target_profit)
    
        ### 右子フレーム
        self.frame_fight_child_2 = ttk.Frame(self.frame_fight, padding=10, style='My.TFrame')
        self.frame_fight_child_2.grid(column=0, row=3, rowspan=2, sticky=tk.N + tk.S)

        # 保存ボタン
        self.save =  tk.Button(self.frame_fight_child_2, text="保存", width=10, relief='groove', fg='#2196F3', bg='white', command=self.save_btn)
        self.save.grid(column=0, row=0, ipadx=10, ipady=5, pady=5)
        
        # リセットボタン
        self.reset =  tk.Button(self.frame_fight_child_2, text="リセット", width=10, relief='groove', fg='#2196F3', bg='white', command=self.reset_btn)
        self.reset.grid(column=1, row=0, ipadx=10, ipady=5, padx=(10, 0) ,pady=5)
        
        # お知らせテキスト
        self.ms = tk.StringVar()
        self.ms.set('')
        tk.Label(self.frame_fight_child_2, textvariable=self.ms).grid(column=0, row=1, padx=5, pady=5)
    
    # 数字の入力のみ許可
    def validate_input_items(self, validate_value):
        return validate_value.isdigit()
    
    ### 左 関数

    # 仕入価格
    def all_sum00(self, event):
        global buy
        if self.buy.get().isdecimal() :
            buy = int(self.buy.get())
            x = profit(item_id=item_id, buy=buy, sell=sell, weight=weight, switch=switch, area=area, target=target)
            self.text_04.set('仕入価格：' + str(x[2]) + '円')
            self.text_03.set('販売価格：' + str(x[3]) + '円')
            self.text_00.set('利益    ：' + str(x[0]))
            self.text_01.set('利益率  ：' + str(x[1]))
            self.text_02.set('目標売価：' + str(x[6]) + 'ドル（' + str(x[7]) + '円）')
            self.text_05.set('発送料  ：' + str(x[4]))
            self.text_06.set('手数料  ：' + str(x[5]))

    # 販売価格
    def all_sum01(self, event):
        global sell
        if self.sell.get():
            sell = float(self.sell.get())
            x = profit(item_id=item_id, buy=buy, sell=sell, weight=weight, switch=switch, area=area, target=target)
            self.text_04.set('仕入価格：' + str(x[2]) + '円')
            self.text_03.set('販売価格：' + str(x[3]) + '円')
            self.text_00.set('利益    ：' + str(x[0]))
            self.text_01.set('利益率  ：' + str(x[1]))
            self.text_02.set('目標売価：' + str(x[6]) + 'ドル（' + str(x[7]) + '円）')
            self.text_05.set('発送料  ：' + str(x[4]))
            self.text_06.set('手数料  ：' + str(x[5]))
    
    # 重さ
    def all_sum02(self, event):
        global weight
        if self.weight.get().isdecimal() :
            weight = int(self.weight.get())
            x = profit(item_id=item_id, buy=buy, sell=sell, weight=weight, switch=switch, area=area, target=target)
            self.text_04.set('仕入価格：' + str(x[2]) + '円')
            self.text_03.set('販売価格：' + str(x[3]) + '円')
            self.text_00.set('利益    ：' + str(x[0]))
            self.text_01.set('利益率  ：' + str(x[1]))
            self.text_02.set('目標売価：' + str(x[6]) + 'ドル（' + str(x[7]) + '円）')
            self.text_05.set('発送料  ：' + str(x[4]))
            self.text_06.set('手数料  ：' + str(x[5]))
            
    # 為替上書きの処理
    def fx_calc(self, event):
        global dollar
        dollar = float(self.fx_box.get())
        x = profit(item_id=item_id, buy=buy, sell=sell, weight=weight, switch=switch, area=area, target=target)
        self.text_04.set('仕入価格：' + str(x[2]) + '円')
        self.text_03.set('販売価格：' + str(x[3]) + '円')
        self.text_00.set('利益    ：' + str(x[0]))
        self.text_01.set('利益率  ：' + str(x[1]))
        self.text_02.set('目標売価：' + str(x[6]) + 'ドル（' + str(x[7]) + '円）')
        self.text_05.set('発送料  ：' + str(x[4]))
        self.text_06.set('手数料  ：' + str(x[5]))
            
    # 目標利益
    def target_profit(self, event):
        global target
        if self.target.get().isdecimal():
            target = int(self.target.get())
            x = profit(item_id=item_id, buy=buy, sell=sell, weight=weight, switch=switch, area=area, target=target)
            self.text_04.set('仕入価格：' + str(x[2]) + '円')
            self.text_03.set('販売価格：' + str(x[3]) + '円')
            self.text_00.set('利益    ：' + str(x[0]))
            self.text_01.set('利益率  ：' + str(x[1]))
            self.text_02.set('目標売価：' + str(x[6]) + 'ドル（' + str(x[7]) + '円）')
            self.text_05.set('発送料  ：' + str(x[4]))
            self.text_06.set('手数料  ：' + str(x[5]))
            
    # 保存ボタンの処理
    def save_btn(self):
        """保存処理の詳細

        1. 在庫リストCSVファイルを読み込む
        2. 現在入力されている商品IDが在庫リストに存在するか確かめる
        3. ある場合は、「在庫が重複している」というメッセージ
        4. ない場合は、最終行に新しく追加する
        5. 入力されている商品情報（名, URL, ID）をリセット
        """
        if self.item_name.get():
            if self.item_url.get():
                if self.itemid.get():
                    if self.buy.get():
                        if self.sell.get():
                            import pandas as pd
                            get_item_id = self.itemid.get()
                            csv = pd.read_csv('stock_check/ebay_melon2020_2020.csv', encoding='shift-jis')
                            if get_item_id in csv['商品ID'].values:
                                self.ms.set('商品IDが重複しています')
                            else:
                                item_name = self.item_name.get()
                                item_url = self.item_url.get()
                                item_buy = self.buy.get()
                                item_sell = self.sell.get()
                                value = [(get_item_id, item_name, item_url, item_buy, item_sell)]

                                cols = ['商品ID', '商品名', '商品URL', '仕入価格', '販売価格']
                                new_df = pd.DataFrame(value, columns=cols)
                                csv = csv.append(new_df, ignore_index=True)
                                csv.to_csv('stock_check/ebay_melon2020_2020.csv', index=False, encoding="shift-jis")
                                self.ms.set('保存しました♪')
                else:
                    self.ms.set('商品IDがない')
            else:
                self.ms.set('商品URLがない')
        else:
            self.ms.set('商品名がない')

    # リセッtボタン
    def reset_btn(self):
        # リストで指定したEntryの文字列を空にする
        entrys = [self.item_name, self.item_url, self.itemid, self.weight, self.buy, self.sell]
        for i in entrys:
            i.delete(0, tk.END)
        
        self.fx_var.set(dollar_calc())
        self.target_var.set(300)
        self.area_combo.current(1)
        self.ms.set('')
            
    # 発送地域
    def ship_area(self, event):
        global area
        area = self.area_combo.current()
        x = profit(item_id=item_id, buy=buy, sell=sell, weight=weight, switch=switch, area=area, target=target)
        self.text_04.set('仕入価格：' + str(x[2]) + '円')
        self.text_03.set('販売価格：' + str(x[3]) + '円')
        self.text_00.set('利益    ：' + str(x[0]))
        self.text_01.set('利益率  ：' + str(x[1]))
        self.text_02.set('目標売価：' + str(x[6]) + 'ドル（' + str(x[7]) + '円）')
        self.text_05.set('発送料  ：' + str(x[4]))
        self.text_06.set('手数料  ：' + str(x[5]))

def profit(item_id, buy, sell, weight, switch, area, target):
    # 重さ分岐
    if weight > 2001:
        weight = 2000
    bins = np.array([101, 201, 301, 401, 501, 601, 701, 801, 901, 1001, 1251, 1501, 1751, 2001])
    sip_cha = np.digitize(weight, bins)

    # エリアによる分岐
    if area == 0:
        wma = basic[sip_cha]
    elif area == 1:
        wma = basic[sip_cha] + eu[sip_cha]
    elif area == 2:
        wma = basic[sip_cha] + sa[sip_cha]

    # 販売価格を円に変換
    sell_sum = round((sell * dollar), 2)
    # 利益の計算
    notincom = sell_sum * (1 - ((paypal + fxfee + ebay) /100)) - (buy + wma)
    # 純利益の表示
    pri_notincom = '{:,}円'.format(round(notincom, 2))
    # 利益率の計算と表示
    profitrate = '{:.1%}'.format(notincom / buy)

    # 手数料
    fee = '{:,}円'.format(int(sell_sum - (sell_sum * (1 - ((paypal + fxfee + ebay) /100)))))
    
    # 目標価格から利益を引いて差額をドルに変換
    target_sum01 = (target - int(notincom)) / dollar
    # 上記の結果を売値に足し、ドル表記
    target_dollar = '{:.2f}'.format(sell + target_sum01)
    # ドルを円に変換
    target_jpy = int(float(target_dollar) * dollar)
    
    return [pri_notincom, profitrate, buy, sell_sum, wma, fee, target_dollar, target_jpy]

def main():
    app = App()    
    app.mainloop()
    
main()


# In[ ]:




