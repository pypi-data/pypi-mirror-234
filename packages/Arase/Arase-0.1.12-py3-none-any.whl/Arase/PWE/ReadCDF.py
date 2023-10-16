import numpy as np
import os
from .. import Globals
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from ..Tools.ReadCDF import ReadCDF as RCDF

def ReadCDF(Date,subcomp,L,prod):
	'''
	Reads the CDF file containing Arase XEP data.

	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	subcomp : string
		Name of sub component of instrument
	L : int
		Level of data to download
	prod : str
		Data product to download


	Available data products
	=======================
	subcomp		L		prod
	efd			2		'E_spin'
	efd			2		'pot'
	efd			2		'spec'
	hfa			2		'high'
	hfa			2		'low'
	hfa			2		'monit'
	hfa			3		''
	ofa			2		'complex'
	ofa			2		'matrix'
	ofa			2		'spec'
	
	Returns
	=======
	data : dict
		Dictionary containing the data for each variable stored within 
		the CDF file.
	meta : dict
		Dictionary containing the metadata for each variable in the data
		dictionary.
	
	'''

	if subcomp == 'hfa' and L == 3:
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}.dat'.format(L,subcomp)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/'.format(subcomp,L)
	else:	
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}-{:s}.dat'.format(L,subcomp,prod)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/{:s}/'.format(subcomp,L,prod)


	#read the data index
	idx = _ReadDataIndex(idxfname)

	#check the index for the appropriate date
	use = np.where(idx.Date == Date)[0]
	if use.size == 0:
		print('Date not found, run Arase.Pos.DownloadData() to check for updates.')
		return None,None
	idx = idx[use]
	mx = np.where(idx.Version  == np.max(idx.Version))[0]
	mx = mx[0]
	
	#get the file name
	fname = idx[mx].FileName
	
	#path
	fname = datapath + fname
	
	#check file exists
	if not os.path.isfile(fname):
		print('Index is broken: Update the data index')
		return None,None
		
	#read the file
	return RCDF(fname)
