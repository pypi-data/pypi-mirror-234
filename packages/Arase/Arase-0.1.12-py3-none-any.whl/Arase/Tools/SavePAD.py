import numpy as np
import os
import PyFileIO as pf

def SavePAD(Date,path,spec,Overwrite=False):
	'''
	Save pitch angle distribution data
	
	'''
	#create the output path
	outpath = path + '{:08d}/'.format(Date)
	if not os.path.isdir(outpath):
		os.system('mkdir -pv '+outpath)
		os.system('chmod 777 '+outpath)
	#create a list of spectra
	keys = list(spec.keys())
	
	#loop through and save each one
	for k in keys:
		tmp = spec[k]
		
		fname = outpath + k + '.bin'
		if os.path.isfile(fname) and not Overwrite:
			continue
		print('saving file: {:s}'.format(fname))
		f = open(fname,'wb')
		pf.ArrayToFile(tmp['Date'],'int32',f)
		pf.ArrayToFile(tmp['ut'],'float32',f)
		pf.ArrayToFile(tmp['utc'],'float64',f)
		pf.ArrayToFile(tmp['Emin'],'float32',f)
		pf.ArrayToFile(tmp['Emax'],'float32',f)
		pf.ArrayToFile(tmp['Alpha'],'float32',f)
		pf.ArrayToFile(tmp['Flux'],'float32',f)
		f.close()

		#change permissions
		os.system('chmod 666 '+fname)
