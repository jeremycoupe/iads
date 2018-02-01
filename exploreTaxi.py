import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats

dateVecIADS = []
dateVecSummary = []


str0 = '201712'
str1 = '2017-12-'
for i in range(4,32):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		dateVecSummary.append(str1 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		dateVecSummary.append(str1 + str(i) )



deltaVec = []
deltaVecBank2 = []
aboveThreshold = []

dfIads = pd.read_csv('data/0.6/20180104_flight_specific_0.6.csv' , sep=',' , index_col=False)
dfSummary = pd.read_csv('~/Documents/Reports/opsSummaryDirectory/tacticalStitched/v0.2/tactical.v0.2._KCLT.flightSummary.v0.3.20180104.09.00-20180105.08.59.20180105.15.15.04.csv' , sep=',' , index_col=False)

for flight in range(len(dfSummary['gufi'])):
	print(flight)
	print(str(dfSummary['Track_Hit_Out_Time'][flight]))
	if str(dfSummary['Track_Hit_Out_Time'][flight]) == str('False'):
		print('HERE')
		if str(dfSummary['Excess_Taxi_Time'][flight]) != 'nan':
			try:
				print(dfSummary['gufi'][flight])
				summaryTaxi = dfSummary['Excess_Taxi_Time'][flight]
				dfTemp0 = dfIads[ dfIads['gufi'] == dfSummary['gufi'][flight] ]
				dfTemp = dfTemp0.reset_index(drop=True)
				iadsTaxi = dfTemp['Excess_AMA_Taxi_Out'][0] / float(60)
				delta = max([0,summaryTaxi]) - max([0,iadsTaxi])
				if str(delta) != 'nan':
					deltaVec.append(delta)
				print(delta)
				print('\n')
				if str(dfTemp['Broader Bank Number'][0]) == str(2.0):
					deltaVecBank2.append(delta)
					if delta > 14:
						aboveThreshold.append(delta)

			except:
				print(dfTemp)
				print('THERE WAS A PROBLEM WITH ' + dfSummary['gufi'][flight])

print(len(aboveThreshold))		
print(deltaVec)
print(np.mean(deltaVec))
print(np.std(deltaVec))
plt.hist(deltaVec)
plt.figure()
plt.hist(deltaVecBank2)
plt.show()

	

# dateVecIADS = []

# str0 = '201711'
# for i in range(1,31):
# 	if i < 10:
# 		dateVecIADS.append(str0 + '0' + str(i) )
# 	else:
# 		dateVecIADS.append(str0 + str(i) )


# str0 = '201712'
# for i in range(1,32):
# 	if i < 10:
# 		dateVecIADS.append(str0 + '0' + str(i) )
# 	else:
# 		dateVecIADS.append(str0 + str(i) )

# str0 = '201801'
# for i in range(1,23):
# 	if i < 10:
# 		dateVecIADS.append(str0 + '0' + str(i) )
# 	else:
# 		dateVecIADS.append(str0 + str(i) )


# excludeVec = ['20171209','20180111']

# ThresholdVec = [14,18,22]

# def plotAbove(ThresholdVec):

# 	xTickVec = []
# 	aboveThresholdVec = np.zeros((len(ThresholdVec),len(dateVecIADS)))
# 	for date in range(len(dateVecIADS)):
# 		xTickVec.append(dateVecIADS[date])
# 		try:
# 			dfIads = pd.read_csv('data/' + dateVecIADS[date]+ '_flight_specific_0.5.csv' , sep=',' , index_col=False)
# 			dfIadsSummary = pd.read_csv('data/' + dateVecIADS[date] + '_iads_summary_0.5.csv' , sep=',' , index_col=False)
		
			

# 			bankIndex = -1
# 			for j in range(len(dfIadsSummary['Broader Bank Number'])):
# 				if str(dfIadsSummary['Broader Bank Number'][j]) == str(2.0):
# 					bankIndex = j

# 			if dateVecIADS[date] not in excludeVec:
				
				
# 				print(dateVecIADS[date])
# 				for flight in range(len(dfIads['gufi'])):
# 					if str(dfIads['Broader Bank Number'][flight]) == str(2.0):
# 						if str(dfIads['Excess_AMA_Taxi_Out'][flight]) != 'nan':
# 							if str(dfIads['apreq_final'][flight]) == 'nan':
# 								for val in range(len(ThresholdVec)):
# 									if (dfIads['Excess_AMA_Taxi_Out'][flight] / float(60)) > ThresholdVec[val]:
# 										aboveThresholdVec[val,date] +=1
# 										# if dateVecIADS[date] == '20171206':
# 										# 	print(dfIads['gufi'][flight])

# 		except:
# 			print('Bad Data Day ' + dateVecIADS[date])

# 	for val in range(len(ThresholdVec)):
# 		plt.plot(aboveThresholdVec[val,:],'-*',label='Threshold = ' + str(ThresholdVec[val]))
	
# 	plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90)
# 	plt.ylabel

# plotAbove(ThresholdVec)

# plt.legend()
# plt.show()

		






















