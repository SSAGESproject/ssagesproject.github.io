#!/usr/bin/env python
#from initialize import *
import scipy.misc
from mix import *
import matplotlib.pyplot as plt

#Initalization constants
m = 2.457 #segment length
sigma = 3.044 #segment diameter
epsilon = 213.48 #well depth
num_assocs = 3.0 #number of association sites
ikappa = 1.0 #interaction strength paramater kappa
ieps_ass = 1.0 #interaction strength paramater epsilon


#Put these into a single class
compound = Compound(sigma,epsilon,m,num_assocs,ikappa,ieps_ass,9999)
#Temperature
T = 0.363365

dens_num = 0.001

def simpleHelmholtz_HS(T,dens_num,compound,eta):
		#Calculate the eta term for RDF 
		a_hs = (4.0*eta - 3.0*eta**2) / ( 1.0 - eta)**2
		return a_hs


def simpleHS_Diameter(T,m,sigma,epsilon):
		"""
		Calculates the Hard Sphere Diameter 
		T = Temp \K
		m = number of segments in chain
		"""

		fm = 0.0010477 + 0.025337*(m-1)/m 	#Eq. 3 of reference
		f = (1 + 0.2977*(T/epsilon)) / (1 + 0.33163*(T/epsilon) + fm*(T/epsilon)**2) 	#Eq. 2 of reference
		d = sigma*f 	#Eq. 1 of reference
		return d

def simpleHelmholtz(eta,T,dens_num,compound):
		"""Provides the Association contribution to Helmholtz energy
		for a simple, indistinguishable system.
		"""

		#Calculate temp-dependent segment diameter for each compound
		d=0 #FIXMELATER
		d = simpleHS_Diameter(T,compound.m,compound.sigma,compound.epsilon)
		

		#Calculate the eta term for RDF 
		#eta = pi*dens_num*compound.m*d**3 /6.0

		#Calculate the RDF
		RDF = 0
		RDF = (2 - eta) / (2.0 * (1-eta)**3 )

		#Calculate Delta
		#delta =  d**3 *RDF * compound.kappa * ( exp(compound.eps_ass/T) - 1.0 )

		#Debbie's version
		delta =  RDF * compound.kappa * ( exp(compound.eps_ass/T) - 1.0 )
		
		#Calculate X
		#Xa = 2.0 / ( 1 + sqrt( 1 + 4*(compound.num_assocs)*(dens_num)*delta ) )
		#Debbie's version
		Xa = 2.0 / ( 1 + sqrt( 1 + 4*(compound.num_assocs)*(eta)*(6.0/pi)*delta ) )
		


		#Finally Calculate A_Assoc
		A_assoc = compound.num_assocs* ( log(Xa) - Xa/2.0 + 0.5 )

		#Add A_HS
		ahs = simpleHelmholtz_HS(T,dens_num,compound,eta)

		#eta term and log(eta)
		sum = eta * (log(eta) + A_assoc + ahs)

		return sum

def CritPointFunction(guess,dens_num,compound):
	#this x0 needs to be a variable
	eta = guess[0]
	T = guess[1]
	Ad2 =scipy.misc.derivative(simpleHelmholtz, eta, dx=1e-4, n=2, args=(T,dens_num,compound), order=3)
	Ad3 =scipy.misc.derivative(simpleHelmholtz, eta, dx=1e-4, n=3, args=(T,dens_num,compound), order=5)
	return [Ad2,Ad3]

def findCrit(guess,dens_num,compound):
	crit=fsolve(CritPointFunction, guess, args = (dens_num,compound),factor=100,xtol=1e-6 )
	
	return crit
		
def SpinodalFunction(guess,dens_num,compound,T):
	eta = guess
	Ad2 =scipy.misc.derivative(simpleHelmholtz, eta, dx=1e-4, n=2, args=(T,dens_num,compound), order=3)
	return Ad2


