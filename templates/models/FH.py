#!/usr/bin/env python
from math import *
import numpy as np
#from general_route_functions import flip
from plotter import *
from flask import request

""" Flory Huggins"""
def fun(x,na,nb,phi1):
	"""These are the functions necessary to solve the binodal:
	F1 is the criteria that the chemical potentials are equal, whereas F2 is the definition of the derivative w.r.t. phi
	F1 = f'(phi_1a) - f'(phi_2a);
	F2 = (b-a) * f'(phi_1a) - [ f(phi_2a) - f(phi_1a) ]
	"""

	#Convert to floats
	na = float(na)
	nb = float(nb)

	#Actual expression of F1, and F2 are housed in this array, this is more for formatting reasons
	return np.array([ 

			log(phi1) - log(x[0]) + x[1]*x[0]*(1-x[0])*na
			- x[1]*phi1*(1-phi1)*na + x[0] - phi1 - x[1]*na*(1-x[0]) + x[1]*na*(1-phi1)
			+ (na/nb)*(1-x[0]) - (na/nb)*(1-phi1),

			(x[0] - phi1)*(1./na - 1./nb + x[1] - 2*x[1]*phi1
			- log(1-phi1)/nb + log(phi1)/na) - ((x[0]/na)*log(x[0])
			+ ((1-x[0])/nb)*log(1-x[0]) + x[1]*x[0]*(1-x[0]))
			+ ((phi1/na)*log(phi1) + ((1-phi1)/nb)*log(1-phi1) + x[1]*(phi1)*(1-phi1))
			])	

def jac(x,na,nb,phi1):
	""" This the expression for the jacobian, given by the following:
	[[df1/dphi2, df1/dchi]
	[df2/dphi2, df2/dchi] ]
	"""
	#Convert to floats
	na = 1.0*na
	nb = 1.0*nb

	return np.array([
			[1 + x[1]*na - na/nb + x[1]*na*(1-x[0]) - 1.0/x[0] - x[1]*na*x[0],
			na*(1-phi1) - na*(1-phi1)*phi1 - na*(1-x[0]) + na*(1-x[0])*(x[0])],
			[log(phi1)/na -log(x[0])/na - log(1-phi1)/nb + log(1-x[0])/nb
			- 2*x[1]*phi1 + 2*x[1]*x[0], (x[0] - phi1)**2]])

def NR(na,nb,crit_chi):
		" Newton Raphson solver for the binary mixture"
		# Set up parameters, initial guesses, formatting, initializing etc.

		#Establish the critical point analytically
		if na != nb:
			crit_phi = (-nb + sqrt(na*nb))/(na-nb)
		else:
			crit_phi = .5  	

		#Set up the array of phi_a in phase 1
		phi1vals = np.arange(.001,crit_phi-.001,.001)
		phi1vals = phi1vals.tolist()

		#Establish initial guess
		guess = [0,0]
		new_guess = [0.5,3]
		iter = 0

		#Generate Arrays
		x1 = np.zeros((len(phi1vals),1)) # Final array to hold phi_a in phase 1
		x2 = np.zeros((len(phi1vals),1)) # Final array to hold phi_a in phase 2
		binodal = np.zeros((len(phi1vals),1)) # Final array to hold chi

		max_iter = 2000
		damp = 0.05 #Damping constant to help the solver 

		#Loop to find the roots using Multivariate Newton-Rhapson
		for phi in phi1vals:
			iter = 0
			while iter < max_iter :
				iter += 1
				index = phi1vals.index(phi)
				guess = new_guess
				jacobian = jac(guess,na,nb,phi) #Evaluate the jacobian
				invjac = np.linalg.inv(jacobian) #Inverse jacobian
				f1 = fun(guess,na,nb,phi) #Calculate the function 
				new_guess = guess - damp*np.dot(invjac,f1) 

				#Tolerance criterion
				if abs(new_guess[0] - guess[0]) < 1e-8 and abs(new_guess[1]-guess[1]) < 1e-8: 
					x1[index] = phi
					x2[index] = new_guess[0]
					binodal[index] = new_guess[1]
					break

		n = np.size(x1) + 1
		x1 = np.reshape(np.append(x1,crit_phi),(n,1))

		x1=x1.tolist()
		x2=x2.tolist()

		#Has to reverse the order of x2, which was converted to a tuple in the previous line
		x2=x2[::-1] 

		#Adds crit chi to the end of binodal
		binodal = np.reshape(np.append(binodal,crit_chi),(n,1))
		binodal= binodal.tolist()
		binodali = binodal[::-1]
		binodali.pop(0)

		#Concatenate the lists together
		phi = x1 + x2
		binodal = binodal + binodali


		phi = np.asarray(phi)
		return phi,binodal

