import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.SpecCls import SpecCls
import DateTimeTools as TT
from ..Tools.ListDates import ListDates

def ReadEFD(Date):
	'''
	Reads the level 2 EFD part of PWE data.
	
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
		'Spectra' : SpecCls object, contains Spectra
		'SpectraEvEv' : SpecCls object, contains Spectra
		'SpectraEuEu' : SpecCls object, contains Spectra
		'SpectraEuEvRe' : SpecCls object, contains Spectra
		'SpectraEuEvIm' : SpecCls object, contains Spectra
		
	For more information about the SpecCls object, see Arase.Tools.SpecCls 
		

	'''		

	#List the fields to output
	fields = {	'spectra' : 		('Spectra','Frequency, $f$ (Hz)',r'EFD spectrum, $E_v$ ((mV/m)$^2$/Hz)'),
				'spectra_EvEv' : 	('SpectraEvEv','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_v)^2+\Im(E_v)^2$ ((mV/m)$^2$/Hz)'),
				'spectra_EuEu' : 	('SpectraEuEu','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_u)^2+\Im(E_u)^2$ ((mV/m)$^2$/Hz)'),
				'spectra_EuEv_re' : ('SpectraEuEvRe','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_u)\Re(E_v)+\Im(E_u)\Im(E_v)$ ((mV/m)$^2$/Hz)'),
				'spectra_EuEv_im' : ('SpectraEuEvIm','Frequency, $f$ (Hz)',r'EFD spectrum, $\Re(E_u)\Im(E_v)+\Im(E_u)\Re(E_v)$ ((mV/m)$^2$/Hz)'),}
				

	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'Spectra' : None,
			'SpectraEvEv' : None,
			'SpectraEuEu' : None,
			'SpectraEuEvRe' : None,
			'SpectraEuEvIm' : None}


	#loop through dates
	for date in dates:	


		#read the CDF file
		data,meta = ReadCDF(date,'efd',2,'spec')		
		

		if data is None:
			continue
			
		#get the time 
		sEpoch = data['Epoch']
		sDate,sut = TT.CDFEpochtoDate(sEpoch)
		
		#the frequency arrays
		sF = data['frequency']
		sF100 = data['frequency_100hz']
				
		#now to store the spectra
		for k in list(fields.keys()):
			spec = data[k]
			bad = np.where(spec < 0)
			spec[bad] = np.nan
			field,ylabel,zlabel = fields[k]
			f = data[meta[k]['DEPEND_1']]
			if meta[k]['DEPEND_1'] == 'frequency':
				bw = data['band_width']
			else:
				bw = np.ones(f.size,dtype='float32')
			if out[field] is None:
				out[field] = SpecCls(SpecType='freq',ylabel=ylabel,zlabel=zlabel,ScaleType='positive',zlog=True)
			out[field].AddData(sDate,sut,sEpoch,f,spec,Meta=meta[k],dt=1.0,bw=bw)
			
	return out	
				
				
	
