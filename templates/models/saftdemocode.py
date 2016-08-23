import simpleA
import matplotlib.pyplot as plt
import json
import mpld3

def saft_plot():
	#Initalization constants
	m = 2.457 #segment length
	sigma = 3.044 #segment diameter
	epsilon = 213.48 #well depth
	num_assocs = 3.0 #number of association sites
	ikappa = 1.0 #interaction strength paramater kappa
	ieps_ass = 1.0 #interaction strength paramater epsilon
	dens_num = 0.001

	#Put these into a single class
	compound = simpleA.Compound(sigma,epsilon,m,num_assocs,ikappa,ieps_ass,9999)



	#Set up demo
	eta = 0.05
	T = 0.2
	guess = [eta,T]

	#Generate Critical Point
	critvals = simpleA.findCrit(guess,dens_num,compound)
	Tc = critvals[1]
	Nc = critvals[0]

	#Generate Spinodal 
	Tvals, spin = simpleA.findSpin(Tc,Nc,dens_num,compound)
	Tvals =Tvals.tolist()
	spin =spin.tolist()

	while len(spin) > 100:
		del spin[::2]
		del Tvals[::2]


	#Set up figure and d3 plot 
	fig = plt.figure()
	fig.set_facecolor('white')
	axis = fig.add_subplot(1, 1, 1,axisbg='#f5f5f5')
	axis.set_xlabel('Eta')
	axis.set_ylabel('Temperature, T')
	axis.set_title('SAFT LLEPhase Diagram')
	#canvas = FigureCanvas(fig)

	#Plot spinodal
	spinline = axis.plot(spin,Tvals,'r',lw=2,label = "Spinodal")

	#Generate Binodal
	Tvals, bin = simpleA.findBinodal(dens_num,Tc,Nc,compound)
	Tvals =Tvals.tolist()
	bin =bin.tolist()

	while len(bin) > 200:
		del bin[::2]
		del Tvals[::2]

	#Plot Binodal
	binline = axis.plot(bin,Tvals,'b',lw=2, label = "Binodal") 

	axis.legend()
	#plugins.connect(fig, plugins.MousePosition())

	id1 = "fig01"
	json01 = json.dumps(mpld3.fig_to_dict(fig))

	#Attempt to make dictionary of plots
	plot_dict= dict()
	plot_dict['id'] = "fig01"
	pdid = "fig01"
	plot_dict['json'] = json01
	pdjson = json01
	
	list_of_plots = list()
	list_of_plots.append(plot_dict)

	#Generate table
	zipped2 = zip(Tvals,spin,bin)
		
	while len(zipped2) > 20:
		del zipped2[::2]

	#Critical point form
	critphi2 = critvals

	return pdid, pdjson, zipped2, critphi2, list_of_plots
