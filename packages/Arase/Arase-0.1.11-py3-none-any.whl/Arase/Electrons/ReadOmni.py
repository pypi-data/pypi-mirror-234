import numpy as np
from ..LEPe.ReadOmni import ReadOmni as LEP 
from ..MEPe.ReadOmni import ReadOmni as MEP 
from ..HEP.ReadOmni import ReadOmni as HEP 
from ..XEP.ReadOmni import ReadOmni as XEP 
from ..Tools.CombinePSpecCls import CombinePSpecCls

def ReadOmni(Date,Instruments=['LEPe','MEPe','HEP','XEP'],JoinBins=False):
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
		'LEPe'|'LEP'|'MEPe'|'MEP'|'HEP'|'XEP'
		
	Returns
	=======
	Arase.Tools.PSpecCls object
		
	
	'''

	
	Data = []
	
	if 'LEP' in Instruments or 'LEPe' in Instruments:
		#Add LEP spectra
		tmp = LEP(Date,KeV=True,JoinBins=JoinBins)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFlux'])
			
			
			
	if 'MEP' in Instruments or 'MEPe' in Instruments:
		#Add MEP spectra
		tmp = MEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFlux'])
			
			
	if 'HEP' in Instruments:
		#Add HEP spectra
		tmp = HEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFluxL'])
			Data.append(tmp['eFluxH'])


			
	if 'XEP' in Instruments:
		#Add XEP spectra
		tmp = XEP(Date)
		
		if not len(list(tmp.keys())) == 0:
			Data.append(tmp['eFluxSSD'])
			
	return CombinePSpecCls(Data)
