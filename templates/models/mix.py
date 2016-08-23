#!/usr/bin/env python
import numpy as np
from scipy.optimize import fsolve
from math import *

"""
Mix.py is a file that designates 2 classes: Compound, and Mix
These are just a good way to organize component parameters. 
For future SAFT developement...
"""

class Compound:
	"""Simple Compound"""
	def __init__(self,sigma,epsilon,m,num_assocs,kappa,eps_ass,xcomp):
			self.sigma = sigma
			self.epsilon = epsilon
			self.m = m
			self.num_assocs = num_assocs
			self.kappa = kappa
			self.eps_ass = eps_ass
			self.xcomp = xcomp

class Mix:
	"""Mixture"""
	def __init__(self,c1,c2,kij):
			self.sigma = [c1.sigma,c2.sigma]
			self.epsilon = [c1.epsilon, c2.epsilon]
			self.m = [c1.m,c2.m]
			self.num_assocs = [c1.num_assocs, c2.num_assocs]
			self.kappa = [c1.kappa, c2.kappa]
			self.eps_ass = [c1.eps_ass,c2.eps_ass]
			self.xcomp = [c1.xcomp, c2.xcomp]
			self.k = kij
			
