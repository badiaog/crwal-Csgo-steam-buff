import os
import time
import requests
import pandas as pd
import random
from fake_useragent import UserAgent
from urllib.parse import urlencode


class BuffCsgo:
    def __init__(self, category, save_file_path, _, price_range):
        # 貌似是一个时间戳类似的玩意 暂且放着
        self._ = _
        # 类目
        self.category = category
        # 存储位置
        self.save_file_path = save_file_path
        # 价格区间 从10起步
        self.price_range = price_range
        # 一个临时的存储当前页信息的列表
        self.item_datas = []
        # 不变的url
        self.base_url = 'https://buff.163.com/api/market/goods?'

    # buff要获取当前类目总页码必须点最后一页才能得到正确的页码数
    def get_total_page(self):
        params = {
            'game': 'csgo',
            'page_num': 2000,
            'category_group': self.category,
            'min_price': 10,
            'max_price': 10 + self.price_range,
            '_': self._
        }
        url = self.base_url + urlencode(params)
        response = requests.get(url=url, headers=self.init_headers(), timeout=10)
        if response.json().get('data'):
            self._ += random.randint(1, 3)
            total_page = response.json().get('data').get('total_page')
            return total_page

    def get_page(self):
         for page in range(1,self.get_total_page()+1):
        #for page in range(1, 4):  # 测试
            params = {
                'game': 'csgo',
                'page_num': page,
                'category_group': self.category,
                'min_price': 10,
                'max_price': 10 + self.price_range,
                '_': self._
            }
            current_url = self.base_url + urlencode(params)
            try:
                response = requests.get(url=current_url, headers=self.init_headers(), proxies = self.random_ip(),timeout=10)
                if response.status_code == 200:
                    print(f'已获取第{page}页')
                    self._ += random.randint(1, 3)
                    page_text = response.json()
                    self.parse_page(page_text)
                    self.save_to_csv()
                    time.sleep(random.random() * 5)
            except requests.ConnectionError as e:
                print('获取失败')

    def parse_page(self, page_text):
        if page_text.get('data').get('items'):
            for item in page_text.get('data').get('items'):
                info = {}
                info['Buff饰品名称'] = item.get('name')
                info['Buff当前价格'] = item.get('quick_price')
                info['Buff当前在售数量'] = item.get('sell_num')
                self.item_datas.append(info)

    def init_headers(self):
        cookie = 'yourcookie'
        headers = {
            'User-Agent': UserAgent().random,
            'Cookie': cookie
        }
        return headers

    # 随机取ip
    def random_ip(self):
        proxies = [
            '120.232.150.110:80',
            '106.45.221.69:3256',
            '47.98.208.18:8080',
            '117.24.80.59:3256',
            '111.179.73.203:3256',
            '47.95.178.212:3128',
            '125.87.84.82:3256',
            '47.98.179.39:8080',
            '116.62.113.142:1081',
            '114.215.172.136:31280',
            '47.98.183.59:3128',
            '118.194.242.184:80',
            '114.67.108.243:8081',
            '120.232.150.100:80'
        ]
        proxy = {
            'http': 'http://' + random.choice(proxies)
        }
        return proxy

    # 存储到csv
    def save_to_csv(self):
        df = pd.DataFrame(self.item_datas)
        df = df.reindex(columns=['Buff饰品名称', 'Buff当前价格', 'Buff当前在售数量'])
        if os.path.exists(self.save_file_path) and os.path.getsize(self.save_file_path):
            df.to_csv(self.save_file_path, mode='a', encoding='utf-8', header=None, index=False)
        else:
            df.to_csv(self.save_file_path, mode='a', encoding='utf-8', index=False)
            print('已创建' + self.save_file_path)
        self.item_datas = []


for category in ['pistol', 'rifle', 'smg', 'shotgun', 'machinegun']: #刀拳套贴花没爬:
    save_file_path = '{}.csv'.format(category)
    B = BuffCsgo(category, save_file_path, 1614323440986, 200)
    total_page = B.get_total_page()
    print(f'当前{category}类目共有{total_page}页')
    B.get_page()
