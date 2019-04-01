'''
This code is used to create buckets of MFHs.
'''

import os
import glob
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import normalize

def comp_na(series):    #Function fill NA by previous value
    mask=(np.isnan(series))
    for i in range(len(mask)):
        if mask[i]==True:
            series[i]=series[i-1]

def annualise(daily_returns):
    #annual=(np.power((1+daily_returns.mean()),250)-1)
    annual=(np.prod(1+daily_returns))**0.2-1
    return (annual)

def alpha_beta(series):
    series.dropna(inplace=True)
    m=[]
    s=[]
    MF_returns=np.log(series/series.shift(1))
    std=MF_returns.std()
    market_returns=np.log(market.Close/market.Close.shift(1))
    MF_returns.dropna(inplace=True)
    market_returns.dropna(inplace=True)
    market_return=annualise(market_returns) #annualise returns
    MF_return=annualise(MF_returns) #annualise returns
    for date in market_returns.index.tolist():
       if date in MF_returns.index.tolist():
           m.append(market_returns.loc[date])
           s.append(MF_returns.loc[date])
    beta=np.cov(s,m)[0,1]/np.var(m)
    risk_free_rate=0.07
    alpha=MF_return-(beta*(market_return-risk_free_rate))-risk_free_rate
    return (alpha,beta,std,MF_return)

def bucket_cal(weights,returns,risk):
    weighted_return=0
    weighted_risk=0
    prop=0
    check=0
    for mf in returns.index.tolist():
        if(mf not in weights.index.tolist()):
            continue
        if (weights[mf]=="#VALUE!"):
            continue
        print (mf)
        weighted_return+=(np.float64(weights[mf])*returns[mf])
        weighted_risk+=(np.float64(weights[mf])*risk[mf])
        check+=np.float64(weights[mf])
        prop+=np.float64(weights[mf])
    return (weighted_return/check,weighted_risk,prop)

path=os.getcwd()
csv_files=glob.glob(path+"\*.csv")
market=pd.read_csv(path+"\\Nifty.csv")
market.index=market.iloc[:,0]
market.drop(market.columns[0],inplace=True,axis=1)
if path+"\\buckets.csv" in csv_files:
    csv_files.remove(path+"\\buckets.csv")
if path+"\\Nifty.csv" in csv_files:
    csv_files.remove(path+"\\Nifty.csv")

#MFH_dict={} #All MFHs level
final_df=pd.DataFrame(columns=("MFH","scheme","std","beta","alpha","return"))

for name in csv_files:
    csv=pd.read_csv(name)
    csv.index=csv.iloc[:,0]
    csv.drop(csv.columns[0],inplace=True,axis=1)
    #csv.apply(comp_na,axis=0)
    temp_df=pd.DataFrame(columns=("MFH","scheme","std","beta","alpha","return"))
    for MF in csv.columns:
        (alpha,beta,std,returns)=alpha_beta(csv[[MF]].iloc[:,0])
        temp_df['MFH']=[(name.split("\\")[-1]).split(".")[0]]
        temp_df['scheme']=[MF]
        temp_df['std']=[std]
        temp_df['return']=[returns]
        temp_df['beta']=[beta]
        temp_df['alpha']=[alpha]
        final_df=final_df.append(temp_df,ignore_index=True)
    
#Make Buckets
k=4
for x in ["std","alpha","beta"]:
    final_df.drop(final_df.index[np.isnan(final_df[x])],axis=0,inplace=True)
    final_df["norm_"+x] =  final_df[x]/ np.linalg.norm(final_df[x])
kmeans = KMeans(n_clusters=k, random_state=1).fit(final_df[["norm_std","norm_alpha","norm_beta"]].values)
final_df['bucket']=kmeans.labels_

fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(111, projection='3d')
x = np.array(final_df['std'])
y = np.array(final_df['alpha'])
z = np.array(final_df['beta'])
ax.scatter(x,y,z, marker="x", c=final_df["bucket"], s=25)
plt.xlabel("Std")
plt.ylabel("alpha")
#plt.zlabel("beta")
plt.savefig("{}_buckets-(rm).jpg".format(k))

for x in range(0,k):
    print ("cluster{}".format(x))
    print (np.mean(final_df[(final_df['bucket']==x)][["std","alpha","beta","return"]]))
    print ("No.={}\n".format(sum((final_df['bucket']==x))))

agg_df=pd.DataFrame(columns=("MFH","Return","Risk","bucket")) 
temp_df=pd.DataFrame(columns=("MFH","Return","Risk","bucket"))
weight_files=glob.glob(path+"\\weights\*.csv")
for name in final_df['MFH'].unique().tolist():
    a=[(name.split("Time")[0] in x) for x in weight_files]
    weight_name=weight_files[a.index(True)]
    weight_file=pd.read_csv(weight_name)
    temp=final_df[final_df['MFH']==name]
    weight_file["SchemeCode"]=weight_file["SchemeCode"].apply(str)
    weight_file.index=weight_file["SchemeCode"]
    temp["Scheme Code"]=temp["Scheme Code"].apply(str)
    for x in [0,2,3]:
         temp.index=temp['Scheme Code']
         #weight_file.index = weight_file['SchemeCode']
         mask=(temp['bucket']==x)
         temp_df["MFH"]=[name]
         w_return,w_risk, prop=bucket_cal(weight_file['weight'],
                                          temp[mask]["return"], 
                                          temp[mask]["std"])
         temp_df['Risk']=[w_risk]
         temp_df['Return']=[w_return]
         temp_df["bucket"]=[x]
         temp_df["Proportion"] = prop
         agg_df=agg_df.append(temp_df)

final_df.to_csv("buckets_rm.csv",index=False)
agg_df.to_csv("bucket_details_rm.csv",index=False)
