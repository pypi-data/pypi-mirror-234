import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.PSpecCls import PSpecCls
import DateTimeTools as TT
from ..Tools.ListDates import ListDates

def ReadOmni(Date):
	'''
	Reads the level 2 omniflux data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
		If Date is a single integer - one date is loaded.
		If Date is a 2-element tuple or list, all dates from Date[0] to
		Date[1] are loaded.
		If Date contains > 2 elements, all dates within the list will
		be loaded.
			
	Returns
	=======
	data : dict
		Contains the following fields:
		'eFlux' : PSpecCls object, contains electron fluxes
		
	For more information about the PSpecCls object, see Arase.Tools.PSpecCls 
		

	'''		
				


	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'eFlux' : None}


	#loop through dates
	for date in dates:	
					
		#read the CDF file
		data,meta = ReadCDF(date,2,'omniflux')		

		if data is None:
			continue
		

		#get the time 
		sEpoch = data['epoch']
		sDate,sut = TT.CDFEpochtoDate(sEpoch)
		
		#the energy arrays
		sEnergy = data['FEDO_Energy']
		

		#replace bad data
		s = data['FEDO']
		bad = np.where(s < 0)
		s[bad] = np.nan
		

		
		#plot labels
		ylabel = 'Energy (keV)'
		zlabel = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		
		
		#now to store the spectra
		if out['eFlux'] is None:
			out['eFlux'] = PSpecCls(SpecType='e',ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
		out['eFlux'].AddData(sDate,sut,sEpoch,sEnergy,s,Meta=meta['FEDO'],Label='MEPe')
			
			
	return out	
