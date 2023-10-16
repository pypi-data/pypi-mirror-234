import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.SpecCls import SpecCls
import DateTimeTools as TT
from ..Tools.ListDates import ListDates

def ReadHFAHigh(Date):
	'''
	Reads the level 2 high HFA data.
	
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
		'SpectraEu' : SpecCls object, contains Spectra
		'SpectraEv' : SpecCls object, contains Spectra
		'SpectraBgamma' : SpecCls object, contains Spectra
		'SpectraEsum' : SpecCls object, contains Spectra
		'SpectraEr' : SpecCls object, contains Spectra
		'SpectraEl' : SpecCls object, contains Spectra
		'SpectraEmix' : SpecCls object, contains Spectra
		'SpectraEAR' : SpecCls object, contains Spectra
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		
	#List the fields to output
	fields = {	'spectra_eu' : 		('SpectraEu','Frequency, $f$ (kHz)','Power spectra $E_u^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_ev' : 		('SpectraEv','Frequency, $f$ (kHz)','Power spectra $E_v^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_bgamma' : 	('SpectraBgamma','Frequency, $f$ (kHz)','Power spectra $B_{\gamma}^2$ (pT$^2$/Hz)'),
				'spectra_esum' : 	('SpectraEsum','Frequency, $f$ (kHz)','Power spectra $E_u^2 + E_v^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_er' : 		('SpectraEr','Frequency, $f$ (kHz)','Power spectra $E_{right}^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_el' : 		('SpectraEl','Frequency, $f$ (kHz)','Power spectra $E_{left}^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_e_mix' : 	('SpectraEmix','Frequency, $f$ (kHz)','Power spectra $E_u^2$ or $E_v^2$ or $E_u^2 + E_v^2$ (mV$^2$/m$^2$/Hz)'),
				'spectra_e_ar' : 	('SpectraEAR','Frequency, $f$ (kHz)','Spectra Axial Ratio LH:-1/RH:+1'),}
				

	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'SpectraEu' : None,
			'SpectraEv' : None,
			'SpectraBgamma' : None,
			'SpectraEsum' : None,
			'SpectraEr' : None,
			'SpectraEl' : None,
			'SpectraEmix' : None,
			'SpectraEAR' : None}


	#loop through dates
	for date in dates:	


		#read the CDF file
		data,meta = ReadCDF(date,'hfa',2,'high')		
		
		if data is None:
			continue
		
		#get the time 
		sEpoch = data['Epoch']
		sDate,sut = TT.CDFEpochtoDate(sEpoch)
		
		#the frequency arrays
		sF = data['freq_spec']
				
		#now to store the spectra
		for k in list(fields.keys()):
			spec = data[k]

			field,ylabel,zlabel = fields[k]
			if k == 'spectra_e_ar':
				ScaleType = 'range'
			else:
				ScaleType = 'positive'
			bad = np.where(spec == -999.9)
			spec[bad] = np.nan
			if out[field] is None:
				out[field] = SpecCls(SpecType='freq',ylabel=ylabel,zlabel=zlabel,ScaleType=ScaleType,ylog=True,zlog=True)
			out[field].AddData(sDate,sut,sEpoch,sF,spec,Meta=meta[k],dt=data['time_step']/3600.0)
		
	return out	
