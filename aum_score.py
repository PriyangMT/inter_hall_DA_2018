'''
This code is used to determine the %percent of investment in each sector by each MFH.
'''
import numpy as np
from numpy import genfromtxt

MFH_percentage = ["HDFC_percentage.csv","Aditya_percentage.csv","ICICI_percentage.csv","reliance_percentage.csv","SBI_percentage.csv","Sundaram_percentage.csv","Tata_percentage.csv","UTI_percentage.csv"] 
MFH_aum = ["hdfc.csv","aditya.csv","icici.csv","reliance.csv","sbi.csv","sundaram.csv","tata.csv","uti.csv"]


for MFH in range(0,8):
	Percentage_data = np.genfromtxt(MFH_percentage[MFH], delimiter = ',')
	aum_data = np.genfromtxt(MFH_aum[MFH], delimiter = ',')

	r = min(Percentage_data.shape[0],aum_data.shape[0])
	# aum = np.zeros((r,aum_data.shape[1]))
	aum = np.zeros((r,1))
	percentage =np.zeros((r,Percentage_data.shape[1]-1))

	temp = 1
	count = 0
	for i in range(1,aum_data.shape[0]):
		for j in range(temp,Percentage_data.shape[0]):
			if(aum_data[i][0] == Percentage_data[j][0]):
				temp = j
				# aum[count] = aum_data[i]
				aum[count] = aum_data[i][-1]
				percentage[count] = Percentage_data[j][1:Percentage_data.shape[1]]
				count += 1
				break 
    where_are_NaNs = np.isnan(percentage)
    percentage[where_are_NaNs] = 0
    where_are_NaNs = np.isnan(aum)
    aum[where_are_NaNs] = 0
    aum = np.transpose(aum)
    aum_total = np.sum(aum)
    x = np.dot(aum,(percentage/100))/aum_total
    print(x.shape)
    np.savetxt('aum_score_'+MFH_aum[MFH], x, delimiter=',')
