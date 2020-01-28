

Unit Commitment problem
========================


Unit commitment is the problem of determining the least cost schedule of generating units subject to power balance and network constraints. In OATS, the unit commitment problem is modelled as a
mixed integer linear programming problem. The objective function
is to minimise the total cost of generation over a given time horizon.
The constraints in each step are of power balance, restrictions on
ramp rates, zonal net transfer limits and generation limits.

A mathematical formulation of the UC problem
--------------------------------------------

Several mathematical formulations of the unit commitment problem exists in literature. The current release of oats implement a formulation from the following paper:

G. Morales-España, J. M. Latorre and A. Ramos, "Tight and Compact MILP Formulation for the Thermal Unit Commitment Problem," in IEEE Transactions on Power Systems, vol. 28, no. 4, pp. 4897-4908, Nov. 2013.
doi: 10.1109/TPWRS.2013.2251373

Note that the above formulation provides several tight relaxations around minimum start-up (shut-down) times of the thermal generators. These relaxations can easily be implemented in OATS by adopting the current ‘UC.mod’ model file. In case of any issues, the user is encouraged to raise an issue via GitHub page for support.

Solving UC problems in OATS
---------------------------
.. automodule:: oats
    :members: uc
