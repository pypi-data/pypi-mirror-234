import numpy as np
from scipy.interpolate import interp1d

def _Gradient(x,y):
	
	dydx = (y[1:] - y[:-1])/(x[:1] - x[:-1])
	return dydx

def  _TraceB(S,R,B,z,LCAlts):
	Re = 6378.0

	Ralts = LCAlts/6378.0 + 1.0

	
	#calculate the indices for northern and southern bits of the field line
	dRdS = _Gradient(S,R)
	zc = 0.5*(z[1:] + z[:-1])
	
	#north
	indn = np.where((dRdS < 0) & (zc > 0))[0]
	if indn.size > 1:
		indn = indn[-1]
		fn = interp1d(R[:indn][::-1],B[:indn][::-1],bounds_error=False,fill_value=np.nan)
		Bn = fn(Ralts)
	else:
		Bn = np.zeros(LCAlts.size,dtype='float32') + np.nan
	
	
	
	inds = np.where((dRdS > 0) & (zc < 0))[0]
	if inds.size > 1:
		inds = inds[0]
		fs = interp1d(R[inds:],B[inds:],bounds_error=False,fill_value=np.nan)
		Bs = fs(Ralts)
	else:
		Bs = np.zeros(LCAlts.size,dtype='float32') + np.nan

	return Bn,Bs
	
	
def LossCone(T,B0,LCAlt,Verbose=True):
	
	#calculate the B magnitude at each altitude
	nAlt = np.size(LCAlt)
	nT = T.n
	BaltN = np.zeros((nT,nAlt),dtype='float32')
	BaltS = np.zeros((nT,nAlt),dtype='float32')
	
	nT = T.n
	print('Calculating Loss Cone Fields')
	for i in range(0,nT):
		if Verbose:
			print('\rTrace {0} of {1}'.format(i+1,nT),end='')
		B = np.sqrt(T.Bx[i]**2 + T.By[i]**2 + T.Bz[i]**2)[:np.int32(T.nstep[i])]
		S = T.s[i][:np.int32(T.nstep[i])]
		R = T.R[i][:np.int32(T.nstep[i])]
		z = T.z[i][:np.int32(T.nstep[i])]
		BaltN[i],BaltS[i] = _TraceB(S,R,B,z,LCAlt)
	if Verbose:
		print()
	
	AlphaN = np.arcsin(np.sqrt(B0/BaltN.T).T)*180/np.pi
	AlphaS = np.arcsin(np.sqrt(B0/BaltS.T).T)*180/np.pi

	return AlphaN,AlphaS,BaltN,BaltS
