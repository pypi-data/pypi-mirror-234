import numpy as np
from ..Tools.ReadPAD import ReadPAD as RPAD
from ..Tools.ReadMirrorAlt import ReadMirrorAlt
from .. import Globals
from ..Tools.PSpecPADCls import PSpecPADCls

def ReadPAD(Date,SpecType,ReturnSpecObject=True,ReadMirror=True):
	'''
	Date : int
		Date to download data for in format yyyymmdd
		If single date - only data from that one day will be fetched
		If 2-element array - dates from Date[0] to Date[1] will be downloaded
		If > 2 elements - this is treated as a specific list of dates to download
	SpecType : str
		'eFlux'
	ReturnSpecObject : bool
		If True, then a PSpecPADCls object (which can plot the data) is 
		returned, otherwise a dictionary containing the data is returned
		
	
	'''

	path = Globals.DataPath + 'LEPe/PAD/'
	
	pad = RPAD(Date,path,SpecType)

	if ReturnSpecObject:
		if ReadMirror:
			Mirror = ReadMirrorAlt(Date,path)
			return PSpecPADCls(pad,'LEPe',Mirror=Mirror)
		else:
			return PSpecPADCls(pad,'LEPe')
	else:
		return pad
