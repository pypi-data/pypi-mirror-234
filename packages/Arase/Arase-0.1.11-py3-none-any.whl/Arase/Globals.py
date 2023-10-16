import os

#try and find the ARASE_PATH variable - this is where data will be stored
ModulePath = os.path.dirname(__file__)+'/'
try:
	DataPath = os.getenv('ARASE_PATH')+'/'
except:
	print('Please set ARASE_PATH environment variable')
	DataPath = ''


#data type for the position
PosDtype = [('Date','int32'),('ut','float32'),('utc','float64'),
		('Xgeo','float32'),('Ygeo','float32'),('Zgeo','float32'),
		('Xgm','float32'),('Ygm','float32'),('Zgm','float32'),
		('Xgse','float32'),('Ygse','float32'),('Zgse','float32'),
		('Xgsm','float32'),('Ygsm','float32'),('Zgsm','float32'),
		('Xsm','float32'),('Ysm','float32'),('Zsm','float32')]
Pos = None

