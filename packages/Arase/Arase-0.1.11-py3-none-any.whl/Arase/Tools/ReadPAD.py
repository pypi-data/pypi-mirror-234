import numpy as np
import os
import PyFileIO as pf

def ReadPAD(Date,path,SpecType):
	'''
	Read a PAD file
	
	'''	
	#get the file name
	fname = path + '{:08d}/'.format(Date) + SpecType + '.bin'

	#check it exists
	if not os.path.isfile(fname):
		print('File not found')
		return None
		
	#read the data
	f = open(fname,'rb')
	out = {}
	out['Date'] = pf.ArrayFromFile('int32',f)
	out['ut'] = pf.ArrayFromFile('float32',f)
	out['utc'] = pf.ArrayFromFile('float64',f)
	out['Emin'] = pf.ArrayFromFile('float32',f)
	out['Emax'] = pf.ArrayFromFile('float32',f)
	out['Alpha'] = pf.ArrayFromFile('float32',f)
	out['Flux'] = pf.ArrayFromFile('float32',f)	
	f.close()
	return out
