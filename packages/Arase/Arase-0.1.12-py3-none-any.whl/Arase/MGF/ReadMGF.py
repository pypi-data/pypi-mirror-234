import numpy as np
from .ReadCDF import ReadCDF
import DateTimeTools as TT
from ..Tools.ListDates import ListDates

def ReadMGF(Date):
	'''
	Reads the level 2 8sec data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
		If Date is a single integer - one date is loaded.
		If Date is a 2-element tuple or list, all dates from Date[0] to
		Date[1] are loaded.
		If Date contains > 2 elements, all dates within the list will
		be loaded.
			
	Returns
	=======
	data : numpy.recarray
		Contains the following fields:
				'Date' : int32
				'ut' : float32
				'Epoch' : int64
				'BxGSE' : float32
				'ByGSE' : float32
				'BzGSE' : float32
				'BxGSM' : float32
				'ByGSM' : float32
				'BzGSM' : float32
				'BxSM' : float32
				'BySM' : float32
				'BzSM' : float32
				'B' : float32	
		

	'''	


	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()


	dtype = [	('Date','int32'),
				('ut','float32'),
				('Epoch','int64'),
				('BxGSE','float32'),
				('ByGSE','float32'),
				('BzGSE','float32'),
				('BxGSM','float32'),
				('ByGSM','float32'),
				('BzGSM','float32'),
				('BxSM','float32'),
				('BySM','float32'),
				('BzSM','float32'),
				('B','float32')]	
		
	ne = []	
	datarr = []

	#loop through dates
	for date in dates:	

		#read the CDF file
		data,meta = ReadCDF(date,2,'8sec')		

		if data is None:
			continue

		#create output array

					
		n = data['epoch_8sec'].size
		out = np.recarray(n,dtype=dtype)
		
		#get the data
		out.Date,out.ut = TT.CDFEpochtoDate(data['epoch_8sec'])
		out.Epoch = data['epoch_8sec']

		#copy the various fields across
		out.B = data['magt_8sec']
		out.BxGSE = data['mag_8sec_gse'][:,0]
		out.ByGSE = data['mag_8sec_gse'][:,1]
		out.BzGSE = data['mag_8sec_gse'][:,2]
		out.BxGSM = data['mag_8sec_gsm'][:,0]
		out.ByGSM = data['mag_8sec_gsm'][:,1]
		out.BzGSM = data['mag_8sec_gsm'][:,2]
		out.BxSM = data['mag_8sec_sm'][:,0]
		out.BySM = data['mag_8sec_sm'][:,1]
		out.BzSM = data['mag_8sec_sm'][:,2]
		
		for f in out.dtype.names:
			if 'B' in f:
				bad = np.where(out[f] <= -1e+30)[0]
				out[f][bad] = np.nan
				
		datarr.append(out)
		ne.append(n)
		
	#combine together
	n = np.sum(ne,dtype='int32')
	out = np.recarray(n,dtype=dtype)
	p = 0
	for i in range(0,len(datarr)):
		out[p:p+ne[i]] = datarr[i]
		p += ne[i]
	
	return out
	
				
