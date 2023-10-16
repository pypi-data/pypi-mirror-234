import numpy as np
from .CalculatePADs import CalculatePADs
from ..Tools.SavePAD import SavePAD
from .. import Globals
from .ReadIndex import ReadIndex
from .. import MGF
from ..MGF.DownloadData import DownloadData as DownloadMGF
from .DownloadData import DownloadData
from .DeleteDate import DeleteDate
from ..Tools.ListDates import ListDates
from .SaveMirrorAlts import SaveMirrorAlts
import os

def SavePADs(Date,na=18,Overwrite=False,DownloadMissingData=True,
		DeleteNewData=True,Verbose=True):
	'''
	Save the PADs for a date or dates.
	
	Input
	=====
	Date : int
		Date to download data for in format yyyymmdd
		If single date - only data from that one day will be fetched
		If 2-element array - dates from Date[0] to Date[1] will be downloaded
		If > 2 elements - this is treated as a specific list of dates to download
	na : int
		Number of alpha bins
	Overwrite: bool
		Overwrite existing PADs
	DownloadMissingData : bool
		Download missing 3dflux data
	DeleteNewData : bool
		If we had to download any new data, then delete it to save space
	'''
	
	#populate the list of dates to save
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	path = Globals.DataPath + 'MEPi/PAD/'
		
	#read the data index to see what data we have
	idx = ReadIndex(2,'3dflux')
	magidx = MGF.ReadIndex(2,'8sec')
		
	for date in dates:
		print('Saving date {:08d}'.format(date))
		
		#check if the 3dflux data exists
		downloadednew = False
		exists3d = date in idx.Date
		if not exists3d and DownloadMissingData:
			DownloadData(2,'3dflux',date,Verbose=Verbose)
			idx = ReadIndex(2,'3dflux')
			exists3d = date in idx.Date
			downloadednew = True
		#check if the MGF data exists
		existsmag = date in magidx.Date
		if not existsmag and DownloadMissingData:
			DownloadMGF(2,'8sec',date,Verbose=Verbose)
			magidx = ReadIndex(2,'8sec')
			existsmag = date in magidx.Date
		
		if existsmag and exists3d:
		
			pad = CalculatePADs(date,na,Verbose)
			SavePAD(date,path,pad,Overwrite)

		if downloadednew and DeleteNewData:
			DeleteDate(date,2,'3dflux',False)

		#save mirror stuff if needed
		mirrexists = os.path.isfile(path+ '{:08d}/Mirror.bin'.format(date))
		if (not mirrexists) or Overwrite:
			SaveMirrorAlts(date,na,Overwrite)
