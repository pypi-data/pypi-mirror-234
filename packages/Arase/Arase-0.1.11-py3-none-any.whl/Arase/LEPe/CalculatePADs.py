import numpy as np
from .Read3D import Read3D
from .GetPitchAngle import GetPitchAngle
import DateTimeTools as TT
import DateTimeTools as TT
from scipy.stats import binned_statistic

def CalculatePADs(Date,na=18,Verbose=True):
	'''
	Calculates a pitch angle distribution of the differential energy flux
	data using the level 2 3dflux data.
	
	WARNING: This may not be exactly the same as level 3 data, also 
	some level 2 data is missing the instrument orientation data required
	
	Inputs
	======
	Date : int
		Date to alcualte PAD for
	na : int
		Number of alpha (pitch angle) bins to create in the range 0 to 
		180 degrees
	Verbose: bool
		Display progress
		
		
	Returns
	=======
	out : dict
		Contains a dict for each species
	
	'''
		
	#this is the output dictionary
	out = {}
	
	#read the 3D data in
	data,meta = Read3D(Date)
	
	#calculate alpha
	alpha = GetPitchAngle(Date,data=data)
	
	#determine the size of the output arrays
	nt = data['Epoch'].size
	ne = data['FEDU_Energy'].shape[2]
	
	#get the dates/times
	Date,ut = TT.CDFEpochtoDate(data['Epoch'])
	utc = TT.ContUT(Date,ut)
	
	#get the energy arrays (shape: (nt,ne))
	EMin = data['FEDU_Energy'][:,0,:]/1000.0
	EMax = data['FEDU_Energy'][:,1,:]/1000.0
	Emid = 10.0**(0.5*(np.log10(EMin) + np.log10(EMax)))
	
	#get the alpha limits
	Alpha = np.linspace(0.0,180.0,na+1)

	#create 3D array for fluxes
	flux = np.zeros((nt,ne,na),dtype='float32') + np.nan
	
	
	#loop through each dimension (slow!)
	FLUX = data['FEDU']*1000.0
	bad = np.where(FLUX <= 0)
	FLUX[bad] = np.nan
		
	for i in range(0,nt):
		if Verbose:
			print('\r{:6.2f}%'.format(100.0*(i+1)/nt),end='')
		for j in range(0,ne):
			a = alpha[i].flatten()
			f = FLUX[i,j].flatten()
			good = np.where(np.isfinite(f))[0]
			if good.size > 0:
				flux[i,j],_,_ = binned_statistic(a[good],f[good],statistic='mean',bins=Alpha)
	if Verbose:
		print()		
	
	tmp = {}
	tmp['Date'] = Date
	tmp['ut'] = ut
	tmp['utc'] = utc
	tmp['Emin'] = EMin
	tmp['Emax'] = EMax
	tmp['Alpha'] = Alpha
	tmp['Flux'] = flux
	
	out['eFlux'] = tmp
	
	return out
