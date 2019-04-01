'''
This code is used to convert Time Series data into weekly format.
'''

import pandas as pd
import numpy as np
import os

exception=[1,3,6]
print( os.listdir('NAV Time Series/'))
for no,file in enumerate(os.listdir('NAV Time Series/')):
	data=pd.read_csv('NAV Time Series/'+file,delimiter=',',parse_dates=['Dates'])
	print( data.shape)
	print( file)
	new=pd.DataFrame(columns=data.columns,index=[i for i in range(0,400)])
	for col in range(1,data.shape[1]):
		print( col)
		new_index=1
		i=5
		sum=0.0
		count=0
		if(no in exception):
			for k in range(0,6):
				if(pd.isnull(data.iloc[k,col])):
					continue
				count+=1
				sum+=data.iloc[k,col]
		else:	
			for k in range(0,5):
				if(pd.isnull(data.iloc[k,col])):
					continue
				count+=1
				sum+=data.iloc[k,col]
		new.iloc[0,0]=data.iloc[0,0]
		if(count!=0):
			new.iloc[0,col]=sum/count
		else:
			new.iloc[0,col]=np.nan
		while(i<data.shape[0]):
			j=0
			sum=0.0
			count=0
			# new=pd.DataFrame(columns=data.columns,index=[1])
			while(i+j<data.shape[0] and data.iloc[i+j,0]-data.iloc[i,0]<pd.Timedelta('7 days')):
				if(pd.isnull(data.iloc[i+j,col])):
					j+=1
					continue
				sum+=data.iloc[i+j,col]
				count+=1
				j+=1
			if(col==1):
				new.iloc[new_index,0]=data.iloc[i,0]
			if(count!=0):
				new.iloc[new_index,col]=sum/count
			else:
				new.iloc[new_index,col]=np.nan
			new_index+=1
			i+=j
			# print new_index
		# print new
	new.to_csv(file,index=False)