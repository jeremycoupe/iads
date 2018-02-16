import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
from scipy.interpolate import spline
from scipy.stats import *

excludeEarlyDays = True
filterTail = True

dfTrigger = pd.read_csv('~/Desktop/testFormat.csv' , sep=',' , index_col=False)


#'N_BE/A/T=36C'
utilization = 'N_BE/A/T=36C'
stSave = utilization.replace('/','-')

if excludeEarlyDays:
	if filterTail:
		stSaveFig = 'figs/' + stSave + 'FilterDaysFilterTailWithArrival.png'
	else:
		stSaveFig = 'figs/' + stSave + 'FilterDaysWithArrival.png'
else:
	if filterTail:
		stSaveFig = 'figs/' + stSave + 'FilterTailWithArrival.png'
	else:
		stSaveFig = 'figs/' + stSave + 'WithArrival.png'

taxiUpperBound = 45
rampTaxiUpperBound = 25
A14UpperBound = 60

# taxiUpperBound = 100
# rampTaxiUpperBound = 100


dateVecIADS = []
dateVecTrigger = []

str0 = '201711'
str2 = '11/'
for i in range(1,31):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		#dateVecTrigger.append(str2 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		#dateVecTrigger.append(str2  + str(i) )
	dateVecTrigger.append(str2 + str(i) + '/17')
	


str0 = '201712'
str2 = '12/'
for i in range(1,32):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		#dateVecTrigger.append(str2 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		#dateVecTrigger.append(str2  + str(i) )
	dateVecTrigger.append(str2 + str(i) + '/17')
	

str0 = '201801'
str2 = '1/'
for i in range(1,25):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		#dateVecTrigger.append(str2 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		#dateVecTrigger.append(str2  + str(i) )
	dateVecTrigger.append(str2 + str(i) + '/18')

AvgExcessTaxiIn = []
AvgRampTaxiIn = []
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
taxiInTotal = []
gateConflicts = []
preGateConflicts = []
postGateConflicts = []
sFlowBinary = []
preMeterRampIN = []
postMeterRampIN = []
preMeterAMAIN = []
postMeterAMAIN=[]
preA14 = []
postA14 = []

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

countMeterStart = 0
triggerVec = []

