import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats

files = os.listdir('/Users/wcoupe/Documents/Reports/opsSummaryDirectory/tacticalStitched/v0.2')

dateVecIADS = []
dateVecTrigger = []

str0 = '201712'
str2 = '12/'
#for i in range(3,4):
for i in range(3,32):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
	dateVecTrigger.append(str2 + str(i) + '/17')


str0 = '201801'
str2 = '1/'
for i in range(1,25):
	if i != 17:
		if i < 10:
			dateVecIADS.append(str0 + '0' + str(i) )
		else:
			dateVecIADS.append(str0 + str(i) )
		dateVecTrigger.append(str2 + str(i) + '/18')

#dfFlightSpecifc = pd.read_csv('data/0.6/20180106_flight_specific_0.6.csv' , sep=',' , index_col=False)
# dateVecIADS = ['20171205']
# dateVecTrigger= ['12/5/17']
#dfTacticalSummary = pd.read_csv('~/Documents/Reports/opsSummaryDirectory/tacticalStitched/v0.2/tactical.v0.2._KCLT.flightSummary.v0.3.20171205.09.00-20171206.09.00.20171221.05.10.11.csv' )
#dfTrigger = pd.read_csv('~/Documents/iads/CleanTriggerData.v1.csv', sep=',' , index_col=False)

dfTrigger = pd.read_csv('~/Desktop/testFormat.csv' , sep=',' , index_col=False)


cols = ['actualOff', 'actualOUT' , 'Total Excess Taxi' , 'Ramp Excess Taxi' , 'AMA Excess Taxi' , 'predictedDelay','controlled' ,'target','Gate Hold']

### define DFStats data frame



#df.loc[idx] = vecInclude
preFixAMA = []
postFixAMA = []

runwayVec = ['18L' , '18C' , '36R' , '36C']



for date in range(len(dateVecIADS)):
	dfFlightSpecifc = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_flight_specific_0.6.csv' , sep=',' , index_col=False)
	print(dateVecIADS[date])
	beforeFixFlag = False
	afterFixFlag = False
	if pd.Timestamp(dateVecIADS[date] + ' 00:00:00') < pd.Timestamp('2017-12-17 00:00:00'):
		beforeFixFlag = True
	if pd.Timestamp(dateVecIADS[date] + ' 00:00:00') > pd.Timestamp('2018-01-10 00:00:00'):
		afterFixFlag = True

	for tacticalFile in range(len(files)):
		strFind = '_KCLT.flightSummary.v0.3.' + dateVecIADS[date]
		if strFind in files[tacticalFile]:
			dfTacticalSummary = pd.read_csv('~/Documents/Reports/opsSummaryDirectory/tacticalStitched/v0.2/' + files[tacticalFile] , sep=',' , index_col=False)


	getTarget = True
	for idx in range(len(dfTrigger['date'])):
		if getTarget:
			if str(dfTrigger['date'][idx]) == dateVecTrigger[date]:
				targetValue = dfTrigger['time-based-target-excess-queue-minutes'][idx]
				getTarget = False

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
						#print(dfTemp)
						
						realizedHold = 0

						if dfTemp['Tactical_Controlled_Flight'][dfTemp.index[0]] not in ['APREQ_DEPARTURE' , 'EDCT_DEPARTURE']:
							if dfTemp['Tactical_Exempt_Flight'][dfTemp.index[0]] != 'EXEMPT_DEPARTURE':
								if str(dfTemp['Held_While_Metering_On_Scheduled_Runway'][dfTemp.index[0]]) == 'True':
									if str(dfTemp['Held_With_Non_Zero_Advisory'][dfTemp.index[0]]) == 'True':
										realizedHold = dfTemp['Total_Realized_Hold'][dfTemp.index[0]] / float(60)
										if realizedHold < 0:
											realizedHold = 0

										tVal = dfFlightSpecifc['Pos_Excess_AMA_Taxi_Out'][flight]
										if str(tVal) != 'nan':
											if beforeFixFlag:
												preFixAMA.append(tVal/float(60))
											
											if afterFixFlag:
												postFixAMA.append(tVal/float(60))

						# if str(realizedGate Hold) == 'nan':
						# 	realizedGate Hold = 0



						dataVec = [actualOff,actualOUT,totalExcess,excessRamp,excessAMA,predictedDelay,controlled,targetValue,realizedHold]
						idx+=1
						df.loc[idx] = dataVec



		dfSorted0 = df.sort_values(by=['actualOff'])
		dfSorted = dfSorted0.reset_index(drop=True)
		testdf = df.sort_values(by=['Gate Hold'])
		print(testdf)
		if idx>5:
			ax = dfSorted.plot(x='actualOff',y='target',figsize=(14,12))
			#dfSorted.plot.bar(x='actualOff',y=['Total Excess Taxi', 'AMA Excess Taxi','Ramp Excess Taxi'], color = ['cyan' , 'magenta' , 'grey'],alpha=0.6,ax=ax)
			dfSorted.plot.bar(x='actualOff',y=['AMA Excess Taxi','Ramp Excess Taxi'],width=0.3, position = -0.25, color = [ 'magenta' , 'grey'],alpha=0.6,ax=ax)
			dfSorted.plot.bar(x='actualOff',y=['Total Excess Taxi','Gate Hold'], width = 0.15, position = 0.5, stacked=True, color = [ 'cyan' , 'red'],alpha=0.6,ax=ax)
			plt.title('Runway ' + runwayVec[rwy] + ' ' + dateVecIADS[date])
			plt.ylabel('Excess Taxi Time [Minutes]')
			plt.xlabel('Actuall Off Time [EST]')
			plt.ylim([0,30])
			plt.tight_layout()
			#plt.savefig('figs/flightSpecificDelay/' + runwayVec[rwy]+dateVecIADS[date] + '.png')
			plt.savefig('figs/flightSpecificDelay/v2/' + runwayVec[rwy]+dateVecIADS[date] + '.png')


print(np.mean(preFixAMA))
print(np.mean(postFixAMA))


