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
for i in range(4,32):
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
plt.figure(10, figsize=(12,10))
ax10 = plt.gca()
plt.figure(11, figsize=(12,10))
ax11 = plt.gca()
plt.figure(12, figsize=(12,10))
ax12 = plt.gca()
plt.figure(13, figsize=(12,10))
ax13 = plt.gca()
plt.figure(14, figsize=(12,10))
ax14 = plt.gca()
plt.figure(15, figsize=(12,10))
ax15 = plt.gca()


dfTrigger = pd.read_csv('~/Desktop/CleanTriggerData.v1.csv', sep=',' , index_col=False)


AverageExcessTaxiVecForTrigger = []
activeDelayVecForTrigger = []
sumActivePlanningVecForTrigger = []
numPlanningVecForTrigger = []
numActiveForTrigger = []
apreqMeterVec = []
apreqVec = []
apreqExemptVec = []
excessTaxiVec = []
numHeldVec = []
sumHeldVec = []
totalExemptVec = []
timeTriggerVec = []
averageHoldVec = []
totalFlightsVec = []
totalDeparturesVec = []
totalArrivalsVec = []
overlapVec = []
for date in range(len(dateVecSummary)):
	try:
		dfIads = pd.read_csv('~/Desktop/iads/' + dateVecIADS[date] + '_iads_summary_0.2.csv' , sep=',' , index_col=False)
		dfSummary = pd.read_csv('~/Desktop/MeteringStatsV2/SummaryMeteringStats.v0.' + dateVecSummary[date] + '.csv' , sep=',' , index_col=False)

		bankIndex = -1
		for j in range(len(dfIads['Broader Bank Number'])):
			#print(dfIads['Broader Bank Number'][j])
			if str(dfIads['Broader Bank Number'][j]) == str(2.0):
				bankIndex = j
		
		if str(dfIads['Runway Utilization At Start'][bankIndex]) == 'N_BE/A/T=36C':
			print(dateVecSummary[date])
			delayIndexVec = []
			activeDelay = []
			planningDelay = []
			numActive = []
			numPlanning = []
			sumActivePlanning = []	
			timeTrigger = []	
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
						print(dfTrigger['Time_Metering_Triggered'][k])
						t0 = str(dfTrigger['Time_Metering_Triggered'][k]).split(' ')[0] + ' 13:30:00'
						v1 = pd.Timestamp(dfTrigger['Time_Metering_Triggered'][k]) - pd.Timestamp(t0)
						v2 = v1.total_seconds() / float(60)
						timeTrigger.append( v2 )
						print(v2)
					# print('HERE')

			#print(activeDelay)
		
			excessTaxi = dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]
			bank = dfIads['Broader Bank Number'][bankIndex]
			totalApreq = dfIads['Number of Total APREQs in this Bank'][bankIndex]
			totalApreqMetering = dfIads['Number of APREQ flights during surface metering were'][bankIndex]
			totalExempt = dfIads['Number of Exempt flights from surface metering were'][bankIndex]
			averageHold = dfIads['Average Metering Hold'][bankIndex]
			totalFlights = dfIads['Total_Flights_In_Bank'][bankIndex]
			totalDepartures = dfIads['Flights_In_Departure_Bank'][bankIndex]
			totalArrivals = dfIads['Flights_In_Arrival_Bank'][bankIndex]
			numberHeld = dfSummary['Number Aircraft Held For Surface Metering'][0]
			overlap0 =  pd.Timestamp(dfIads['Start_Arrival_Bank'][bankIndex]) - pd.Timestamp(dfIads['Start_Departure_Bank_Out'][bankIndex])
			overlap = overlap0.total_seconds() / float(60)
			
			if str(totalApreq) == 'nan':
				totalApreq = 0

			if str(totalApreqMetering) == 'nan':
				totalApreqMetering = 0

			if str(totalExempt) == 'nan':
				totalExempt = 0

			if str(averageHold) == 'nan':
				averageHold = 0

			if numberHeld == 0:
				sumHold = 0
			else:
				sumHold = dfSummary['Sum of Total Realized Hold (Minutes)'][0]
			

			if str(excessTaxi) != 'nan':
				
				excessTaxiVec.append(excessTaxi)
				apreqMeterVec.append(totalApreqMetering)
				apreqVec.append(totalApreq)
				aeVal = int(totalApreqMetering) + int(totalExempt)
				apreqExemptVec.append(aeVal)
				numHeldVec.append(numberHeld)
				sumHeldVec.append(sumHold)
				totalExemptVec.append(totalExempt)
				averageHoldVec.append(averageHold)
				totalFlightsVec.append(totalFlights)
				totalDeparturesVec.append(totalDepartures)
				totalArrivalsVec.append(totalArrivals)
				overlapVec.append(overlap)


				rho1, pval1 = stats.spearmanr(numHeldVec,excessTaxiVec)
				rho2, pval2 = stats.spearmanr(sumHeldVec,excessTaxiVec)
				rho7, pval7 = stats.spearmanr(apreqVec,excessTaxiVec)
				rho8, pval8 = stats.spearmanr(apreqMeterVec,excessTaxiVec)
				rho9, pval9 = stats.spearmanr(totalExemptVec,excessTaxiVec)
				rho11, pval11 = stats.spearmanr(averageHoldVec,excessTaxiVec)

				rho12, pval12 = stats.spearmanr(totalFlightsVec,excessTaxiVec)
				rho13, pval13 = stats.spearmanr(totalDeparturesVec,excessTaxiVec)
				rho14, pval14 = stats.spearmanr(totalArrivalsVec,excessTaxiVec)
				rho15, pval15 = stats.spearmanr(overlapVec,excessTaxiVec)




				ax1.plot(numberHeld,excessTaxi,'o' , markersize = 10)
				ax1.set_xlabel('Number Aircraft Held')
				ax1.set_ylabel('Excess AMA Taxi Time')
				ax1.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho1)[0:4] + ' p value = ' + str(pval1)[0:4])
				
				ax2.plot(sumHold,excessTaxi,'o' , markersize = 10)
				ax2.set_xlabel('Sum Hold Time [Minutes]')
				ax2.set_ylabel('Excess AMA Taxi Time')
				ax2.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho2)[0:4] + ' p value = ' + str(pval2)[0:4])

				ax7.plot(totalApreq,excessTaxi,'o' , markersize = 10)
				ax7.set_xlabel('Total Number APREQ in Bank')
				ax7.set_ylabel('Excess AMA Taxi Time')
				ax7.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho7)[0:4] + ' p value = ' + str(pval7)[0:4])

				ax8.plot(totalApreqMetering,excessTaxi,'o' , markersize = 10)
				ax8.set_xlabel('Total Number APREQ During Metering')
				ax8.set_ylabel('Excess AMA Taxi Time')
				ax8.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho8)[0:4] + ' p value = ' + str(pval8)[0:4])

				ax9.plot(totalExempt,excessTaxi,'o' , markersize = 10)
				ax9.set_xlabel('Total Number Exempt in Bank')
				ax9.set_ylabel('Excess AMA Taxi Time')
				ax9.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho9)[0:4] + ' p value = ' + str(pval9)[0:4])

				ax11.plot(totalExempt,excessTaxi,'o' , markersize = 10)
				ax11.set_xlabel('Average Metering Hold')
				ax11.set_ylabel('Excess AMA Taxi Time')
				ax11.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho11)[0:4] + ' p value = ' + str(pval11)[0:4])

				ax12.plot(totalFlights,excessTaxi,'o' , markersize = 10)
				ax12.set_xlabel('Total Flights in Bank')
				ax12.set_ylabel('Excess AMA Taxi Time')
				ax12.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho12)[0:4] + ' p value = ' + str(pval12)[0:4])

				ax13.plot(totalDepartures,excessTaxi,'o' , markersize = 10)
				ax13.set_xlabel('Total Departures in Bank')
				ax13.set_ylabel('Excess AMA Taxi Time')
				ax13.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho13)[0:4] + ' p value = ' + str(pval13)[0:4])

				ax14.plot(totalArrivals,excessTaxi,'o' , markersize = 10)
				ax14.set_xlabel('Total Arrivals in Bank')
				ax14.set_ylabel('Excess AMA Taxi Time')
				ax14.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho14)[0:4] + ' p value = ' + str(pval14)[0:4])

				ax15.plot(overlap,excessTaxi,'o' , markersize = 10)
				ax15.set_xlabel('Time Between Start Departure Bank and Start Arrival Bank [Minutes]')
				ax15.set_ylabel('Excess AMA Taxi Time')
				ax15.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho15)[0:4] + ' p value = ' + str(pval15)[0:4])

				

				

				if len(activeDelay) > 0:
					for delayVal in range(len(activeDelay)):
						val = pd.Timedelta(activeDelay[delayVal])
						valSeconds = val.total_seconds() / float(60)	
						
						sumActivePlanningVecForTrigger.append(sumActivePlanning[delayVal])
						activeDelayVecForTrigger.append(valSeconds)
						AverageExcessTaxiVecForTrigger.append(excessTaxi)
						numPlanningVecForTrigger.append(numPlanning[delayVal])
						numActiveForTrigger.append(numActive[delayVal])
						timeTriggerVec.append(timeTrigger[delayVal])


						rho3, pval3 = stats.spearmanr(activeDelayVecForTrigger,AverageExcessTaxiVecForTrigger)
						rho4, pval4 = stats.spearmanr(numActiveForTrigger,AverageExcessTaxiVecForTrigger)
						rho5, pval5 = stats.spearmanr(numPlanningVecForTrigger,AverageExcessTaxiVecForTrigger)
						rho6, pval6 = stats.spearmanr(sumActivePlanningVecForTrigger,AverageExcessTaxiVecForTrigger)
						rho10, pval10 = stats.spearmanr(timeTriggerVec,AverageExcessTaxiVecForTrigger)

						ax3.plot(valSeconds,excessTaxi,'o' , markersize = 10)
						ax3.set_xlabel('Active Delay When Triggered [Minutes]')
						ax3.set_ylabel('Excess AMA Taxi Time')
						ax3.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho3)[0:4] + ' p value = ' + str(pval3)[0:4])


						ax4.plot(numActive[delayVal],excessTaxi,'o' , markersize = 10)
						ax4.set_xlabel('Number Active When Triggered')
						ax4.set_ylabel('Excess AMA Taxi Time')
						ax4.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho4)[0:4] + ' p value = ' + str(pval4)[0:4])

						ax5.plot(numPlanning[delayVal],excessTaxi,'o' , markersize = 10)
						ax5.set_xlabel('Number Planning When Triggered')
						ax5.set_ylabel('Excess AMA Taxi Time')
						ax5.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho5)[0:4] + ' p value = ' + str(pval5)[0:4])

						ax6.plot(sumActivePlanning[delayVal],excessTaxi,'o' , markersize = 10)
						ax6.set_xlabel('Number Active + Planning When Triggered')
						ax6.set_ylabel('Excess AMA Taxi Time')
						ax6.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho6)[0:4] + ' p value = ' + str(pval6)[0:4])
						

						ax10.plot(timeTrigger[delayVal],excessTaxi,'o' , markersize = 10)
						ax10.set_xlabel('Minutes After 13:30:00 Metering Was Triggered')
						ax10.set_ylabel('Excess AMA Taxi Time')
						ax10.set_title('Configuration = ' + dfIads['Runway Utilization At Start'][bankIndex] + ' rho = ' + str(rho10)[0:4] + ' p value = ' + str(pval10)[0:4])

				if excessTaxi < 5:
					print('AMA TAXI < 2 : ' + dateVecSummary[date] + ' BANK NUMBER: ' + str(bank))

	except:
		print('THIS IS A BAD DATA DAY ' + dateVecSummary[date])


