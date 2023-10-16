import numpy as np
import datetime


def GetCurrentDate():
    
	dt = datetime.datetime.today()
	s = dt.strftime('%Y%m%d')
	return np.int32(s)