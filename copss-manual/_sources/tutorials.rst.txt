.. _tutorials:

Tutorials
==========


Input Data File
---------------------
A data file is required to perform a COPSS simulation to define initial configurations of
the particles and fluid domain. Current code implementation requires the data file to be
named as `point_particle_data.in` for point particle systems, and `rigid_particle_data.in`
for finite-size particle systems.

- **point_particle_data.in**

  The format for `point_particle_data.in` follows LAMMPS format for atoms. It can be
  generated using `Pizza <http://pizza.sandia.gov/>`_. A sample `point_particle_data.in`
  for a polymer chain is shown below:

    ::

        LAMMPS FENE chain data file
        11 atoms
        10 bonds
        1 atom types
        1 bond types
        -129.872397092 129.872397092 xlo xhi
        -129.872397092 129.872397092 ylo yhi
        -12.9872397092 12.9872397092 zlo zhi

        Masses

        1 1.0

        Atoms


        1     1 1  -100.493 124.921 -9.297    1  1 1
        2     1 1  -98.1669 114.712 -8.822    1  1 1
        3     1 1  -105.113 111.118 -6.809    1  1 1
        4     1 1  -109.612 107.256 -4.316     1  1 1
        5     1 1  -111.706 103.445 -8.997    1  1 1
        6     1 1  -108.48 97.904 -8.306     1  1 1
        7     1 1  -116.487 93.504 -3.521    1  1 1
        8     1 1  -115.789 85.646 -4.134    1  1 1
        9     1 1  -115.317 78.980 -4.137    1  1 1
        10    1 1  -122.011 80.645 -1.357    1  1 1
        11    1 1  -126.976 80.933 0.209    1  1 1

        Bonds

        1 1 1 2
        2 1 2 3
        3 1 3 4
        4 1 4 5
        5 1 5 6
        6 1 6 7
        7 1 7 8
        8 1 8 9
        9 1 9 10
        10 1 10 11

- **rigid_particle_data.in**

  The format for `rigid_particle_data.in` is different compared to `point_particle_data.in`, as
  it needs extra information (e.g., size, orientation) of finite-size particles. A sample
  `rigid_particle_data.in` for 6 spherical particles is shown below:

    ::

        COPSS rigid particle data file
        6 particles
        1 particle types
        1 mesh types

        Masses

        1 1.0  #Currently mass is not used, since the motion in low Re flows is inertialess

        Particle Meshes

        1 /home/user/surface_mesh_sphere_triMesh_1.e
        #mesh_type,  location and name of the mesh file for the arbitrary shaped particle

        Particles

        1 1 1   -6.793      2.182     -3.278      3.000      3.000      3.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000
        2 1 1   -2.650     -7.185      5.366      3.000      3.000      3.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000
        3 1 1    -2.487      7.503      3.479      3.000      3.000      3.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000
        4 1 1    -2.998     -5.620     -6.768      3.000      3.000      3.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000
        5 1 1     0.925      5.060     -9.369      3.000      3.000      3.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000
        6 1 1    -6.725      0.703      8.300      3.000      3.000      3.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000      0.000

    The particles are defined as:

        ``particle_id p_type mesh_type x  y z magx magy magz th0 th1 th2 Q0 e_in G_x G_y G_z``

        * magx, magy, magz  are scale ratio in x, y, z directions. This is useful for changing the size of the particle. If we use sphere with radius of 1, then 3, 3, 3 means changing its radius to 3.
        * th0, th1, th2  are orientation angles for cylinderical particles.
        * Q0, e_in are charge and dielectric constant of the particle.
        * G_x, G_y, G_z are external body force density on the particle in x, y, z directions.


Input Control File
-------------------

A control file is required to perform a COPSS simulation to define system configurations.
Current code implementation requires the data file to be named as `point_particle_control.in`
for point particle systems, and `rigid_particle_control.in` for finite-size particle systems.
Sample control files can be found in the ``examples/`` directory. The key parameters are user_defined
as follows:

- ``test_name = sedimentation``

    Test_name: it is an optional parameter.

- ``particle_type = rigid_particle``

    Particle's type: so far only `point_particle` and `rigid_particle` are supported. Point
    particles have only translational motion and is often used to model polymers in fluids.
    Rigid particles (finite-size particles) can have arbitrary shapes and both translational
    and rotational motions are considered.

