import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats

excludeEarlyDays = True

#'N_BE/A/T=36C'
utilization = 'N_BE/A/T=36C_V1'
stSave = utilization.replace('/','-')

if excludeEarlyDays:
	stSaveFig = 'figs/Threshold' + stSave + 'FilterDays.png'
else:	
	stSaveFig = 'figs/Threshold' + stSave + '.png'

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
for i in range(1,25):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )


excludeVec = ['20171113','20171101','20171226','20171227', '20180106', '20180110',  '20180111',  '20180115' , '20180117','20180112']

if excludeEarlyDays == True:
	excludeVec.append('20171129')
	excludeVec.append('20171130')

	str0 = '201712'
	for i in range(1,17):
		if i < 10:
			excludeVec.append(str0 + '0' + str(i) )
		else:
			excludeVec.append(str0 + str(i) )


plt.figure(1,figsize=(10,6))
#ThresholdVec = [16,20,24]
ThresholdVec = [16]

def plotAbove(ThresholdVec):
	countMeterStart = 0
	xTickVec = []
	aboveThresholdVec = np.zeros((len(ThresholdVec),len(dateVecIADS)))
	binaryVec = np.zeros(len(dateVecIADS))
	#aboveThresholdVec = {}
	for date in range(len(dateVecIADS)):
		# xTickVec.append(dateVecIADS[date])
		try:
			dfIads = pd.read_csv('data/0.6/' + dateVecIADS[date]+ '_flight_specific_0.6.csv' , sep=',' , index_col=False)
			dfIadsSummary = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_iads_summary_0.6.csv' , sep=',' , index_col=False)
		
			

			bankIndex = -1
			for j in range(len(dfIadsSummary['Broader Bank Number'])):
				if str(dfIadsSummary['Broader Bank Number'][j]) == str(2.0):
					bankIndex = j

			if dateVecIADS[date] not in excludeVec:
				#if True:
				if str(dfIadsSummary['Runway Utilization At Start'][bankIndex]) == 'N_BE/A/T=36C':
					if str(dfIadsSummary['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]) != 'nan':
						if dateVecIADS[date] == '20171217':
							meterStartIndex = countMeterStart
						countMeterStart+=1
						xTickVec.append(dateVecIADS[date])
						binaryVec[date] = 1
						print(dateVecIADS[date])
						for flight in range(len(dfIads['gufi'])):
							if str(dfIads['Bank Number'][flight]) == str(2.0):
								if str(dfIads['Pos_Excess_AMA_Taxi_Out'][flight]) != 'nan':
									if str(dfIads['apreq_final'][flight]) == 'nan':
										for val in range(len(ThresholdVec)):
											if (dfIads['Pos_Excess_AMA_Taxi_Out'][flight] / float(60)) > ThresholdVec[val]:
												aboveThresholdVec[val,date] +=1

												# if dateVecIADS[date] == '20171206':
												# 	print(dfIads['gufi'][flight])
										

		except:
			print('Bad Data Day ' + dateVecIADS[date])

	for val in range(len(ThresholdVec)):
		pltVec = []
		for date in range(len(dateVecIADS)):
			if binaryVec[date] == 1:
				pltVec.append(aboveThresholdVec[val,date]) 
		plt.plot(pltVec,'-*',label='Threshold = ' + str(ThresholdVec[val]))
	
	plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90)
	plt.ylabel

	return meterStartIndex

meterStartIndex = plotAbove(ThresholdVec)
plt.plot([meterStartIndex,meterStartIndex] , [0,21] , '--' , color = 'grey' , alpha =0.5, label = 'Metering ON / OFF')
plt.title('Utilization: ' + utilization)
plt.ylabel('Number of Aircraft Above Threshold')
plt.ylim([0,21])
plt.legend()
plt.tight_layout()
plt.savefig(stSaveFig)
plt.show()

		






















