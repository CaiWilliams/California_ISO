import pandas as pd
import zipfile
import numpy as np
import gzip
import matplotlib.pyplot as plt
import os

data_dir = os.path.join(os.getcwd(),'data')
data_dirs = os.listdir(data_dir)
data_dirs = [os.path.join(data_dir,dir) for dir in data_dirs if '.xml.zip' not in dir]
data_dirs = [pd.read_csv(dir,compression='zip') for dir in data_dirs]
data = pd.concat(data_dirs)

data = data[data['RENEWABLE_TYPE'] == 'Solar']
data = data.drop(columns=['LABEL','XML_DATA_ITEM','MARKET_RUN_ID_POS','RENEW_POS','MARKET_RUN_ID','GROUP','RENEWABLE_TYPE','INTERVALSTARTTIME_GMT','INTERVALENDTIME_GMT','OPR_INTERVAL'])

data['OPR_HR'].values[data['OPR_HR'] >= 24] = 0
Date = data['OPR_DT'] +' '+ data['OPR_HR'].astype(str)+':00:00'
data = data.set_index(pd.DatetimeIndex(Date))
data = data.drop(columns=['OPR_DT','OPR_HR'])

d = data[data['TRADING_HUB'] == 'NP15']
d = d.resample('D').sum()
plt.plot(d)

d = data[data['TRADING_HUB'] == 'ZP26']
d = d.resample('D').sum()
plt.plot(d)

plt.show()