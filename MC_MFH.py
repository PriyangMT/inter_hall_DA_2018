'''
This code is used to calculate management consistency of a MFH from 
the responsive scores of their mutual funds
'''

import glob
import math
import numpy as np
import pandas as pd
import scipy

def sigi(x):
    return np.log(abs(x/(1-x)))

def sigmoid(x):
    return (1/(1+math.exp(-x)))

lof=glob.glob('AUM_scheme/*.csv')
rmfh=pd.DataFrame(columns=['MFH','responsiveness'])
fin=pd.read_csv('Responsive Score.csv')
fin['responsiveness']=fin['responsiveness']+fin['conc']
fin.dropna(how="all",subset=['responsiveness'],axis=0,inplace=True)
for i in range(len(lof)):
    df=pd.read_csv(lof[i])
    MFH=(df['SchemeName'][2].split(' '))[0]               
    df.dropna(how="all",axis=0,inplace=True)       
    last=df.columns.values       
    df.dropna(how="all",inplace=True,subset=[last[-1]],axis=0)
    if(MFH=='Aditya'): 
        MFH='AdityaBirla' 
    sch_cod=df['SchemeCode'].unique()
    temp=fin[fin['MFH']==MFH]
    num=0
    den=0
    
    for j in sch_cod:
        if j in fin['Scheme Code'].unique():
             q=df[df['SchemeCode']==j]  
             AUM=q[last[-1]].iloc[0]
             Scheme_loc = fin['Scheme Code']==j
             if(fin['responsiveness'][Scheme_loc].values[0] != np.NAN): 
                 num+=AUM*sigi(fin['responsiveness'][Scheme_loc].values[0])
                 den+=AUM 
             
    temp1=pd.DataFrame(columns=['MFH','responsiveness'])
    temp1['MFH']=[MFH]
    print (MFH)
    print (num,den,num/den)
    temp1['responsiveness']=[sigmoid(num/(den))]
    rmfh=rmfh.append(temp1,ignore_index=True)

rmfh.to_csv("RespoMFH.CSV")