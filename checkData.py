import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy import stats
from scipy.interpolate import spline
from scipy.stats import *

utilization = 'N_BE/A/T=36C'

dateVecIADS = []

str0 = '201711'
str2 = '11/'
for i in range(1,31):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		#dateVecTrigger.append(str2 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		#dateVecTrigger.append(str2  + str(i) )
	
	


str0 = '201712'
str2 = '12/'
for i in range(1,32):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		#dateVecTrigger.append(str2 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		#dateVecTrigger.append(str2  + str(i) )
	
	

str0 = '201801'
str2 = '1/'
for i in range(1,25):
	if i < 10:
		dateVecIADS.append(str0 + '0' + str(i) )
		#dateVecTrigger.append(str2 + '0' + str(i) )
	else:
		dateVecIADS.append(str0 + str(i) )
		#dateVecTrigger.append(str2  + str(i) )
	

dateVecIADS = ['20180116']

AvgExcessAMA = []
flightSpecificAMA = []
for date in range(len(dateVecIADS)):
	dfIads = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_iads_summary_0.6.csv' , sep=',' , index_col=False)
	dfFlightSpecifc = pd.read_csv('data/0.6/' + dateVecIADS[date] + '_flight_specific_0.6.csv' , sep=',' , index_col=False)

	bankIndex = -1
	for j in range(len(dfIads['Broader Bank Number'])):
		if str(dfIads['Broader Bank Number'][j]) == str(2.0):
			bankIndex = j

	if str(dfIads['Runway Utilization At Start'][bankIndex]) == utilization:
		if str(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex]) != 'nan':
			AvgExcessAMA.append(dfIads['Positive Excess AMA taxi-out time statistics without FAA Controlled(mean)'][bankIndex])

			computeAMA = []
			for flight in range(len(dfFlightSpecifc['gufi'])):
				if str(dfFlightSpecifc['isArrival'][flight]) == 'False':
					if str(dfFlightSpecifc['Bank Number'][flight]) == str(2.0):
						if str(dfFlightSpecifc['clear_gate_pushback_approved'][flight]) != 'nan':
							if str(dfFlightSpecifc['pushback_clearance_undone'][flight]) == 'False':
								if str(dfFlightSpecifc['apreq_final'][flight]) == 'nan':
									tVal = dfFlightSpecifc['Pos_Excess_AMA_Taxi_Out'][flight]
									if str(tVal) != 'nan':
										computeAMA.append(tVal/float(60))
			flightSpecificAMA.append(np.mean(computeAMA))
			print(len(computeAMA))



print(AvgExcessAMA)
print(flightSpecificAMA)


