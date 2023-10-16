import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.CombineSpecCls import CombineSpecCls
import DateTimeTools as TT
from .ReadHFAHigh import ReadHFAHigh
from .ReadHFALow import ReadHFALow

def ReadHFA(Date):
	'''
	Reads the level 2 high and low HFA data.
	
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
	
	#read the data in
	datah = ReadHFAHigh(Date)
	datal = ReadHFALow(Date)
	
	#list the fields
	fields = ['SpectraEu','SpectraEv','SpectraBgamma','SpectraEsum',
			'SpectraEr','SpectraEl','SpectraEmix','SpectraEAR']
	
	#now to combine each one
	out = {}
	for f in fields:
		out[f] = CombineSpecCls([datal[f],datah[f]])
		
	return out
	
	
		

