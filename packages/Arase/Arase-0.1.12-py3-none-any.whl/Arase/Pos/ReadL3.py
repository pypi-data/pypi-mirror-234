import numpy as np
from ._ReadCDF import _ReadCDF
import DateTimeTools as TT
import DateTimeTools as TT

def ReadL3(Date):
	'''
	Reads the 'l3' position files for a given date
	
	'''
	
	#read the CDF file
	data,meta = _ReadCDF(Date,'l3')

	if data is None:
		return None

	#create an output array
	dtype = [	('Date','int32'),					#Date in format yyyymmdd
				('ut','float32'),					#Hours from beginning of the day
				('utc','float64'),					#Hours from beginning of 19500101
				('Epoch','int64'),					#CDF Epoch time
				('PosEq','float32',(2,)),			#Equatorial footprint
				('NFPLatLon','float32',(2,)),		#Northern ionospheric lat and long
				('SFPLatLon','float32',(2,)),		#Southern ionospheric lat and long
				('Lm','float32',(9,)),				#McIlwain's L parameter for pitch angles of 90, 80, 70, 60, 50, 40, 30, 20 and 10 deg in descending order (using OP77Q model)
				('Lstar','float32',(9,)),			#L-star parameter for pitch angles of 90, 80, 70, 60, 50, 40, 30, 20 and 10 deg in descending order (using OP77Q model)
				('I','float32',(9,)),				#I: the integral invariant (Roederer, J. G., Dynamics of the geomagnetically trapped radiation, Springer New York, pp. 48, 1970)
				('BmagLocal','float32'),			#Local magnetic model field magnitude
				('BmagEq','float32')]				#Equatorial magnetic model field magnitude
	
	n = data['epoch'].size
	out = np.recarray(n,dtype=dtype)
	
	#list the field mappings
	fields = {	'pos_eq_op' : 'PosEq', 
				'pos_iono_north_op' : 'NFPLatLon', 
				'pos_iono_south_op' : 'SFPLatLon', 
				'pos_blocal_op' : 'BmagLocal', 
				'pos_beq_op' : 'BmagEq', 
				'pos_lmc_op' : 'Lm', 
				'pos_lstar_op' : 'Lstar',
				'pos_I_op' : 'I'}
				
	print(fields.keys(), data.keys())
				
	#convert dates and times
	out.Date,out.ut = TT.CDFEpochtoDate(data['epoch'])
	out.utc = TT.ContUT(out.Date,out.ut)
	
	#move the data into the recarray
	for f in list(fields.keys()):
		out[fields[f]] = data[f]
		if 'FILLVAL' in list(meta[f].keys()):
			badval = np.float32(meta[f]['FILLVAL'])
			bad = np.where(out[fields[f]] == badval)
			try:
				out[fields[f]][bad] = np.nan
			except:
				pass

		
	return out
