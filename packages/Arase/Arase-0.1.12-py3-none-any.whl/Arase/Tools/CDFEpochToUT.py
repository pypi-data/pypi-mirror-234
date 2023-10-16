import numpy as np
import cdflib

def CDFEpochToUT(E):
	'''
	Uses cdflib to conver CDF Epoch to date and ut arrays.
	'''
	#break the date down into year, month etc.
	dt = cdflib.cdfepoch.breakdown(E,to_np=True)
	
	#get the date array
	Date = (dt[:,0]*10000 + dt[:,1]*100 + dt[:,2]).astype('int32')
	
	#now for the time
	sec = dt[:,5].astype('float64') + dt[:,6]/1000.0 + dt[:,7]/1e6 + dt[:,8]/1e9
	ut = (dt[:,3].astype('float64') + dt[:,4]/60.0).astype('float64') + sec/3600.0 
	
	return Date,ut