- ``viscosity = 43.3E-15``

    Viscosity of the fluid. It is only used for calculation of characteristic time
    scale. We use the unit of cP. For example, the viscosity of water is
    1 cP = 1 mPa·s = 0.001 Pa·s = 0.001 N·s·m−2 = 1E-15 N*s/um^2.

- ``bead_radius = 0.1``

    The hydrodynamic radius of a single bead with a unit of :math`\mu m` (micro meter).

- ``temperature = 297``

    Temperature with a unit of K (Kelvin).


- ``particle_mesh_type = 'surface_mesh'``

    Particle mesh type are ONLY required for finite-size particles. As of now, two options are available:
    ``surface_mesh`` and ``volume_mesh``. Surface_mesh implies that mesh file for the surface of the particle
    is the required input from the users; while in the case of volume_mesh mesh file for the volume of the particle
    is the required input. In the latter case, COPSS will read in the
    volume mesh and automatically generate a surface mesh from it. The surface mesh is
    the one actually used in the hydrodynamic calculations. The directory to the mesh file
    needs to be specified in ``rigid_particle_data.in`` file. The details of particle mesh files can
    also be found in `Particle Mesh File`_

- ``dimension = 3``

    Dimensionality of the simulation system. Only 3D is supported.

- ``generate_mesh = true``

    This feature lets user chose if COPSS should generate the fluid mesh. If true, COPSS will generate
    the fluid mesh, however, only cubical geometry is supported; if false, user
    needs to provide the fluid mesh file generated using a third-party mesh generator.
    Further details on fluid mesh can be found in section `Fluid Mesh File`_.

- ``slit = '-100. +100. -100. +100. -4.5 +4.5'``

    Defines the boundaries of a cubical simulation box. The sequence in the entry is -X +X -Y +Y -Z +Z.

- ``n_mesh = '60 60 4'``

    This is used in case of `generate_mesh = true`. It defines the number of elements along x, y, z directions of the simulation box.

- ``domain_mesh_file = '/home/user/user_fluid_domain.e'``

    This is used when `generate_mesh = false`. It defines location and name of the fluid mesh file generated by the user.

- ``wall_type = slit``

    Type of the confined box. Currently two options are available: `slit` and `sphere`. For `slit`, the upper and lower
    wall in z-direction are the confining walls. For `sphere`, the spherical boundary is the confining wall.

- ``periodicity = 'true true false'``

    Only works for cuboidal geometry. This parameter is used to specify if the system is periodic in x, y, or z directions.

- ``inlet = 'false false false'``
- ``inlet_pressure = '0 0 0'``

    This feature is only implemented for cuboidal and cylindrical geometries. The `inlet` specifies whether or not x, y, or z direction has a
    pressure gradient. The `inlet_pressure` specify the normal stress on pressure sides of the cuboidal domain in x, y,
    or z direction.

- ``shear = 'false false false'``
- ``shear_rate = '0. 0. 0.'``

    Specifies the surface to which shear is applied in the cuboidal geometry. The `share_rate` specifies the
    shear velocity which can be related to shear rate by shear_velocity = shear_rate*L.

- ``force_field = 'surface_constraint  lj_cut'``
- ``surface_constraint = '10. 10.'``
- ``lj_cut = '1. 2.2 2.5'``

    Defines the force fields in the system. Details can be found in section `Force Field`_.

- ``alpha = 0.2``

    The smoothing parameter in GGEM (dimensionless). This is a very important parameter as it controls the balance
    between local and global calculations, which in turn controls the spread of local force density in space.
    The larger :math:`\alpha` makes sharper Gaussian kernel. A few rules need to be satisfied while choosing
    :math:`alpha`:

        - The cutoff radius, :math:`4/\alpha` cannot be larger than half of the box size in either of the directions.

        - The minimal fluid mesh size has to be smaller than $1 / (\sqrt{2}\alpha)$


    In case of a very large :math:`\alpha`, the cut-off radius is small, but the fluid mesh will be very fine, and most of the computational time
    will be spent on the finite element Stokes solver. On the other hand, in case of a very small :math:`\alpha`, the cut-off radius is large,
    but the fluid mesh will be very coarse, so most of the computational time will be spent on local velocity calculation. Practically, one
    can test the total computation time needed to solve the Stokes equation for one step and choose the :math:`\alpha` that corresponds to
    the least computation time.

