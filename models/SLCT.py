#!/usr/bin/env python

from math import *
from flask import request
import numpy as np
from scipy.optimize import fsolve
from plotter import *


""" Simple Lattice Cluster """


def SLCTfree(r1,r2,z,p1,p2,na,nb,chidb):
		"""This is a function that generates the enthalpy,
		entropy, and free energy curve and returns them"""

		#Incorporating chidb value
		#0. Process the chidb data
		chidb =float(chidb)

		#Initialize
		z = 6.0 #Coordination number
		phivals = np.arange(0.0001,1.0,0.001)
		enthalpy = np.zeros(( len(phivals) ))
		entropy = np.zeros(( len(phivals) ))
		f = np.zeros(( len(phivals) ))
		i=0
		for phi in phivals:
			#1. Convert chidb to epsilon (depends on phi)
			a = (r1-r2)**2 / z**2
			b = (z-2)/2.0 - (1.0/z)*(p1*(1-phi) + p2*phi)
			c = 3.0*(p1-p2)/(1.0*z)
			eps = (chidb - a)/ ( b + c*phi)
			#2. Generate the last term in the free energy function (not the same as 1)
			chiterm = (r1-r2)**2 / z**2 + eps*( (z-2)/2.0 - (1.0/z)*(p1*(1-phi) + p2*phi))
			#3. Calculate free energy
			enthalpy[i] = phi*(1-phi)*chiterm
			entropy[i] = (phi/na)*np.log(phi) + ((1-phi)/nb)*np.log(1-phi) 
			f[i] = entropy[i] + enthalpy[i]
			i += 1

		return phivals, enthalpy, entropy, f


def SLCT_crit(r1,r2,z,p1,p2,na,nb,chidb):
		"""This is a function that calculates the critical point"""
		#Use numpy root to calculate phi_c
		a = (r1 - r2)**2 / z**2
		b =((z-2)/2 + (1/z)*(-2*p1 + p2)) #Technically this is b/(eps/kt) which is factored out
		c = (3/z)*(p1 - p2) #Technically c/(eps/kt) 
		m = na
		k = nb*1.0/na
		coeff = [2*a*c, 2*c*(k-1)/(m*k), (b*(k-1) - c*(4*k - 1))/(m*k) - 2*a*c , 2*(c - b)/m , b/m]


		phi_c_temp =  np.roots(coeff)


		#Make sure that you pick the root that is real, positive and bounded by 0 and 1
		for critval in phi_c_temp:
			if critval > 0 and critval < 1 and critval.imag == 0:
				phi_c = critval.real

	
		#Convert chidb to epsilon
		chidb = float(chidb)
		a = (r1-r2)**2 / z**2
		b = (z-2)/2.0 - (1.0/z)*(p1*(1-phi_c) + p2*phi_c)
		c = 3.0*(p1-p2)/(1.0*z)
		eps = (chidb - a)/ ( b + c*phi_c)

		#Calculate the critical temperature
		Tc = 2*(b + c*phi_c)/(1.0/(m*phi_c) + 1.0/(m*k*(1-phi_c)) - 2*a)
		Tc = Tc*eps #eps/kb was taken out of b and c, so putting it back in now
		print "CRIT PHI CRIT CHI"
		print phi_c, Tc
		return phi_c, Tc


def SLCT_Spinodal(r1,r2,z,p1,p2,na,nb,flipper):
		"""This is a function that calculates the Spinodal curve, this is not numerical"""
		phi = np.arange(0.01,.99,0.001)
		a = (r1 - r2)**2 / z**2
		b =((z-2)/2 + (1.0/z)*(-2*p1 + p2)) #Technically this is b/(eps/kt) which is factored out
		c = (3.0/z)*(p1 - p2) #Technically c / (eps/kt) 
		f = (.5*(1./(na*phi) + 1./(nb-nb*phi)))
		spin1 = (f - a) / (b + c*phi)

		#Currently returns the function

		if flipper == 1:
				phi = 1 - phi

		return phi,spin1


