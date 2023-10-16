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
	ne = data['FEDU_Energy'].size
	
	#get the dates/times
	Date,ut = TT.CDFEpochtoDate(data['epoch'])
	utc = TT.ContUT(Date,ut)
	
	#get the energy arrays (shape: (nt,ne))
	Emid = data['FEDU_Energy']
	lE = np.log10(Emid)
	dE = np.abs(lE[1:] - lE[:-1])
	lEmin = np.append(lE[0]-dE[0]/2.0,lE[1:]-dE/2.0)
	lEmax = np.append(lE[:-1]+dE/2.0,lE[-1]+dE[-1]/2.0,)
	
	EMin = 10**lEmin
	EMax = 10**lEmax
	
	#get the alpha limits
	Alpha = np.linspace(0.0,180.0,na+1)

	#create 3D array for fluxes
	flux = np.zeros((nt,ne,na),dtype='float32') + np.nan
	
	
	#loop through each dimension (slow!)
	FLUX = data['FEDU']
	bad = np.where(FLUX <= 0)
	FLUX[bad] = np.nan
	for i in range(0,nt):
		if Verbose:
			print('\r{:6.2f}%'.format(100.0*(i+1)/nt),end='')
		for j in range(0,ne):
			a = alpha[i].flatten()
			f = FLUX[i,:,j].flatten()
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
