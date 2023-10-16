import numpy as np


def MirrorField(B0,alpha0):
	'''
	Given a local field magnitude and pitch angle, calculate the 
	magnetic field required to mirror a particle.
	
	Inputs
	======
	B0 : float
		Array of B magnitude length nB
	alpha0 : float
		Array of pitch angles, length na (degrees)
	
	Returns
	=======
	Bm : float
		Magnetic field of mirror point for each alpha at each B, shape
		(nB,na)
	
	'''

	#mesh together
	alpha = 90 - (np.abs(90-alpha0))
	sin2a = np.sin(alpha*np.pi/180.0)**2
	a,b = np.meshgrid(sin2a,B0)
	
	#get Bm
	Bm = b/a
	
	return Bm