def SLCT_fun(x,phi1,r1,r2,z,p1,p2,na,nb):
		"""This is a function that gives the 2 functions which need to simultaneously be solved for np.roots,
		This is called in the numerical solver, returns an np.array of the 2 functions evaluated, [f1,f2]"""
		a = (r1 - r2)**2 / z**2

		#Convert to float
		m1 = na*1.0
		m2 = nb*1.0
		
		return np.array([
				a*m1*(1-phi1) - m1*(1-phi1)/m2 - phi1 - a*m1*(1-phi1)*phi1 - a*m1*(1-x[0]) 
				+ m1*(1-x[0])/m2 + x[0] + a*m1*(1-x[0])*x[0] - m1*(1-phi1)*x[1]
				+ m1*(1-phi1)*phi1*x[1] + m1*(1-x[0])*x[1] - m1*(1-x[0])*x[0]*x[1]
				+ phi1*(1-phi1)*(1-phi1)*m1*p1*x[1]/z - x[0]*(1-x[0])*(1-x[0])*m1*p1*x[1]/z
				- m1*(1-phi1)*(1-phi1)*p1*x[1]/z + m1*(1-phi1)*(1-phi1)*phi1*p1*x[1]/z 
				+ phi1*phi1*(1-phi1)*m1*p2*x[1]/z - x[0]*x[0]*(1-x[0])*m1*p2*x[1]/z
				- 2*m1*(1-phi1)*phi1*p2*x[1]/z + m1*(1-phi1)*phi1*phi1*p2*x[1]/z + m1*p1*(1-x[0])*(1-x[0])*x[1]/z  
				+ 2*m1*p2*(1-x[0])*x[0]*x[1]/z - m1*p1*(1-x[0])*(1-x[0])*x[0]*x[1]/z 
				- m1*p2*(1-x[0])*x[0]*x[0]*x[1]/z + 0.5*m1*(1-phi1)*x[1]*z - 0.5*m1*(1-phi1)*phi1*x[1]*z
				- 0.5*m1*(1-x[0])*x[1]*z + 0.5*m1*(1-x[0])*x[0]*x[1]*z + log(phi1) - log(x[0]),

				- phi1/m1 + phi1/m2 + a*phi1*phi1 + x[0]/m1 - x[0]/m2 - 2*a*phi1*x[0] + a*x[0]*x[0] 
				- phi1*phi1*x[1] + 2*phi1*x[0]*x[1] - x[0]*x[0]*x[1] - 2*phi1*phi1*p1*x[1]/z
				+ 2*phi1*phi1*phi1*p1*x[1]/z + phi1*phi1*p2*x[1]/z - 2*phi1*phi1*phi1*p2*x[1]/z 
				+ 4*phi1*p1*x[0]*x[1]/z - 3*phi1*phi1*p1*x[0]*x[1]/z - 2*phi1*p2*x[0]*x[1]/z
				+ 3*phi1*phi1*p2*x[0]*x[1]/z -2*p1*x[0]*x[0]*x[1]/z + p2*x[0]*x[0]*x[1]/z 
				+ p1*x[0]*x[0]*x[0]*x[1]/z - p2*x[0]*x[0]*x[0]*x[1]/z 
				+ 0.5*phi1*phi1*x[1]*z - phi1*x[0]*x[1]*z + 0.5*x[0]*x[0]*x[1]*z 
				+ log(1-phi1)/m2 - x[0]*log(1-phi1)/m2 + x[0]*log(phi1)/m1 
				- log(1-x[0])/m2 + x[0]*log(1-x[0])/m2 -x[0]*log(x[0])/m1
				]) 


