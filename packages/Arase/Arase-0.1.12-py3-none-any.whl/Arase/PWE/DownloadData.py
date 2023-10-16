from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData

def DownloadData(subcomp,L,prod='',Date=[20170101,20200101],Overwrite=False,Verbose=True):
	'''
	Downloads Arase PWE data. This routine will look for newer versions
	of existing data too.

	Inputs
	======
	subcomp : string
		Name of sub component of instrument
	L : int
		Level of data to download
	prod : str
		Data product to download
	Date : int
		Date to download data for in format yyyymmdd
		If single date - only data from that one day will be fetched
		If 2-element array - dates from Date[0] to Date[1] will be downloaded
		If > 2 elements - this is treated as a specific list of dates to download
	Overwrite : bool
		Overwrites existing data if True

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


	'''

	url0 = 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/pwe/{:s}/l{:01d}/'.format(subcomp,L)

	if subcomp == 'hfa' and L == 2:
		url0 += 'spec/{:s}/'.format(prod)
	elif subcomp == 'hfa' and L == 3:
		pass
	elif subcomp == 'ofa' or subcomp == 'efd':
		url0 += '{:s}/'.format(prod)
	url0 += '{:04d}/{:02d}/'

	vfmt = ['v','_']

	if subcomp == 'hfa' and L == 3:
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}.dat'.format(L,subcomp)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/'.format(subcomp,L)
	else:	
		idxfname = Globals.DataPath + 'PWE/Index-L{:01d}-{:s}-{:s}.dat'.format(L,subcomp,prod)
		datapath = Globals.DataPath + 'PWE/{:s}/L{:01d}/{:s}/'.format(subcomp,L,prod)
		

	_DownloadData(url0,idxfname,datapath,Date,vfmt,Overwrite,Verbose)

			
