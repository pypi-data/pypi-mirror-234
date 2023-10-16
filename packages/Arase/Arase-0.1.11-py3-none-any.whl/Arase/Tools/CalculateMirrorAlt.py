import numpy as np
import PyGeopack as gp
from .MirrorField import MirrorField
from ..Pos.GetPos import GetPos
import DateTimeTools as TT
from scipy.interpolate import interp1d
from ..MGF.ReadMGF import ReadMGF
from .MirrorAlt import MirrorAlt
from .LossCone import LossCone

def CalculateMirrorAlt(utc,na,Verbose=True):
	'''
	Given an array of continuous time and a number of pitch angle bins,
	calculate the altitude at which the particles should mirror using
	field traces.
	
	'''
	#get the date/time limits
	Date,ut = TT.ContUTtoDate(utc)
	Date0 = TT.MinusDay(Date.min())
	Date1 = TT.PlusDay(Date.max())
	
	
	#calcualte alpha
	alpha = np.linspace(0.0,180.0,na+1)
	alphac = 0.5*(alpha[1:] + alpha[:-1])
	
	#get the spacecraft position
	pos = GetPos()
	use = np.where((pos.Date >= Date0) & (pos.Date <= Date1) & np.isfinite(pos.Xgse))[0]
	pos = pos[use]
	fx = interp1d(pos.utc,pos.Xgse)
	fy = interp1d(pos.utc,pos.Ygse)
	fz = interp1d(pos.utc,pos.Zgse)
	x = fx(utc)
	y = fy(utc)
	z = fz(utc)

	#get the magnetic field
	mag = ReadMGF([Date0,Date1])
	mutc = TT.ContUT(mag.Date,mag.ut)
	B = np.sqrt(mag.BxSM**2 + mag.BySM**2 + mag.BzSM**2)
	gdb = np.where(np.isfinite(B))[0]
	fB = interp1d(mutc[gdb],B[gdb],bounds_error=False,fill_value='extrapolate')
	B0 = fB(utc)
	
	#get the mirror field strength
	Bm = MirrorField(B0,alpha)
	BmMid = MirrorField(B0,alphac)
	
	#field traces
	T = gp.TraceField(x,y,z,Date,ut,Model='T96',CoordIn='GSE',CoordOut='SM',Verbose=Verbose,Alt=0.0)
	
	#calculate the positions on the field line where the mirror points would be
	Alt = MirrorAlt(T,Bm,alpha,Verbose=Verbose)
	AltMid = MirrorAlt(T,BmMid,alphac,Verbose=Verbose)
	
	#calculate the pitch angle which would reach a bunch of altitudes
	LCAlt = np.linspace(0.0,1000.0,11)
	AlphaN,AlphaS,BaltN,BaltS = LossCone(T,B0,LCAlt,Verbose=Verbose)
	
	
	out = {}
	out['Date'] = Date
	out['ut'] = ut
	out['utc'] = utc
	out['Alt'] = Alt
	out['AltMid'] = AltMid
	out['Bm'] = Bm
	out['BmMid'] = BmMid
	out['B0'] = B0
	out['AlphaN'] = AlphaN
	out['AlphaS'] = AlphaS
	out['BaltN'] = BaltN
	out['BaltS'] = BaltS
	out['LCAlt'] = LCAlt
	return out
	
