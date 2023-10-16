import numpy as np
from .ReadMGF import ReadMGF
from scipy.interpolate import interp1d
from scipy.ndimage import uniform_filter
import DateTimeTools as TT

def InterpObj(Date,Coords='GSE',Smooth=None):
	'''
	Return interpolation objects for MGF data.
	
	'''
	
	#read the data in
	mag = ReadMGF(Date)
	
	#get continuous time
	mutc = TT.ContUT(mag.Date,mag.ut)
	
	#interpolate the bad data
	good = np.where(np.isfinite(mag['Bx'+Coords]))[0]
	bad = np.where(np.isfinite(mag['Bx'+Coords]) == False)[0]
	fx = interp1d(mutc[good],mag['Bx'+Coords][good],bounds_error=False,fill_value='extrapolate')
	fy = interp1d(mutc[good],mag['By'+Coords][good],bounds_error=False,fill_value='extrapolate')
	fz = interp1d(mutc[good],mag['Bz'+Coords][good],bounds_error=False,fill_value='extrapolate')
	
	if not Smooth is None:
	
		mag['Bx'+Coords][bad] = fx(mutc[bad])
		mag['By'+Coords][bad] = fy(mutc[bad])
		mag['Bz'+Coords][bad] = fz(mutc[bad])
			


		#interpolation objects
		fx = interp1d(mutc,uniform_filter(mag['Bx'+Coords],Smooth),bounds_error=False,fill_value='extrapolate')
		fy = interp1d(mutc,uniform_filter(mag['By'+Coords],Smooth),bounds_error=False,fill_value='extrapolate')
		fz = interp1d(mutc,uniform_filter(mag['Bz'+Coords],Smooth),bounds_error=False,fill_value='extrapolate')
		
		
	return fx,fy,fz