def SLCT_jac(x,phi1,r1,r2,z,p1,p2,na,nb):
	a = (r1 - r2)**2 / z**2
	m1 = na*1.0
	m2 = nb*1.0
	
	return np.array([[
			1 + a*m1 - m1/m2 + a*m1*(1-x[0]) - 1.0/x[0] - a*m1*x[0] - m1*x[1] - m1*(1-x[0])*x[1] + m1*x[0]*x[1] 
			- 2*m1*p1*(1-x[0])*x[1]/z + 2*m1*p2*(1-x[0])*x[1]/z - 2*m1*p1*(1-x[0])*(1-x[0])*x[1]/z 
			- 2*m1*p2*x[0]*x[1]/z + 4*m1*p1*(1-x[0])*x[0]*x[1]/z - 4*m1*p2*(1-x[0])*x[0]*x[1]/z 
			+ 2*m1*p2*x[0]*x[0]*x[1]/z + m1*x[1]*z/2 + 0.5*m1*(1-x[0])*x[1]*z - 0.5*m1*x[0]*x[1]*z,

			2*m1*phi1 - m1*phi1*phi1 - 2*m1*x[0] + m1*x[0]*x[0] + 4*m1*phi1*p1/z - 5*m1*phi1*phi1*p1/z 
			+ 2*m1*phi1*phi1*phi1*p1/z - 2*m1*phi1*p2/z + 4*m1*phi1*phi1*p2/z - 2*m1*phi1*phi1*phi1*p2/z
			- 4*m1*p1*x[0]/z + 2*m1*p2*x[0]/z + 5*m1*p1*x[0]*x[0]/z - 4*m1*p2*x[0]*x[0]/z - 2*m1*p1*x[0]*x[0]*x[0]/z 
			+ 2*m1*p2*x[0]*x[0]*x[0]/z - m1*phi1*z + 0.5*m1*phi1*phi1*z + m1*x[0]*z - 0.5*m1*x[0]*x[0]*z],
			[ 

			- 1.0/m2 - 2*a*phi1 + 1.0/(m2*(1-x[0])) + 2*a*x[0] - x[0]/(m2*(1-x[0])) 
			+ 2*phi1*x[1] - 2*x[0]*x[1] + 4*phi1*p1*x[1]/z
			- 3*phi1*phi1*p1*x[1]/z - 2*phi1*p2*x[1]/z + 3*phi1*phi1*p2*x[1]/z 
			- 4*p1*x[0]*x[1]/z + 2*p2*x[0]*x[1]/z + 3*p1*x[0]*x[0]*x[1]/z
			- 3*p2*x[0]*x[0]*x[1]/z - phi1*x[1]*z + x[0]*x[1]*z - log(1-phi1)/m2 
			+ log(phi1)/m2 + log(1-x[0])/m2 - log(x[0])/m1,

			-phi1*phi1 + 2*phi1*x[0] - x[0]*x[0] - 2*phi1*phi1*p1/z 
			+ 2*phi1*phi1*phi1*p1/z + phi1*phi1*p2/z - 2*phi1*phi1*phi1*p2/z
			+ 4*phi1*p1*x[0]/z - 3*phi1*phi1*p1*x[0]/z - 2*phi1*p2*x[0]/z 
			+ 3*phi1*phi1*p2*x[0]/z - 2*p1*x[0]*x[0]/z + p2*x[0]*x[0]/z
			+ p1*x[0]*x[0]*x[0]/z - p2*x[0]*x[0]*x[0]/z + phi1*phi1*z/2 
			- phi1*x[0]*z + x[0]*x[0]*z/2


			]])


def SLCT_semiflex_params(T_semi,flex):
	z = 6.0 #2d system coordination number

	#Pull out semiflexibility data
	a0 = flex[0]
	a1 = flex[1]
	gamma111 = flex[2]
	gamma21 = flex[3]
	gamma3  = flex[4]
	Eb = flex[5]

	g =  z / (z - 1 + np.exp(Eb/T_semi))
	r = a0 + a1*g
	p = gamma111 + gamma21*(g) + gamma3*(g**2)
	return r,p

