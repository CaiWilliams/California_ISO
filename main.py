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

# data_dirs = os.listdir(data_dir)
# data_dirs = [os.path.join(data_dir,dir) for dir in data_dirs if '.xml.zip' in dir]
# data_dirs = [pd.read_xml(dir,compression='zip') for dir in data_dirs]
# data = pd.concat(data_dirs)
# print(data)
#data = pd.concat([data,data_2])

data = data[data['RENEWABLE_TYPE'] == 'Solar']
data = data.drop(columns=['LABEL','XML_DATA_ITEM','MARKET_RUN_ID_POS','RENEW_POS','MARKET_RUN_ID','GROUP','RENEWABLE_TYPE','INTERVALSTARTTIME_GMT','INTERVALENDTIME_GMT','OPR_INTERVAL'])

data['OPR_HR'].values[data['OPR_HR']>=24] = 0
Date = data['OPR_DT'] +' '+ data['OPR_HR'].astype(str)+':00:00'
data = data.set_index(pd.DatetimeIndex(Date))
data = data.drop(columns=['OPR_DT','OPR_HR'])
print(data)
data = data.groupby(data.index.date)['MW'].sum()/1e3
plt.plot(data)
plt.show()