import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import talib

df=ts.get_hist_data('600848',start='2015-01-01',end='2015-12-31')
df=df.sort_index()
df.index=pd.to_datetime(df.index,format='%Y-%m-%d')
#收市股价
close= df.close
highPrice=df.high
lowPrice=df.low
#每天的股价变动百分率
ret=df.p_change/100
 # 调用talib计算MACD指标
df['k'],df['d']=talib.STOCH(np.array(highPrice),np.array(lowPrice),np.array(close),
  fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)

sig_k=df.k
sig_d=df.d
sig_j=df.k*3-df.d*2

kdSignal=pd.Series(0,index=close.index)
#策略 k值大于d值，并且k小于85，d大于20
for i in range(10,len(close)):
    if sig_k[i]>sig_d[i] and sig_d[i]>=20:
        kdSignal[i]=1

kdTrade=kdSignal.shift(1).dropna()
kdSignalRet=ret*kdTrade.dropna()


#累积收益表现
#股票累积收益率
cumStock=np.cumprod(1+ret[kdSignalRet.index[0]:])-1
#策略累积收益率
cumTrade=np.cumprod(1+kdSignalRet)-1
plt.rcParams['font.sans-serif']=['SimHei']
plt.plot(cumStock,label="cumStock",color='k')
plt.plot(cumTrade,label="kdjTrade",color='r',linestyle=':')
plt.title("股票累积收益率与kdj策略收益率")
plt.legend()
plt.show()