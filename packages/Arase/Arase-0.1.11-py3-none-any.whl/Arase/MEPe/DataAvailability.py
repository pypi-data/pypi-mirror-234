import numpy as np
from .ReadIndex import ReadIndex

def DataAvailability(L,prod):
	'''
	Provide a list of dates for which there are data.

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
	dates : int
		Array of dates which have data
	
	'''
	idx = ReadIndex(L,prod)
	return np.unique(idx.Date)
