import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from .. import Globals

def ReadIndex(subcomp,L,prod):
	'''
	Reads the index file for a given data product.
	
	Inputs
	======
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
	numpy.recarray
	
	'''
	if subcomp == 'hfa' and L == 3:
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}.dat'.format(L,subcomp)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/'.format(subcomp,L)
	else:	
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}-{:s}.dat'.format(L,subcomp,prod)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/{:s}/'.format(subcomp,L,prod)
	
	return _ReadDataIndex(idxfname)
