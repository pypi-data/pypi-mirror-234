import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.SpecCls import SpecCls
import DateTimeTools as TT

def Read3D(Date):
	'''
	Reads the level 2 3dflux data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
	
	Returns
	=======
	data : dict
		Dictionary containing the data for each variable stored within 
		the CDF file.
	meta : dict
		Dictionary containing the metadata for each variable in the data
		dictionary.
		
	NOTE: In future, the data and meta dicts may be replaced by an object
	similar to that returned from ReadOmni.	
	'''
				
	#read the CDF file
	data,meta = ReadCDF(Date,2,'3dflux')		

	if data is None:
		return None

	return data,meta
