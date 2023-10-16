import numpy as np
from .SpecCls import SpecCls


def CombineSpecCls(A):
	'''
	Combine an array/list/tuple of SpecCls objects into a single one.
	This assumes that all axis labels and stuff are identical.
	
	Input
	=====
	A : array/list/tuple
		Each element should be a SpecCls object
		
	Returns
	=======
	SpecCls
	
	'''
	
	#count them
	n = np.size(A)
	
	#create the initial object
	out = SpecCls(xlabel=A[0].xlabel,ylabel=A[0].ylabel,zlabel=A[0].zlabel,ylog=A[0]._ylog,zlog=A[0]._zlog,ScaleType=A[0]._ScaleType,nStd=A[0]._nStd)
	
	#loop through and add each one
	for i in range(0,n):
		#we must loop through each elements in each one too
		for j in range(0,A[i].n):
			out.AddData(A[i].Date[j],A[i].ut[j],A[i].Epoch[j],A[i].Freq[j],A[i].Spec[j],bw=A[i].bw[j],dt=A[i].dt[j],Meta=A[i].Meta[j],Label=A[i].Label[j])
	
	return out
