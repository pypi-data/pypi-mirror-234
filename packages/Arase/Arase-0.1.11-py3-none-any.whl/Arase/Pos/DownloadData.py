from .. import Globals
import numpy as np
from ..Tools.Downloading._DownloadData import _DownloadData
from ..Tools.ListDates import ListDates
from ..Tools.GetCurrentDate import GetCurrentDate

def DownloadData(prod='def',Date=[20170101,None],Overwrite=False,Verbose=False):
	'''
	Downloads Arase position data.

	Inputs
	======
	prod : str
		'l3' or 'def' - 'def' is the default and is what is used by other routines.
	Date : int|list
		Single date, pair of dates (as a range) or list of 3 or more specific dates.
	Overwrite : bool
		Force overwriting of data files.
	Verbose : bool
		More output if True.
		
	'''
	url0 = 'https://ergsc.isee.nagoya-u.ac.jp/data/ergsc/satellite/erg/orb/{:s}/'.format(prod)
	vfmt = ['v']	
	idxfname = Globals.DataPath + 'Pos/Index-{:s}.dat'.format(prod)
	datapath = Globals.DataPath + 'Pos/{:s}/'.format(prod)

	#populate the list of dates to download
	if np.size(Date) == 1:
		if Date is None:
			Date = GetCurrentDate()
		dates = np.array([Date])
	elif np.size(Date) == 2:
		if Date[1] is None:
			Date[1] = GetCurrentDate()
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	#a hack because of directory structures
	if prod == 'l3':
		u16 = np.where(dates < 20170101)[0]
		dates16 = dates[u16]
		u17 = np.where(dates >= 20170101)[0]
		dates = dates[u17]
	else:
		dates16 = np.array([])
		
	if dates16.size > 0 :
		url16 = url0 + '{:04d}/tmp/'
		_DownloadData(url16,idxfname,datapath,dates16,vfmt,Overwrite,Verbose)
		StartYear = 2017
	
	url0 += '{:04d}/'
	_DownloadData(url0,idxfname,datapath,dates,vfmt,Overwrite,Verbose)
	
