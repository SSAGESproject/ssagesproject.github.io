.. _getting-started:

Getting Started
================

Installation
--------------
**COPSS** is based on the `LIBMESH <http://libmesh.github.io/>`_ framework. It also
requires `PETSc <https://www.mcs.anl.gov/petsc/index.html>`_ for parallel linear
equation solvers and `SLEPc <http://slepc.upv.es/>`_ for scalable Eigenvalue
computations. In order to achieve the best parallel performance
of COPSS, we strongly suggest you to install the dependent libraries on a Linux cluster environment.
Below are the instructions to install COPSS.

0. System environment preparation

 - `CMAKE <https://cmake.org/>`_ (e.g., but not necessarily, version 3.6.2)
 - `GCC <https://gcc.gnu.org/>`_ (e.g., but not necessarily, version 6.2)
 - `PYTHON <https://www.python.org/>`_ (python 2)
 - `OPENMPI <https://www.open-mpi.org/>`_ (e.g., but not necessarily, version 2.0.1)


1. Installing PETSc

 - Download PETSC's latest release ( version 3.7.4 or later ) from `PETSc download page <https://www.mcs.anl.gov/petsc/download/index.html>`_, or git clone PETSc repository and follow
   these steps:

    - ``mkdir $HOME/projects/``

    - ``cd $HOME/projects/``

    - ``git clone -b maint https://bitbucket.org/petsc/petsc petsc``

 - Configure PETSc:

    - ``cd $HOME/projects/petsc``

    - ``./configure --with-cc=mpicc --with-cxx=mpicxx --with-mpiexec=mpiexec``
      ``--with-fc=mpif90 --download-fblaslapack --download-scalapack --download-mumps``
      ``--download-superlu_dist --download-hypre --download-ml --download-parmetis``
      ``--download-metis --download-triangle --download-chaco --with-debugging=0``

    - And then follow the instructions on screen to install and test the package.

 - Export environment variables: add the following lines to ``~/.bashrc`` and
   execute ``source ~/.bashrc`` before next step. (``/path/to/PETSC`` and ``PETSC_ARCH_NAME`` can be found on the screen after the installation.)

    - ``export PETSC_DIR=/path/to/PETSC``

    - ``export PETSC_ARCH=PETSC_ARCH_NAME``


 - In case of any trouble, please refer to `PETSC installation <https://www.mcs.anl.gov/petsc/documentation/installation.html>`_.

2. Installing SLEPc

 - Download SLEPC's latest release (version 3.7.3 or later) from `SLEPc download <http://slepc.upv.es/download/download.htm>`_,
   or git clone PETSc repository:

    - ``cd $HOME/projects/``

    - ``git clone -b maint https://bitbucket.org/slepc/slepc slepc``

 - Configure PETSc:

        - ``cd $HOME/projects/slepc``

        - ``./configure``

        - And then follow the instructions on screen to install the package

 - Exporting environment variables: add the following codes to ``~/.bashrc`` and ``source ~/.bashrc``
   before next step. (``/path/to/SLEPC`` and ``SLEPC_ARCH_NAME`` can be found on the screen post installation.)

        - ``export SLEPC_DIR=/path/to/SLEPC``

        - ``export SLEPC_ARCH=SLEPC_ARCH_NAME``

 - Test the package (highly recommended bu not necessary)

        - ``make test``

 - In case of any trouble, please refer to `SLEPC installation <http://slepc.upv.es/documentation/instal.html>`_.