- ``ibm_beta = 0.35``

    This feature is required ONLY for finite-size particles. This value should be tuned depending on discretization of the finite-size particle.
    For example, if a unit sphere's surface is discretized by 20 surface nodes, we have found that ibm_beta = 0.35 gives the best results
    for sedimenting velocity of a single particle in a slit compared with analytical solution; if the unit sphere's surface is
    discretized by 40 surface nodes, then the optimal ibm_beta was found to be 0.64. We recommend the user to perform
    some test cases for the validation against analytical solutions to find the optimal value of ibm_beta associated with a specific surface mesh.


- ``stokes_solver = superLU_dist``

    Define the type of StokesSolver: ``field_split`` or ``superLU_dist``.

    - ```field_split`` is an iterative solver

    - ```superLU_dist`` is the direct solver. Direct solver is recommended unless it crashes because of memory limitation
      (typically ~1 million degrees of freedom for a finite element problem tested on computer node with 128GB memory).


- ``max_linear_iterations = 300``

    Maximum number of linear iterations for the iterative Stokes finite element solver beyond which the code crashes if the convergence is not reached.

- ``linear_solver_rtol = 1E-6``
- ``linear_solver_atol = 1E-6``

    Linear solver tolerances, default =1E-6

- ``user_defined_pc = true``

    User defined preconditioning matrix. ONLY used for the iterative solver.

- ``schur_user_ksp = true``
- ``schur_user_ksp_rtol = 1E-9``
- ``schur_user_ksp_atol = 1E-6``

    User defined KSP for the schur complement. ONLY needed for the iterative solver.

- ``schur_pc_type = SMp``

    Schur complement preconditioning type. ONLY used with iterative solver `SMp`: use the pressure mass matrix (*Recommended*). `SMp_lump`:  lumped pressure mass matrix.

- ``compute_eigen = true``

    Depending on whether wants compute eigenvalues or not. ONLY for Brownian systems with Hydrodynamic interactions in restart mode.
    When compute_eigen is false, the program will read 'out.eigenvalue' from previous simulations before restart.

- ``tol_eigen = 0.01``

    Tolerance for eigenvalue calculation using SLEPc.

- ``max_n_cheb = 50``

    Maximum order of Chebyshev polynomial that are used in computing Brownian displacements.

- ``tol_cheb = 0.1``

    Tolerance of the convergence of Chebyshev polynomial method to compute Brownian displacements.

- ``eig_factor = 1.05``

    This factor is used to enlarge range between eig_max and eig_min, when Chebyshev polynomial method fails to converge.

- ``with_hi = true``

    This feature is sued to specify whether hydrodynamic interactions are computed. If `false`, overdamped (non-inertial) Langevin dynamics will be used.

- ``with_brownian  = true``

    Whether or not to include Brownian motion on particles.

- ``adaptive_dt    = false``

    Used to specify if adaptive time stepping should be used. If `false`, constant time step will be used.

- ``max_dr_coeff   = '9. 0.1 0.01'``

    It is a user defined quantity. In the above mentioned example, the simulation time is smaller than 9,
    we use 0.1 as the maximum time step, i.e., :math:`dt = 0.1 / max(|v|)` (v is the velocity of particles);
    when simulation time is larger than 9, we use 0.01 as the maximum time step.


- ``update_neighbor_list_everyStep = true``

    Whether or not to update particles' neighbor list at every time step.

- ``restart        = false``

    Whether or not to restart simulation from a checkpoint. If true, COPSS will restart from the configuration  saved in the output file at the last time step.

- ``random_seed    = 456789``

    Random seed for generating random vector for Brownian dynamics.

- ``nstep          = 30000``

    Total number of steps for the simulation run.

- ``n_relax_step = 1``

    Perform some Free draining steps in case Chebyshev cannot converge even after recalculating the eigenvalues.

- ``write_interval = 100``

    Interval to write output information, e.g. particles' coordinates, fluid velocities, pressure, etc.

>  ``output_file    = 'equation_systems particle_mesh trajectory surface_node'``

    Output files.
        - ``equation_systems``: output system solution in .e files.
        - ``particle_mesh``: output surface mesh finite-size particles.
        - ``trajectory``: output trajectory of the center of mass for arbitrary shaped particles or the center of mass for polymer chains.
        - ``surface_node``: output surface node positions of the finite-size particles (note that surface_node is needed to restart the rigid particle systems).

- ``print_info     = false``

    This feature lets the user to control if detailed output of simulation information is needed. Note that, if `true`, it will produce a lot of data to the disk.


