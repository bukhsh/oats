

Quick Start
============
OATS is a powerful power systems optimisation toolbox. OATS include implementation of the following steady-state analysis models:

* DC/AC load flow problem
* DC/AC optimal power flow problem
* Security constrained optimal power flow problem
* Unit commitment problem

Solving a problem in OATS
--------------------------
.. code-block:: python

      import oats
      oats.dcopf()


The above command will solve a DC optimal power flow problem on a default 24-bus IEEE reliability test system. A user provide their own network by using the keyword 'tc', as shown in an example below.

.. code-block:: python

      import oats
      oats.dcopf(tc='mynetwork.xlsx',)

Other options allow a user to specify solver: either on NEOS server of locally on a machine. The following set of lines solves a DC optimal power flow problem using a local installation of the solver 'cplex'.

.. code-block:: python

      import oats
      oats.dclf(tc='mynetwork.xlsx',solver='cplex',neos=False,out=0):


Output
------
A 'results.xlsx' file is produced after an OATS model is solved. This file in created in the directory where the oats in called. The results file has a same data format as the input test case.
