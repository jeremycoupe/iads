import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

dateVecIADS = []
dateVecSummary = []
dateVecTrigger = []
str0 = '201712'
str1 = '2017-12-'
str2 = '12/'
for i in range(5,32):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		dateVecSummary.append(str1 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		dateVecSummary.append(str1 + str(i) )
	dateVecTrigger.append(str2 + str(i) + '/17')

str0 = '201801'
str1 = '2018-01-'
str2 = '1/'
for i in range(1,14):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		dateVecSummary.append(str1 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		dateVecSummary.append(str1 + str(i) )
	dateVecTrigger.append(str2 + str(i) + '/18')

# print(dateVecSummary)
# print(dateVecIADS)

plt.figure(1, figsize=(12,10))
ax1 = plt.gca()
plt.figure(2, figsize=(12,10))
ax2 = plt.gca()
plt.figure(3, figsize=(12,10))
ax3 = plt.gca()
plt.figure(4, figsize=(12,10))
ax4 = plt.gca()
plt.figure(5, figsize=(12,10))
ax5 = plt.gca()
plt.figure(6, figsize=(12,10))
ax6 = plt.gca()
plt.figure(7, figsize=(12,10))
ax7 = plt.gca()
plt.figure(8, figsize=(12,10))
ax8 = plt.gca()
plt.figure(9, figsize=(12,10))
ax9 = plt.gca()

dfTrigger = pd.read_csv('~/Desktop/CleanTriggerData.v1.csv', sep=',' , index_col=False)


delayVec = []
activeDelayVec = []
sumAircraftVec = []
numPlanningVec = []
numActiveVec = []
apreqMeterVec = []
apreqVec = []
apreqExemptVec = []
excessTaxiVec = []
numHeldVec = []
for date in range(len(dateVecSummary)):
	try:
		dfIads = pd.read_csv('~/Desktop/iads/' + dateVecIADS[date] + '_iads_summary_0.2.csv' , sep=',' , index_col=False)
		dfSummary = pd.read_csv('~/Desktop/MeteringStatsV2/SummaryMeteringStats.v0.' + dateVecSummary[date] + '.csv' , sep=',' , index_col=False)

		bankIndex = -1
		for j in range(len(dfIads['Broader Bank Number'])):
			#print(dfIads['Broader Bank Number'][j])
			if str(dfIads['Broader Bank Number'][j]) == str(2.0):
				bankIndex = j
		
		delayIndexVec = []
		activeDelay = []
		planningDelay = []
		numActive = []
		numPlanning = []
		sumActivePlanning = []		
		for k in range(len(dfTrigger['Date'])):
			# print(str(dfTrigger['Date'][k]))
			# print(str(dateVecTrigger[date]))
			if str(dfTrigger['Date'][k]) == str(dateVecTrigger[date]):
				delayIndexVec.append(k)
				if str(dfTrigger['Max_Active_Delay_When_Triggered'][k]) != str('FALSE'):
					activeDelay.append(dfTrigger['Max_Active_Delay_When_Triggered'][k])
					numActive.append(dfTrigger['Number_Active_Aircraft_When_Triggered'][k])
					numPlanning.append(dfTrigger['Number_Planning_Aircraft_When_Triggered'][k])
					sumVal = int(dfTrigger['Number_Active_Aircraft_When_Triggered'][k]) + int(dfTrigger['Number_Planning_Aircraft_When_Triggered'][k])
					sumActivePlanning.append(  sumVal)
				# print('HERE')

		print(activeDelay)
	
		excessTaxi = dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]
		bank = dfIads['Broader Bank Number'][bankIndex]
		totalApreq = dfIads['Number of Total APREQs in this Bank'][bankIndex]
		totalApreqMetering = dfIads['Number of APREQ flights during surface metering were'][bankIndex]
		totalExempt = dfIads['Number of Exempt flights from surface metering were'][bankIndex]
		numberHeld = dfSummary['Number Aircraft Held For Surface Metering'][0]
		
		if str(totalApreq) == 'nan':
			totalApreq = 0

		if str(totalApreqMetering) == 'nan':
			totalApreqMetering = 0

		if str(totalExempt) == 'nan':
			totalExempt = 0

		if numberHeld == 0:
			sumHold = 0
		else:
			sumHold = dfSummary['Sum of Total Realized Hold (Minutes)'][0]
		if str(excessTaxi) != 'nan':
			ax1.plot(numberHeld,excessTaxi,'o' , markersize = 10)
			ax1.set_xlabel('Number Aircraft Held')
			ax1.set_ylabel('Excess AMA Taxi Time')
			
			ax2.plot(sumHold,excessTaxi,'o' , markersize = 10)
			ax2.set_xlabel('Sum Hold Time [Minutes]')
			ax2.set_ylabel('Excess AMA Taxi Time')

			ax7.plot(totalApreq,excessTaxi,'o' , markersize = 10)
			ax7.set_xlabel('Total Number APREQ in Bank')
			ax7.set_ylabel('Excess AMA Taxi Time')

			ax8.plot(totalApreqMetering,excessTaxi,'o' , markersize = 10)
			ax8.set_xlabel('Total Number APREQ During Metering')
			ax8.set_ylabel('Excess AMA Taxi Time')

			ax9.plot(totalExempt,excessTaxi,'o' , markersize = 10)
			ax9.set_xlabel('Total Number Exempt in Bank')
			ax9.set_ylabel('Excess AMA Taxi Time')

			excessTaxiVec.append(excessTaxi)
			apreqMeterVec.append(totalApreqMetering)
			apreqVec.append(totalApreq)
			aeVal = int(totalApreqMetering) + int(totalExempt)
			apreqExemptVec.append(aeVal)
			numHeldVec.append(numberHeld)

			if len(activeDelay) > 0:
				for delayVal in range(len(activeDelay)):
					val = pd.Timedelta(activeDelay[delayVal])
					valSeconds = val.total_seconds() / float(60)	
					ax3.plot(valSeconds,excessTaxi,'o' , markersize = 10)
					ax3.set_xlabel('Active Delay When Triggered [Minutes]')
					ax3.set_ylabel('Excess AMA Taxi Time')


					ax4.plot(numActive[delayVal],excessTaxi,'o' , markersize = 10)
					ax4.set_xlabel('Number Active When Triggered')
					ax4.set_ylabel('Excess AMA Taxi Time')

					ax5.plot(numPlanning[delayVal],excessTaxi,'o' , markersize = 10)
					ax5.set_xlabel('Number Planning When Triggered')
					ax5.set_ylabel('Excess AMA Taxi Time')

					ax6.plot(sumActivePlanning[delayVal],excessTaxi,'o' , markersize = 10)
					ax6.set_xlabel('Number Active + Planning When Triggered')
					ax6.set_ylabel('Excess AMA Taxi Time')
					

					sumAircraftVec.append(sumActivePlanning[delayVal])
					activeDelayVec.append(valSeconds)
					delayVec.append(excessTaxi)
					numPlanningVec.append(numPlanning[delayVal])
					numActiveVec.append(numActive[delayVal])

			if excessTaxi < 5:
				print('AMA TAXI < 2 : ' + dateVecSummary[date] + ' BANK NUMBER: ' + str(bank))

	except:
		print('THIS IS A BAD DATA DAY ' + dateVecSummary[date])


rho, pval = stats.spearmanr(sumAircraftVec,delayVec)
print(rho)
print(pval)
rho2, pval2 = stats.spearmanr(activeDelayVec,delayVec)
print(rho2)
print(pval2)
rho3, pval3 = stats.spearmanr(numPlanningVec,delayVec)
print(rho3)
print(pval3)
rho4, pval4 = stats.spearmanr(numActiveVec,delayVec)
print(rho4)
print(pval4)
print(apreqMeterVec)
rho5, pval5 = stats.spearmanr(apreqMeterVec,excessTaxiVec)
print(rho5)
print(pval5)
rho6, pval6 = stats.spearmanr(apreqVec,excessTaxiVec)
print(rho6)
print(pval6)
rho7, pval7 = stats.spearmanr(apreqExemptVec,excessTaxiVec)
print(rho7)
print(pval7)
rho8, pval8 = stats.spearmanr(numHeldVec,excessTaxiVec)
print(rho8)
print(pval8)
plt.show()