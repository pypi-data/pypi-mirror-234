from .. import Globals
import numpy as np
from ..Tools.Downloading._ReadDataIndex import _ReadDataIndex as RDI

def _ReadDataIndex(prod):
	'''
	Reads index file containing a list of all of the dates with their
	associated data file name (so that we can pick the version 
	automatically).
	'''
	idxfname = Globals.DataPath + 'Pos/Index-{:s}.dat'.format(prod)

	#read the data index
	idx = RDI(idxfname)
	
	return idx
