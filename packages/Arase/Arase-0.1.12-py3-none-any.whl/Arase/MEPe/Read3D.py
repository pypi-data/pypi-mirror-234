import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.SpecCls import SpecCls
import DateTimeTools as TT

def Read3D(Date,l=2):
	'''
	Reads the level 2 or 3 3dflux data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	
	Returns
	=======
	data : dict
		Dictionary containing the data for each variable stored within 
		the CDF file.
	meta : dict
		Dictionary containing the metadata for each variable in the data
		dictionary.
		
	NOTE: In future, the data and meta dicts may be replaced by an object
	similar to that returned from ReadOmni.	
	'''
				
	#read the CDF file
	data,meta = ReadCDF(Date,l,'3dflux')		

	if data is None:
		return None
	
	# #output dict
	# out = {}
	
	# #get the time 
	# out['EpochL'] = data['Epoch_L']
	# out['DateL'],out['utL'] = TT.CDFEpochtoDate(out['EpochL'])
	# out['EpochH'] = data['Epoch_H']
	# out['DateH'],out['utH'] = TT.CDFEpochtoDate(out['EpochH'])
	
	# #the energy arrays
	# out['EnergyL'] = data['FEDO_L_Energy']
	# out['EnergyH'] = data['FEDO_H_Energy']
	
	# #get the midpoints
	# eL = np.mean(out['EnergyL'],axis=0)
	# eH = np.mean(out['EnergyH'],axis=0)
	
	# #replace bad data
	# L = data['FEDO_L']
	# bad = np.where(L < 0)
	# L[bad] = np.nan
	
	# H = data['FEDO_H']
	# bad = np.where(H < 0)
	# H[bad] = np.nan
	
	# #now to store the spectra
	# out['SpectraL'] = SpecCls(out['DateL'],out['utL'],out['EpochL'],eL,L,Meta=meta['FEDO_L'])
	# out['SpectraH'] = SpecCls(out['DateH'],out['utH'],out['EpochH'],eH,H,Meta=meta['FEDO_H'])
		
	data['Epoch'] = data['epoch']
	data['Date'],data['ut'] = TT.CDFEpochtoDate(data['epoch'])
	data['EpochSP'] = data['epoch_sp']
	data['DateSP'],data['utSP'] = TT.CDFEpochtoDate(data['epoch_sp'])		
	
	return data,meta