def flory_G(phi,na,nb,chi):
	"""Plots free energy"""
	enthalpy = chi*phi*(1-phi)
	entropy = phi/na * log(phi) + (1.-phi)/nb * log(1-phi) 
	f = phi/na * log(phi) + (1.-phi)/nb * log(1-phi) + chi*phi*(1-phi)
	return enthalpy,entropy,f

def fPlot(polya,polyb,na,nb,v0,jsondata):

	#The chi value from the USER INPUT
	chi = float(request.form['chivalue'])
	chi = chi/v0

	try:
		chi_type = jsondata['0']['type']
	except:
		jsondata = {"status":"user","0":{"doi":"10.1021/ma400597j","type":"Type 0","temperature":"NA","temperature_unit":"C","userchi":"0.41","chierror":"0.02","notes":"User Inputed","indirect":"0","paper_link":"#"}}
		chi_type = jsondata['0']['type']
		jsondata['0']['userchi'] = chi

	#Calculate the critical point
	crit_chi = .5*((1/(na**.5) + 1/(nb**.5))**2)
	if na == nb:
		crit_phi = 0.5
	else:
		crit_phi = (-nb + sqrt(na*nb) )/(na-nb)

	#Calculate the binodal and spinodal
	phi1, binodal =  NR(na,nb,crit_chi)
	spinodal = (.5*(1./(na*phi1) + 1./(nb-nb*phi1)))



	#Convert list to np array
	binodal = np.asarray(binodal)
	spinodal= np.asarray(spinodal)

	#Flip the plot w/ chi to be a function of temperature
	temp_unit = jsondata['0']['temperature_unit']

	if chi_type == "Type 1":
		chi = float(jsondata['0']['chi'])

	
		binodal = (chi/v0)/binodal
		spinodal = (chi/v0)/spinodal
		crit_chi = (chi/v0)/crit_chi

	elif chi_type == "Type 2":
		binodal = float(jsondata['0']['chib']) / ( binodal - float(jsondata['0']['chia']))
		spinodal = float(jsondata['0']['chib']) / (spinodal - float(jsondata['0']['chia']))
		crit_chi= float(jsondata['0']['chib']) / (crit_chi- float(jsondata['0']['chia']))

	###Phase Plot
	#xlabel = 'Volume Fraction, \u03a6'
	philetter = u'\u03a6'
	xlabel = 'Volume Fraction (' + philetter + ')'
	ylabel = 'Temperature, K'
	title = 'Flory-Huggins Phase Diagram'
	FHplot = phasePlot(xlabel,ylabel,title,phi1,spinodal,binodal)


	####Free Energy
	phi = np.arange(0.0001,0.99,0.001)
	h = np.zeros(( len(phi) ))
	s = np.zeros(( len(phi) ))
	g = np.zeros(( len(phi) ))
	i = 0
	for current_phi in phi:
		h[i],s[i],g[i] = flory_G(current_phi,na,nb,chi)
		i += 1

	xlabel = 'Volume Fraction (' + philetter + ')'
	ylabel = "Free Energy"
	title = "Flory-Huggins Free Energy Diagram"
	FEplot = freeEnergyPlot(xlabel,ylabel,title,phi,h,s,g)

	###########################################

	#LIST OF DICTIONARIES
	list_of_plots = list()                                        
	list_of_plots.append(FEplot.plot_dict)
	list_of_plots.append(FHplot.plot_dict)


	#Generate table
	#Prune and preen the data set so its nicer looking
	phi1 = np.round(phi1,2)
	phi1 = phi1.tolist()
	phi1 = [i[0] for i in phi1]
	spinodal = np.round(spinodal,4)
	spinodal = spinodal.tolist()
	spinodal = [i[0] for i in spinodal]
	binodal = np.round(binodal,4)
	binodal = binodal.tolist()
	binodal= [i[0] for i in binodal]
	while len(phi1) > 20:
		del phi1[::2]
		del spinodal[::2]
		del binodal[::2]
	zipped = zip(phi1,spinodal,binodal)

	#Critical point
	critvals = [crit_phi,crit_chi]

	return jsondata,critvals,list_of_plots,zipped