- ``debug_info     = false``

    Whether or not to output debug information. This feature is recommended to be used by the developers only.


Force Field
--------------

Force fields in COPSS are designed to be extensible, so that the user can build their own
force fields with minimal efforts. All force fields source codes can be found in the ``src/fix``
directory. For point particles, the base class can be found in ``fix_point.h`` and ``fix_point.C``;
for finite-size particles, the base class can be found in ``fix_rigid.h`` and ``fix_rigid.C``.
All force fields are derived from these base classes. The available force fields are listed
in the following subsections.


1. Particle - particle force types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Particle-particle force types defines the inter particle force types. Let us suppose
that two particles :math:`i` and :math:`j`, located at :math:`R_i` and :math:`R_j` and
have forces acting on them: math:`f_i` and :math:`f_j` respectively. Some variables are defined
as follows:

    :math:`\vec{f}_{ij}`: force acting on particle :math:`i` by particle :math:`j`.

    :math:`\vec{R}_{ij}`: vector pointing from :math:`i` to :math:`j` , i.e., :math:`\vec{R}_{ij} = \vec{R}_j - \vec{R}_i`, which is automatically updated due to periodic boundary conditions.

    :math:`\vec{r}_{ij}` : unit vector of :math:`\vec{R}_{ij}`.

    :math:`a`: bead radius. All lengths are non-dimensionalized by this length.

    :math:`b_k`: Kuhn length.

    :math:`N_{k,s}`: number of Kuhn length per spring.

    :math:`q_0`: maximum spring length, :math:`q_0 = N_{k,s} * b_k`.

    :math:`L`: contour length of the DNA molecule, :math:`L = N_s * q_0`.

    :math:`S_s^2`: radius of gyration of an ideal chain consisting of :math:`N_{k,s}` Kuhn segments, :math:`S_s^2 = N_{k,s}*b_k^2/6`.

Usage:

    ::

        particle_particle_force_types = 'pp_ev_gaussian, pp_ev_gaussian_polymerChain, ...'

        pp_ev_gaussian = 'param1, param2, ...'

        pp_ev_gaussian_polymerChain = 'param1, param2, ...'

Supported particle force types are listed as follows:

- **pp_ev_gaussian**: defines a gaussian potential between point particles (\ **beads only**\ ),
  two dimensionless parameters need to be given for this force type, :math:`c_1` (energy)
  and :math:`c_2` (length).

    - Equations:

        :math:`\vec{f}_{ij} = -c_1c_2e^{-c_2 |R_{ij}|^2}*\vec{r}_{ij}`

        :math:`\vec{f}_i += \vec{f}_{ij}`

    - Usage:

        pp_ev_gaussian = ":math:`c_1`, :math:`c_2`"

- **pp_ev_gaussian_polymerChain**: defines a gaussian potential between beads of worm-like
  polymer chain **(polymer chain only)**\ , the only required parameter :math:`ev` is the
  dimensionless excluded volume of beads.

    - Equations:

        :math:`\vec{f}_{ij} = -c_1 c_2 e^{-c_2 |R_{ij}|^2} \vec{r}_{ij}`

        :math:`\vec{f}_i += \vec{f}_{ij}`

        where,

        :math:`c_1 = ev*\ a^3 N_{k,s}^2 (\frac{3}{4 \pi S_s^2})^{3/2}`

        :math:`c_2 =  3 \frac{a^2}{4 S_s^2}`

    - Usage:

        pp_ev_gaussian_polymerChain = ":math:`ev`"


- **pp_ev_lj_cut**: defines a Lennard-Jones potential between two particle :math:`i`
  and :math:`j`. Three non-dimensional parameters, :math:`\epsilon` (energy),
  :math:`\sigma` (particle diameter or slighter bigger, e.g., 2.1), :math:`r_{cut}`
  (cutoff radius) are required for this force field.

    - Equations:

        if  :math:`|R_{ij}| <=  r_{cut}`:

            :math:`\vec{f}_{ij} = -24 \epsilon (2 (\frac{\sigma}{R_{ij}})^{12} - (\frac{\sigma}{|R_{ij}|})^{6} ) * \vec{R}_{ij} / |R_{ij}|^2`

            :math:`\vec{f}_i  += \vec{f}_{ij}`

        else:

            :math:`\vec{f}_i  += \vec{0}`

    - Usage:

        pp_ev_lj_cut = ':math:`\epsilon`, :math:`\sigma`, :math:`r_{cut}`'


