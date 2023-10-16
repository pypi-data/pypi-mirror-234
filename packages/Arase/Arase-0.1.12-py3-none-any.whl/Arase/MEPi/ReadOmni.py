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
		'H+Flux' : PSpecCls object, contains proton fluxes
		'He++Flux' : PSpecCls object, contains helium ++ ion fluxes
		'He+Flux' : PSpecCls object, contains helium ion fluxes
		'O++Flux' : PSpecCls object, contains oxygen ++ ion fluxes
		'O+Flux' : PSpecCls object, contains oxygen ion fluxes
		'O2+Flux' : PSpecCls object, contains molecular oxygen ion fluxes
		'H+FluxTOF' : PSpecCls object, contains proton fluxes
		'He++FluxTOF' : PSpecCls object, contains helium ++ ion fluxes
		'He+FluxTOF' : PSpecCls object, contains helium ion fluxes
		'O++FluxTOF' : PSpecCls object, contains oxygen ++ ion fluxes
		'O+FluxTOF' : PSpecCls object, contains oxygen ion fluxes
		'O2+FluxTOF' : PSpecCls object, contains molecular oxygen ion fluxes
		
	For more information about the PSpecCls object, see Arase.Tools.PSpecCls 
		

	'''			


	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'H+Flux' : None,
			'He+Flux' : None,
			'He++Flux' : None,
			'O++Flux' : None,
			'O+Flux' : None,
			'O2+Flux' : None,
			'H+FluxTOF' : None,
			'He+FluxTOF' : None,
			'He++FluxTOF' : None,
			'O++FluxTOF' : None,
			'O+FluxTOF' : None,
			'O2+FluxTOF' : None}


	#replace bad data
	fields = {	'FPDO' : 		('H+Flux','Energy (keV/q)','H$^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','H'),
				'FHE2DO' : 		('He++Flux','Energy (keV/q)','He$^{++}$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','He'),
				'FHEDO' : 		('He+Flux','Energy (keV/q)','He$^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','He'),
				'FOPPDO' : 		('O++Flux','Energy (keV/q)','O$^{++}$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','O'),
				'FODO' : 		('O+Flux','Energy (keV/q)','O$^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','O'),
				'FO2PDO' : 		('O2+Flux','Energy (keV/q)','O$_2^+$ Flux\n((s cm$^{2}$ sr keV)$^{-1}$)','O2'),
				'FPDO_tof' : 	('H+FluxTOF','Energy (keV/q)','H$^+$ Flux for TOF data ((s cm$^{2}$ sr keV)$^{-1}$)','H'),
				'FHE2DO_tof' : 	('He++FluxTOF','Energy (keV/q)','He$^{++}$ Flux for TOF data ((s cm$^{2}$ sr keV)$^{-1}$)','He'),
				'FHEDO_tof' : 	('He+FluxTOF','Energy (keV/q)','He$^+$ Flux for TOF data ((s cm$^{2}$ sr keV)$^{-1}$)','He'),
				'FOPPDO_tof' : 	('O++FluxTOF','Energy (keV/q)','O$^{++}$ Flux for TOF data ((s cm$^{2}$ sr keV)$^{-1}$)','O'),
				'FODO_tof' : 	('O+FluxTOF','Energy (keV/q)','O$^+$ Flux for TOF data ((s cm$^{2}$ sr keV)$^{-1}$)','O'),
				'FO2PDO_tof' : 	('O2+FluxTOF','Energy (keV/q)','O$_2^+$ Flux for TOF data ((s cm$^{2}$ sr keV)$^{-1}$)','O2') }


	#loop through dates
	for date in dates:	
				
		#read the CDF file
		data,meta = ReadCDF(date,2,'omniflux')		

		if data is None:
			continue
		
	
		#get the time 
		sEpoch = data['epoch']
		sDate,sut = TT.CDFEpochtoDate(sEpoch)
		sEpochTOF = data['epoch_tof']
		sDateTOF,sutTOF = TT.CDFEpochtoDate(sEpochTOF)
		
		#the energy arrays
		sEnergy = data['FIDO_Energy']
		
		
		for k in list(fields.keys()):
			s = data[k]
			bad = np.where(s < 0)
			s[bad] = np.nan
			
			field,ylabel,zlabel,spectype = fields[k]
			
			
			
			#now to store the spectra
			if not '_tof' in k:
				if out[field] is None:
					out[field] = PSpecCls(SpecType=spectype,ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
				out[field].AddData(sDate,sut,sEpoch,sEnergy,s,Meta=meta[k],Label='MEPi')
			else:
				if out[field] is None:
					out[field] = PSpecCls(SpecType=spectype,ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
				out[field].AddData(sDateTOF,sutTOF,sEpochTOF,sEnergy,s,Meta=meta[k],Label='MEPi')
				
	return out	
