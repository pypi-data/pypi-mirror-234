import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import interp1d
from .PSDtoCounts import PSDtoCounts
from .PSDtoFlux import PSDtoFlux
from .CountstoFlux import CountstoFlux
from .CountstoPSD import CountstoPSD
from scipy.stats import mode
import DateTimeTools as TT
from ..Pos.ReadFieldTraces import ReadFieldTraces
from .PosDTPlotLabel import PosDTPlotLabel
from .RelVelocity import RelVelocity
from .ColorMap import jetish
import matplotlib.patheffects as path_effects
from scipy.stats import mode
import matplotlib.patheffects as path_effects


defargs = {	'tlabel' : 'UT',
			'elabel' : '$E$ (keV)',
			'vlabel' : '$V$ (m s$^{-1}$)',
			'alabel' : r'Pitch Angle, $\alpha$ ($^{\circ}$)',
			'flabel' : 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)',
			'plabel' : 'PSD (s$^3$ m$^{-6}$)',
			'elog' : True,
			'vlog' : True,
			'flog' : True, 
			'plog' : True, 
			'ScaleType' : 'range',
			'nStd' : 2}

amu = 1.6605e-27

ParticleMass = { 	'e' : 9.10938356e-31,
					'H' : 1.6726219e-27,
					'He' : 4.002602*amu,
					'O' : 15.999*amu,
					'O2' : 15.999*amu*2}
	
#list of bins to group together for the stack plot				
SpecBins = {	'LEPe' : [[0,3],[4,7],[8,11],[12,15],[16,19],[20,23],[24,27]],
				'LEPi' : [[0,3],[4,7],[8,11],[12,15],[16,19],[20,23],[24,27],[28,31]],
				'MEPe' : [[0,1],[2,3],[4,5],[6,7],[8,9],[10,11],[12,13],[14,15]],
				'MEPi' : [[0,1],[2,3],[4,5],[6,7],[8,9],[10,11],[12,13],[14,15]],
				'HEPL'  : [[0,1],[2,3],[4,5],[6,7],[8,9],[10,11],[12,13],[14,15]], 
				'HEPH'  : [[0,2],[2,3],[4,5],[6,7],[8,9],[10,10]], }

