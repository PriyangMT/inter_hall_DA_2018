'''
This code is used to create a file named Anomalies containing GDP, CPI, %change of NIFTY, %change of USD.
'''

import pandas as pd
import numpy as np
import glob
import datetime
from datetime import datetime

lof=glob.glob("MEF/*.csv")

#Anomalies
#SENSEX:10- 1.477, 5-1.87
#Excha_rate($ to):10-0.66, 5-0.87 , 0.9
#Excha_rate(pound to ):10-1.02, 5-1.25
#NIFTY:10-1.52 , 5-1.85, 2.3,21775
ano_NIF=2.3/100
ano_do=0.9/100


a=["Exchange" in x for x in lof]
df_ex=pd.read_csv(lof[a.index(True)])
df_ex['Date']=pd.to_datetime(df_ex['Date'])
df_ex['pcUSD']=(df_ex['US Dollar']/df_ex['US Dollar'].shift(1))-1
df_ex=df_ex.dropna(how='all',axis=0)

a=["index" in x for x in lof]
df_nifty=pd.read_csv(lof[a.index(True)])
df_nifty['Date']=pd.to_datetime(df_nifty['Date'])
df_nifty['pcNIF']=(df_nifty['Close']/df_nifty['Close'].shift(1))-1
df_nifty=df_nifty.dropna(how='all',axis=0)

date=[]
a=["CPI" in x for x in lof]
df_cpi=pd.read_csv(lof[a.index(True)])
df_cpi['Date']=pd.to_datetime(df_cpi['Date'])
for i in df_cpi['Date'].unique():
    date.append(i)


a=["GDP" in x for x in lof]
df_gdp=pd.read_csv(lof[a.index(True)])
df_gdp['GDP']=(df_gdp['Total Gross value added at basic price']/df_gdp['Total Gross value added at basic price'].shift(1))-1
df_gdp=df_gdp.dropna(how="any",subset=['GDP'],axis=0)
df_gdp['Date']=pd.to_datetime(df_gdp['Date'])
for i in df_gdp['Date'].unique():
    if i not in date:
        date.append(i)


er=df_ex.loc[(df_ex['pcUSD']>=ano_do) | (df_ex['pcUSD']<=-ano_do)]
for i in er['Date'].unique():
    if i not in date:
        date.append(i)

mr=df_nifty.loc[(df_nifty['pcNIF']>=ano_NIF) | (df_nifty['pcNIF']<=-ano_NIF)]
for i in mr['Date'].unique():
    if i not in date:
        date.append(i)

fin=pd.DataFrame(columns=['Date','GDP','CPI','pcNIF','pcUSD'])
#date.sort()
#temp=pd.DataFrame(columns=['Date','GDP','CPI','pcNIF','pcUSD'])
for i in range(len(date)):
    temp=pd.DataFrame(columns=['Date','GDP','CPI','pcNIF','pcUSD'])
    temp["Date"]=[date[i]]
    if date[i] in df_cpi['Date'].unique():
        temp['CPI']=[df_cpi['Inflation Y-o-Y'][df_cpi['Date']==date[i]].values[0]]
    if date[i] in df_ex['Date'].unique():
        temp['pcUSD']=[df_ex['pcUSD'][df_ex['Date']==date[i]].values[0]]
    if date[i] in df_gdp['Date'].unique():
        temp['GDP']=[df_gdp['GDP'][df_gdp['Date']==date[i]].values[0]]
    if date[i] in df_nifty['Date'].unique():
        temp['pcNIF']=[df_nifty['pcNIF'][df_nifty['Date']==date[i]].values[0]]
    fin=fin.append(temp)

fin=fin.replace(to_replace=np.nan,value=0)        
fin.to_csv('MEF/Anomalies.csv',index=False)

