# Csgo饰品 Buff商城及Steam市场的部分数据爬取
Python所写,爬虫小白的练手,代码有不少不合理的地方,望各位大佬指正
主要为了方便朋友找到合适饰品去以折扣价"充值Steam余额"来买游戏

## 获取到的字段
### Buff商城
- 饰品名称
- Buff饰品在售数量
- Buff饰品价格

### Steam市场
- 饰品名称
- Steam饰品在售数量
- Steam饰品价格

## 需要传入的信息
### Buff爬虫
- category:所需要爬取的类目 Buff将手枪机枪等分类 如pistol shotgun 等
- save_file_path:所需要存储的路径 后缀需是.csv
- _: Buff商城 类似时间戳的玩意 不太清楚这东西,可以在浏览器抓包工具XHR中获取
- price_range:价格区间 若填写200 则为10-210 400则为10-410
- cookie:另外需要在初始化请求头的函数中填入你在Buff的cookie

### Steam爬虫
- start:从第几个商品开始爬取 已设置为价格升序 6500差不多是1.5刀
- save_file_path:所需要存储的路径 后缀需是.csv
- page_num:要爬多少页 每页已设置为100个商品
不需要Cookie 但可能需要梯子

## 可获得结果
- 将获取的数据通过简单的分析后,筛选出在售数量>100 且根据当前美元汇率得出最终的倒卖比,再以倒卖比升序进行排序输出DataFrame
- 图示为2021/2/26日
![image](https://github.com/badiaog/crwal-Csgo-steam-buff/blob/main/imgs/image.png)

- 其中steam的饰品价格为美元 
- Steam当前可获收益的计算公式为:steam饰品价格 * 当天美元汇率 * 0.85(steam卖出需15%手续费)
- 倒卖比即Buff当前价格 / Steam当前可获收益 可以理解为可以以多少折扣购入steam余额


- 声明:此代码仅个人小白学习练手,代码多有不合理之处望各位指点
