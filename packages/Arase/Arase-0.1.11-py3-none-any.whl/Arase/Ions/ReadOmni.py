import numpy as np
from ..LEPi.ReadOmni import ReadOmni as LEP 
from ..MEPi.ReadOmni import ReadOmni as MEP 

from ..Tools.CombinePSpecCls import CombinePSpecCls

def ReadOmni(Date,Instruments=['LEPi','MEPi']):
	'''
	Get a SpecCls object containing all of the electron data in one place.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
		If Date is a single integer - one date is loaded.
		If Date is a 2-element tuple or list, all dates from Date[0] to
		Date[1] are loaded.
		If Date contains > 2 elements, all dates within the list will
		be loaded.
	Instruments : str
		List of instruments to combine, can contain any of the following:
		'LEPi'|'LEP'|'MEPi'|'MEP'
				
	Returns
	=======
	Arase.Tools.PSpecCls object

				
	'''

	
	DataH = []
	DataHe = []
	DataO = []
	
	if 'LEP' in Instruments or 'LEPi' in Instruments:
		#Add LEP spectra
		tmp = LEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			DataH.append(tmp['H+Flux'])
			DataHe.append(tmp['He+Flux'])
			DataO.append(tmp['O+Flux'])
			
			
			
	if 'MEP' in Instruments or 'MEPi' in Instruments:
		#Add MEP spectra
		tmp = MEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			DataH.append(tmp['H+Flux'])
			DataHe.append(tmp['He+Flux'])
			DataO.append(tmp['O+Flux'])			
				
	return CombinePSpecCls(DataH),CombinePSpecCls(DataHe),CombinePSpecCls(DataO)