def SLCT_NR(r1,r2,z,p1,p2,na,nb,flipper,eps,flex1,flex2,chidb):
		" Newton Raphson solver for the binary mixture"
		# Set up parameters, initial guesses, formatting, initializing etc.


		#Generates the critical point,
		#this provides the vertex of the plot, also provides a good guess
		phi_c, Tc = SLCT_crit(r1,r2,z,p1,p2,na,nb,chidb) #Critical Point

		print "Critical Phi along with Critical Temperature"
		print phi_c, Tc
	
		phi1vals = np.arange(.01,phi_c,.009)#Set up values from 0.01 to the critical phi(abscissa)
		phi1vals = phi1vals.tolist() #Convert to a list

		#Initialize boring stuff
		guess = [0,0]
		new_guess = [0.88,2] #Guess parameters are as follows: [Phi_a in phase 2 (phia'') , epsilon/kbT]
		iter = 0
		length = len(phi1vals)
		y2 = np.zeros((length,1))
		x2 = np.zeros((length,1))
		x1 = np.zeros((length,1))

		max_iter = 5000 #Max number of iterations
		#Loop to find the np.roots using Multivariate Newton-Rhapson
		for phi in phi1vals:
			iter = 0
			damp = 0.5

			"""
			#Convert chidb to epsilon
			chidb = float(chidb)
			a = (r1-r2)**2 / z**2
			b = (z-2)/2.0 - (1.0/z)*(p1*(1-phi) + p2*phi)
			c = 3.0*(p1-p2)/(1.0*z)
			eps = (chidb - a)/ ( b + c*phi)
			print phi, eps
			"""
			
			while iter < max_iter :

				iter += 1
				index = phi1vals.index(phi)
				guess = new_guess
				T_semi = eps/new_guess[1] #have to evaluate temp
				r1,p1 = SLCT_semiflex_params(T_semi,flex1)
				r2,p2 = SLCT_semiflex_params(T_semi,flex2)
				#Calculate analytical jacobian, and inverse
				jacobian = SLCT_jac(guess,phi,r1,r2,z,p1,p2,na,nb)
				invjac = np.linalg.inv(jacobian)

				#Set of functions f1[0],f1[1] to satisfy
				f1 = SLCT_fun(guess,phi,r1,r2,z,p1,p2,na,nb)
				new_guess = guess - damp*np.dot(invjac,f1)
				if abs(new_guess[0] - guess[0]) < 1e-6 and abs(new_guess[1]-guess[1]) < 1e-6: 
					x1[index] = phi
					x2[index] = new_guess[0]
					y2[index] = new_guess[1]
					break
		#Convert Numpy np.arrays (x1,x2,y2) to a list
		if flipper ==1:
			x1 = 1 - x1
			x2 = 1 - x2


		n = np.size(x1) + 1
#		x1 = np.reshape(np.append(x1,phi_c),(n,1))
		#This is mostly to make the plot, plottable, I'd leave this be
		x1=x1.tolist()

		x2=x2.tolist()
		x2 = x2[::-1] #Has to reverse the order of x2, which was converted to a tuple in the previous line

#		Tc = eps/Tc #Rest of data currently in form of eps/kT, plot for temperature post-processed in flory.py, so this one is done now.

		#Add critical Temperature
#		y2 = np.reshape(np.append(y2,Tc),(n,1))
		y2=y2.tolist()
		y2i = y2[::-1]
#		y2i.pop(0)


		phi = x1 + x2
		y2 = y2 + y2i

		return (phi,y2)


def run_SLCT_flexspinodal(r1,r2,z,p1,p2,na,nb,flex1,flex2,eps,flipper,phiarray,chidb):
	phivals = phiarray
	i=0
	tempforphi = np.zeros(( len(phivals) ))

	for phi in phivals:
		#Convert chidb to epsilon
		chidb = float(chidb)
		a = (r1-r2)**2 / z**2
		b = (z-2)/2.0 - (1.0/z)*(p1*(1-phi[0]) + p2*phi[0])
		c = 3.0*(p1-p2)/(1.0*z)
		eps = (chidb - a)/ ( b + c*phi[0])

		if eps > 0:
			x0 = 350.0
		else:
			x0 = -385.0
		tempforphi[i] = fsolve(SLCT_flexspin,x0,args=(na,nb,flex1,flex2,eps,phi[0]) ,factor=0.001)
		i = i+1

	if flipper == 1:
		phivals = 1 - phivals

	return phivals, tempforphi

