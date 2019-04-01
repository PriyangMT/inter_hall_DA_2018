'''
Code is used to convert the unstructured data to structured data.
'''

import os
import glob
import pandas as pd
import numpy as np

path=os.getcwd()
file_names=glob.glob(path+"\*.csv")

def my_sum(x):
    x.dropna(inplace=True)
    return (np.sum(x))
    
month=["Mar","Jun","Sep","Dec"]
year=[str(x) for x in range(13,18)]
col_names=["Scheme Name","Scheme Code"]
for i in year:
    for j in month:
        col_names.append(j+"-"+i)
col_names=tuple(col_names)        
structured=pd.DataFrame(columns=col_names)
AUM_size = {}
for name in file_names:         
    unstructured=pd.read_csv(name)
    for col in col_names:
        structured[[col]]=unstructured[[col]]
    #structured.index=structured["Scheme Name"]
    #structured.drop(["Scheme Name"], axis=1)
    structured.to_csv(path+"\\structured files\\"+name.split("\\")[-1], index=False)   