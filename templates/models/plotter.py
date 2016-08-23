import matplotlib.pyplot as plt
import json
import mpld3
from mpld3 import plugins

class generalPlot:
	""" Class to construct Phase Diagrams """
	def __init__(self,xlabel,ylabel,title):
		"Initialize the Plot object"
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.title = title
		self.fig, self.axis = self.constructPlot()

	def constructPlot(self):
		fig = plt.figure()
		fig.set_facecolor('white')
		axis = fig.add_subplot(1, 1, 1,axisbg='#f5f5f5')
		axis.set_xlabel(self.xlabel)
		axis.set_ylabel(self.ylabel)
		axis.set_title(self.title)
		plugins.connect(fig, plugins.MousePosition())
		return fig,axis

class freeEnergyPlot(generalPlot):
	def __init__(self,xlabel,ylabel,title,phi,h,s,g):
		generalPlot.__init__(self,xlabel,ylabel,title)
		self.phi = phi
		self.h = h
		self.s = s
		self.g = g

		hline = self.axis.plot(self.phi,self.h,'r',lw=1,alpha= 0.5,label = "Enthalpy")
		sline = self.axis.plot(self.phi,self.s,'b',lw=1,alpha= 0.5,label = "Entropy")
		gline = self.axis.plot(self.phi,self.g,'g',lw=1,label = "Free Energy")
		self.axis.legend()
		self.keyval = "fig01"
		self.jsonval = json.dumps(mpld3.fig_to_dict(self.fig))
		self.plot_dict = dict()
		self.plot_dict['id'] = self.keyval
		self.plot_dict['json'] = self.jsonval

class phasePlot(generalPlot):
	def __init__(self,xlabel,ylabel,title,phi,spinodal,binodal):
		generalPlot.__init__(self,xlabel,ylabel,title)
		self.phi = phi
		self.spinodal = spinodal
		self.binodal = binodal

		spinline = self.axis.plot(self.phi,self.spinodal,'r',lw=2,label = "Spinodal")
		binline = self.axis.plot(self.phi,self.binodal,'b',lw=2, label = "Binodal") 
		self.axis.legend()
		self.plot_dict = dict()
		self.keyval = "fig02"
		self.jsonval = json.dumps(mpld3.fig_to_dict(self.fig))
		self.plot_dict = dict()
		self.plot_dict['id'] = self.keyval
		self.plot_dict['json'] = self.jsonval

