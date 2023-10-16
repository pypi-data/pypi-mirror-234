import numpy as np
import os
import PyFileIO as pf

def SaveMirrorAlt(Date,path,Mirror,Overwrite=False):
	'''
	Save mirror altitudes and fields to go with the pitch angle 
	distribution data
	
	'''
	#create the output path
	outpath = path + '{:08d}/'.format(Date)
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
		os.system('chmod 777 '+outpath)

	
	#loop through and save each one
	fname = outpath + 'Mirror.bin'
	if os.path.isfile(fname) and not Overwrite:
		return
	print('saving file: {:s}'.format(fname))
	f = open(fname,'wb')
	keys = ['Date','ut','utc','Alt','AltMid','Bm','BmMid','B0',
			'AlphaN','AlphaS','BaltN','BaltS','LCAlt']
	for k in keys:
		if k == 'utc':
			dtype = 'float64'
		else:
			dtype = 'float32'
		pf.ArrayToFile(Mirror[k],dtype,f)

	f.close()

	#change permissions
	os.system('chmod 666 '+fname)
