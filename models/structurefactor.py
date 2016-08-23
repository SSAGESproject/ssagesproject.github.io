#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import *
import numpy as np
from plotter import generalPlot
import json
import mpld3

#Simple Calculation of RPA structure factor
def structure_factor(na,nb,ba,bb,phi,chi):
	#Radius of Gyration
	Rga = na*ba**2 / 6.0 
	Rgb = nb*bb**2 / 6.0

	maxb = min(ba,bb)

	endq = 1.0/maxb

	qvals = np.arange(0.001,endq,0.005)
	sinv = np.zeros(( len(qvals) ))

	i = 0
	for q in qvals:

		#G_D(q^2,Rg^2)
		xa = q**2 * Rga**2
		g_a =(2.0/(xa**2)) * (xa - 1 + exp(-1*xa) )

		xb = q**2 * Rgb**2
		g_b =(2.0/(xb**2)) * (xb - 1 + exp(-1*xb) )

		#Inverse Structure Factor
		S1 = 1.0 / (na * phi * g_a)
		S2 = 1.0 / (nb * (1.0-phi) * g_b)
		sinv[i] = S1 + S2 - 2*chi
		sinv[i] = 1.0/sinv[i]

		i += 1
	return qvals,sinv

def rpaPlot(na,nb,ba,bb,phi,chi):
	#fig is the figure axis is the subplot (only 1)
	q = 'q'
	sq = 'S(q)'
	sfword = 'structure factor'
	genplot = generalPlot(q,sq,sfword)

	q,sq = structure_factor(na,nb,ba,bb,phi,chi)
	gline = genplot.axis.plot(q,sq,'m',lw=3)
	legend = genplot.axis.legend()
	
	#id for dictionary
	id = "fig01"
	#turns the figure into a json dump
	json01 = json.dumps(mpld3.fig_to_dict(genplot.fig))

	#Generate table of q, sq values
	zipped = zip(q,sq)
	while len(zipped) > 20:
		del zipped[::2]

	return id, json01, zipped


