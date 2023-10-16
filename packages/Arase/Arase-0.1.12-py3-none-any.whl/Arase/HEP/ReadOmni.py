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
		'eFluxL' : PSpecCls object, contains electron fluxes
		'eFluxH' : PSpecCls object, contains electron fluxes
		
	For more information about the PSpecCls object, see Arase.Tools.PSpecCls 
		

	'''	
	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'eFluxL' : None,
			'eFluxH' : None}

	#loop through dates
	for date in dates:	
				
		#read the CDF file
		data,meta = ReadCDF(date,2,'omniflux')		

		if data is None:
			continue
		
		
		#get the time 
		sEpochL = data['Epoch_L']
		sDateL,sutL = TT.CDFEpochtoDate(sEpochL)
		sEpochH = data['Epoch_H']
		sDateH,sutH = TT.CDFEpochtoDate(sEpochH)
		
		#the energy arrays
		sEnergyL = data['FEDO_L_Energy']
		sEnergyH = data['FEDO_H_Energy']
		
		#get the midpoints
		eL = 10**np.mean(np.log10(sEnergyL),axis=0)
		eH = 10**np.mean(np.log10(sEnergyH),axis=0)
		
		#replace bad data
		L = data['FEDO_L']
		bad = np.where(L < 0)
		L[bad] = np.nan
		
		H = data['FEDO_H']
		bad = np.where(H < 0)
		H[bad] = np.nan

		
		#labels
		zlabelH = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		zlabelL = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		ylabelH = 'Energy (keV)'
		ylabelL = 'Energy (keV)'
		
		
		#now to store the spectra
		if out['eFluxL'] is None:
			out['eFluxL'] = PSpecCls(SpecType='e',ylabel=ylabelL,zlabel=zlabelL,ylog=True,zlog=True,ScaleType='positive')
		out['eFluxL'].AddData(sDateL,sutL,sEpochL,eL,L,ew=None,dt=None,Meta=meta['FEDO_L'],Label='HEP-L')
		
		if out['eFluxH'] is None:
			out['eFluxH'] = PSpecCls(SpecType='e',ylabel=ylabelH,zlabel=zlabelH,ylog=True,zlog=True,ScaleType='positive')
		out['eFluxH'].AddData(sDateH,sutH,sEpochH,eH,H,ew=None,dt=None,Meta=meta['FEDO_H'],Label='HEP-H')
			
	return out	