def findSpin(Tc,Nc,dens_num,compound):
	#Initialize
	Tvals = np.arange(Tc*.900,Tc*.9999,Tc*.001)
	lhs_spin = np.zeros(( len(Tvals) ))
	rhs_spin = np.zeros(( len(Tvals) ))
	
	#Set up guesses to be near the crit point
	guess_RHS = Nc + 0.01
	guess_LHS = Nc - 0.01

	i = 0
	for Tval in Tvals:

		#Evaluate LHS and RHS separately
		lhs_spin[i]= fsolve(SpinodalFunction, guess_LHS, args = (dens_num,compound,Tval),factor=0.1,xtol=1e-8 )
		rhs_spin[i]= fsolve(SpinodalFunction, guess_RHS, args = (dens_num,compound,Tval),factor=0.1,xtol=1e-8 )

		#Use results from the last run as guesses for the next
		guess_RHS = rhs_spin[i]
		guess_LHS = lhs_spin[i]
		i += 1

	#Concatenate the 2 spinodal array's, flip one and append
	#Reverse the order of the RHS spinodal
	#..and therefore, the temperature array that goes with it
	rhs_spin = rhs_spin[::-1]
	Tvals2 = Tvals[::-1]

	#Add the critical values, must be done *after* reversing
	lhs_spin = np.append(lhs_spin,Nc)
	Tvals = np.append(Tvals,Tc)

	#Concatenate both variables
	spin = np.concatenate((lhs_spin,rhs_spin) )
	T = np.concatenate((Tvals,Tvals2) )
	return T,spin


def binodalFunction(guess,Nc,T,dens_num,compound):
	n1 = guess[0] #LHS
	n2 = guess[1] #RHS


	#Evaluate the function
	fmin1 = (Nc - n2) / (n1 - n2) * ( simpleHelmholtz(n1,T,dens_num,compound) )
	fmin2 = (n1 - Nc) / (n1 - n2) * ( simpleHelmholtz(n2,T,dens_num,compound) )
	fmin = fmin1 + fmin2
	return fmin


def findBinodal(dens_num,Tc,Nc,compound):

	#Initialize
	Tvals = np.arange(Tc*.900,Tc*.9999,Tc*.001)
	bin = np.zeros(( len(Tvals) ))
	eta1 = np.zeros(( len(Tvals) ))
	eta2 = np.zeros(( len(Tvals) ))
	
	#Set up guesses to be near the crit point
	guess_RHS = Nc + 0.001
	guess_LHS = Nc - 0.001

	guess = [guess_LHS,guess_RHS]
	

	#Set up bounds
	bnds = ( (0.001, Nc), (Nc, 999) )

	i = 0
	for Tval in Tvals:

		#Minimize the function
		res = scipy.optimize.minimize(binodalFunction, guess, args = (Nc,Tval,dens_num,compound), bounds = bnds, tol = 1e-12)
		#Store the values in bin
		bin = res.x
		#bin returns [eta1,eta2]
		eta1[i] = bin[0]
		eta2[i] = bin[1]

		#Use the results for the last value
		guess = [bin[0],bin[1]]

		i += 1 #iterate

	#Reverse the order of the RHS spinodal
	#..and therefore, the temperature array that goes with it
	eta2 =eta2[::-1]
	Tvals2 = Tvals[::-1]

	#Add the critical values, must be done *after* reversing
	eta1= np.append(eta1,Nc)
	Tvals = np.append(Tvals,Tc)

	#Concatenate both variables
	spin = np.concatenate((eta1,eta2) )
	T = np.concatenate((Tvals,Tvals2) )
	return T,spin





#################### END OF FUNCTIONS ##########################





	

"""
#This is just code to run the function, not useful for site
#Put in your guess parameters, for critical point
eta = 0.05
T = 0.2
guess = [eta,T]

#The actual free energy
simpleHelmholtz(eta,T,dens_num,compound)

#The critical point
CritVals = findCrit(guess,dens_num,compound)
Tc = CritVals[1]
Nc = CritVals[0]

#Spinodal
Tvals, spin = findSpin(Tc,Nc,dens_num,compound)

a,b =findBinodal(dens_num,Tc,Nc,compound)
"""








