import numpy as np
from .ReadIndex import ReadIndex

def DataAvailability(subcomp,L,prod):
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
	dates : int
		Array of dates which have data
	
	'''
	idx = ReadIndex(subcomp,L,prod)
	return np.unique(idx.Date)
