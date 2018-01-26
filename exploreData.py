import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats

dateVecIADS = []

str0 = '201711'
for i in range(1,31):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )


str0 = '201712'
for i in range(1,32):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )

str0 = '201801'
for i in range(1,23):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )


AvgExcessAMA = []
AvgExcessRamp = []
xTickVec = []

for date in range(len(dateVecIADS)):
	try:
		dfIads = pd.read_csv('data/' + dateVecIADS[date] + '_iads_summary_0.5.csv' , sep=',' , index_col=False)
	except:
		print('Bad Data Day = ' + str(dateVecIADS[date]))
		break
	

	bankIndex = -1
	for j in range(len(dfIads['Broader Bank Number'])):
		if str(dfIads['Broader Bank Number'][j]) == str(2.0):
			bankIndex = j

	if str(dfIads['Runway Utilization At Start'][bankIndex]) == 'N_BE/A/T=36C':
		if str(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]) != 'nan':
			xTickVec.append(dateVecIADS[date])
			AvgExcessAMA.append(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
			AvgExcessRamp.append(dfIads['Positive Excess Ramp taxi-out time statistics without FAA Controlled(mean)'][bankIndex])

plt.plot(AvgExcessAMA,label='Excess AMA Taxi')
plt.plot(AvgExcessRamp,label='Excess Ramp Taxi')
plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90)
plt.show()
	