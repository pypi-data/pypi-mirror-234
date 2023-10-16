import numpy as np
from ..Tools.Downloading._DeleteDate import _DeleteDate
from .. import Globals

def DeleteDate(Date,L,prod,Confirm=True):
	'''
	Delete all of the files from a given date
	
	'''
	idxfname = Globals.DataPath + 'HEP/Index-L{:01d}-{:s}.dat'.format(L,prod)
	datapath = Globals.DataPath + 'HEP/l{:01d}/{:s}/'.format(L,prod)

	_DeleteDate(Date,idxfname,datapath,Confirm)
