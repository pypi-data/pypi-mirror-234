import numpy as np
import DateTimeTools as TT
from ..MGF.InterpObj import InterpObj

def CalculatePitchAngles(Date,ut,angles,mag):
	'''
	Calculate the pitch angles for the 3D particle data.
	
	Inputs
	======
	Date : int
		Date array
	ut : flout
		UT time array (hours from start of day)
	angles : float
		Array of instrument azimuths and elevations in GSE coords
	mag : None or numpy.recarray
		Set to MGF data array, or None and it will be loaded 
		automatically
		
	Returns
	=======
	Estimated pitch angles
	
	'''
	#continuous time axis
	putc = TT.ContUT(Date,ut)
	
	#work out unit vector in cartesian coordinates
	px = np.cos(angles[:,0])*np.cos(angles[:,1])
	py = np.cos(angles[:,0])*np.sin(angles[:,1])
	pz = np.sin(angles[:,0])
	
	if mag is None:
		fx,fy,fz = InterpObj(np.unique(Date),Smooth=8)		
	else:
		fx,fy,fz = mag
			

	#interpolate mag data to the time axis of the particle spectra
	bx = fx(putc)
	by = fy(putc)
	bz = fz(putc)
	
	#work out magnitude
	B = np.sqrt(bx**2 + by**2 + bz**2)
	
	#convert to unit vector
	bx/=B
	by/=B
	bz/=B
	
	#create b arrays the same shape as px,py,pz arrays
	bx = (np.zeros(px.shape).T + bx).T
	by = (np.zeros(py.shape).T + by).T
	bz = (np.zeros(pz.shape).T + bz).T
	
	#now calculate the pitch angle
	alpha = 180.0 - np.arccos((bx*px + by*py + bz*pz))*180.0/np.pi	

	return alpha
