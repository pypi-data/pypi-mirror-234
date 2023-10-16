import numpy as np
import matplotlib.pyplot as plt

def PlotLabel(ax,label,color=[0.0,0.0,0.0],fontsize=None,x=0.05,y=0.95,ha='center',va='center'):
	
	ax.text(x,y,label,color=color,ha=ha,va=va,transform=ax.transAxes,fontsize=fontsize)