def SLCT_flexspin(T,na,nb,flex1,flex2,eps,phi):
	"""Auxillary function, which is called by solve, finds the value of the Spinodal at a fixed phi"""
	phi = np.asarray(phi)

	z = 6.0

	
	#Parameters for A
	a0_a = flex1[0]
	a1_a = flex1[1]
	g111_a = flex1[2]
	g21_a = flex1[3]
	g3_a = flex1[4]
	Eb_a = flex1[5]

	#Parameters for B
	a0_b = flex2[0]
	a1_b = flex2[1]
	g111_b = flex2[2]
	g21_b = flex2[3]
	g3_b = flex2[4]
	Eb_b = flex2[5]


	#Dependent on T
	#A terms
	g_a = z /  (z - 1 + exp( Eb_a/T ) )
	r1 = a0_a + a1_a*g_a
	p1 = g111_a + g21_a*g_a + g3_a*(g_a**2)

	#B terms
	g_b = z /  (z - 1 + exp(Eb_b/T))
	r2 = a0_b + a1_b*g_b
	p2 = g111_b + g21_b*g_b + g3_b*g_b**2
	
	a = (r1 - r2)**2 / z**2
	b =((z-2)/2 + (1.0/z)*(-2*p1 + p2)) #Technically this is b/(eps/kt) which is factored out
	c = (3.0/z)*(p1 - p2) #Technically c / (eps/kt) 
	f = (.5*(1./(na*phi) + 1./(nb-nb*phi)))

	#Calculate the residual
	rhs = (f - a) / (b+c*phi)
	res = eps/T - (f - a) / (b + c*phi)
	return res


