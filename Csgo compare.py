import pandas as pd
import re
import requests
from lxml import etree

df_steam = pd.read_csv('./CsgoSteam.csv')
df_buffrifle = pd.read_csv('./rifle.csv')
df_buffsmg = pd.read_csv('./smg.csv')
df_buffshotgun = pd.read_csv('./shotgun.csv')
df_buffmachinegun = pd.read_csv('./machinegun.csv')
#拼接buff的数据
df_buff = pd.read_csv('./pistol.csv')
df_buff = pd.concat((df_buff,df_buffrifle,df_buffshotgun,df_buffsmg,df_buffmachinegun))
df_buff = df_buff[df_buff['Buff当前在售数量']>=100] #筛选大于100在售
#只选择steam中在售数量>=100的
df_steam = df_steam[df_steam['当前在售数量']>=100]

#横向拼接两组数据中相同名称的行
df = pd.merge(df_steam,df_buff,how='outer')
df = df.dropna()
df.drop_duplicates()

#自定义函数以找出steam当前价格中的数字
def find_nums(s):
    return re.findall(r"\d+\.?\d*",str(s))[0]
df['饰品价格'] = df['饰品价格'].map(find_nums)
df["饰品价格"] = pd.to_numeric(df["饰品价格"],errors='coerce')

#获取当前美元汇率
def get_rate():
    url = 'https://www.huilv.cc/USD_CNY/'
    response = requests.get(url = url).text
    tree = etree.HTML(response)
    rate = float(tree.xpath('//*[@id="main"]/div[1]/div[2]/span[1]/text()')[0])
    return rate

#得出倒卖比并排序
rate = get_rate()
df['steam当前可获得收益'] = df['饰品价格']*rate*0.85
df['倒卖比'] = df['Buff当前价格'] / df['steam当前可获得收益']
df.sort_values(by = '倒卖比').drop_duplicates()