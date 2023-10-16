from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData

def DownloadData(L,prod,Date=[20170101,20200101],Overwrite=False,Verbose=True):
	'''
	Downloads Arase LEPe data. This routine will look for newer versions
	of existing data too.

	Inputs
	======
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
	L		prod
	2		'omniflux'
	2		'3dflux'
	
	'''
	
	url0 = 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/lepe/l{:01d}/{:s}/'.format(L,prod) + '{:04d}/{:02d}/'
	vfmt = ['v','_']
	idxfname = Globals.DataPath + 'LEPe/Index-L{:01d}-{:s}.dat'.format(L,prod)
	datapath = Globals.DataPath + 'LEPe/l{:01d}/{:s}/'.format(L,prod)
	
	_DownloadData(url0,idxfname,datapath,Date,vfmt,Overwrite,Verbose)

			
			
