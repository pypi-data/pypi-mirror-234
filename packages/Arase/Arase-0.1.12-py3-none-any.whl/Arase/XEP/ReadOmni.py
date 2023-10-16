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
		'eFluxSSD' : SpecCls object, contains SSD electron fluxes
		'eFluxGSO' : SpecCls object, contains GSO electron fluxes
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		
	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'eFluxSSD' : None,
			'eFluxGSO' : None}

	#loop through dates
	for date in dates:					
		
		#read the CDF file
		data,meta = ReadCDF(date,2,'omniflux')		
		

		if data is None:
			continue
		
		#get the time 
		sEpoch = data['Epoch']
		sDate,sut = TT.CDFEpochtoDate(sEpoch)
		
		#the energy arrays
		sEnergySSD = data['FEDO_SSD_Energy']
		sEnergyGSO = data['FEDO_GSO_Energy']
		
		#get the midpoints
		essd = 10**np.mean(np.log10(sEnergySSD),axis=0)
		egso = 10**np.mean(np.log10(sEnergyGSO),axis=0)
		
		#replace bad data
		ssd = data['FEDO_SSD']
		bad = np.where(ssd < 0)
		ssd[bad] = np.nan
		
		gso = data['FEDO_GSO']
		bad = np.where(gso < 0)
		gso[bad] = np.nan
		
		
		#plot labels
		zlabelS = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		ylabelS = 'Energy (keV)'
		zlabelG = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		ylabelG = 'Energy (keV)'
		
		
		#now to store the spectra
		if out['eFluxSSD'] is None:
			out['eFluxSSD'] = PSpecCls(SpecType='e',ylabel=ylabelS,zlabel=zlabelS,ylog=True,zlog=True,ScaleType='positive')
		out['eFluxSSD'].AddData(sDate,sut,sEpoch,essd,ssd,Meta=meta['FEDO_SSD'],Label='XEP')
		if out['eFluxGSO'] is None:
			out['eFluxGSO'] = PSpecCls(SpecType='e',ylabel=ylabelG,zlabel=zlabelG,ylog=True,zlog=True,ScaleType='positive')
		out['eFluxGSO'].AddData(sDate,sut,sEpoch,egso,gso,Meta=meta['FEDO_GSO'],Label='XEP')
			
	return out	
