import numpy as np
from ._ReadCDF import _ReadCDF
import DateTimeTools as TT
import DateTimeTools as TT

def ReadDef(Date):
	'''
	Reads the 'def' position (l2) files for a given date
	
	'''
	
	#read the CDF file
	data,meta = _ReadCDF(Date,'def')

	if data is None:
		return None

	#create an output array
	dtype = [	('Date','int32'),					#Date in format yyyymmdd
				('ut','float32'),					#Hours from beginning of the day
				('utc','float64'),					#Hours from beginning of 19500101
				('Epoch','int64'),					#CDF Epoch time
				('LatLonR','float32',(3,)),			#Geocentric latitude, longitude, and radial distance of the satellite position in unit of deg, deg, and km, respectively
				('PosGSE','float32',(3,)),			#position in GSE coords
				('PosGSM','float32',(3,)),			#position in GSM coords
				('PosSM','float32',(3,)),			#position in SM coords
				('PosRMLatMLon','float32',(3,)),	#R, magnetic latitude, and magnetic local time of spacecraft positions (using IGRF model)
				('PosEq','float32',(2,)),			#Equatorial footprint
				('NFPLatLon','float32',(2,)),		#Northern ionospheric lat and long
				('SFPLatLon','float32',(2,)),		#Southern ionospheric lat and long
				('BvecLocal','float32',(3,)),		#Local magnetic model field vector
				('BmagLocal','float32'),			#Local magnetic model field magnitude
				('BvecEq','float32',(3,)),			#Equatorial magnetic model field vector
				('BmagEq','float32'),				#Equatorial magnetic model field magnitude
				('Lm','float32',(3,)),				#McIlwain's L parameter for pitch angles of 30, 60, and 90 deg, in descending order
				('VelGSE','float32',(3,)),			#Velocity in GSE coords
				('VelGSM','float32',(3,)),			#Velocity in GSM coords
				('VelSM','float32',(3,)),			#Velocity in SM coords
				('SpinNo','int16'),					#Spin number
				('ManPrep','int8'),					#Flag for maneuver preparation
				('ManOnOff','int8'),				#Flag for maneuver on/off
				('Eclipse','int8')]					#Flag for eclipse
	n = data['epoch'].size
	out = np.recarray(n,dtype=dtype)
	
	#list the field mappings
	fields = {	'pos_llr' : 'LatLonR', 
				'pos_gse' : 'PosGSE', 
				'pos_gsm' : 'PosGSM', 
				'pos_sm' : 'PosSM', 
				'pos_rmlatmlt' : 'PosRMLatMLon', 
				'pos_eq' : 'PosEq', 
				'pos_iono_north' : 'NFPLatLon', 
				'pos_iono_south' : 'SFPLatLon', 
				'pos_blocal' : 'BvecLocal', 
				'pos_blocal_mag' : 'BmagLocal', 
				'pos_beq' : 'BvecEq', 
				'pos_beq_mag' : 'BmagEq', 
				'pos_Lm' : 'Lm', 
				'vel_gse' : 'VelGSE', 
				'vel_gsm' : 'VelGSM', 
				'vel_sm' : 'VelSM', 
				'spn_num' : 'SpinNo', 
				'man_prep_flag' : 'ManPrep', 
				'man_on_flag' : 'ManOnOff', 
				'eclipse_flag' : 'Eclipse'}
				
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
