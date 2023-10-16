import numpy as np
from .. import Globals
from ..Tools.Downloading._RebuildDataIndex import _RebuildDataIndex


def RebuildDataIndex(L,prod):
	
	vfmt = ['v']
	idxfname = Globals.DataPath + 'Pos/Index-{:s}.dat'.format(prod)
	datapath = Globals.DataPath + 'Pos/{:s}/'.format(prod)
	
	_RebuildDataIndex(datapath,idxfname,vfmt)