def SLCT_semiflex(poly,k,m,Eb_a):
		z = 6.0

		#Need to fix this temp thing
		T = 300

		g_a =  z / ( z - 1 + np.exp(Eb_a/T) )

		if poly == "PA":
			#PE
			gamma111 = 0.0
			gamma21 = 0.0
			gamma3 = 1.0
			alpha0 = 0.0
			alpha1 = 1.0

		elif poly == "PB":
			gamma111 = 0.0 
			gamma21 = 2./3.
			gamma3 = 2./3.
			alpha0 = 2./3.
			alpha1 = 2./3.

		elif poly == "PC":
			gamma111 = 0	
			gamma21 = 0.4
			gamma3 = 0.8
			alpha0 = 0.4	
			alpha1 = 0.8

		elif poly == "PD":
			gamma111 = 1./6.
			gamma21 = 4./6.
			gamma3 = 4./6.
			alpha0 = 4./6.
			alpha1 = 4./6.
			 
		elif poly == "PE":
			#PIB
			gamma111 = 0
			gamma21 = 1.0
			gamma3 = 0.5
			alpha0 = 1.0
			alpha1 = 0.75
			
		elif poly == "PF":
			#uses k
			gamma111 = 0.0
			gamma21 = 4.0/(2.0+k)
			gamma3 = k/(2.0+k)
			alpha0 =  2.0/(2+k) 
			alpha1 = (k+1)/(2+k) 

		elif poly == "PG":
			#uses k
			gamma111 = 0.0
			gamma21 = 4.0/(4.0+k)
			gamma3 = (2.0+k)/(4.0+k)
			alpha0 = 2.0/(4.0+k)
			alpha1 = 1.0 - 1.0/(4+k)

		elif poly == "PH":
			#uses k
			gamma111 = 0.0
			gamma21 = 4.0/(3.0+k)
			gamma3 = (1.0+k)/(3.0+k)
			alpha0 = 2.0/(3.0+k)
			alpha1 = 1.0 - 1.0/(3+k)

		elif poly == "PI":
			#uses k
			gamma111 = 0.0
			gamma21 = 6.0/(3.0+k)
			gamma3 = (1.0+k)/(3.0+k)
			alpha0 = 4.0/(3+k)
			alpha1 = (k+2)/(3+k)

		elif poly == "PJ":
			#uses k and m
			gamma111 = 0.0
			gamma21 = 8.0/(2 + m + k)
			gamma3 = (m+k)/((1.0)*(2+m+k))
			alpha0 = 4.0/(2+m+k)
			alpha1 = (1+m+k)/(2+m+k)

		elif poly == "PK":
			gamma111 = 0.4
			gamma21 = 0.8
			gamma3 = 0.4
			alpha0 = 0.8
			alpha1 = 0.6

		elif poly == "PL":
			gamma111 = 4.0/6.0
			gamma21 = 4.0/6.0
			gamma3 = 2.0/6.0
			alpha0 = 1.0
			alpha1 = 0.667

		elif poly == "PM":
			gamma111 = 2./6.
			gamma21 = 5./6.
			gamma3 = 3./6.
			alpha0 =2./3.
			alpha1 =2./3.

		elif poly == "PN":
			gamma111 = 3./7.
			gamma21 = 6./7.
			gamma3 = 3./7.
			alpha0 = 6./7.
			alpha1 = 4./7.

		elif poly == "PO":
			gamma111 = 2./7.
			gamma21 = 8./7.
			gamma3 = 4./7.
			alpha0 = 6./7.
			alpha1 = 5./7.

		elif poly == "PP":
			gamma111 = 4./8
			gamma21 = 5./8.
			gamma3 = 3./8.
			alpha0 = 0.75
			alpha1 = 0.625

		elif poly == "PQ":
			gamma111 = 8./9.
			gamma21 = 8./9.
			gamma3 = 3./9.
			alpha0 = 10./9.
			alpha1 = 2./9.

		elif poly == "PR":
			gamma111 = 4./9.
			gamma21 = 8./9.
			gamma3 = 4./9.
			alpha0 = 8./9.
			alpha1 = 5./9.
			 
		elif poly == "PS":
			gamma111 = .375
			gamma21 = .875
			gamma3 = 0.5
			alpha0 = .75
			alpha1 = .625

		elif poly == "PT":
			gamma111 = 1.0
			gamma21 = .75
			gamma3 = .25
			alpha0 = 1.0
			alpha1 = 0.625

		elif poly == "PU":
			gamma111 = 4./7.
			gamma21 = 6./7.
			gamma3 = 3./7.
			alpha0 = 6./7.
			alpha1 = 5./7.

		#Evaluate semiflexibility constants
		p_a = gamma111 + gamma21*g_a + gamma3*g_a**2
		r_a = alpha0 + alpha1*g_a
		flexlist = [alpha0,alpha1,gamma111,gamma21,gamma3]

		return r_a, p_a, flexlist
		