saveUtil = str(dfIads['Runway Utilization At Start'][bankIndex]).replace('/' , '-')

for i in range(1,16):
	plt.figure(i)
	plt.savefig('figs/utilization' + saveUtil + '_fig' + str(i) + '.png')

#print(averageHoldVec)
# rho, pval = stats.spearmanr(sumActivePlanningVecForTrigger,AverageExcessTaxiVecForTrigger)
# print(rho)
# print(pval)
# rho2, pval2 = stats.spearmanr(activeDelayVecForTrigger,AverageExcessTaxiVecForTrigger)
# print(rho2)
# print(pval2)
# rho3, pval3 = stats.spearmanr(numPlanningVecForTrigger,AverageExcessTaxiVecForTrigger)
# print(rho3)
# print(pval3)
# rho4, pval4 = stats.spearmanr(numActiveForTrigger,AverageExcessTaxiVecForTrigger)
# print(rho4)
# print(pval4)
# print(apreqMeterVec)
# rho5, pval5 = stats.spearmanr(apreqMeterVec,excessTaxiVec)
# print(rho5)
# print(pval5)
# rho6, pval6 = stats.spearmanr(apreqVec,excessTaxiVec)
# print(rho6)
# print(pval6)
# rho7, pval7 = stats.spearmanr(apreqExemptVec,excessTaxiVec)
# print(rho7)
# print(pval7)
# rho8, pval8 = stats.spearmanr(numHeldVec,excessTaxiVec)
# print(rho8)
# print(pval8)
plt.show()