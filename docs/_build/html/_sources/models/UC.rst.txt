

Unit Commitment problem
========================


Unit commitment is the problem of determining the least cost schedule of generating units subject to power balance and network constraints. In OATS, the unit commitment problem is modelled as a
mixed integer linear programming problem. The objective function
is to minimize the total cost of generation over a given time horizon.
The constraints in each step are of power balance, restrictions on
ramp rates, zonal net transfer limits and generation limits.


.. automodule:: oats
    :members: uc
