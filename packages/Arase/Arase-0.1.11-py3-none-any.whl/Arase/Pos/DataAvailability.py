import numpy as np
from ._ReadDataIndex import _ReadDataIndex

def DataAvailability(prod='def'):
	'''
	Provide a list of dates for which there are data.

	Inputs
	======
	prod : str
		'l3' or 'def'
	
	Returns
	=======
	dates : int
		Array of dates which have data
	
	'''
	idx = _ReadDataIndex(prod)
	return np.unique(idx.Date)
