import numpy as np


def RelVelocity(K,m):
	'''
	Calculate the relativistic velocity of a particle (hopefully correctly).
	
	Inputs
	======
	K : float
		Energy in keV
	m : float 
		mass of particle in kg
		
	Returns
	=======
	v : float
		velocity in m/s
	
	'''
	
	#convert keV to J
	e = 1.6022e-19
	E = 1000*e*K
	
	#now the velocity
	c = 3e8
	c2 = c**2
	mc2 = m*c2
	v = np.sqrt((1.0-1.0/(((E/(mc2)) + 1)**2))*c2)
	
	return v