class PSpecPADCls(object):
	def __init__(self,PADSpec,Instrument,SpecType='e',Mirror=None,**kwargs):
		'''
		An object for storing and plotting particle spectral data.
		
		See SpecCls.Plot, SpecCls.PlotSpectrum and SpecCls.GetSpectrum
		for more information.
		
		Inputs
		=====
		PADSpec : dict
			dictionary containing the pitch angle distribution data
		SpecType : str
			'e'|'H'|'He'|'O'|'O2'
		tlabel : str
			Label for time axis
		elabel : str
			Label for Energy axis
		vlabel : str
			Label for velocity axis
		alabel : str
			Label for pitch angle axis
		flabel : str
			Label for fluxes
		plabel : str
			Label for PSD
		elog : bool
			True for logarithmic energy axis
		vlog : bool
			True for logarithmic velocity axis
		flog : bool
			True for logarithmic flux axis
		plog : bool
			True for logarithmic PSD axis
		
		'''
		
		#create lists to store the input variables
		self.Mass = ParticleMass.get(SpecType,9.10938356e-31)
		self.n = 0
		self.SpecType = SpecType
		self.Instrument = Instrument

		#store the input variables by appending to the existing lists
		self.Date = PADSpec['Date']
		self.ut = PADSpec['ut']
		self.utc = PADSpec['utc']
		self.Emax = PADSpec['Emax']
		self.Emin = PADSpec['Emin']
		self.Alpha = PADSpec['Alpha']
		self.Flux = PADSpec['Flux']

		if not Mirror is None:
			keys = ['Alt','AltMid','Bm','BmMid','B0',
					'AlphaN','AlphaS','BaltN','BaltS','LCAlt']
			for k in keys:
				setattr(self,k,Mirror[k])
	
		#Process the energy bins
		self._ProcessEnergy()

		#get phase space density
		self._CalculatePSD()
		
		#calculate dt
		self._ProcessDT()


		
		
		#and the keywords
		self.tlabel = kwargs.get('tlabel',defargs['tlabel'])
		self.elabel = kwargs.get('elabel',defargs['elabel'])
		self.vlabel = kwargs.get('vlabel',defargs['vlabel'])
		self.alabel = kwargs.get('alabel',defargs['alabel'])
		self.flabel = kwargs.get('flabel',defargs['flabel'])
		self.plabel = kwargs.get('plabel',defargs['plabel'])
		self._elog = kwargs.get('elog',defargs['elog'])
		self._vlog = kwargs.get('vlog',defargs['vlog'])
		self._flog = kwargs.get('flog',defargs['flog'])
		self._plog = kwargs.get('plog',defargs['plog'])
		self._ScaleType = kwargs.get('ScaleType',defargs['ScaleType'])
		self._nStd = kwargs.get('nStd',defargs['nStd'])
		
		#calculate the new time, energy and z scale limits
		self._CalculateTimeLimits() 
		self._CalculateEnergyLimits()
		self._CalculateScale()
		self._CalculateVLimits()
		self._CalculatePSDScale()		

	
	def _ProcessEnergy(self):
		'''
		Process the energy bins
		
		'''


		#calculate the middle (logarithmically)
		lemin = np.log10(self.Emin)
		lemax = np.log10(self.Emax)
		self.Emid = 10.0**(0.5*(lemin + lemax))

		
		#sort everything in ascending order of energy
		if len(self.Emid.shape) == 2:
			m,_ = mode(self.Emid,axis=0,keepdims=True)
			srt = np.argsort(m[0])
			self.Emid = self.Emid[:,srt]
			self.Emin = self.Emin[:,srt]
			self.Emax = self.Emax[:,srt]
		else:
			srt = np.argsort(self.Emid)
			self.Emid = self.Emid[srt]
			self.Emin = self.Emin[srt]
			self.Emax = self.Emax[srt]		
		self.Flux = self.Flux[:,srt,:]
		
		
	def _ProcessDT(self):
		#set the interval between each measurement (assuming ut is start 
		#of interval and that ut + dt is the end
		dt = (self.utc[1:] - self.utc[:-1])
		self.dt = np.append(dt,dt[-1]).clip(max=8.0/3600.0)
		

	def _CalculatePSD(self):
		e = 1.6022e-19
		self.V = np.sqrt(np.float64(e*2000.0*self.Emid)/self.Mass)
		self.V0 = np.sqrt(np.float64(e*2000.0*(self.Emin)/self.Mass))
		self.V1 = np.sqrt(np.float64(e*2000.0*(self.Emax)/self.Mass))
		
		self.V = RelVelocity(self.Emid,self.Mass)
		self.V0 = RelVelocity(self.Emin,self.Mass)
		self.V1 = RelVelocity(self.Emax/2.0,self.Mass)

		psd = np.zeros(self.Flux.shape,dtype='float64')
		if np.size(self.V.shape) == 1: 
			nv = self.V.size
			for i in range(0,nv):
				psd[:,i,:] =  np.float64(self.Flux[:,i,:])*(np.float64(self.Mass)/(2000*e*np.float64(self.Emid[i]/self.Mass))) * np.float64(10.0/e)
		else:
			nv = self.V.shape[-1]
			for i in range(0,nv):
				psd[:,i,:] =  (np.float64(self.Flux[:,i,:].T)*(np.float64(self.Mass)/(2000*e*np.float64(self.Emid[:,i]/self.Mass))) * np.float64(10.0/e)).T
		self.PSD = psd
			
	
	
	# def _GetSpectrum(self,I,sutc,dutc,Method,PSD):
	
		# #get the appropriate data
		# l = self.Label[I]
		# utc = self.utc[I]
		# if PSD:
			# f = self.V[I]
			# Spec = self.PSD[I]		
		# else:
			# f = self.Energy[I]
			# Spec = self.Spec[I]		
		
		# #find the nearest
		# dt = np.abs(utc - sutc)
		# near = np.where(dt == dt.min())[0][0]
		
		# #check if the nearest is within dutc
		# if dt[near] > dutc:
			# return [],[],[]
			
		
		# #check if we are past the end of the time series, or Method is nearest
		# if (Method == 'nearest') or (sutc < utc[0]) or (sutc > utc[-1]):
			# s = Spec[near,:]
			# if len(f.shape) == 2:
				# e = f[near,:]
			# else:
				# e = f
			
		# else:
			# #in this case we need to find the two surrounding neighbours
			# #and interpolate between them
			# bef = np.where(utc <= sutc)[0][-1]
			# aft = np.where(utc > sutc)[0][0]
			
			# s0 = Spec[bef,:]
			# s1 = Spec[aft,:]
			
			# if len(f.shape) == 2:
				# e0 = f[near,:]
				# e1 = f[near,:]
			# else:
				# e0 = f
				# e1 = f
			
			# dx = utc[aft] - utc[bef]
			# ds = s1 - s0
			# de = e1 - e0
			
			# dsdx = ds/dx
			# dedx = de/dx
			
			# dt = sutc - utc[bef]
			
			# s = s0 + dt*dsdx
			# e = e0 + dt*dedx
		
		
		# #remove rubbish
		# good = np.where(e > 0)[0]
		# e = e[good]
		# s = s[good]
			
		# #sort by e
		# srt = np.argsort(e)
		# e = e[srt]
		# s = s[srt]
		# return e,s,l

	def _GetSpectrum(self,sutc,dutc,Method,xparam,zparam):
		'''
		Return a 2D array of the nearest spectrum to the specified time
		(or interpolated between the two surrounding ones)
		'''
		#select PSD or Flux
		if xparam == 'V':
			x = self.V
			x0 = self.V0
			x1 = self.V1
			xlabel = self.vlabel
		else:
			x = self.Emid
			x0 = self.Emin
			x1 = self.Emax
			xlabel = self.elabel
		y = 0.5*(self.Alpha[1:] + self.Alpha[:-1])
		y0 = self.Alpha[:-1]
		y1 = self.Alpha[1:]
		ylabel = self.alabel
		if zparam == 'PSD':
			z = self.PSD
			zlabel = self.plabel
		else:
			z = self.Flux
			zlabel = self.flabel
			
		#sort the E/V axis
		if len(x.shape) == 1:
			srt = np.argsort(x)
			x = x[srt]
			x0 = x0[srt]
			x1 = x1[srt]
		else:
			srt = np.argsort(x[0,:])
			x = x[:,srt]
			x0 = x0[:,srt]
			x1 = x1[:,srt]
		z = z[:,srt,:]
			
		#find the surrounding utc
		utc = self.utc
		dt = np.abs(utc - sutc)
		near = np.where(dt == dt.min())[0][0]
		
		#check if the nearest is within dutc
		if dt[near] > dutc:
			return None,None,None		
			
		if (Method == 'nearest') or (sutc < utc[0]) or (sutc > utc[-1]):
			z = z[near,:,:]
			if len(x.shape) == 2:
				x = x[near,:]
				x0 = x0[near,:]
				x1 = x1[near,:]
			
		else:
			#in this case we need to find the two surrounding neighbours
			#and interpolate between them
			bef = np.where(utc <= sutc)[0][-1]
			aft = np.where(utc > sutc)[0][0]
			
			z0 = z[bef,:,:]
			z1 = z[aft,:,:]
			
			if len(x.shape) == 2:
				_x0 = x[near,:]
				_x1 = x[near,:]
				_x00 = x0[near,:]
				_x01 = x0[near,:]
				_x10 = x1[near,:]
				_x11 = x1[near,:]
			else:
				_x0 = x
				_x1 = x
				_x00 = x0
				_x01 = x0
				_x10 = x1
				_x11 = x1
			
			dt = utc[aft] - utc[bef]
			dz = z1 - z0
			dx = _x1 - _x0
			
			dzdt = dz/dt
			dxdt = dx/dt
			
			m = sutc - utc[bef]
			
			z = z0 + m*dzdt
			x = _x0 + m*dxdt	
			x0 = _x00 + m*dxdt	
			x1 = _x10 + m*dxdt	
				
		return (x,x0,x1),(y,y0,y1),z,xlabel,ylabel,zlabel
		
	def GetSpectrum2D(self,ut,Method='nearest',Maxdt=60.0,xparam='E',zparam='Flux'):
		'''
		Return a 2D particle spectrum
		
		Inputs
		======
		ut : float
			Time of particle spectrum to get (hours from start of day)
		Method : str
			'Nearest'|'Interp' - either find the nearest time (within
			Maxdt seconds of ut, or interpolate if possible between two
			nearest spectra)
		Maxdt : float
			Maximum acceptable difference in time between ut and the 
			returned spectrum
		xparam : str
			One dimension of the returned spectrum
			'E' - Energy
			'V' - Velocity
		zparam : str
			'Flux'|'PSD' - type of spectrum to return.
		
		Returns
		=======
		(x,x0,x1) : middle,minimum,maximum of xparam bins
		(y,y0,y1) : middle,minimum,maximum of alpha (pitch angle) bins
		z : 2D array of either Flux or PSD
		xlabel : Plot label for x-axis
		ylabel : Plot label for y-axis
		zlabel : Plot label for z-axis
		'''
		
		
		#get the current date
		Date = mode(self.Date,keepdims=True)[0][0]
		
		#get the utc
		utc = TT.ContUT(Date,ut)[0]
		
		#get the 2D spectrum
		x,y,z,xlabel,ylabel,zlabel = self._GetSpectrum(utc,Maxdt/3600.0,Method,xparam,zparam)
	
	
		return x,y,z,xlabel,ylabel,zlabel
	
	def GetSpectrum1D(self,ut,Bin=0,Method='nearest',Maxdt=60.0,xparam='E',yparam='Flux'):
		'''
		Return a 1D particle spectrum
		
		Inputs
		======
		ut : float
			Time of particle spectrum to get (hours from start of day)
		Bin : int
			Index of bin to use - when xparam is 'alpha', Bin corresponds
			to the energy/velocity bin, otherwise Bin corresponds to the
			pitch angle bin number.
		Method : str
			'Nearest'|'Interp' - either find the nearest time (within
			Maxdt seconds of ut, or interpolate if possible between two
			nearest spectra)
		Maxdt : float
			Maximum acceptable difference in time between ut and the 
			returned spectrum
		xparam : str
			One dimension of the returned spectrum
			'E' - Energy
			'V' - Velocity
			'alpha' - pitch angle
		yparam : str
			'Flux'|'PSD' - type of spectrum to return.
		
		Returns
		=======
		(x,x0,x1) : middle,minimum,maximum of xparam bins
		y : 1D array of either Flux or PSD
		xlabel : Plot label for x-axis
		ylabel : Plot label for y-axis
		'''
	
		#get the current date
		Date = mode(self.Date,keepdims=True)[0][0]
		
		#get the utc
		utc = TT.ContUT(Date,ut)[0]
		
		#get the 2D spectrum (this could get a little confusing)
		if xparam == 'alpha':
			_,x,y,_,xlabel,ylabel = self._GetSpectrum(utc,Maxdt/3600.0,Method,'E',yparam)
			y = y[Bin]
		else:
			x,_,y,xlabel,_,ylabel = self._GetSpectrum(utc,Maxdt/3600.0,Method,xparam,yparam)
			y = y[:,Bin]
	
		return x,y,xlabel,ylabel

	def PlotSpectrum1D(self,ut,Bin=0,Method='nearest',Maxdt=60.0,
		xparam='E',yparam='Flux',fig=None,maps=[1,1,0,0],color=None,
		xlog=None,ylog=None,nox=False,noy=False):	
		'''
		Plot a 1D particle spectrum
		
		Inputs
		======
		ut : float
			Time of particle spectrum to get (hours from start of day)
		Bin : int
			Index of bin to use - when xparam is 'alpha', Bin corresponds
			to the energy/velocity bin, otherwise Bin corresponds to the
			pitch angle bin number.
		Method : str
			'Nearest'|'Interp' - either find the nearest time (within
			Maxdt seconds of ut, or interpolate if possible between two
			nearest spectra)
		Maxdt : float
			Maximum acceptable difference in time between ut and the 
			returned spectrum
		xparam : str
			One dimension of the returned spectrum
			'E' - Energy
			'V' - Velocity
			'alpha' - pitch angle
		yparam : str
			'Flux'|'PSD' - type of spectrum to return.
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		maps : list
			[xmaps,ymaps,xmap,ymap] controls position of subplot
		xlog : bool
			if True, color scale is logarithmic
		ylog : bool
			If True, y-axis is logarithmic
		nox : bool
			If True, no labels or tick marks are drawn for the x-axis
		noy : bool
			If True, no labels or tick marks are drawn for the y-axis
		color : None or list
			Define the color of the line to be plotted
		'''


		
		
		#get the spectrum
		x,y,xlabel,ylabel = self.GetSpectrum1D(ut,Bin,Method,Maxdt,xparam,yparam)
		x = x[0]

		
		#create the figure
		if fig is None:
			fig = plt
			fig.figure()
		if hasattr(fig,'Axes'):	
			ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		else:
			ax = fig	
			
		#get the yparameter stuff
		if xparam == 'E':
			if xlog is None:
				xlog = self._elog
			ax.set_xlim(self._elim)
		elif xparam == 'V':
			if xlog is None:
				xlog = self._vlog
			ax.set_xlim(self._vlim)
		elif xparam == 'alpha':
			xlog = False
			ax.set_xlim([0.0,180.0])
		else:
			return		
				
		if xlog:
			ax.set_xscale('log')
			

		#turn axes off when needed
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])
		
		#get z stuff
		if yparam == 'Flux':
			if ylog is None:
				ylog = self._flog
		elif yparam == 'PSD':
			if ylog is None:
				ylog = self._plog

		if ylog:
			ax.set_yscale('log')
				
		#plot the data
		ax.plot(x,y,marker='.',color=color)
		
		
		#labels
		ax.set_xlabel(xlabel)
		ax.set_ylabel(ylabel)

		Date = mode(self.Date,keepdims=True)[0][0]
		hh,mm,ss,_ = TT.DectoHHMM(ut)
		ax.set_title('{:08d} {:02d}:{:02d}:{:02d} UT, Bin {:d}'.format(Date,hh[0],mm[0],ss[0],Bin))			
				
		return ax
						
		
	def PlotSpectrum2D(self,ut,Method='nearest',Maxdt=60.0,xparam='E',zparam='Flux',
		fig=None,maps=[1,1,0,0],xlog=None,zlog=None,nox=False,noy=False,
		scale=None,cmap='gnuplot'):	
		'''
		Plot a 2D particle spectrum
		
		Inputs
		======
		ut : float
			Time of particle spectrum to get (hours from start of day)
		Method : str
			'Nearest'|'Interp' - either find the nearest time (within
			Maxdt seconds of ut, or interpolate if possible between two
			nearest spectra)
		Maxdt : float
			Maximum acceptable difference in time between ut and the 
			returned spectrum
		xparam : str
			One dimension of the returned spectrum
			'E' - Energy
			'V' - Velocity
		zparam : str
			'Flux'|'PSD' - type of spectrum to return.
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		maps : list
			[xmaps,ymaps,xmap,ymap] controls position of subplot
		xlog : bool
			if True, x-axis is logarithmic
		zlog : bool
			If True, color scale is logarithmic
		nox : bool
			If True, no labels or tick marks are drawn for the x-axis
		noy : bool
			If True, no labels or tick marks are drawn for the y-axis
		cmap : str
			String containing the name of the colomap to use
		scale : list
			2-element list or tuple containing the minimum and maximum
			extents of the color scale
		'''
		


	
		
		#get the spectra
		x,y,z,xlabel,ylabel,zlabel = self.GetSpectrum2D(ut,Method,Maxdt,xparam,zparam)
		ye = np.append(y[1],y[2][-1])
		
		#create the figure
		if fig is None:
			fig = plt
			fig.figure()
		if hasattr(fig,'Axes'):	
			ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		else:
			ax = fig	
			
		#get the yparameter stuff
		if xparam == 'E':
			if xlog is None:
				xlog = self._elog
			ax.set_xlim(self._elim)
			x0 = x[1]
			x1 = x[2]
			ax.set_xlabel(self.elabel)
		elif xparam == 'V':
			if xlog is None:
				xlog = self._vlog
			ax.set_xlim(self._vlim)
			x0 = x[1]
			x1 = x[2]
			ax.set_xlabel(self.vlabel)
		else:
			return		
				
		if xlog:
			ax.set_xscale('log')
			
		ax.set_ylabel(self.alabel)
	
		#turn axes off when needed
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])

		#get z stuff
		if zparam == 'Flux':
			zlabel = self.flabel
			if zlog is None:
				zlog = self._flog
			if scale is None:
				scale = self._scale
		elif zparam == 'PSD':
			zlabel = self.plabel
			if zlog is None:
				zlog = self._plog
			if scale is None:
				scale = self._psdscale
			
		#get color scale
		if zlog:
			norm = colors.LogNorm(vmin=scale[0],vmax=scale[1])
		else:
			norm = colors.Normalize(vmin=scale[0],vmax=scale[1])
	
		for i in range(0,x[0].size):				
			xtmp = np.array([x0[i],x1[i]])
			if np.isfinite(xtmp).all():
				#plot each row of energy/velocity
				xg,yg = np.meshgrid(xtmp,ye)
				
				ztmp = np.array([z[i]])
				
				sm = ax.pcolormesh(xg,yg,ztmp.T,cmap=cmap,norm=norm)
		
		#colorbar
		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="2.5%", pad=0.05)

		cbar = fig.colorbar(sm,cax=cax) 
		cbar.set_label(zlabel)		
		
		#get the title
		Date = mode(self.Date,keepdims=True)[0][0]
		hh,mm,ss = TT.DectoHHMM(ut,ss=True,Split=True)
		ax.set_title('{:08d} {:02d}:{:02d}:{:02d} UT'.format(Date,hh,mm,ss))	
						
		return ax
	
	def PlotSpectrogramStack(self,Bins=None,ut=None,fig=None,
				scale=[1e3,1e9],cmap='gnuplot',zparam='Flux',
				ShowLossCone=True,LCAlt=100.0):
		'''
		Plot a stack of spectrograms.
		
		Inputs
		======
		Bins : list
			List of bin ranges to combine, if set to None then a default
			set of bin lists will be used.
		ut : list/tuple
			2-element start and end times for the plot, where each 
			element is the time in hours sinsce the start fo the day,
			e.g. 17:30 == 17.5.
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		scale : list
			2-element list or tuple containing the minimum and maximum
			extents of the color scale
		cmap : str
			String containing the name of the colomap to use
		zparam : str
			'Flux'|'PSD' - type of spectrum to return.

		Returns
		=======
		ax : list
			List of Axes instances
		
		'''			
		if Bins is None:
			Bins = SpecBins[self.Instrument]
		
		#find number of axes to create
		Bins = np.array(Bins)
		na = Bins.shape[0]
		
		#create the figure
		fig = plt
		fig.figure(figsize=(11,8))
		
		#create blank axes
		cf = fig.gcf()
		axb = plt.subplot2grid((1,1),(0,0))
		axb.spines['top'].set_color('none')
		axb.spines['bottom'].set_color('none')
		axb.spines['left'].set_color('none')
		axb.spines['right'].set_color('none')
		axb.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
		
		if cmap == 'jetish':
			cmap = jetish
		sm = plt.cm.ScalarMappable(cmap=cmap, norm=colors.LogNorm(vmin=scale[0], vmax=scale[1]))
		sm._A = []
		
		
		#plot each one
		ax = []
		for i in range(0,na):
			nox = i != 0
			tmpax = self.PlotSpectrogram(Bins[i],ut=ut,fig=fig,
					maps=[1,na,0,na-i-1],cmap=cmap,scale=scale,yparam='alpha',
					nox=nox,ColorBar=False,ShowLossCone=ShowLossCone,LCAlt=LCAlt)
			title = tmpax.get_title()
			tmpax.set_title('')
			tmpax.set_ylabel(r'$\alpha$ ($^\circ$)')
			txt = tmpax.text(0.01,0.9,title,color='black',ha='left',va='center',transform=tmpax.transAxes)
			txt.set_path_effects([path_effects.Stroke(linewidth=2,foreground='white'),path_effects.Normal()])
			ax.append(tmpax)
		
		
		fig.subplots_adjust(hspace=0.0,right=0.8,top=0.95,bottom=0.15)

		#spax = fig.gca()
		p = axb.get_position().extents
		
		cbar_ax = cf.add_axes([0.85, 0.1*(p[3]-p[1]) + p[1], 0.025, 0.8*(p[3]-p[1])])
		cbar=fig.colorbar(sm, cax=cbar_ax)
		if zparam == 'PSD':
			zlabel = defargs['plabel']
		else:
			zlabel = defargs['flabel']
		cbar.set_label(zlabel)		
		
		return ax
		
	def PlotSpectrogram(self,Bin,ut=None,fig=None,maps=[1,1,0,0],
			yparam='E',zparam='Flux',ylog=None,scale=None,zlog=None,
			cmap='gnuplot',nox=False,noy=False,TickFreq='auto',
			PosAxis=True,ColorBar=True,ShowLossCone=True,LCAlt=100.0):
		'''
		Plots the spectrogram
		
		Inputs
		======
		ut : list/tuple
			2-element start and end times for the plot, where each 
			element is the time in hours sinsce the start fo the day,
			e.g. 17:30 == 17.5.
		Bin : int
			Index of pitch angle bin to use - scan be a scalar or an 
			array. If Bin is an array of two elements, then it will be 
			treated as a range; if there are more than two then each one
			will be used. Fluxes from multiple bins will be summed.
		yparam : str
			One dimension of the returned spectrum
			'E' - Energy
			'V' - Velocity
		zparam : str
			'Flux'|'PSD' - type of spectrum to return.
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		maps : list
			[xmaps,ymaps,xmap,ymap] controls position of subplot
		xlog : bool
			if True, color scale is logarithmic
		ylog : bool
			If True, y-axis is logarithmic
		cmap : str
			String containing the name of the colomap to use
		scale : list
			2-element list or tuple containing the minimum and maximum
			extents of the color scale
		nox : bool
			If True, no labels or tick marks are drawn for the x-axis
		noy : bool
			If True, no labels or tick marks are drawn for the y-axis
		'''
		
		#get the list of bins to use
		if hasattr(Bin,'__iter__'):
			if np.size(Bin) == 2:
				bins = np.arange(Bin[0],Bin[1]+1)
				binstr = 'Bins {:d} to {:d}'.format(bins[0],bins[-1])
			else:
				bins = np.array(Bins)
				if np.size(bins) == 1:
					binstr = 'Bin {:d}'.format(bins[0])
				else:
					binstr = ['{:d}, '.format(bins[i]) for i in range(bins.size-1)]
					binstr.append('and {:d}'.format(bins[-1]))
					binstr = 'Bins '+''.join(binstr)
		else:
			bins = np.array([Bin])
			binstr = 'Bin {:d}'.format(Bin)


		#create the plot
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		#set time axis limits
		if ut is None:
			ax.set_xlim(self._utlim)
		else:
			Date = mode(self.Date,keepdims=True)[0][0]
			utclim = TT.ContUT(np.array([Date,Date]),np.array(ut))
			ax.set_xlim(utclim)
			
		#get the yparameter stuff
		if yparam == 'E':
			Arange = [self.Alpha[bins[0]],self.Alpha[bins[-1]+1]]
			title = r'$\alpha$ {:s} ({:4.1f} - {:4.1f}'.format(binstr,Arange[0],Arange[1])+'$^{\circ}$)'
			if ylog is None:
				ylog = self._elog
			ax.set_ylim(self._elim)
			y0 = self.Emin
			y1 = self.Emax
			ax.set_ylabel(self.elabel)
		elif yparam == 'V':
			Arange = [self.Alpha[bins[0]],self.Alpha[bins[-1]+1]]
			title = r'$\alpha$ {:s} ({:4.1f} - {:4.1f}'.format(binstr,Arange[0],Arange[1])+'$^{\circ}$)'
			if ylog is None:
				ylog = self._vlog
			ax.set_ylim(self._vlim)
			y0 = self.V0
			y1 = self.V1
			ax.set_ylabel(self.vlabel)
		elif yparam == 'alpha':
			if len(self.Emin.shape) == 2:
				Energies = self.Emid[:,bins]
			else:
				Energies = self.Emid[bins]
			Erange = [np.nanmin(Energies),np.nanmax(Energies)]
			title = '$E$/$V$ {:s} ({:5.2f} - {:5.2f} keV)'.format(binstr,Erange[0],Erange[1])
			ylog = False
			ax.set_ylim([0.0,180.0])
			y0 = self.Alpha[:-1]
			y1 = self.Alpha[1:]
			ax.set_ylabel(self.alabel)
		else:
			return			
		if ylog:
			ax.set_yscale('log')
		ax.set_xlabel(self.tlabel)
		ax.set_title(title)
	


		#get z stuff
		if zparam == 'Flux':
			if yparam == 'alpha':
				z = np.nansum(self.Flux[:,bins,:],axis=1)
			else:
				z = np.nansum(self.Flux[:,:,bins],axis=2)
			
			zlabel = self.flabel
			if zlog is None:
				zlog = self._flog
			if scale is None:
				scale = self._scale
		elif zparam == 'PSD':
			if yparam == 'alpha':
				z = np.nansum(self.PSD[:,bins,:],axis=1)
			else:
				z = np.nansum(self.PSD[:,:,bins],axis=2)
			zlabel = self.plabel
			if zlog is None:
				zlog = self._plog
			if scale is None:
				scale = self._psdscale
			
		#get color scale
		if zlog:
			norm = colors.LogNorm(vmin=scale[0],vmax=scale[1])
		else:
			norm = colors.Normalize(vmin=scale[0],vmax=scale[1])
		if cmap == 'jetish':
			cmap = jetish
		
		
		#create plots
		sm = self._PlotSpectrogram(ax,y0,y1,z,norm,cmap)

		#turn axes off when needed
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		else:
			#sort the UT axis out
			if PosAxis:
				Date = mode(self.Date,keepdims=True)[0][0]
				Pos = ReadFieldTraces(Date)
				
				#get the Lshell, Mlat and Mlon
				good = np.where(np.isfinite(Pos.Lshell) & np.isfinite(Pos.MlatN) & np.isfinite(Pos.MlonN))[0]
				Pos = Pos[good]
				fL = interp1d(Pos.utc,Pos.Lshell,bounds_error=False,fill_value='extrapolate')
				fLon = interp1d(Pos.utc,Pos.MlonN,bounds_error=False,fill_value='extrapolate')
				fLat = interp1d(Pos.utc,Pos.MlatN,bounds_error=False,fill_value='extrapolate')
			
				PosDTPlotLabel(ax,self.utc,self.Date,fL,fLon,fLat,TickFreq=TickFreq)
				ax.set_xlabel('')
			else:
				TT.DTPlotLabel(ax,self.utc,self.Date,TickFreq=TickFreq)
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])

		if ShowLossCone and (yparam == 'alpha'):
			self._PlotLossCone(ax,LCAlt)
			
		#colorbar
		if ColorBar:
			divider = make_axes_locatable(ax)
			cax = divider.append_axes("right", size="2.5%", pad=0.05)

			cbar = fig.colorbar(sm,cax=cax) 
			cbar.set_label(zlabel)	
		self.currax = ax	
		return ax

	def _PlotLossCone(self,ax,LCAlt):
		
		#interpolate the loss cone altitudes first
		if LCAlt < 0.0:
			An = self.AlphaN[:,0]
			As = self.AlphaS[:,0]
			
		elif LCAlt > self.LCAlt[-1]:
			An = self.AlphaN[:,-1]
			As = self.AlphaS[:,-1]
		
		else:
			if LCAlt < 200.0:
				i0 = 2
				i1 = 3
			else:
				i0 = np.where(self.LCAlt <= LCAlt)[0][-1]
				i1 = np.where(self.LCAlt >= LCAlt)[0][0]
			if i0 == i1:
				An = self.AlphaN[:,i0]
				As = self.AlphaS[:,i0]
			else:
				A0 = self.LCAlt[i0]
				A1 = self.LCAlt[i1]
				Alpha0N = self.AlphaN[:,i0]
				Alpha0S = self.AlphaS[:,i0]
				Alpha1N = self.AlphaN[:,i1]
				Alpha1S = self.AlphaS[:,i1]

				dAlphaN = Alpha1N - Alpha0N
				dAlphaS = Alpha1S - Alpha0S
				dA = A1 - A0
				dANdA = dAlphaN/dA
				dASdA = dAlphaS/dA

				CN = Alpha0N
				CS = Alpha0S
				
				An = dANdA*(LCAlt-A0) + CN
				As = dASdA*(LCAlt-A0) + CS

			
		#plot North at bottom and South at top
		ln = ax.plot(self.utc,An,color=[0.0,1.0,0.0],linestyle='--')
		ls = ax.plot(self.utc,180.0-As,color=[0.0,1.0,0.0],linestyle='--')

		ln[0].set_path_effects([path_effects.Stroke(linewidth=2,foreground='k'),path_effects.Normal()])
		ls[0].set_path_effects([path_effects.Stroke(linewidth=2,foreground='k'),path_effects.Normal()])

	

	def UpdateTimeAxis(self,ax=None,ut=None,TickFreq='auto'):
		'''
		Update the time ax is limits and labels.
		
		Inputs
		======
		ax : None or Axes object
			If None, then the current Axes instance will be used
		ut : list/tuple
			2-element start and end times for the plot, where each 
			element is the time in hours sinsce the start fo the day,
			e.g. 17:30 == 17.5.
		TickFreq : str or float
			If 'auto' the tick spacing will be calculated automatically,
			otherwise set to a number of hours between each tick.
		
		'''
		
		#check if an Axes instance has been supplied (if not, try getting the current one)
		if ax is None:
			ax = self.currax
			
		#check if we need to resize
		if not ut is None:
			Date = mode(self.Date,keepdims=True)[0][0]
			utclim = TT.ContUT(np.array([Date,Date]),np.array(ut))
			ax.set_xlim(utclim)		
			
		#now update the axis
		if PosAxis:
			Date = mode(self.Date,keepdims=True)[0][0]
			
			Pos = ReadFieldTraces(Date)
			
			#get the Lshell, Mlat and Mlon
			good = np.where(np.isfinite(Pos.Lshell) & np.isfinite(Pos.MlatN) & np.isfinite(Pos.MlonN))[0]
			Pos = Pos[good]
			fL = interp1d(Pos.utc,Pos.Lshell,bounds_error=False,fill_value='extrapolate')
			fLon = interp1d(Pos.utc,Pos.MlonN,bounds_error=False,fill_value='extrapolate')
			fLat = interp1d(Pos.utc,Pos.MlatN,bounds_error=False,fill_value='extrapolate')
		
		
			PosDTPlotLabel(ax,self.utc,self.Date,fL,fLon,fLat,TickFreq=TickFreq)
		else:
			TT.DTPlotLabel(ax,self.utc,self.Date,TickFreq=TickFreq)


	def _PlotSpectrogram(self,ax,y0,y1,z,norm,cmap):
		'''
		This will plot a single spectrogram
		
		'''
		#get the y ranges for each row of data
		bad = np.where(np.isnan(y0) | np.isnan(y1))
		y0[bad] = 0.0
		y1[bad] = 0.0

		#get the ut array limits
		t0 = self.utc
		t1 = self.utc + self.dt
		utc = self.utc
		
		#look for gaps in ut
		if len(y0.shape) > 1:

			isgap = ((utc[1:] - utc[:-1]) > 60.0/3600.0) | (((y0[1:,:] - y0[:-1,:]) != 0) | ((y0[1:,:] - y0[:-1,:]) != 0)).any(axis=1)
			ne = y0.shape[1]
		else:
			#isgap = (utc[1:] - utc[:-1]) > 1.1*dt[:-1]
			isgap = (utc[1:] - utc[:-1]) > 60.0/3600.0
			ne = y0.size
		gaps = np.where(isgap)[0] + 1
		if gaps.size == 0:
			#no gaps
			i0 = [0]
			i1 = [utc.size]
		else:
			#lots of gaps
			i0 = np.append(0,gaps)
			i1 = np.append(gaps,utc.size)
		ng = np.size(i0)

		#loop through each continuous block of utc
		for i in range(0,ng):
			ttmp = np.append(t0[i0[i]:i1[i]],t1[i1[i]-1])
			st = z[i0[i]:i1[i]]
			for j in range(0,ne):				
				if len(y0.shape) > 1:
					etmp = np.array([y0[i0[i],j],y1[i0[i],j]])
				else:
					etmp = np.array([y0[j],y1[j]])
				if np.isfinite(etmp).all():
					#plot each row of energy
					tg,eg = np.meshgrid(ttmp,etmp)
					s = np.array([st[:,j]])
					
					sm = ax.pcolormesh(tg,eg,s,cmap=cmap,norm=norm)
			
		return sm
		
	def _CalculateTimeLimits(self):
		'''
		Loop through all of the stored spectra and find the time limits.
		
		'''
		#initialize time limits
		self._utlim = [np.nanmin(self.utc),np.nanmax(self.utc)]
		
		
	def _CalculateEnergyLimits(self):
		'''
		Loop through all of the stored spectra and work out the energy
		range to plot.
		
		'''

		goodmin = np.where((self.Emin > 0) & np.isfinite(self.Emin))
		goodmax = np.where((self.Emax > 0) & np.isfinite(self.Emax))

		self._elim = [np.nanmin(self.Emin[goodmin]),np.nanmax(self.Emax[goodmax])]


	def _CalculateVLimits(self):
		'''
		Loop through all of the stored spectra and work out the velocity
		range to plot.
		
		'''
		goodmin = np.where((self.V0 > 0) & np.isfinite(self.V0))
		goodmax = np.where((self.V1 > 0) & np.isfinite(self.V1))

		self._vlim = [np.nanmin(self.V0[goodmin]),np.nanmax(self.V1[goodmax])]


		
	def _CalculateScale(self):
		'''
		Calculate the default scale limits for the plot.
		
		'''
		ls = np.log10(self.Flux)
		bad = np.where(self.Flux <= 0)
		ls[bad] = np.nan
				
		if self._ScaleType == 'std':
			mu = np.nanmean(self.Flux)
			std = np.std(self.Flux)
			
			lmu = np.nanmean(ls)
			lstd = np.std(ls)
				
			tmpscale = [mu - self._nStd*std, mu + self._nStd*std]
			tmplogscale = 10**np.array([lmu - self._nStd*lstd, lmu + self._nStd*lstd])					
			
		elif self._ScaleType == 'positive':
			#calculate the scale based on all values being positive 
			std = np.sqrt((1.0/np.sum(self.Flux.size))*np.nansum((self.Flux)**2))
			lstd = np.sqrt(((1.0/np.sum(np.isfinite(ls))))*np.nansum((ls)**2))
				
			tmpscale = [0.0,std*self._nStd]
			tmplogscale = 10**np.array([np.nanmin(ls),lstd*self._nStd])			
		else:
			#absolute range
			tmpscale = [np.nanmin(self.Flux),np.nanmax(self.Flux)]
			tmplogscale = 10**np.array([np.nanmin(ls),np.nanmax(ls)])


	
		self._scale = tmpscale
		self._logscale = tmplogscale
	
	def _CalculatePSDScale(self):
		'''
		Calculate the default scale limits for the plot.
		
		'''

		ls = np.log10(self.PSD)
		bad = np.where(self.PSD <= 0)
		ls[bad] = np.nan
				
		if self._ScaleType == 'std':
			mu = np.nanmean(self.PSD)
			std = np.std(self.PSD)
			
			lmu = np.nanmean(ls)
			lstd = np.std(ls)
				
			tmpscale = [mu - self._nStd*std, mu + self._nStd*std]
			tmplogscale = 10**np.array([lmu - self._nStd*lstd, lmu + self._nStd*lstd])					
			
		elif self._ScaleType == 'positive':
			#calculate the scale based on all values being positive 
			std = np.sqrt((1.0/np.sum(self.Flux.size))*np.nansum((self.PSD)**2))
			lstd = np.sqrt(((1.0/np.sum(np.isfinite(ls))))*np.nansum((ls)**2))
				
			tmpscale = [0.0,std*self._nStd]
			tmplogscale = 10**np.array([np.nanmin(ls),lstd*self._nStd])			
		else:
			#absolute range
			tmpscale = [np.nanmin(self.PSD),np.nanmax(self.PSD)]
			tmplogscale = 10**np.array([np.nanmin(ls),np.nanmax(ls)])


		
		self._psdscale = tmpscale
		self._psdlogscale = tmplogscale