3. Installing LIBMESH

 - Download LIBMESH's latest release ( version 1.1.0 or later ) from `LIBMESH download <https://github.com/libMesh/libmesh/releases>`_, or git clone PETSc repository:

    - ``cd $HOME/projects/``

    - ``git clone git://github.com/libMesh/libmesh.git``

 - Build LIBMESH:

        - ``cd $HOME/projects/libmesh``

        - ``./configure -prefix=$HOME/projects/libmesh/libmesh-opt --enable-optional``
          ``--enable-vtk  --enable-gzstream --enable-trilinos --disable-strict-lgpl``
          ``--enable-laspack --enable-capnproto --enable-trilinos --enable-nodeconstraint``
          ``--enable-perflog --enable-ifem --enable-petsc --enable-blocked-storage``
          ``--enable-slepc --enable-unique-id --enable-unique-ptr --enable-parmesh 2>&1``
          ``| tee my_config_output_opt.txt``
          (Read the configuration output, make sure **PETSC** and **SLEPC** are enabled).

        - And then follow the instructions on screen to install and test the package.

 - Export environment variables: add the following codes to ``~/.bashrc`` and ``source ~/.bashrc``
   before next step. (``/path/to/PETSC`` can be found on the screen after installation.)

    - ``export LIBMESH_DIR=/path/to/LIBMESH``

 - If you meet any trouble, please refer to `LIBMESH installation <https://libmesh.github.io/installation.html>`_, or reach out to **LIBMESH** community for help.

4. Install COPSS-hydrodynamics

 - Download the latest COPSS codes

    - ``git clone https://bitbucket.org/COPSS/copss-hydrodynamics-public.git``

 - Add the path to COPSS to system environment: add the following code block to ``~/.bashrc``
   and source it prior to the next steps.

    - ``export COPSS_DIR="/path/to/copss"``  (notice: be careful not to include '/' at the end)

   For example, in my system:

    - ``export COPSS_DIR="/scratch/midway2/jyli/bitbucket/MICCOM/copss/copss-hydrodynamics-private"``

 - Compiling the codes

    1) Manually compile the code by following steps

        - ``cd $COPSS_DIR/src/``
        - ``make package=POINTPARICLE`` (for point particle systems)
        - ``make package=RIGIDPARTICLE`` (for rigid particle systems)

    2) Use auto compilation tool: the compilation tool is located at ``$COPSS_DIR/tools/compile.sh``.
       To use it, depending on your purpose, execute one of the following commands:

        - ``cd $COPSS_DIR/tools/``
        - ``bash compile.sh -h`` (For help)
        - ``bash compile.sh -p POINTPARTICLE`` (Compile PointParticle package)
        - ``bash compile.sh -a clean_first -p POINTPARTICLE`` (Compile POINTPARTICLE package after cleaning)

    3) To run a sedimentation example for rigid particles

        - ``cd $COPSS_DIR/examples/general_rigid_particle/sedimentation_benchmark/``

        - ``bash run.sh``


**Build documentation**
-------------------------------------------
After building **COPSS-Hydrodynamics** successfully, you can further build the documentation
in ``docs/`` directory.

1. Doxygen
    The documentation built using **Doxygen** gives the code-level details, including
    the code structures, class inheritance, details of functions, etc. To compile the documentation,
    make sure [Doxygen](http://www.stack.nl/~dimitri/doxygen/) is ready to be used in the system, then:

    - ``cd $COPSS_DIR/docs/doxygen/``

    - ``doxygen Doxyfile.bak``

    then you can view the documentation in an IE browser:

    - ``google-chrome [path-to-copss]/docs/doxygen/html/index.html``

2. Sphinx
   The documentation built using **Sphinx** gives the tutorial-level details, including
   features of the package, how to run a simulation, how to use a tool, etc. To compile Sphinx,
   make sure you have `Sphinx <http://www.sphinx-doc.org/en/master/>`_ ready, then:

    - ``cd $COPSS_DIR/docs/sphinx``

    - ``make html``

   then you can view the documentation in an IE browser:

    - ``google-chrome [path-to-copss]/docs/sphinx/build/html/index.html``

   To modify Sphinx documentation, you need to write the documentation in one of the rst files,
   for example, if the documentation is about how to run a simulation, it should be written into:

    - ``$COPSS_DIR/docs/sphinx/source/tutorials.rst``