def SLCT_constants(polya,polyb,k1,k2,m1,m2):
		if polya == "PA":
				r1 = 1.0
				p1 = 1.0
		if polya == "PB":
				r1 = 1.333
				p1 = 1.333
		if polya == "PC":
				r1 = 6./5.
				p1 = 6./5.
		if polya == "PD":
				r1 = 4./3.
				p1 = 9./6.
		if polya == "PE":
				r1 = 7./4.
				p1 = 6./4.
		if polya == "PF":
				r1 = (3.+k1)/(2.+k1)
				p1 = (4.+k1)/(2.+k1)
		if polya == "PG":
				r1 = (5.+k1)/(4.+k1)
				p1 = (6.+k1)/(4.+k1)
		if polya == "PH":
				r1 = (4.+k1)/(3.+k1)
				p1 = (5.+k1)/(3.+k1)
		if polya == "PI":
				r1 = (6.+k1)/(3.+k1)
				p1 = (7.+k1)/(3.+k1)
		if polya == "PJ":
				r1 = (5.+k1+m1)/(2.+k1+m1)
				p1 = (8.+k1+m1)/(2.+k1+m1)
		if polya == "PK":
				r1 = 7./5.
				p1 = 8./5.
		if polya == "PL":
				r1 = 5./3.
				p1 = 5./3.
		if polya == "PM":
				r1 = 16./9.
				p1 = 19./9.
		if polya == "PN":
				r1 = 4./3.
				p1 = 5./3.
		if polya == "PO":
				r1 = 10./7.
				p1 = 12./7.
		if polya == "PP":
				r1 = 9./7.
				p1 = 14./7.
		if polya == "PQ":
				r1 = 11./7.
				p1 = 14./7.
		if polya == "PR":
				r1 = 11./7.
				p1 = 13./7.
		if polya == "PS":
				r1 = 13./8.
				p1 = 16./9.
		if polya == "PT":
				r1 = 11./8.
				p1 = 14./8.
		if polya == "PU":
				r1 = 13./9.
				p1 = 16./9.

		if polyb == "PA":
				r2 = 1.0
				p2 = 1.0
		if polyb == "PB":
				r2 = 1.333
				p2 = 1.333
		if polyb == "PC":
				r2 = 6./5.
				p2 = 6./5.
		if polyb == "PD":
				r2 = 4./3.
				p2 = 9./6.
		if polyb == "PE":
				r2 = 7./4.
				p2 = 6./4.
		if polyb == "PF":
				r2 = (3.+k2)/(2.+k2)
				p2 = (4.+k2)/(2.+k2)
		if polyb == "PG":
				r2 = (5.+k2)/(4.+k2)
				p2 = (6.+k2)/(4.+k2)
		if polyb == "PH":
				r2 = (4.+k2)/(3.+k2)
				p2 = (5.+k2)/(3.+k2)
		if polyb == "PI":
				r2 = (6.+k2)/(3.+k2)
				p2 = (7.+k2)/(3.+k2)
		if polyb == "PJ":
				r2 = (5.+k2+m2)/(2.+k2+m2)
				p2 = (8.+k2+m2)/(2.+k2+m2)
		if polyb == "PK":
				r2 = 7./5.
				p2 = 8./5.
		if polyb == "PL":
				r2 = 5./3.
				p2 = 5./3.
		if polyb == "PM":
				r2 = 16./9.
				p2 = 19./9.
		if polyb == "PN":
				r2 = 4./3.
				p2 = 5./3.
		if polyb == "PO":
				r2 = 10./7.
				p2 = 12./7.
		if polyb == "PP":
				r2 = 9./7.
				p2 = 14./7.
		if polyb == "PQ":
				r2 = 11./7.
				p2 = 14./7.
		if polyb == "PR":
				r2 = 11./7.
				p2 = 13./7.
		if polyb == "PS":
				r2 = 13./8.
				p2 = 16./9.
		if polyb == "PT":
				r2 = 11./8.
				p2 = 14./8.
		if polyb == "PU":
				r2 = 13./9.
				p2 = 16./9.
		if polyb == "PS":
				r2 = 13.0/8.0
				p2 = 16.0/9.0

		return r1,p1,r2,p2

