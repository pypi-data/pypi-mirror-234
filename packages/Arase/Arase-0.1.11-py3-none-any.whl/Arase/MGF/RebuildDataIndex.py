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
	2		'8sec'

	'''		
	vfmt = ['v','.']
	idxfname = Globals.DataPath + 'MGF/Index-L{:01d}-{:s}.dat'.format(L,prod)
	datapath = Globals.DataPath + 'MGF/l{:01d}/{:s}/'.format(L,prod)
	
	_RebuildDataIndex(datapath,idxfname,vfmt)
