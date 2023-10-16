import numpy as np
from .ReadCDF import ReadCDF
from ..Tools.PSpecCls import PSpecCls
import DateTimeTools as TT
from ..Tools.ListDates import ListDates

def ReadOmni(Date,KeV=True,JoinBins=False):
	'''
	Reads the level 2 omniflux data product for a given date.
	
	Inputs
	======
	Date : int
		Integer date in the format yyyymmdd
		If Date is a single integer - one date is loaded.
		If Date is a 2-element tuple or list, all dates from Date[0] to
		Date[1] are loaded.
		If Date contains > 2 elements, all dates within the list will
		be loaded.
	Kev : bool
		Converts units to be KeV instead of eV
	
	Returns
	=======
	data : dict
		Contains the following fields:
		'eFlux' : PSpecCls object, contains electron fluxes
		
	For more information about the PSpecCls object, see Arase.Tools.PSpecCls 
		

	'''		
	print('The keyword "KeV" will be removed in a future version of Arase.LEPe.ReadOmni')
	#get a list of the dates to load		
	if np.size(Date) == 1:
		dates = np.array([Date])
	elif np.size(Date) == 2:
		dates = ListDates(Date[0],Date[1])
	else:
		dates = np.array([Date]).flatten()
		
	out = {	'eFlux' : None}

	#loop through dates
	for date in dates:	
				
		#read the CDF file
		data,meta = ReadCDF(date,2,'omniflux')		

		if data is None:
			continue
		

		#get the time 
		sEpoch = data['Epoch']
		sDate,sut = TT.CDFEpochtoDate(sEpoch)
		

		
		
		#the energy arrays
		sEnergy = data['FEDO_Energy']
		if KeV:
			sEnergy = sEnergy/1000.0

		#we need to sort the energy bins because they are not in order
		I = np.arange(32).reshape((4,8)).T[:,[0,2,1,3]].flatten()
		sEnergy = sEnergy[:,:,I]
		
		#calculate mid point of energy bins
		emid = 10**np.mean(np.log10(sEnergy),axis=1)
		

		#get spectrum and remove bad data
		s = data['FEDO']
		bad = np.where(s < 0)
		s[bad] = np.nan
		s = s[:,I]		
		
		#set energy to np.nan where it is 0
		bad = np.where(emid <= 0)
		emid[bad] = np.nan
		
		le = np.log10(sEnergy)
		if JoinBins:
			le0 = le[:,0,:]
			le1 = le[:,1,:]
			lemid = np.log10(emid)
			
			#find the unique sets of energy bins
			y = np.ascontiguousarray(emid).view(np.dtype((np.void,emid.dtype.itemsize*emid.shape[1])))
			_,idx = np.unique(y,return_index=True)
			
			for ii in idx:
				#list all of the places with this set of energies
				use = np.where(y == y[ii])[0]
				
				#copy the array
				_le0 = le0[ii]
				_le1 = le1[ii]
				_lemid = lemid[ii]
							
				#get all the finite elements
				fin = np.where(np.isfinite(_le0) & np.isfinite(_le1))[0]
				
				if fin.size > 0:
					#mid point between top of one bin and bottom of next
					mp = 0.5*(_le1[fin[:-1]] + _le0[fin[1:]])
					
					#get the new bin edges
					newle0 = np.copy(_le0)
					newle1 = np.copy(_le1)
					d0 = mp[0] - _lemid[fin[0]]
					d1 = _lemid[fin[-1]] - mp[-1]
					l0 = _lemid[fin[0]] - d0
					l1 = _lemid[fin[-1]] + d1
					newle0[fin] = np.append(l0,mp)
					newle1[fin] = np.append(mp,l1)
				
					le0[use] = newle0
					le1[use] = newle1
					
			ew = 10**(le1 - le0)
			ew[bad] = np.nan	
		else:
			ew = 10**(le[:,1,:] - le[:,0,:])
			ew[bad] = np.nan


		if KeV:
			s = s*1000.0
		
			#plot labels
			ylabel = 'Energy (keV)'
			zlabel = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		else:
			
			#plot labels
			ylabel = 'Energy (eV)'
			zlabel = 'Flux\n((s cm$^{2}$ sr keV)$^{-1}$)'
		

		#now to store the spectra
		if out['eFlux'] is None:
			out['eFlux'] = PSpecCls(SpecType='e',ylabel=ylabel,zlabel=zlabel,ylog=True,zlog=True)
		out['eFlux'].AddData(sDate,sut,sEpoch,emid,s,Meta=meta['FEDO'],ew=ew,Label='LEPe')
			
	

	return out
