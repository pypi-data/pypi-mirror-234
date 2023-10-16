import numpy as np
from .PSpecCls import PSpecCls


def CombinePSpecCls(A):
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
	out = PSpecCls(	SpecType=A[0].SpecType,
					xlabel=A[0].xlabel,
					ylabele=A[0].ylabele,
					ylabelv=A[0].ylabelv,
					zlabelp=A[0].zlabelp,
					zlabelf=A[0].zlabelf,
					ylog=A[0]._ylog,
					zlog=A[0]._zlog,
					ScaleType=A[0]._ScaleType,
					nStd=A[0]._nStd)
	
	#loop through and add each one
	for i in range(0,n):
		#we must loop through each elements in each one too
		for j in range(0,A[i].n):
			out.AddData(A[i].Date[j],A[i].ut[j],A[i].Epoch[j],A[i].Energy[j],A[i].Spec[j],ew=A[i].ew[j],dt=A[i].dt[j],Meta=A[i].Meta[j],Label=A[i].Label[j])
	
	return out
