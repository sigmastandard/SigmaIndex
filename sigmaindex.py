import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pylab as pl
import tushare as ts
from datetime import datetime
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

btcma = pd.DataFrame(cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=3000),columns=['market_caps'])
btcmc = btcma['market_caps'].apply(lambda x: pd.Series(x))
btcmc.columns = ['date','btc_market_caps']
btcmc['date'] = pd.to_datetime(btcmc['date'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

ethma = pd.DataFrame(cg.get_coin_market_chart_by_id(id='ethereum', vs_currency='usd', days=3000),columns=['market_caps'])
ethmc = ethma['market_caps'].apply(lambda x: pd.Series(x))
ethmc.columns = ['eth_date','eth_market_caps']
ethmc['eth_date'] = pd.to_datetime(ethmc['eth_date'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

usdtma = pd.DataFrame(cg.get_coin_market_chart_by_id(id='tether', vs_currency='usd', days=3000),columns=['market_caps'])
usdtmc = usdtma['market_caps'].apply(lambda x: pd.Series(x))
usdtmc.columns = ['usdt_date','usdt_market_caps']
usdtmc['usdt_date'] = pd.to_datetime(usdtmc['usdt_date'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

usdcma = pd.DataFrame(cg.get_coin_market_chart_by_id(id='usd-coin', vs_currency='usd', days=3000),columns=['market_caps'])
usdcmc = usdcma['market_caps'].apply(lambda x: pd.Series(x))
usdcmc.columns = ['usdc_date','usdc_market_caps']
usdcmc['usdc_date'] = pd.to_datetime(usdcmc['usdc_date'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

busdma = pd.DataFrame(cg.get_coin_market_chart_by_id(id='binance-usd', vs_currency='usd', days=3000),columns=['market_caps'])
busdmc = busdma['market_caps'].apply(lambda x: pd.Series(x))
busdmc.columns = ['busd_date','busd_market_caps']
busdmc['busd_date'] = pd.to_datetime(busdmc['busd_date'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

daima = pd.DataFrame(cg.get_coin_market_chart_by_id(id='dai', vs_currency='usd', days=3000),columns=['market_caps'])
daimc = daima['market_caps'].apply(lambda x: pd.Series(x))
daimc.columns = ['dai_date','dai_market_caps']
daimc['dai_date'] = pd.to_datetime(daimc['dai_date'], unit='ms').dt.strftime('%Y-%m-%d %H:%M')

# 合并所有成分的dateframe
index = pd.concat([btcmc, ethmc,usdtmc,usdcmc,busdmc,daimc ], axis=1, sort=False)


# 处理空值，向下移动

index['eth_date']=index['eth_date'].shift(index['eth_date'].isna().sum())
index['eth_market_caps']=index['eth_market_caps'].shift(index['eth_market_caps'].isna().sum())
index['usdt_date']=index['usdt_date'].shift(index['usdt_date'].isna().sum())
index['usdt_market_caps']=index['usdt_market_caps'].shift(index['usdt_market_caps'].isna().sum())
index['usdc_date']=index['usdc_date'].shift(index['usdc_date'].isna().sum())
index['usdc_market_caps']=index['usdc_market_caps'].shift(index['usdc_market_caps'].isna().sum())
index['busd_date']=index['busd_date'].shift(index['busd_date'].isna().sum())
index['busd_market_caps']=index['busd_market_caps'].shift(index['busd_market_caps'].isna().sum())
index['dai_date']=index['dai_date'].shift(index['dai_date'].isna().sum())
index['dai_market_caps']=index['dai_market_caps'].shift(index['dai_date'].isna().sum())
# 空值处理为0
index=index.fillna(0)
# 删除多余时间列
index=index.drop(columns=['eth_date', 'usdt_date', 'usdc_date', 'busd_date', 'dai_date'])
# 设定变量date为index
index.set_index("date", inplace=True)
# 产出marketcap函数
index['marketcap']=index['btc_market_caps']+index['eth_market_caps']+index['usdt_market_caps']+index['usdc_market_caps']+index['busd_market_caps']+index['dai_market_caps']
index['sigma']=index['marketcap']/1454000000000
