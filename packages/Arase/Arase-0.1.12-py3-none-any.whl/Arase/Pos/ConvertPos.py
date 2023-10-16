import numpy as np
from ._ReadCDF import _ReadCDF
from ._ReadDataIndex import _ReadDataIndex
import os
from .. import Globals
import PyGeopack as gp
from scipy.interpolate import interp1d
import RecarrayTools as RT
import DateTimeTools as TT
import DateTimeTools as TT

def _MagGeo(xm,ym,zm,Date,ut):
	r = np.sqrt(xm**2 + ym**2 + zm**2)
	mlon = np.arctan2(ym,xm)*180.0/np.pi
	mlat = np.arctan2(zm,np.sqrt(ym**2 + xm**2))*180.0/np.pi
	glon,glat = gp.Coords.MAGtoGEOLL(mlon,mlat,Date,ut)
	xg = r*np.cos(mlon)*np.cos(mlat)
	yg = r*np.sin(mlon)*np.cos(mlat)
	zg = r*np.sin(mlat)
	return xg,yg,zg
	

def ConvertPos():
	'''
	Converts the position from the CDF format to a smaller binary format.
	
	
	'''
	#use the index to list all of the dates
	idx = _ReadDataIndex('def')
	dates = idx.Date
	dates.sort()
	nd = dates.size
	
	#the output dtype
	dtype = Globals.PosDtype
	
	#output array (number of days * minutes in a day)
	n = nd*1440
	out = np.recarray(n,dtype=dtype)
	
	#loop through each date
	p = 0
	nbad = 0
	ut = np.arange(1440,dtype='float32')/60.0
	for i in range(0,nd):
		print('\rReading Date {0} of {1} ({2})'.format(i+1,nd,dates[i]),end='')
		#read cdf
		tmp = _ReadCDF(dates[i],'def')
			
		if not tmp is None:
			data,meta = tmp
			
			d,t = TT.CDFEpochtoDate(data['epoch'])
			
						
			#get date and time
			#d = np.int32(data['date_time'][0]) * 10000 + np.int32(data['date_time'][1]) * 100 + np.int32(data['date_time'][2])
			#t = np.float32(data['date_time'][3]) + data['date_time'][4]/60.0 + data['date_time'][5]/3600.0
			
			#make sure all are on the same date
			use = np.where(d == dates[i])[0]
			out.Date[p:p+1440] = dates[i]
			out.ut[p:p+1440] = ut
			
			#convert gse
			f = interp1d(t,data['pos_gse'][:,0])
			out.Xgse[p:p+1440] = f(ut)
			f = interp1d(t,data['pos_gse'][:,1])
			out.Ygse[p:p+1440] = f(ut)
			f = interp1d(t,data['pos_gse'][:,2])
			out.Zgse[p:p+1440] = f(ut)
			#convert gsm
			f = interp1d(t,data['pos_gsm'][:,0])
			out.Xgsm[p:p+1440] = f(ut)
			f = interp1d(t,data['pos_gsm'][:,1])
			out.Ygsm[p:p+1440] = f(ut)
			f = interp1d(t,data['pos_gsm'][:,2])
			out.Zgsm[p:p+1440] = f(ut)
			#convert sm
			f = interp1d(t,data['pos_sm'][:,0])
			out.Xsm[p:p+1440] = f(ut)
			f = interp1d(t,data['pos_sm'][:,1])
			out.Ysm[p:p+1440] = f(ut)
			f = interp1d(t,data['pos_sm'][:,2])
			out.Zsm[p:p+1440] = f(ut)
			
			#use PyGeopack to get the geo and mag coords
			for j in range(0,1440):
				out.Xgm[p+j],out.Ygm[p+j],out.Zgm[p+j] = gp.Coords.GSEtoMAG(out.Xgse[p+j],out.Ygse[p+j],out.Zgse[p+j],dates[i],ut[j])
				#out.Xgeo[p+j],out.Ygeo[p+j],out.Zgeo[p+j] = gp.MAGtoGEOUT(out.Xgm[p+j],out.Ygm[p+j],out.Zgm[p+j],dates[i],ut[j])
				out.Xgeo[p+j],out.Ygeo[p+j],out.Zgeo[p+j] = _MagGeo(out.Xgm[p+j],out.Ygm[p+j],out.Zgm[p+j],dates[i],ut[j])
			p += 1440
		else:
			nbad += 1
	print()
	out.utc = TT.ContUT(out.Date,out.ut)
	out = out[:p]
	#save the output file
	outfile = Globals.DataPath+'Pos/pos.bin'
	RT.SaveRecarray(out,outfile)
