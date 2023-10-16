import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex
from .. import Globals

def ReadIndex(L,prod):
	'''
	Reads the index file for a given data product.
	
	Inputs
	======
	L : int
		Level of data to download
	prod : str
		Data product to download


	Available data products
	=======================
	L		prod
	2		'omniflux'
	2		'3dflux'
	3		'3dflux'
	
	
	Returns
	=======
	numpy.recarray
	
	'''
	idxfname = Globals.DataPath + 'MEPe/Index-L{:01d}-{:s}.dat'.format(L,prod)
	return _ReadDataIndex(idxfname)
