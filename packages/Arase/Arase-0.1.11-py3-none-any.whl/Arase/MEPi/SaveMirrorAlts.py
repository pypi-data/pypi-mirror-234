import numpy as np
from ..Tools.ReadPAD import ReadPAD as RPAD
from ..Tools.CalculateMirrorAlt import CalculateMirrorAlt
from ..Tools.SaveMirrorAlt import SaveMirrorAlt
import os
from .. import Globals
import DateTimeTools as TT
from .. import MGF

def SaveMirrorAlts(Date,na=18,Overwrite=False,Verbose=False):
	'''
	Save the mirroring altitudes and field strengths to file.
	
	'''
	#populate the list of dates to save
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = TT.ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	path = Globals.DataPath + 'MEPi/PAD/'
		
	#read the data index to see what data we have
	magidx = MGF.ReadIndex(2,'8sec')
	
	for date in dates:	
		print('Saving date {:08d}'.format(date))
		
		#get the pitch ange dist object
		existsmag = date in magidx.Date
		
		#check if the mirror file exists
		mirrexists = os.path.isfile(path+ '{:08d}/Mirror.bin'.format(date))
		pad = RPAD(date,path,'H+Flux')

		if (not pad is None) and ((not mirrexists) or Overwrite) and existsmag:
			Mirror = CalculateMirrorAlt(pad['utc'],na)
			SaveMirrorAlt(Date,path,Mirror,Overwrite,Verbose=Verbose)
	
