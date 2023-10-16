import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import DateTimeTools as TT
from scipy.interpolate import interp1d
from ..Pos.ReadFieldTraces import ReadFieldTraces
from .PosDTPlotLabel import PosDTPlotLabel

defargs = {	'Meta' : None,
			'dt' : None,
			'bw' : None,
			'xlabel' : 'UT',
			'ylabel' : 'Frequency, $f$',
			'zlabel' : '',
			'ylog' : False,
			'zlog' : False, 
			'ScaleType' : 'range',
			'nStd' : 2}


class SpecCls(object):
	def __init__(self,**kwargs):
		'''
		An object for storing and plotting spectral data,
		
		See SpecCls.Plot, SpecCls.PlotSpectrum and SpecCls.GetSpectrum
		for more information.
		
		Inputs
		=====
		xlabel : str
			Label for x-axis
		ylabel : str
			Label for y-axis
		zlabel : str
			Label for color scale
		ylog : bool
			True for logarithmic y-axis
		zlog : bool
			True for logarithmic color scale
		
		'''
		
		#create lists to store the input variables
		self.Date = []
		self.ut = []
		self.Epoch = []
		self.Freq = []
		self.Spec = []
		self.utc = []
		self.bw = []
		self.dt = []
		self.Meta = []
		self.Label = []
		self.n = 0
		
		#and the keywords
		self.xlabel = kwargs.get('xlabel',defargs['xlabel'])
		self.ylabel = kwargs.get('ylabel',defargs['ylabel'])
		self.zlabel = kwargs.get('zlabel',defargs['zlabel'])
		self._ylog = kwargs.get('ylog',defargs['ylog'])
		self._zlog = kwargs.get('zlog',defargs['zlog'])
		self._ScaleType = kwargs.get('ScaleType',defargs['ScaleType'])
		self._nStd = kwargs.get('nStd',defargs['nStd'])
		
			

	
	def _ProcessBW(self,bw,Freq):
		
		if bw is None:
			#if bandwidth is None, then we must calculate it from the fequencies
			#Freqs are not necessarily in order annoyingly
			if len(Freq.shape) == 1:
				#remove bad ones first
				good = np.where((Freq > 0) & np.isfinite(Freq))[0]
				if good.size > 1:
					Fg = Freq[good]
					
					#get just unique ones
					Fu,ind,inv,cts = np.unique(Fg,return_counts=True,return_index=True,return_inverse=True)
					
					df = Fu[1:] - Fu[:-1]
					df = np.concatenate(([df[0]],df,[df[1]]))/2.0
					bwtmp = df[1:] + df[:-1]	
					
					bw = np.zeros(Freq.shape,dtype='float32') + np.nan
					bw[good] = bwtmp[inv]	
				else:
					bw = np.zeros(Freq.shape,dtype='float32') + np.nan	
			else:
				srt = np.argsort(Freq[0,:])
				tmpF = Freq[:,srt]
			
				df = tmpF[1:] - tmpF[:-1]
				df = np.concatenate(([df[0]],df,[df[1]]))/2.0
				bwtmp = df[1:] + df[:-1]
				
				
				bw = np.zeros(Freq.shape,dtype='float32')
				bw[srt] = bwtmp	
			
		elif np.size(bw) == 1:
			#if it is a single value, then turn it into an array the same size as Freq
			bw = np.zeros(Freq.shape,dtype='float32') + bw	
		
		return bw
		
	def _ProcessDT(self,dt,ut):
		#set the interval between each measurement (assuming ut is start 
		#of interval and that ut + dt is the end
		if dt is None:
			dt = (ut[1:] - ut[:-1])*3600.0
			u,c = np.unique(dt,return_counts=True)
			dt = u[np.where(c == c.max())[0][0]]
		
		#convert it to an array the same length as ut
		dt = np.zeros(ut.size,dtype='float32') + dt/3600.0
		return dt
		

					
	
	def AddData(self,Date,ut,Epoch,Freq,Spec,bw=None,dt=None,Meta=None,Label=''):
		'''
		Adds data to the object
		
		Inputs
		======
		Date : int
			Array of dates in format yyyymmdd
		ut : float
			Array of times since beginning of the day
		Epoch : float
			CDF epoch 
		Freq : float
			Array of frequencies
		Spec : float
			2D array containing the spectral data, shape (nt,nf) where
			nt is ut.size and nf is Freq.size
		bw : None or float
			Width of the frequency bins
		dt : None or float
			duration of each spectrum in units of seconds!
		Meta : dict
			Meta data from CDF - not used
		Label : str
			String containing a plot label if desired
		'''

		#store the input variables by appending to the existing lists
		self.Date.append(Date)
		self.ut.append(ut)
		self.Epoch.append(Epoch)
		self.Freq.append(Freq)
		self.Spec.append(Spec)		
		self.Meta.append(Meta)
		self.Label.append(Label)

	
		#get the bandwidth in the appropriate format
		self.bw.append(self._ProcessBW(bw,Freq))


		#calculate continuous time axis
		self.utc.append(TT.ContUT(Date,ut))
		
		#calculate dt
		self.dt.append(self._ProcessDT(dt,ut))

		#calculate the new time, frequency and z scale limits
		self._CalculateTimeLimits() 
		self._CalculateFrequencyLimits()
		self._CalculateScale()

		#add to the total count of spectrograms stored
		self.n += 1
	
	def _GetSpectrum(self,I,sutc,dutc,Method):
	
		#get the appropriate data
		l = self.Label[I]
		utc = self.utc[I]
		f = self.Freq[I]
		Spec = self.Spec[I]		
		
		#find the nearest
		dt = np.abs(utc - sutc)
		near = np.where(dt == dt.min())[0][0]
		
		#check if the nearest is within dutc
		if dt[near] > dutc:
			return [],[],[]
			
		
		#check if we are past the end of the time series, or Method is nearest
		if (Method == 'nearest') or (sutc < utc[0]) or (sutc > utc[-1]):
			s = Spec[near,:]
			if len(f.shape) == 2:
				e = f[near,:]
			else:
				e = f
			
		else:
			#in this case we need to find the two surrounding neighbours
			#and interpolate between them
			bef = np.where(utc <= sutc)[0][-1]
			aft = np.where(utc > sutc)[0][0]
			
			s0 = Spec[bef,:]
			s1 = Spec[aft,:]
			
			if len(f.shape) == 2:
				e0 = f[near,:]
				e1 = f[near,:]
			else:
				e0 = f
				e1 = f
			
			dx = utc[aft] - utc[bef]
			ds = s1 - s0
			de = e1 - e0
			
			dsdx = ds/dx
			dedx = de/dx
			
			dt = sutc - utc[bef]
			
			s = s0 + dt*dsdx
			e = e0 + dt*dedx
		
		
		#remove rubbish
		good = np.where(e > 0)[0]
		e = e[good]
		s = s[good]
			
		#sort by e
		srt = np.argsort(e)
		e = e[srt]
		s = s[srt]
		return e,s,l

	
	def GetSpectrum(self,Date,ut,Method='nearest',Maxdt=60.0,Split=False):
		'''
		This method will return a spectrum from a given time.
		
		Inputs
		======
		Date : int
			Date in format yyyymmdd
		ut : float
			Time in hours since beginning of the day
		Method : str
			'nearest'|'interpolate' - will find the nearest spectrum to
			the time specified time, or will interpolate between two 
			surrounding spectra.
		Maxdt : float
			Maximum difference in time between the specified time and the
			time of the spectra in seconds.
		Split : bool
			If True, the spectra will be returned as a list, if False,
			they will be combined to form a single spectrum.
		
		Returns
		=======
		freq : float/list
			Array(s) of frequencies
		spec : float/list
			Array(s) containing specral data
		labs : list
			List of plot labels
		
		'''
	
		#convert to continuous time
		utc = TT.ContUT(np.array([Date]),np.array([ut]))[0]
		dutc = Maxdt/3600.0
		
		#create the objects to store spectra and energy/frequency bins
		spec = []
		freq = []
		labs = []
		
		#get the spectra for each element in  self.Spec
		for i in range(0,self.n):
			e,s,l = self._GetSpectrum(i,utc,dutc,Method)
			if len(s) > 0:
				spec.append(s)
				freq.append(e)
				labs.append(l)
			
		#combine if necessary
		if not Split:
			spec = np.concatenate(spec)
			freq = np.concatenate(freq)
			srt = np.argsort(freq)
			spec = spec[srt]
			freq = freq[srt]
			
		return freq,spec,labs
		
	def PlotSpectrum(self,Date,ut,Method='nearest',Maxdt=60.0,Split=False,
		fig=None,maps=[1,1,0,0],color=None,xlog=True,ylog=None,
		nox=False,noy=False):
		'''
		This method will plot a spectrum from a given time.
		
		Inputs
		======
		Date : int
			Date in format yyyymmdd
		ut : float
			Time in hours since beginning of the day
		Method : str
			'nearest'|'interpolate' - will find the nearest spectrum to
			the time specified time, or will interpolate between two 
			surrounding spectra.
		Maxdt : float
			Maximum difference in time between the specified time and the
			time of the spectra in seconds.
		Split : bool
			If True, the spectra will be returned as a list, if False,
			they will be combined to form a single spectrum.
		fig : None, matplotlib.pyplot or matplotlib.pyplot.Axes instance
			If None - a new plot is created
			If an instance of pyplot then a new Axes is created on an existing plot
			If Axes instance, then plotting is done on existing Axes
		maps : list
			[xmaps,ymaps,xmap,ymap] controls position of subplot
		xlog : bool
			if True, x-axis is logarithmic
		ylog : bool
			If True, y-axis is logarithmic

		
				
		'''	
		
		#get the spectra
		freq,spec,labs = self.GetSpectrum(Date,ut,Method,Maxdt,Split)
		
		
		#create the figure
		if fig is None:
			fig = plt
			fig.figure()
		if hasattr(fig,'Axes'):	
			ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		else:
			ax = fig	
			
		#plot
		if Split:
			if not color is None:
				nc = len(color)
			for i in range(0,len(spec)):
				if color is None:
					ax.plot(freq[i],spec[i],label=labs[i],marker='.')
				else:
					ax.plot(freq[i],spec[i],color=color[i % nc],label=labs[i],marker='.')
			
		else:
			ax.plot(freq,spec,color=color,marker='.')

		#set the x-axis scale
		if xlog is None:
			xlog = self._ylog
		if xlog:
			ax.set_xscale('log')
		
		#set the y-axis scale
		if ylog is None:
			ylog = self._zlog
		if ylog:
			ax.set_yscale('log')
			
		#set the axis labels
		ax.set_xlabel(self.ylabel)
		ax.set_ylabel(self.zlabel)
			
		#turn axes off when needed
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])


		ax.legend(fontsize=8)
			
		return ax
				
		
	def Plot(self,Date=None,ut=[0.0,24.0],fig=None,maps=[1,1,0,0],
			ylog=None,scale=None,zlog=None,cmap='gnuplot',nox=False,
			noy=False,TickFreq='auto',PosAxis=True):
		'''
		Plots the spectrogram
		
		Inputs
		======
		Date : int32
			This, along with 'ut' controls the time limits of the plot,
			either set as a single date in the format yyyymmdd, or if 
			plotting over multiple days then set a 2 element tuple/list/
			numpy.ndarray with the start and end dates. If set to None 
			(default) then the time axis limits will be calculated 
			automatically.
		ut : list/tuple
			2-element start and end times for the plot, where each 
			element is the time in hours sinsce the start fo the day,
			e.g. 17:30 == 17.5.
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
		
		
		
		#create the plot
		if fig is None:
			fig = plt
			fig.figure()
		ax = fig.subplot2grid((maps[1],maps[0]),(maps[3],maps[2]))
		
		#set axis limits
		if Date is None:
			ax.set_xlim(self._utlim)
		else:
			if np.size(Date) == 1:
				Date0 = Date
				Date1 = Date
			else:
				Date0 = Date[0]
				Date1 = Date[1]
			utclim = TT.ContUT(np.array([Date0,Date1]),np.array(ut))
			ax.set_xlim(utclim)
		if ylog is None:
			ylog = self._ylog
		if ylog:
			ax.set_yscale('log')
			ax.set_ylim(self._logflim)
		else:
			ax.set_ylim(self._flim)
			
		#and labels
		ax.set_xlabel(self.xlabel)
		ax.set_ylabel(self.ylabel)
	

			
		#get color scale
		if zlog is None:
			zlog = self._zlog
		if scale is None:
			if zlog:
				scale = self._logscale
			else:
				scale = self._scale
		if zlog:
			norm = colors.LogNorm(vmin=scale[0],vmax=scale[1])
		else:
			norm = colors.Normalize(vmin=scale[0],vmax=scale[1])
			
		#create plots
		for i in range(0,self.n):
			tmp = self._PlotSpectrogram(ax,i,norm,cmap)
			if i == 0:
				sm = tmp

		#sort the UT axis out
		tdate = np.concatenate(self.Date)
		tutc = np.concatenate(self.utc)
		srt = np.argsort(tutc)
		tdate = tdate[srt]
		tutc = tutc[srt]

		#turn axes off when needed
		if noy:
			ax.set_ylabel('')
			ax.yaxis.set_ticks([])
		if nox:
			ax.set_xlabel('')
			ax.xaxis.set_ticks([])
		else:

			if PosAxis:
				udate = np.unique(tdate)

				Pos = ReadFieldTraces([udate[0],udate[-1]])
				
				#get the Lshell, Mlat and Mlon
				good = np.where(np.isfinite(Pos.Lshell) & np.isfinite(Pos.MlatN) & np.isfinite(Pos.MlonN))[0]
				Pos = Pos[good]
				fL = interp1d(Pos.utc,Pos.Lshell,bounds_error=False,fill_value='extrapolate')
				fLon = interp1d(Pos.utc,Pos.MlonN,bounds_error=False,fill_value='extrapolate')
				fLat = interp1d(Pos.utc,Pos.MlatN,bounds_error=False,fill_value='extrapolate')
			
				PosDTPlotLabel(ax,tutc,tdate,fL,fLon,fLat,TickFreq=TickFreq)
				ax.set_xlabel('')
			else:
				TT.DTPlotLabel(ax,tutc,tdate,TickFreq=TickFreq)

		#colorbar
		divider = make_axes_locatable(ax)
		cax = divider.append_axes("right", size="2.5%", pad=0.05)

		cbar = fig.colorbar(sm,cax=cax) 
		cbar.set_label(self.zlabel)		
		return ax

	def _PlotSpectrogram(self,ax,I,norm,cmap):
		'''
		This will plot a single spectrogram (multiple may be stored in
		this object at any one time
		
		'''
		#get the appropriate data
		Date = self.Date[I]
		utc = self.utc[I]
		ut = self.ut[I]
		dt = self.dt[I]
		bw = self.bw[I]
		
		bw = self.bw[I]
		f = self.Freq[I]
		Spec = self.Spec[I]	
		
		#get the frequency band limits
		bad = np.where(np.isnan(f))
		f[bad] = 0.0
		f0 = f - 0.5*bw
		f1 = f + 0.5*bw

		#get the ut array limits
		t0 = utc
		t1 = utc + dt
		
		
		#look for gaps in ut
		if len(f.shape) > 1:
			#isgap = ((utc[1:] - utc[:-1]) > 1.1*dt[:-1]) | ((f[1:,:] - f[:-1,:]) != 0).any(axis=1)
			#minor fudge here
			isgap = ((utc[1:] - utc[:-1]) > 60.0/3600.0) | ((f[1:,:] - f[:-1,:]) != 0).any(axis=1)
			nf = f.shape[1]
		else:
			#isgap = (utc[1:] - utc[:-1]) > 1.1*dt[:-1]
			isgap = (utc[1:] - utc[:-1]) > 60.0/3600.0
			nf = f.size
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
			st = Spec[i0[i]:i1[i]]
			for j in range(0,nf):				
				if len(f.shape) > 1:
					ftmp = np.array([f0[i0[i],j],f1[i0[i],j]])
				else:
					ftmp = np.array([f0[j],f1[j]])
				if np.isfinite(ftmp).all():
					#plot each row of frequency
					tg,fg = np.meshgrid(ttmp,ftmp)
					
					s = np.array([st[:,j]])
					
					sm = ax.pcolormesh(tg,fg,s,cmap=cmap,norm=norm)
			
		return sm
		
	def _CalculateTimeLimits(self):
		'''
		Loop through all of the stored spectra and find the time limits.
		
		'''
		#initialize time limits
		utlim = [np.inf,-np.inf]
		
		#loop through each array
		n = len(self.utc)
		for i in range(0,n):
			mn = np.nanmin(self.utc[i])
			mx = np.nanmax(self.utc[i] + self.dt[i])
			if mn < utlim[0]:
				utlim[0] = mn
			if mx > utlim[1]:
				utlim[1] = mx
		self._utlim = utlim
		
	def _CalculateFrequencyLimits(self):
		'''
		Loop through all of the stored spectra and work out the frequency
		range to plot.
		
		'''
		#initialize frequency limits
		flim = [0.0,-np.inf]
		logflim = [np.inf,-np.inf]
		

		#loop through each array
		n = len(self.Freq)
		for i in range(0,n):
			f0 = self.Freq[i] - self.bw[i]/2.0
			f1 = self.Freq[i] + self.bw[i]/2.0
			mn = np.nanmin(f0)
			mx = np.nanmax(f1)
			if mn < flim[0]:
				flim[0] = mn
			if mx > flim[1]:
				flim[1] = mx
			lf0 = np.log10(f0)
			lf1 = np.log10(f1)
			bad = np.where(self.Freq[i] <= 0.0)
			lf0[bad] = np.nan
			lf1[bad] = np.nan

			lmn = np.nanmin(lf0)
			lmx = np.nanmax(lf1)
			if lmn < logflim[0]:
				logflim[0] = lmn
			if lmx > logflim[1]:
				logflim[1] = lmx

		self._flim = flim
		self._logflim = 10**np.array(logflim)


		
	def _CalculateScale(self):
		'''
		Calculate the default scale limits for the plot.
		
		'''
		scale = [np.inf,-np.inf]
		logscale = [np.inf,-np.inf]
		
		n = len(self.Spec)
		for i in range(0,n):
			ls = np.log10(self.Spec[i])
			bad = np.where(self.Spec[i] <= 0)
			ls[bad] = np.nan
				
			if self._ScaleType == 'std':
				mu = np.nanmean(self.Spec[i])
				std = np.std(self.Spec[i])
				
				lmu = np.nanmean(ls)
				lstd = np.std(ls)
					
				tmpscale = [mu - self._nStd*std, mu + self._nStd*std]
				tmplogscale = 10**np.array([lmu - self._nStd*lstd, lmu + self._nStd*lstd])					
				
			elif self._ScaleType == 'positive':
				#calculate the scale based on all values being positive 
				std = np.sqrt((1.0/np.sum(self.Spec[i].size))*np.nansum((self.Spec[i])**2))
				lstd = np.sqrt(((1.0/np.sum(np.isfinite(ls))))*np.nansum((ls)**2))
					
				tmpscale = [0.0,std*self._nStd]
				tmplogscale = 10**np.array([np.nanmin(ls),lstd*self._nStd])			
			else:
				#absolute range
				tmpscale = [np.nanmin(self.Spec[i]),np.nanmax(self.Spec[i])]
				tmplogscale = 10**np.array([np.nanmin(ls),np.nanmax(ls)])


			if tmpscale[0] < scale[0]:
				scale[0] = tmpscale[0]
			if tmpscale[1] > scale[1]:
				scale[1] = tmpscale[1]
			
			if tmplogscale[0] < logscale[0]:
				logscale[0] = tmplogscale[0]
			if tmplogscale[1] > logscale[1]:
				logscale[1] = tmplogscale[1]
	
		
		self._scale = scale
		self._logscale = logscale
	
	