- **pp_ev_lj_repulsive**: defines a repulsive Lennard-Jones potential between two
  particle :math:`i` and :math:`j`. Two non-dimensional parameters, :math:`\epsilon` (energy),
  and :math:`\sigma` (particle diameter or slighter bigger, e.g., 2.1) are required for this
  force field.

    - Equations:

          if  :math:`|R_{ij}| <=  r_{cut}`:

            :math:`\vec{f}_{ij} = -24 \epsilon (2 (\frac{\sigma}{|R_{ij}|})^{12} - (\frac{\sigma}{|R_{ij}|})^{6} )  \vec{R}_{ij} / |R_{ij}|^2`

            :math:`\vec{f}_i  += \vec{f}_{ij}`

          else:

            :math:`\vec{f}_i  += \vec{0}`

          where :math:`r_{cut}` is set to be the equilibrium length where lj force is zero, i.e.,

            :math:`r_{cut} = 2^{\frac{1}{6}}\sigma`


    - Usage:

         pp_ev_lj_repulsive = ':math:`\epsilon`, :math:`\sigma`'


- **pp_ev_harmonic_repulsive**: defines a repulsive harmonic potential between particle
  :math:`i` and :math:`j`. Two non-dimensional parameters, :math:`k`(energy) and
  :math:`r_0` (equilibrium length) are required for this force field.

    - Equations:

        if :math:`|R_{ij}| < r_0` :

            :math:`\vec{f}_{ij} = k (|R_{ij}| - r_0) \vec{r}_{ij}`

            :math:`\vec{f}_i  += \vec{f}_{ij}`

        else :

            :math:`\vec{f}_i  += \vec{0}`


    - Usage:

        pp_ev_harmonic_repulsive = ':math:`k`, :math:`r_0`'



- **pp_wormLike_spring**: defines spring forces for worm-like bead spring chains
  (**polymer chain only**). All parameters are set by default in COPSS.

    - Equations:

        :math:`\vec{f}_{ij} = c_1 ((1-\frac{|R_{ij}|}{L_s})^{-2} - 1 + 4 \frac{|R_{ij}|}{Ls}) \vec{r}_{ij}`

        :math:`\vec{f}_i  += \vec{f}_{ij}`

        where,

        :math:`c_1 = \frac{a}{2 b_k}`

        :math:`L_s = \frac{N_{k,s} b_k}{a}`

- **p_constant**: defines a constant force field on all of the beads. Three parameters
  (force along :math:`x`, :math:`y`, :math:`z` direction), :math:`f_x`, :math:`f_y`,
  :math:`f_z` are needed for the force field.

    - Equations:

        :math:`\vec{f}_{constant} = (f_x, f_y, f_z)`

        :math:`\vec{f}_i += \vec{f}_{constant}`

    - Usage:

        p_constant = ":math:`f_x`, :math:`f_y`, :math:`f_z`"


2. Particle - wall force types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Particle-wall force types defines the force types between particles and wall,
which should be neither a periodic boundary nor an inlet/outlet. Wall type can only
be either **slit** or **sphere** for now, and will be extended to more types
in the future developments. Assuming that we have a particle :math:`i`, located at
:math:`R_i` and the force on which is :math:`f_i`. Some variables are defined as
follows:

    :math:`\vec{f}_{iw}`: force acting on particle :math:`i` by wall.

    :math:`\vec{R}_{iw}`: vector pointing from :math:`i` to wall in normal direction.

    :math:`\vec{r}_{iw}`: unit vector of :math:`\vec{R}_{iw}`.


If wall_type = 'slit', we compute particle-wall interactions for lower wall and
upper wall separately in each direction, i.e.,

    :math:`\vec{R}_{i,lo} = \vec{box}_{min} - \vec{R}_i`,

    :math:`\vec{R}_{i,hi} = \vec{box}_{max} - \vec{R}_i`

If wall_type = 'sphere' :

    :math:`\vec{R}_{iw} = \vec{r}_i * (R_{sphere} - |\vec{R}_i|)`

    where :math:`\vec{r}_i` is the unit vector of :math:`\vec{R}_i`, and
    :math:`|\vec{R}_i|` is the distance of particle :math:`i` to origin.


Usage:

    ::

        particle_wall_force_types = 'pw_ev_empirical_polymerChain, pw_ev_lj_cut, ...'

        pw_ev_empirical_polymerChain = 'param1, param2, ...'

        pw_ev_lj_cut = 'param1, param2, ...'

