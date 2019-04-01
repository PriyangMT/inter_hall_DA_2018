'''
This code is used to calculate responsiveness and concentration of mutual funds
'''

import os
import datetime
import pandas as pd
import numpy as np
import glob
import math

def sigmoid(x):
    return 1/(1+math.exp(-x))

lof=glob.glob("MutualFunds/*.csv")
Res=pd.DataFrame(columns=['Scheme Code','Responsiveness'])
fin=pd.read_csv('MEF/Anomalies.csv')
fin.index=fin["Date"]

check=2
k1=-0.03699247
k2=0.03121319
k3=0.09246126
k4=1
final_df=pd.DataFrame(columns=("MFH","Scheme Code","responsiveness"))
for name in lof:
    mfh_df=pd.read_csv(name)
    mfh_df.index=mfh_df[mfh_df.columns[0]]
    mfh_df.drop(mfh_df.columns[0],axis=1,inplace=True)
    pc_change=[]
    for mf_name in mfh_df.columns.tolist():
        mf=mfh_df[mf_name]
        mf.dropna(inplace=True)
        temp_df=pd.DataFrame(columns=("MFH","Scheme Code","responsiveness"))
        temp_df['MFH']=[name.split('\\')[-1].split('Time')[0]]
        temp_df['Scheme Code']=[mf_name]
        respo=[]
        for date in fin.index.tolist():
            if (date in mf.index.tolist()):
                i=mf.index.tolist().index(date)
                if i>(len(mf)-3):
                    break
                pc_change=(mf[i+check]-mf[i])/mf[i]
                try:
                    respo.append(sigmoid(pc_change/np.abs(k1*fin['GDP'][date]+
                                                          k2*fin['CPI'][date]+k3*fin['pcUSD'][date]+k4*fin['pcNIF'][date])))
                except:
                    respo.append(1)
                    continue
                temp_df['responsiveness']=np.mean(respo)
        final_df=final_df.append(temp_df,ignore_index=False)
        
file_list=glob.glob("MFH details\*.csv")   
MFH_names=np.unique(final_df['MFH']).tolist()
conc=[]
for name in MFH_names:
    a=[name in x for x in file_list]
    file=pd.read_csv(file_list[a.index(True)])
    file['Scheme Code']=file['Scheme Code'].apply(str)
    for code in final_df['Scheme Code'][final_df['MFH']==name].tolist():
        if code in file['Scheme Code'].tolist():
            conc.append((file['Top 5 Holdings'].loc[(file['Scheme Code'])==(code)].values[0])/100)
        else:
            conc.append(np.nan)

for i in range(len(conc)):
    conc[i]=max(0,(2-2**conc[i])/2)

final_df['conc']=conc


final_df.to_csv("Responsive Score.csv",index=False)
    
    