for date in range(len(dateVecIADS)):
	try:
		if dateVecIADS[date] not in excludeVec:
			dfIads = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_iads_summary_0.6.csv' , sep=',' , index_col=False)
			dfFlightSpecifc = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_flight_specific_0.6.csv' , sep=',' , index_col=False)
		
			#break
		

			bankIndex = -1
			for j in range(len(dfIads['Broader Bank Number'])):
				if str(dfIads['Broader Bank Number'][j]) == str(2.0):
					bankIndex = j
			
			countGateConflicts = 0
			beforeFlag = False
			#if True:
			if str(dfIads['Runway Utilization At Start'][bankIndex]) == utilization:
				if str(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]) != 'nan':
					if dateVecIADS[date] == '20171217':
						meterStartIndex = countMeterStart
					countMeterStart+=1
					xTickVec.append(dateVecIADS[date])
					AvgExcessAMA.append(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					AvgExcessRamp.append(dfIads['Positive Excess Ramp taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					AvgExcessTaxiIn.append(dfIads['Positive Excess AMA taxi-in time statistics(mean)'][bankIndex])
					AvgRampTaxiIn.append(dfIads['Positive Excess ramp taxi-in time statistics(mean)'][bankIndex])
					taxiInTotal.append(dfIads['Positive Excess AMA taxi-in time statistics(mean)'][bankIndex] + dfIads['Positive Excess ramp taxi-in time statistics(mean)'][bankIndex])
					excessRamp = []


					if pd.Timestamp(dateVecIADS[date] + ' 00:00:00') < pd.Timestamp('2017-11-29 00:00:00'):
						triggerVec.append('nan')
					else:
						getTarget = True
						for idx in range(len(dfTrigger['date'])):
							if getTarget:
								print(dfTrigger['date'][idx])
								if str(dfTrigger['date'][idx]) == dateVecTrigger[date]:
									triggerVec.append(dfTrigger['time-based-target-excess-queue-minutes'][idx])
									getTarget = False


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
													beforeFlag = True
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
													

						else:
							if str(dfFlightSpecifc['Bank Number'][flight]) == str(2.0):
								
								if str(dfFlightSpecifc['gate_conflict_values_present'][flight]) == 'True':
									countGateConflicts +=1
									print(countGateConflicts)

								if str(dfFlightSpecifc['Actual_AMA_Taxi_In'][flight]) != 'nan':
									if str(dfFlightSpecifc['Actual_Ramp_Taxi'][flight]) != 'nan':
										if str(dfFlightSpecifc['Pred_AMA_Taxi_at_AMA_Taxi_In_Start'][flight]) != 'nan':
											if str(dfFlightSpecifc['Pred_AMA_Taxi_at_AMA_Taxi_In_Start'][flight]) != 'nan':
												if pd.Timestamp(dfFlightSpecifc['Actual_ON_Time'][flight]) < pd.Timestamp('2017-11-29 00:00:00'):
													rampVal = (dfFlightSpecifc['Actual_Ramp_Taxi'][flight] - dfFlightSpecifc['Ramp_Taxi_Pred_at_AMA_Taxi_In_Start'][flight]) / float(60)
													#amaVal = (dfFlightSpecifc['Actual_AMA_Taxi_In'][flight] - dfFlightSpecifc['Pred_AMA_Taxi_at_AMA_Taxi_In_Start'][flight]) / float(60)
													amaVal = dfFlightSpecifc['Error_AMA_Taxi_In_Pred_while_On_Final'][flight] / float(60)
													preMeterAMAIN.append( max([0,amaVal]) )
													if rampVal < rampTaxiUpperBound + 5:
														preMeterRampIN.append( max([0,rampVal]) )
													A14Val = pd.Timestamp(dfFlightSpecifc['Actual_IN_Time'][flight]) - pd.Timestamp(dfFlightSpecifc['arrival_stand_scheduled_time'][flight])
													if str(A14Val.total_seconds() / float(60)) != 'nan':
														if abs(A14Val.total_seconds() / float(60)) < A14UpperBound:
															preA14.append(A14Val.total_seconds() / float(60))
												else:
													rampVal = (dfFlightSpecifc['Actual_Ramp_Taxi'][flight] - dfFlightSpecifc['Ramp_Taxi_Pred_at_AMA_Taxi_In_Start'][flight]) / float(60)
													#amaVal = (dfFlightSpecifc['Actual_AMA_Taxi_In'][flight] - dfFlightSpecifc['Pred_AMA_Taxi_at_AMA_Taxi_In_Start'][flight]) / float(60)
													amaVal = dfFlightSpecifc['Error_AMA_Taxi_In_Pred_while_On_Final'][flight] / float(60)
													postMeterAMAIN.append(max([0,amaVal]))
													if rampVal < rampTaxiUpperBound + 5:
														postMeterRampIN.append(max([0,rampVal]))
													A14Val = pd.Timestamp(dfFlightSpecifc['Actual_IN_Time'][flight]) - pd.Timestamp(dfFlightSpecifc['arrival_stand_scheduled_time'][flight])
													if str(A14Val.total_seconds() / float(60)) != 'nan':
														if abs(A14Val.total_seconds() / float(60)) < A14UpperBound:
															postA14.append(A14Val.total_seconds() / float(60))
					

					print(dateVecIADS[date])
					print(len(excessRamp))
					AvgExcessRampV2.append(np.mean(excessRamp))
					if beforeFlag:
						preMeterTotal.append(np.mean(excessRamp) + dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					else:
						postMeterTotal.append(np.mean(excessRamp) + dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])
					#print(excessRamp)

					gateConflicts.append(countGateConflicts)
					if beforeFlag:
						if dateVecIADS[date] != '20171113':
							preGateConflicts.append(countGateConflicts)
					else:
						postGateConflicts.append(countGateConflicts)

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

print('\n')
print('\n')
print(preGateConflicts)
print('Pre Gate Conflicts = ' + str(np.mean(preGateConflicts)) ) 
print(postGateConflicts)
print('Post Gate Conflicts = ' + str(np.mean(postGateConflicts)) )

print('\n')
print('\n')
print('Pre Ramp Taxi In = ' + str(np.mean(preMeterRampIN)))
print('Post Ramp Taxi In = ' + str(np.mean(postMeterRampIN)))
print('Pre AMA Taxi In = ' + str(np.mean(preMeterAMAIN)))
print('Post AMA Taxi In = ' + str(np.mean(postMeterAMAIN)))

#plt.figure(1,figsize=(14,14))
fig, host = plt.subplots(figsize=(10,6))

#plt.subplot(4,1,1)
print('THIS IS TRIGGER VEC')
print(triggerVec)
plt.plot(AvgExcessAMA,'-*',label='Excess AMA Taxi OUT')
plt.plot(AvgExcessRampV2,'-*',label='Excess Ramp Taxi OUT')
plt.plot(vecAdd,'-*',label = 'AMA + Ramp Excess Taxi OUT')
plt.plot(triggerVec,'-*' , color='black',label='Target Excess Queue Time')
plt.plot([meterStartIndex,meterStartIndex] , [0,18] , '--' , color = 'grey' , alpha =0.5, label = 'Metering Started')
plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90,fontsize = 6)
plt.ylabel('Average Taxi Out Time [Minutes]')
plt.ylim([0,18])
plt.legend(loc = 'upper left')
plt.title('Utilization: ' + utilization)
plt.tight_layout()
plt.savefig('ExcessTaxiOutWithTarget.png')

fig, host = plt.subplots(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(AvgExcessTaxiIn,'-*',label='Excess AMA Taxi IN')
plt.plot(AvgRampTaxiIn,'-*',label='Excess Ramp Taxi IN')
plt.plot(taxiInTotal,'-*' , label = 'AMA + Ramp Taxi IN')
plt.plot([meterStartIndex,meterStartIndex] , [0,14] , '--' , color = 'grey' , alpha =0.5, label = 'Metering Started')
plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90,fontsize = 6)
plt.ylabel('Average Taxi In Time [Minutes]',fontsize=10)
plt.title('Utilization: ' + utilization)
plt.ylim([0,14])

plt.legend()

plt.subplot(2,1,2)
# par1 = plt.twinx()
# par1.plot(np.array(gateConflicts),'--s',color = 'black', alpha = 0.5,label='Gate Conflicts')
# par1.legend()


plt.plot(np.array(gateConflicts),'--s',color = 'black', alpha = 0.5,label='Gate Conflicts')
plt.plot([meterStartIndex,meterStartIndex] , [0,50] , '--' , color = 'grey' , alpha =0.5, label = 'Metering Started')
plt.xticks(np.arange(len(xTickVec)),xTickVec,rotation =90,fontsize = 6)
plt.ylabel('Number of Gate Conflicts',fontsize=10)
plt.ylim([0,50])
plt.legend()
plt.tight_layout()

plt.savefig('ExcessTaxiIn.png')



# fig, host = plt.subplots(figsize=(10,6))
# plt.subplot(2,1,1)
# xMinVal = min([min(preMeterAMA),min(postMeterAMA)])
# xMaxVal = max([max(preMeterAMA),max(postMeterAMA)])
# plt.hist(preMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'red',alpha = 0.5,normed = True,label='AMA Excess Taxi Before Metering')
# plt.hist(postMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'blue',alpha = 0.5,normed = True,label = 'AMA Excess Taxi After Metering')
# plt.xlabel('Pre-meter mean: ' + str(np.mean(preMeterAMA)) + ', Post-meter mean: ' + str(np.mean(postMeterAMA)))
# plt.legend()

# plt.subplot(2,1,2)
# xMinVal = min([min(preMeterRamp),min(postMeterRamp)])
# xMaxVal = max([max(preMeterRamp),max(postMeterRamp)])
# plt.hist(preMeterRamp,range=[xMinVal,xMaxVal],bins = 20,color = 'red',alpha = 0.5,normed = True,label='Ramp Excess Taxi Before Metering')
# plt.hist(postMeterRamp,range=[xMinVal,xMaxVal],bins = 20,color = 'blue',alpha = 0.5,normed = True,label = 'Ramp Excess Taxi After Metering')
# plt.xlabel('Pre-meter mean: ' + str(np.mean(preMeterRamp)) + ', Post-meter mean: ' + str(np.mean(postMeterRamp)))
# plt.legend()

# plt.tight_layout()
# ##plt.savefig(stSaveFig)

plt.figure(figsize = (10,10))

# y,binEdges=np.histogram(preMeterAMA,range=[xMinVal,xMaxVal],bins = 10,normed = True)
# y2,binEdges2=np.histogram(postMeterAMA,range=[xMinVal,xMaxVal],bins = 10,normed = True)
# bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
# bincenters2 = 0.5*(binEdges2[1:]+binEdges2[:-1])



xMinVal = min([min(preMeterAMA),min(postMeterAMA)])
xMaxVal = max([max(preMeterAMA),max(postMeterAMA)])
kernel = gaussian_kde(preMeterAMA,bw_method=0.6)
kernel2 = gaussian_kde(postMeterAMA,bw_method=0.6)
xVec = np.linspace(xMinVal,xMaxVal,100)


plt.subplot(2,1,1)
plt.plot( xVec, kernel(xVec) , '-' , linewidth = 4, color = 'red',alpha = 0.65,label='AMA Excess Taxi Out Before Metering')
plt.plot(xVec, kernel2(xVec), '-' , linewidth = 4, color = 'blue',alpha = 0.65,label = 'AMA Excess Taxi Out After Metering')
# plt.hist(preMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'red',alpha = 0.5,normed = True,histtype = 'step',label='AMA Excess Taxi Before Metering')
# plt.hist(postMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'blue',alpha = 0.5,normed = True,histtype = 'step',label = 'AMA Excess Taxi After Metering')
plt.title('Excess AMA Taxi Out Time [Minutes] \n Average Before Metering: ' + str(np.mean(preMeterAMA))[0:5] + ', Average After Metering: ' + str(np.mean(postMeterAMA))[0:5])
plt.ylabel('Percentage of Aircraft')
plt.xlabel('Excess AMA Taxi Out [Minutes]', fontsize = 8)
plt.legend()

frame1 = plt.gca()
num = 0
for xlabel_i in frame1.axes.get_yticklabels():
	if num != 0:
		xlabel_i.set_fontsize(0.0)
		xlabel_i.set_visible(False)
	num+=1



plt.subplot(2,1,2)
xMinVal = min([min(preMeterRamp),min(postMeterRamp)])
xMaxVal = max([max(preMeterRamp),max(postMeterRamp)])
kernel = gaussian_kde(preMeterRamp,bw_method=0.75)
kernel2 = gaussian_kde(postMeterRamp,bw_method=0.75)
xVec = np.linspace(xMinVal,xMaxVal,100)
plt.plot( xVec, kernel(xVec) , '-' , linewidth = 4, color = 'red',alpha = 0.65,label='Ramp Excess Taxi Out Before Metering')
plt.plot(xVec, kernel2(xVec), '-' , linewidth = 4, color = 'blue',alpha = 0.65,label = 'Ramp Excess Taxi Out After Metering')
plt.title('Excess Ramp Taxi Out Time [Minutes] \n Average Before Metering: ' + str(np.mean(preMeterRamp))[0:5] + ', Average After Metering: ' + str(np.mean(postMeterRamp))[0:5])
plt.ylabel('Percentage of Aircraft')
plt.xlabel('Excess Ramp Taxi Out [Minutes]', fontsize = 8)
plt.legend()

frame1 = plt.gca()
num = 0
for xlabel_i in frame1.axes.get_yticklabels():
	if num != 0:
		xlabel_i.set_fontsize(0.0)
		xlabel_i.set_visible(False)
	num+=1

plt.tight_layout()
plt.savefig('ExcessAMALineGraphV2.png')


plt.figure(figsize = (10,8))

# plt.subplot(2,1,1)
# xMinVal = min([min(preMeterAMAIN),min(postMeterAMAIN)])
# xMaxVal = max([max(preMeterAMAIN),max(postMeterAMAIN)])
# kernel = gaussian_kde(preMeterAMAIN,bw_method=0.6)
# kernel2 = gaussian_kde(postMeterAMAIN,bw_method=0.6)
# xVec = np.linspace(xMinVal,xMaxVal,100)



# plt.plot( xVec, kernel(xVec) , '-' , linewidth = 4, color = 'red',alpha = 0.65,label='AMA Excess Taxi In Before Metering')
# plt.plot(xVec, kernel2(xVec), '-' , linewidth = 4, color = 'blue',alpha = 0.65,label = 'AMA Excess Taxi In After Metering')
# # plt.hist(preMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'red',alpha = 0.5,normed = True,histtype = 'step',label='AMA Excess Taxi Before Metering')
# # plt.hist(postMeterAMA,range=[xMinVal,xMaxVal],bins = 20,color = 'blue',alpha = 0.5,normed = True,histtype = 'step',label = 'AMA Excess Taxi After Metering')
# plt.title('Excess AMA Taxi In Time [Minutes] \n Average Before Metering: ' + str(np.mean(preMeterAMAIN))[0:5] + ', Average After Metering: ' + str(np.mean(postMeterAMAIN))[0:5])
# plt.ylabel('Percentage of Aircraft')
# plt.legend()

# frame1 = plt.gca()
# num = 0
# for xlabel_i in frame1.axes.get_yticklabels():
# 	if num != 0:
# 		xlabel_i.set_fontsize(0.0)
# 		xlabel_i.set_visible(False)
# 	num+=1



plt.subplot(2,1,1)
xMinVal = min([min(preMeterRampIN),min(postMeterRampIN)])
xMaxVal = max([max(preMeterRampIN),max(postMeterRampIN)])
kernel = gaussian_kde(preMeterRampIN,bw_method=0.75)
kernel2 = gaussian_kde(postMeterRampIN,bw_method=0.75)
xVec = np.linspace(xMinVal,xMaxVal,100)
plt.plot( xVec, kernel(xVec) , '-' , linewidth = 4, color = 'red',alpha = 0.65,label='Ramp Excess Taxi In Before Metering')
plt.plot(xVec, kernel2(xVec), '-' , linewidth = 4, color = 'blue',alpha = 0.65,label = 'Ramp Excess Taxi In After Metering')
plt.title('Excess Ramp Taxi In Time [Minutes] \n Average Before Metering: ' + str(np.mean(preMeterRampIN))[0:5] + ', Average After Metering: ' + str(np.mean(postMeterRampIN))[0:5])
plt.ylabel('Percentage of Aircraft')
plt.xlabel('Excess Ramp Taxi In [Minutes]', fontsize = 8)
plt.legend()

frame1 = plt.gca()
num = 0
for xlabel_i in frame1.axes.get_yticklabels():
	if num != 0:
		xlabel_i.set_fontsize(0.0)
		xlabel_i.set_visible(False)
	num+=1


plt.subplot(2,1,2)
xMinVal = min([min(preA14),min(postA14)])
xMaxVal = max([max(preA14),max(postA14)])
kernel = gaussian_kde(preA14,bw_method=0.3)
kernel2 = gaussian_kde(postA14,bw_method=0.3)
xVec = np.linspace(xMinVal,xMaxVal,100)

plt.plot( xVec, kernel(xVec) , '-' , linewidth = 4, color = 'red',alpha = 0.65,label='<Actuan In> - <Scheduled In> Before Metering')
plt.plot(xVec, kernel2(xVec), '-' , linewidth = 4, color = 'blue',alpha = 0.65,label = '<Actuan In> - <Scheduled In> After Metering')
plt.title('<Actuan In> - <Scheduled In> [Minutes] \n Average Before Metering: ' + str(np.mean(preA14))[0:5] + ', Average After Metering: ' + str(np.mean(postA14))[0:5])
plt.xlabel('Actual In - Scheduled In [Minutes]',fontsize=8)
plt.ylabel('Percentage of Aircraft')

# print(preA14)
# print(postA14)
frame1 = plt.gca()
num = 0
for xlabel_i in frame1.axes.get_yticklabels():
	if num != 0:
		xlabel_i.set_fontsize(0.0)
		xlabel_i.set_visible(False)
	num+=1


plt.legend()
plt.tight_layout()
plt.savefig('ExcessRampInLineGraphV2.png')

plt.show()
	