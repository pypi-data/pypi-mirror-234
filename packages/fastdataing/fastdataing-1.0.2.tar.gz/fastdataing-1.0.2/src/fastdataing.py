"""
Common fast data processing methods
"""
import os
from scipy.interpolate import make_interp_spline
from scipy.signal import savgol_filter
import numpy as np
import matplotlib.pyplot as plt

def smooth_MIS(x,y,factor=300):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factor: smooth factor, like, factor=300
	"""
	x_smooth = np.linspace(x.min(), x.max(), factor)
	y_smooth = make_interp_spline(x, y)(x_smooth)
	return x_smooth,y_smooth


def smooth_SF(x,y,factors=[5,3]):
	"""
	smooth data
	x: x axis data
	y: y axis data
	factors: smooth factors, like, factors=[5,3]
	"""
	y_smooth = savgol_filter(y, factors[0], factors[1], mode= 'nearest')
	x_smooth = x
	return x_smooth,y_smooth


def get_files(directory, suffix):
	"""
	Read files with the same suffix in the folder and save them as a list
	directory: a directory for reading
	suffix: a suffix
	"""
	files = []
	for filename in os.listdir(directory):
		if filename.endswith(suffix):
			files.append(filename)
	return files

def add_fig(figsize=(10,8)):
	"""
	add a canvas, return ax
	"""
	plt.rc('font', family='Times New Roman', size=22)
	fig = plt.figure(figsize=figsize)
	ax = fig.add_subplot(1,1,1)
	return ax

def plot_fig(ax,x,y,label="PotEng",linewidth=1,
	factors=[199,3],color="r",savefig="temp.png",
	xlabel="X axis",ylabel="Y axis",fontweight="bold",
	dpi=300,transparent=True):
	"""
	plot fig
	x,y: x,y
	label: label="PotEng",
	linewidth: linewidth=1,
	factors: factors=[199,3],
	color: color="r",
	savefig: savefig="temp.png",
	xlabel: xlabel="X axis",
	ylabel: ylabel="Y axis",
	fontweight: fontweight="bold",
	dpi: dpi=300,
	transparent: transparent=True)
	"""
	ax.plot(x,y,color=color,linewidth=linewidth,alpha=0.2)	
	x,y = smooth_SF(x,y,factors=factors)
	ax.plot(x,y,color=color,label=label,linewidth=linewidth)
	
	ax.set_xlabel(xlabel,fontweight=fontweight,fontsize=26)
	ax.set_ylabel(ylabel,fontweight=fontweight,fontsize=26)

	ax.patch.set_alpha(0) 
	ax.legend(loc="best",ncols=1).get_frame().set_alpha(0)
	if savefig and savefig != "temp.png":
		plt.savefig(savefig,dpi=dpi,transparent=transparent)
	else:
		pass
	return ax