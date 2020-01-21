

Models
=========

OATS includes implementation of the following steady-state power system optimisation models:


.. toctree::
    :maxdepth: 1

    models/LF
    models/OPF
    models/SCOPF
    models/UC

The mathematical formulation of these models can


+----------+---------------------------+----------------+------------------------+--------------+
| OATS ID  | Model                     | Classification | Selected solver(s)     | References
+==========+===========================+================+========================+==============+
| DCLF     | DC load flow              | LP             | cplex, glpk            | [1,2]      |
+----------+---------------------------+----------------+------------------------+--------------+
| DCOPF    | DC optimal power flow     | LP             | cplex, gurobi          | [3]         |
+----------+---------------------------+----------------+------------------------+--------------+
| SCOPF    | Security constrained OPF  | LP             | cplex, gurobi          | [4]         |
+----------+---------------------------+----------------+------------------------+--------------+
| ACLF     | AC load flow              | NLP            | ipopt                  | [2,3]      |
+----------+---------------------------+----------------+------------------------+--------------+
| ACOPF    | AC optimal power flow     | NLP            | ipopt                  | [5,6]      |
+----------+---------------------------+----------------+------------------------+--------------+
| UC       | Unit commitment problem   | MILP           | cplex, bonmin          | [7]         |
+----------+---------------------------+----------------+------------------------+--------------+


[1] W. Bukhsh, On Solving the Load Flow Problem as an Optimization
Problem. Tech. Report, University of Strathclyde, May 2018. [Online].
Available: https://strathprints.strath.ac.uk/64156/

[2] S. Frank and S. Rebennack, “An introduction to optimal power
flow: Theory, formulation, and examples,” IIE Transactions,
vol. 48, no. 12, pp. 1172–1197, 2016. [Online]. Available:
https://doi.org/10.1080/0740817X.2016.1189626

[3] A. J. Wood, Power generation, operation, and control [internet re-
source], third edition ed., 2014.

[4] D. Phan and J. Kalagnanam, “Some efficient optimization methods for
solving the security-constrained optimal power flow problem,” IEEE
Transactions on Power Systems, vol. 29, no. 2, pp. 863–872, March
2014.

[5] W. Bukhsh, A. Grothey et al., “Local solutions of the optimal power
flow problem,” Power Systems, IEEE Transactions on, vol. 28, no. 4,
pp. 4780–4788, Nov 2013.

[6] M. B. Cain, R. P. O’Neil, and A. Castillo, “History of optimal power
flow and formulations, optimal power flow paper 1,” 2012.

[7] G. Morales-Espana, J. Latorre, and A. Ramos, “Tight and compact milp
formulation for the thermal unit commitment problem,” Power Systems,
IEEE Transactions on, vol. 28, no. 4, pp. 4897–4908, Nov 2013.
