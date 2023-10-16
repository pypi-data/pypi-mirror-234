import numpy as np
from .. import Globals
from ..Tools.Downloading._RebuildDataIndex import _RebuildDataIndex

def RebuildDataIndex(L,prod):
	'''
	Rebuilds the data index for a data product.

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
	'''
	
	vfmt = ['v','_']
	idxfname = Globals.DataPath + 'LEPi/Index-L{:01d}-{:s}.dat'.format(L,prod)
	datapath = Globals.DataPath + 'LEPi/l{:01d}/{:s}/'.format(L,prod)
	
	_RebuildDataIndex(datapath,idxfname,vfmt)
