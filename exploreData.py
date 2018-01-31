import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats


stSaveFig = 'N_BE-A-T=36CFilterDaysFilterTailWithArrival.png'

taxiUpperBound = 30
rampTaxiUpperBound = 15

# taxiUpperBound = 100
# rampTaxiUpperBound = 100


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

AvgExcessTaxiIn = []
AvgExcessAMA = []
AvgExcessRamp = []
AvgExcessRampV2 = []
xTickVec = []
preMeterRamp = []
postMeterRamp = []
preMeterAMA = []
postMeterAMA = []
preMeterTotal = []
postMeterTotal = []

excludeVec = ['20180111','20180117','20180112']

excludeVec.append('20171129')
excludeVec.append('20171130')

str0 = '201712'
for i in range(1,17):
	if i < 10:
		excludeVec.append(str0 + '0' + str(i) )
	else:
		excludeVec.append(str0 + str(i) )

for date in range(len(dateVecIADS)):
	try:
		if dateVecIADS[date] not in excludeVec:
			dfIads = pd.read_csv('data/' + dateVecIADS[date] + '_iads_summary_0.5.csv' , sep=',' , index_col=False)
			dfFlightSpecifc = pd.read_csv('data/' + dateVecIADS[date] + '_flight_specific_0.5.csv' , sep=',' , index_col=False)
		
			#break
		

			bankIndex = -1
			for j in range(len(dfIads['Broader Bank Number'])):
				if str(dfIads['Broader Bank Number'][j]) == str(2.0):
					bankIndex = j
			#if True:
			#'N_BE/A/T=36C'
			if str(dfIads['Runway Utilization At Start'][bankIndex]) == 'N_BE/A/T=36C':
				if str(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]) != 'nan':
					xTickVec.append(dateVecIADS[date])
					AvgExcessAMA.append(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					AvgExcessRamp.append(dfIads['Positive Excess Ramp taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					AvgExcessTaxiIn.append(dfIads['Positive Excess AMA taxi-in time statistics(mean)'][bankIndex])
					excessRamp = []
					for flight in range(len(dfFlightSpecifc['gufi'])):
						if str(dfFlightSpecifc['isArrival'][flight]) == 'False':
							if str(dfFlightSpecifc['Bank Number'][flight]) == str(2.0):
								if str(dfFlightSpecifc['clear_gate_pushback_approved'][flight]) != 'nan':
									if str(dfFlightSpecifc['pushback_clearance_undone'][flight]) == 'False':
										if str(dfFlightSpecifc['apreq_final'][flight]) == 'nan':
								
											excessRamp01 = dfFlightSpecifc['Actual_Ramp_Taxi_Out_Time'][flight] - dfFlightSpecifc['Ramp_Taxi_Pred_at_Ramp_Taxi_Start'][flight]
											excessRamp0 = max([0,excessRamp01])
											if str(excessRamp0) != 'nan':
												excessRamp.append(excessRamp0/ float(60))
												if pd.Timestamp(dfFlightSpecifc['Actual_OUT'][flight]) < pd.Timestamp('2017-11-29 00:00:00'):
													#print('LESS THAN')
													if excessRamp0/ float(60) < rampTaxiUpperBound:
														preMeterRamp.append(excessRamp0/ float(60))
													tVal = dfFlightSpecifc['Pos_Excess_AMA_Taxi_Out'][flight]
													if str(tVal) != 'nan':
														if tVal / float(60) < taxiUpperBound:
															preMeterAMA.append(tVal/float(60))
														else:
															print('LOOK INTO')
															print(dateVecIADS[date])
															print(dfFlightSpecifc['gufi'][flight])

												else:
													if excessRamp0/ float(60) < rampTaxiUpperBound:
														postMeterRamp.append(excessRamp0/ float(60))
													tVal = dfFlightSpecifc['Pos_Excess_AMA_Taxi_Out'][flight]
													if str(tVal) != 'nan':
														if tVal / float(60) < taxiUpperBound:
															postMeterAMA.append(tVal/float(60))
														else:
															print('LOOK INTO')
															print(dateVecIADS[date])
															print(dfFlightSpecifc['gufi'][flight])
												#print('HERE')
												# if (excessRamp0 / float(60)) < -3  :
												# 	print(dateVecIADS[date])
												# 	print(dfFlightSpecifc['gufi'][flight])
					print(dateVecIADS[date])
					print(len(excessRamp))
					AvgExcessRampV2.append(np.mean(excessRamp))
					if pd.Timestamp(dfFlightSpecifc['Actual_OUT'][0]) < pd.Timestamp('2017-11-29 00:00:00'):
						preMeterTotal.append(np.mean(excessRamp) + dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					else:
						postMeterTotal.append(np.mean(excessRamp) + dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					#print(excessRamp)

	except:
		print('Bad Data Day = ' + str(dateVecIADS[date]))



vecAdd = np.array(AvgExcessAMA) + np.array(AvgExcessRampV2)

print('Ramp Taxi Before Metering')
print(np.mean(preMeterRamp))
print('AMA Taxi Before Metering')
print(np.mean(preMeterAMA))
print('Ramp Taxi After Metering')
print(np.mean(postMeterRamp))
print('AMA Taxi After Metering')
print(np.mean(postMeterAMA))


D,pVal = stats.ks_2samp(preMeterAMA,postMeterAMA)
print('THIS IS THE P VALUE')
print(pVal)

plt.figure(1,figsize=(14,14))


plt.subplot(3,1,1)
plt.plot(AvgExcessAMA,'-*',label='Excess AMA Taxi OUT')
#plt.plot(AvgExcessRamp,label='Excess Ramp Taxi')
plt.plot(AvgExcessRampV2,'-*',label='Excess Ramp Taxi OUT')
plt.plot(vecAdd,'-*',label = 'AMA + Ramp Excess Taxi OUT')
plt.plot(AvgExcessTaxiIn,'-*',label='Average Excess Taxi IN')
plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90,fontsize = 6)
plt.legend()






plt.subplot(3,1,2)
xMinVal = min([min(preMeterAMA),min(postMeterAMA)])
xMaxVal = max([max(preMeterAMA),max(postMeterAMA)])
plt.hist(preMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'red',alpha = 0.5,normed = True,label='AMA Excess Taxi Before Metering')
plt.hist(postMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'blue',alpha = 0.5,normed = True,label = 'AMA Excess Taxi After Metering')
plt.xlabel('Pre-meter mean: ' + str(np.mean(preMeterAMA)) + ', Post-meter mean: ' + str(np.mean(postMeterAMA)))
plt.legend()

plt.subplot(3,1,3)
xMinVal = min([min(preMeterRamp),min(postMeterRamp)])
xMaxVal = max([max(preMeterRamp),max(postMeterRamp)])
plt.hist(preMeterRamp,range=[xMinVal,xMaxVal],bins = 20,color = 'red',alpha = 0.5,normed = True,label='Ramp Excess Taxi Before Metering')
plt.hist(postMeterRamp,range=[xMinVal,xMaxVal],bins = 20,color = 'blue',alpha = 0.5,normed = True,label = 'Ramp Excess Taxi After Metering')
plt.xlabel('Pre-meter mean: ' + str(np.mean(preMeterRamp)) + ', Post-meter mean: ' + str(np.mean(postMeterRamp)))
plt.legend()

plt.savefig(stSaveFig)

plt.show()
	