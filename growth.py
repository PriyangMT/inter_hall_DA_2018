'''
This code is used to calculate growth of the last four weeks of NAV prices from the output
of LSTM network. This then multiplied with AUM proportion to yield aggrigate growth of MFHs.
'''

import numpy as np 
from numpy import genfromtxt
import glob
import pandas as pd
import os

folder_list=os.listdir("LSTM_out")
weight_list=glob.glob("weights\*.csv")
final_df=pd.DataFrame(columns=("MFH","NAV_growth_score"))
for MFH_name in folder_list:
    temp_df=pd.DataFrame(columns=("MFH","NAV_growth_score"))
    temp_df['MFH']=[MFH_name.split("Time")[0]]
    file_list=glob.glob("LSTM_out\{}\*.csv".format(MFH_name))
    a=[MFH_name.split("Time")[0] in x for x in weight_list]
    weight_file=pd.read_csv(weight_list[a.index(True)])
    growth=0
    weight_sum=0
    for file in file_list:
        mf=pd.read_csv(file)
        scheme=file.split("\\")[2].split('.')[0]
        if scheme in weight_file.SchemeCode.tolist():
            if (weight_file['weight'][weight_file.SchemeCode==scheme].values[0]!='#VALUE!'):
                weight=np.float64(weight_file['weight'][weight_file.SchemeCode==scheme].values[0])
        weight_sum=weight_sum+weight
        last_5=mf.iloc[-5:,0]
        last_5=1+np.log(last_5/last_5.shift(1))
        last_5.dropna(inplace=True)
        growth=growth+weight*(np.prod(last_5.values)**0.25-1)
    temp_df["NAV_growth_score"]=[growth/weight_sum]
    final_df=final_df.append(temp_df)
    

final_df.to_csv("NAV_growth_score.csv")

#future/past
# min = small something
# max = large something

# result = np.zeros((max - min + 1))

# for j in range(min,max+1):

# np.savetxt("result.csv",result,delimiter = ',')