def sPlot(polya,polyb,na,nb,jsondata):

	try:
		chidb= jsondata['0']['userchi']
		chitemp = jsondata['0']['temperature']
		chi_tempunit = jsondata['0']['temperature_unit']

	except:
		jsondata = {"status":"user","0":{"doi":"10.1021/ma400597j","type":"Type 0","temperature":"NA","temperature_unit":"C","userchi":"0.41","chierror":"0.02","notes":"User Inputed","indirect":"0","paper_link":"#"}}
		chidb= jsondata['0']['userchi']
		chitemp = jsondata['0']['temperature']
		chi_tempunit = jsondata['0']['temperature_unit']
	


	
	if request.form['eba'] == "":
		eba = 0
		ebb = 0
	else:
		eba = float(request.form['eba'])
		ebb = float(request.form['ebb'])

	#Deal with k and m values for now
	if  polya =='PF' or polya == 'PG' or polya == 'PH' or polya == 'PI' or polya == 'PJ':
		k1 = float(request.form['k1'])
		m1 = float(request.form['m1'])
	else:
		k1 = 0
		m1 = 0

	if  polyb =='PF' or polyb == 'PG' or polyb == 'PH' or polyb == 'PI' or polyb == 'PJ':
		k2 = float(request.form['k2'])
		m2 = float(request.form['m2'])
	else:
		k2 = 0
		m2 = 0

	z = 6.0
	
	""" Parameters for specific polymers"""
	r1, p1,flex1 = SLCT_semiflex(polya,k1,m1,eba)
	r2, p2,flex2 =SLCT_semiflex(polyb,k2,m2,ebb)
	flex1.append(eba)
	flex2.append(ebb)

	global flipper

	"""Nice trick to fix asymmetry issue"""
	if na > nb:
			print "we gotta flip!"
			flipper = 1
			na, nb, r1, r2, p1, p2 =  flip(na,nb,r1,r2,p1,p2)
			print r1, r2, z, p1, p2, na, nb
	else:
			flipper = 0

	#flipper is being weird, going to phase out probably, set to 0 for now
	flipper = 0

	if request.form['slctbutton'] == 'Generate Profile!':
		eps = float(request.form['eps'])

		#Free Energy
		z = 6.0
		r1, p1, r2, p2 = SLCT_constants(polya,polyb,k1,k2,m1,m2)
		xlabel = 'Volume Fraction, \u03a6'
		ylabel = 'Free Energy'
		title = 'SLCT Free Energy Diagram'
		phi,h,s,g = SLCTfree(r1,r2,z,p1,p2,na,nb,chidb)
		FEplot = freeEnergyPlot(xlabel,ylabel,title,phi,h,s,g)



		print flex1, flex2
		#spinx,spinodal = SLCT_Spinodal(r1,r2,z,p1,p2,na,nb,flipper)
		phi, binodal = SLCT_NR(r1,r2,z,p1,p2,na,nb,flipper,eps,flex1,flex2,chidb)
		spinx,spinodal = run_SLCT_flexspinodal(r1,r2,z,p1,p2,na,nb,flex1,flex2,eps,flipper,phi,chidb)

		#Convert list to np array
		binodal = np.asarray(binodal)
		spinodal= np.asarray(spinodal)
		#Evaluate w/ epsilon
		binodal = eps/binodal
		if flipper == 1:
			print "we gotta unflip!"
			na, nb, r1, r2, p1, p2 =  flip(na,nb,r1,r2,p1,p2)
			print r1, r2, z, p1, p2, na, nb

		#Phase Plot
		xlabel='Volume Fraction, \u03a6'
		ylabel= 'Temperature, K'
		#ylabel='Interaction Strength, \u03b5/kbT'
		title= 'SLCT Phase Diagram'
		SLCTplot = phasePlot(xlabel,ylabel,title,phi,spinodal,binodal)
		
		#LIST OF DICTIONARIES
		list_of_plots = list()
		list_of_plots.append(FEplot.plot_dict)
		list_of_plots.append(SLCTplot.plot_dict)

		#Generate table
		#Prune and preen the data set so its nicer looking
		phi = np.round(phi,3)
		phi = phi.tolist()
		phi = [i[0] for i in phi]
		spinodal = np.round(spinodal,4)
		spinodal = spinodal.tolist()
		binodal = np.round(binodal,4)
		binodal = binodal.tolist()
		binodal= [i[0] for i in binodal]
		while len(phi) > 20:
			del phi[::2]
			del spinodal[::2]
			del binodal[::2]

		#Generate table
		zipped = zip(phi,spinodal,binodal)

		#Critical point
		critphi = SLCT_crit(r1,r2,z,p1,p2,na,nb,chidb)
		critphi = list(critphi)

		return critphi, list_of_plots, zipped

def propername(polyid,k):
	"""depending on the input, renames the polymers so they can be looked up in the database"""
	if polyid=="PA":
		return "polyethylene"
	elif polyid=="PB":
		return "polypropylene"
	elif polyid=="PC":
		return "poly(ethylene-propylene)"
	elif polyid=="PD":
		return "Syndiotactic%20Polypropylene"
	elif polyid=="PE":	
		return "polybutadiene"
	elif polyid=="PF" and k==2:
		return "polybutylene"
	else:
		return "unknown_type"

def flip(a1,a2,b1,b2,c1,c2):
	return a2,a1,b2,b1,c2,c1


