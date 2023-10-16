import numpy as np
from .. import Globals
from ..Tools.ListFiles import ListFiles

def PADAvailability():
	'''
	Check what dates we have saved pitch angle distribution data for.
	
	'''
	
	#scan the path for files
	path = Globals.DataPath + 'MEPi/PAD/'
	files,names = ListFiles(path,ReturnNames=True)
	nf = files.size
	
	#list the types of data
	uname = np.unique(names)
	nu = uname.size
	
	#strip the names
	for i in range(0,nu):
		uname[i] = uname[i].replace('.bin','')
		
	#create output dictionary
	out = {}
	for i in range(0,nu):
		use = np.where(names == uname[i] + '.bin')[0]
		
		dates = np.zeros(use.size,dtype='int32')
		for j in range(0,use.size):
			f = files[use[j]].split('/')
			dates[j] = np.int32(f[-2])
		dates.sort()
		
		out[uname[i]] = dates
	
	return out
			