Supported particle wall force types are as follows:


- **pw_ev_empirical_polymerChain**: defines an empirical bead_wall repulsive potential
  on polymer beads (**polymer chain only**). All parameters are set by default in COPSS:

  - Equations:

      If :math:`R_{iw} < d_0`:

        :math:`\vec{f}_{iw} = -c_0 (1- \frac{|R_{iw}|}{d_0})^2 \vec{r}_{iw}`

        :math:`= -\frac{25 a}{b_k}(1-\frac{2 |R_{iw}| a}{b_k \sqrt{N_{k,s}}})^2  \vec{r}_{iw}`

        :math:`\vec{f}_i += \vec{f}_{iw}`

      else:

        :math:`\vec{f}_i += 0`

      where,

       :math:`c_1 = a/b_k`

       :math:`c2 = c1/\sqrt{N_{k,s}} = \frac{a}{b_k \sqrt{N_{k,s}}}`

       :math:`d_0 = 0.5/c_2 = \frac{b_k \sqrt{N_{k,s}}}{2 a}`

       :math:`c_0 = 25 c_1 = \frac{25 a}{b_k}`

      The corresponding potential is:

       If :math:`|R_{iw}| < d_0`:

        :math:`U_i^{wall} = \frac{A_{wall}}{3 b_k/a d_0}(|R_{iw}| - d_0)^3`,

       else:

        :math:`U_i^{wall} = 0`

       where,

        where :math:`A_{wall} = 25/a`



- **pw_ev_lj_cut**: defines a Lennard-Jones potential between particle :math:`i`
  and the wall. Three non-dimensional parameters, :math:`\epsilon` (energy),
  :math:`\sigma` (particle radius or slighter bigger, e.g., 1.05),
  :math:`r_{cut}` (cutoff radius) are required for this force field.

  - Equations:

      If  :math:`|R_{iw}| <=  r_{cut}`:

        :math:`\vec{f}_{iw} = -24 \epsilon (2*(\frac{\sigma}{|R_{iw}|})^{12} - (\frac{\sigma}{|R_{iw}|})^{6} ) \vec{R}_{iw} / \vec{R}_{iw}^2`

        :math:`\vec{f}_i  += \vec{f}_{iw}`

      else:

        :math:`\vec{f}_i  += \vec{0}`

  - Usage:

     pw_ev_lj_cut = ':math:`\epsilon`, :math:`\sigma`, :math:`r_{cut}`'


- **pw_ev_lj_repulsive**: defines a repulsive Lennard-Jones potential between particle
  :math:`i` and the wall. Two non-dimensional parameters, :math:`\epsilon` (energy),
  :math:`\sigma` (particle radius or slighter bigger, e.g., 1.05) are required for
  this force field.

  - Equations:

      If  :math:`|R_{iw}| <=  r_{cut}`:

        :math:`\vec{f}_{iw} = -24 \epsilon (2 (\frac{\sigma}{|R_{iw}|})^{12} - (\frac{\sigma}{|R_{iw}|})^{6} ) * \vec{R}_{iw} / |R_{iw}|^2`

        :math:`\vec{f}_i  += \vec{f}_{iw}`

      else:

        :math:`\vec{f}_i  += \vec{0}`

      where :math:`r_{cut}` is set to be the equilibrium length where lj force is zero:

        :math:`r_{cut} = 2^{\frac{1.}{6.}} * \sigma`

  - Usage:

      pw_ev_lj_repulsive = ':math:`\epsilon`, :math:`\sigma`'


* **pw_ev_harmonic_repulsive**: defines a repulsive harmonic potential between particle
  :math:`i` and the wall. Two non-dimensional parameters, :math:`k` (energy) and
  :math:`r_0` (equilibrium length, e.g., 1.1) are required for this force field.

  - Equations:

      If :math:`|R_{iw}| < r_0` :

        :math:`\vec{f}_{iw} = k * (|R_{iw}|- r_0) * \vec{r}_{iw}`

        :math:`\vec{f}_i  += \vec{f}_{iw}`

      else:

        :math:`\vec{f}_i  += \vec{0}`

  - Usage:

      pw_ev_harmonic_repulsive = ':math:`k`, :math:`r_0`'


Fluid Mesh File
-------------------------------------------

