.. COPSS-Hydrodynamics documentation master file, created by
   sphinx-quickstart on Fri Jan  4 15:19:32 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to COPSS-Hydrodynamics's documentation!
===============================================

**COPSS** (Continuum Particle Simulation Software) is an open source software for 
continuum-particle simulations. The package is designed to be easy to use, extensible, 
and scalable. It currently includes three modules, `COPSS-Hydrodynamics
<https://bitbucket.org/COPSS/copss-hydrodynamics-public.git>`_ 
to solve hydrodynamic interactions in confined suspensions, `COPSS-Polarization
<https://bitbucket.org/COPSS/copss-polarization-public>`_ to solve electrostatic 
interactions in heterogeneous dielectric media, and `COPSS-CMA-ES
<https://bitbucket.org/COPSS/copss-cma-es>`_ to inversely solve for charges on 
dielectric particles from particle trajectories.

**COPSS-Hydrodynamics**
----------------------------

**COPSS-Hydrodynamics** solves the hydrodynamic interactions in confined suspensions 
by directly solve the Stokes equation. It is based on an efficient O(N) computational 
approach to model the dynamics of hydrodynamically interacting Brownian or non-Brownian 
particles in arbitrary geometries. A parallel finite element Stokes' solver is the center 
of the algorithm. 

Table of contents
------------------
.. toctree::
    :maxdepth: 2
    :caption: Contents:
    
    getting-started

    introduction

    tutorials
    
    how-to-contribute

    acknowledgments

    license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
