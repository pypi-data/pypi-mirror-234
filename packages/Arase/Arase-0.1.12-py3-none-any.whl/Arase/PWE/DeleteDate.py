import numpy as np
from ..Tools.Downloading._DeleteDate import _DeleteDate
from .. import Globals

def DeleteDate(Date,subcomp,L,prod,Confirm=True):
	'''
	delete all of the files from a given date
	
	'''
	if subcomp == 'hfa' and L == 3:
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}.dat'.format(L,subcomp)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/'.format(subcomp,L)
	else:	
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}-{:s}.dat'.format(L,subcomp,prod)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/{:s}/'.format(subcomp,L,prod)
		
	
	_DeleteDate(Date,idxfname,datapath,Confirm)
