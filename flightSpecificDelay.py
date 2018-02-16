import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats

dateVecIADS = []
dateVecTrigger = []

# str0 = '201712'
# str2 = '12/'
# #for i in range(3,4):
# for i in range(3,32):
# 	if i < 10:
# 		dateVecIADS.append(str0 + '0' + str(i) )
# 	else:
# 		dateVecIADS.append(str0 + str(i) )
# 	dateVecTrigger.append(str2 + str(i) + '/17')


# str0 = '201801'
# str2 = '1/'
# for i in range(1,25):
# 	if i != 17:
# 		if i < 10:
# 			dateVecIADS.append(str0 + '0' + str(i) )
# 		else:
# 			dateVecIADS.append(str0 + str(i) )
# 		dateVecTrigger.append(str2 + str(i) + '/18')

#dfFlightSpecifc = pd.read_csv('data/0.6/20180106_flight_specific_0.6.csv' , sep=',' , index_col=False)
dateVecIADS = ['20180106']
dateVecTrigger= ['1/6/18']
dfTacticalSummary = pd.read_csv('~/Documents/Reports/opsSummaryDirectory/tacticalStitched/v0.2/tactical.v0.2._KCLT.flightSummary.v0.3.20180106.09.00-20180107.08.59.20180107.15.15.04.csv' )
dfTrigger = pd.read_csv('~/Documents/iads/CleanTriggerData.v1.csv', sep=',' , index_col=False)

cols = ['actualOff', 'actualOUT' , 'totalDelay' , 'rampDelay' , 'amaDelay' , 'predictedDelay','controlled' ,'target','hold']

### define DFStats data frame



#df.loc[idx] = vecInclude

runwayVec = ['18L' , '18C' , '36R' , '36C']

for date in range(len(dateVecIADS)):
	dfFlightSpecifc = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_flight_specific_0.6.csv' , sep=',' , index_col=False)
	print(dateVecIADS[date])

	findTarget = True
	for k in range(len(dfTrigger['Date'])):
		if str(dfTrigger['Date'][k]) == str(dateVecTrigger[date]):
			if findTarget:
				targetValue = dfTrigger['Target_Set_By_Controllers'][k]
				findTarget = False

	for rwy in range(len(runwayVec)):
		df = pd.DataFrame(np.empty((1,len(cols)), dtype=object),columns=cols)
		idx = -1
		for flight in range(len(dfFlightSpecifc['gufi'])):
			if str(dfFlightSpecifc['isArrival'][flight]) == 'False':
				if str(dfFlightSpecifc['Broader Bank Number'][flight]) == str(2.0):
					if dfFlightSpecifc['Surface_Model_Actual_Departure_Runway'][flight] == runwayVec[rwy]:	
						
						excessRamp0 = (dfFlightSpecifc['Actual_Ramp_Taxi_Out_Time'][flight] - dfFlightSpecifc['Ramp_Taxi_Pred_at_Ramp_Taxi_Start'][flight]) / float(60)
						excessRamp = max([0,excessRamp0])

						excessAMA = dfFlightSpecifc['Pos_Excess_AMA_Taxi_Out'][flight] / float(60)
						totalExcess = (excessRamp + excessAMA) 
						actualOff = dfFlightSpecifc['Actual_OFF_Time_Start_of_Roll'][flight]
						actualOUT = dfFlightSpecifc['Actual_OUT'][flight]
						predictedDelay = 0
						
						if str(dfFlightSpecifc['apreq_final'][flight]) != 'nan':
							controlled = 1
						else:
							controlled = 0

						dfTemp = dfTacticalSummary[ dfTacticalSummary['gufi'] == dfFlightSpecifc['gufi'][flight] ]
						try:
							realizedHold = dfTemp['Total_Realized_Hold'][0]
						except:
							realizedHold = 'nan'

						dataVec = [actualOff,actualOUT,totalExcess,excessRamp,excessAMA,predictedDelay,controlled,targetValue,realizedHold]
						idx+=1
						df.loc[idx] = dataVec



		dfSorted0 = df.sort_values(by=['actualOff'])
		dfSorted = dfSorted0.reset_index(drop=True)
		#print(dfSorted)
		if idx>5:
			ax = dfSorted.plot(x='actualOff',y='target',figsize=(14,12))
			dfSorted.plot.bar(x='actualOff',y=['totalDelay', 'amaDelay','rampDelay'], color = ['cyan' , 'magenta' , 'grey'],alpha=0.6,ax=ax)
			plt.title('Runway ' + runwayVec[rwy] + ' ' + dateVecIADS[date])
			plt.ylim([0,30])
			plt.tight_layout()
			#plt.savefig('figs/flightSpecificDelay/' + runwayVec[rwy]+dateVecIADS[date] + '.png')

plt.show()