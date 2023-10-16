import numpy as np
import os
import PyFileIO as pf

def ReadMirrorAlt(Date,path):
	'''
	Read a PAD file
	
	'''	
	#get the file name
	fname = path + '{:08d}/'.format(Date) + 'Mirror.bin'

	#check it exists
	if not os.path.isfile(fname):
		print('File not found')
		return None
		
	#read the data
	f = open(fname,'rb')
	out = {}
	keys = ['Date','ut','utc','Alt','AltMid','Bm','BmMid','B0',
			'AlphaN','AlphaS','BaltN','BaltS','LCAlt']
	for k in keys:
		if k == 'utc':
			dtype = 'float64'
		else:
			dtype = 'float32'	
		out[k] = pf.ArrayFromFile(dtype,f)

	f.close()
	return out
