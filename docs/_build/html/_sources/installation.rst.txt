

Installation
==============


OATS
--------------------------
OATS can be installed using pip;

.. code-block:: python

      pip install oatspower

The pip installation is most suited to users wishing to solve standard 'off-the-shelf' power flow problems without the need for full access to the OATS scripts. The ipopt solver is included in the oatspower package along with the following key dependencies:


OATS can also be installed directly from the source available `here <https://github.com/bukhsh/oats/>`__.

Installing OATS from the source offers the advantage of full access to customise the OATS scripts. This is recommended for advanced users comfortable with coding (or learning) in pyomo.

Solvers
--------
A solver is required to solve a power systems optimisation problem in OATS. The choice of problem depends on the type of the optimisation problem. The optimisation problems can be broadly classified into following four main categories:

* Linear programming (LP)
* Nonlinear programming (NLP)
* Mixed integer programming problem (MILP)
* Mixed integer nonlinear programming problem (MINLP)

The following table presents the classification of the traditional optimisation models implemented in OATS and suitable solvers that can be used to solve these problems.

+-----------------------------+------------+---------------------+
| Model                       | Type       | Solver              |
+=============================+============+=====================+
| DC Optimal Power Flow       | LP         | cplex, ipopt, glpk  |
+-----------------------------+------------+---------------------+
| AC Optimal Power Flow       | NLP        |ipopt                |
+-----------------------------+------------+---------------------+
| DC Security Constrained OPF | LP         |  cplex, ipopt, glpk |
+-----------------------------+------------+---------------------+
| Unit commitment             | MILP       | cplex               |
+-----------------------------+------------+---------------------+



NEOS
~~~~~
OATS allow a user to submit the problems to NEOS server. A user can specify neos=True option while calling the function and also can specify the solver to use on the NEOS server by using the option 'solver'.

For more details on the available solvers on the NEOS server, please follow this `link <https://neos-server.org/neos/>`__.


Local installation of solvers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation of a local solver is recommended for using OATS. This is not only computationally efficient, but also allow greater control for specifying options to the solver. The following table provides a number of open-source and free academic license solvers that can be used with OATS.

+---------------+----------------------+-----------------------+-------------+
| Solver name   | Capability           | License               | Reference   |
+===============+======================+=======================+=============+
| glpk          | LP, MILP             | Open source           | [1]         |
+---------------+----------------------+-----------------------+-------------+
| cbc           | LP, MILP             | Open source           | [2]         |
+---------------+----------------------+-----------------------+-------------+
| lp_solve      | LP, MILP             | Open source           | [3]         |
+---------------+----------------------+-----------------------+-------------+
| ipopt         | LP, NLP              | Open source           | [4]         |
+---------------+----------------------+-----------------------+-------------+
| bonmin        | LP, NLP, MILP, MINLP | Open source           | [5]         |
+---------------+----------------------+-----------------------+-------------+
| couen         | LP, NLP, MILP        | Open source           | [6]         |
+---------------+----------------------+-----------------------+-------------+
| gurobi        | LP, QP, MILP         | Free academic license | [7]         |
+---------------+----------------------+-----------------------+-------------+
| CPLEX         | LP, QP, MILP         | Free academic license | [8]         |
+---------------+----------------------+-----------------------+-------------+



[1] “GLPK (GNU linear programming kit),” 2006. [Online]. Available: http://www.gnu.org/software/glpk

[2] J. Forrest and R. Lougee-Heimer, CBC User Guide, ch. Chapter 10, pp. 257–277. [Online]. Available: https://pubsonline.informs.org/doi/abs/10.1287/educ.1053.0020

[3] “lp solve: Documentation 5.52.5,” 2016. [Online]. Available: http://web.mit.edu/lpsolve/doc/

[4] A. WAchter and L. T. Biegler, “On the implementation of an interior-point filter line-search algorithm for large-scale nonlinear programming,” Mathematical Programming, vol. 106, pp. 25–57, 2006.

[5] “bonmin (basic open-source nonlinear mixed integer programming),” 2005. [Online]. Available: https://www.coin-or.org/Bonmin/

[6] P. Belotti, J. Lee et al., “Branching and bounds tightening techniques for non-convex MINLP,” Optimization Methods and Software, vol. 24, no. 4-5, pp. 597–634, 2009. [Online]. Available: https://projects.coinor.org/Couenne

[7] I. Gurobi Optimization, “Gurobi optimizer reference manual,” 2016. [Online]. Available: http://www.gurobi.com

[8] “IBM ILOG CPLEX Optimizer,” http://www01.ibm.com/software/integration/optimization/cplex-optimizer/, Last 2010.
