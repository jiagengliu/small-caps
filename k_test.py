import tushare as ts
import talib
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

df=ts.get_hist_data('600848',start='2015-01-01',end='2017-12-31')
df=df.sort_index()
df.index=pd.to_datetime(df.index,format='%Y-%m-%d')

#print(df)

close= df.close
high=df.high
low=df.low
open = df.open

data= talib.CDL2CROWS(open, high, low, close)
print(np.sum(data))