User need to first design the fluid domain as per the model requirement, and then prepare the finite element mesh file
for the fluid domain. The fluid domain can have arbitrary shapes like ? . COPSS requires that at least one of the boundary of the
fluid domain to be confined.

COPSS itself can generate a mesh with HEX20 element (HEX20 supports second-order shape functions) with the limitation
being that the fluid domain must be cuboid. For example, in the simulation control file, the user can specify:

  ::

      generate_mesh = true                        (use COPSS to generate the cubic mesh)
      slit = '-100. +100. -100. +100. -4.5 +4.5'  (this is the size of the cubic domain, which centers at (0, 0, 0), with side locations specified as -X +X -Y +Y -Z +Z)
  	  n_mesh = '60 60 4'                          (this is the number of elements along X, Y, and Z directions)

If the desired fluid domain is not cuboid, one will need a third-party mesh generator to prepare the mesh.
`CUBIT <https://cubit.sandia.gov/>`_ and the associated Exodus mesh file format are used by COPSS developers.
Please check with your institution to see if a CUBIT license is available. If you could not gain access to
CUBIT, you could resort to open-source mesh generators, such as `Gmsh <http://gmsh.info/>`_ or `TetGen <http://wias-berlin.de/software/index.jsp?id=TetGen&lang=1>`_.
You could also use commercial finite element software (Abaqus) to export a mesh file (.inp format) that libMesh can read.
Current mesh file formats libMesh supports are:

  ::

      *.e    -- Sandia's ExodusII format
      *.exd  -- Sandia's ExodusII format
      *.gmv  -- LANL's General Mesh Viewer format
      *.mat  -- Matlab triangular ASCII file
      *.n    -- Sandia's Nemesis format
      *.nem  -- Sandia's Nemesis format
      *.off  -- OOGL OFF surface format
      *.ucd  -- AVS's ASCII UCD format
      *.unv  -- I-deas Universal format
      *.vtu  -- Paraview VTK format
      *.inp  -- Abaqus .inp format
      *.xda  -- libMesh ASCII format
      *.xdr  -- libMesh binary format
      *.gz   -- any above format gzipped
      *.bz2  -- any above format bzip2'ed
      *.xz   -- any above format xzipped
      *.cpa  -- libMesh Checkpoint ASCII format
      *.cpr  -- libMesh Checkpoint binary format

The above are from libMesh source file: src/mesh/namebased_io.C


Particle Mesh File
-----------------------
This file is ONLY needed for the arbitrary shaped particles.

The user will need to prepare a mesh file for each type of arbitrary shaped particles. Different types of particles can have
different shapes. Because an immersed boundary method is used in the algorithm, only the boundary of the particle
is needed in this simulation method. You could use 2D elements that supports linear shape functions, such as TRI3 or QUAD4 element,
to generate a surface mesh of the particle. You could also provide a volume mesh (3D) for the arbitrary shaped particle,
COPSS will read the volume mesh and automatically extract boundary mesh from it and write the surface mesh to the file.


Integration tests
-------------------
The purpose of integration tests is to make sure new developments do not disturb the system. So far,
we have prepared several integration test systems:

    1) **PointParticle_Polymer_BD_HI**: Single polymer chain diffusing in a slit channel with HI considered.
    2) **RigidParticle_Sphere_Sedimentation_HI**: Single spherical particle sedimenting in a slit channel with HI considered.

The benchmark systems are located at ``$COPSS_DIR/tests/integration_tests/resources/``. For each of the system, benchmark output
for integration tests were generated by running run.sh and input files in each of the folder. These results are stored in the ``output/`` folder,
for example, ``$COPSS_DIR/tests/integration_tests/resources/PointParticle_Polymer_BD_HI/output/``.


How to run integration test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    1. change directory to integration test folder:

        - ``cd $COPSS_DIR/tests/integration_tests``

    2. run the test script using Python 2.7.12 or up with at least 4 cpus available:

        - ``python test.py``

How to add a new integration test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    1. Create a new directory:

        - ``mkdir $COPSS_DIR/tests/integration_tests/resources/NEW_TEST``

    2. Create corresponding **input files**, **"run.sh"** and **"zclean.sh"** under the new folder

    3. Run the simulation use the new files created in step 2 and store necessary outputs under folder,
       ``$COPSS_DIR/tests/integration_tests/resources/NEW_TEST/output``

    4. Modify ``$COPSS_DIR/tests/integration_tests/test.json`` to include the new test.

    5. Testing the new integration test.
