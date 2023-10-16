import numpy as np
from .ReadCDF import ReadCDF
import DateTimeTools as TT
from ..Tools.ListDates import ListDates

def ReadUHDensity(Date):
	'''
	Reads density measured using UH frequency.
	
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
				'Density' : float32
				'Fuh' : float32
				'Quality' : int32
		

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
				('Density','float32'),
				('Fuh','float32'),
				('Quality','int32')]

	ne = []	
	datarr = []

	#loop through dates
	for date in dates:	

		#read the CDF file
		data,meta = ReadCDF(date,'hfa',3,'')		

		if data is None:
			continue

		#create output array

		n = data['Epoch'].size
		out = np.recarray(n,dtype=dtype)
		
		#get the data
		out.Date,out.ut = TT.CDFEpochtoDate(data['Epoch'])
		out.Epoch = data['Epoch']
		out.Density = data['ne_mgf']
		out.Fuh = data['Fuhr']
		out.Quality = data['quality_flag']

		datarr.append(out)
		ne.append(n)

	#combine together
	n = np.sum(ne,dtype='int32')
	out = np.recarray(n,dtype=dtype)
	p = 0
	for i in range(0,len(datarr)):
		out[p:p+ne[i]] = datarr[i]
	
	
	return out
	
				
