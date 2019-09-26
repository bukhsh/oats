

Extending models in OATS
========================

A salient feature of OATS is its ease of extending a model to define a new class of problem.

No modelling tool is capable of capturing all the extensions in constraint handling, or extension in objective function so it is important to give the user freedom to define their problems.

Knowledge of PYOMO modelling language is required to defined OATS models. The `GitHub <https://github.com/bukhsh/oats/tree/master/OATS-models>`_ page of OATS includes a range of models that are extended for specific applications.

Adding variables
----------------
Variables in OATS are defined using Pyomo's 'Var' function. For example, real power generation variable in DCOPF model of OATS is defined as follows:

.. code-block:: python

  model.pG = Var(model.G, domain= Reals)

The above definition of the variable name 'pG' states that it is variable defined on a set of generators 'G' and is with the domain of real numbers.

Adding parameters
------------------
Parameters in OATS are defined using Pyomo's 'Param' function. The following example shows definition of a parameter:

.. code-block:: python

  model.PGmax = Param(model.G, within=NonNegativeReals)


The above definition of a parameter 'PGmax' defines a new parameter that belongs to the set of generators 'G' and since it is modelling the capacity of a generator it's domain is defined as a set of non-negative real numbers. OATS will raise an error if a user tries to input a negative value for a generator capacity.


Modifying objective function
----------------------------
The objective function describes the main aim of the model which is either to minimise or maximise. In power systems optimisation problems often the objective function is to minimise the total cost of generation that is required to meet demand. The objective function of DCOPF and ACOPF models in OATS is written as follows:


.. code-block:: python

  def objective(model):
      obj = sum(model.c2[g]*(model.baseMVA*model.pG[g])**2+model.c1[g]*model.baseMVA*model.pG[g]+ model.c0[g] for g in model.G)+\
      sum(model.VOLL[d]*(1-model.alpha[d])*model.baseMVA*model.PD[d] for d in model.D)
      return obj

The first part of the objective function is to minimise the cost of generation and the second part of the objective function is to minimise the cost of load shedding. 'c2', 'c1' and 'c0' are the coefficients of the quadratic cost function and 'VOLL' represents the value of lost load. 'g' represents a generator in 'model.G' set of generators.  'd' represents a demand in 'model.D' set of demands.

The objective function in OATS can be changed by modifying the 'obj' variable. For example, if it is desired in the ACOPF model that the voltages deviation from 1 p.u. is penalised then that could be achieved by modifying the objective function in the following way:

.. code-block:: python

  def objective(model):
      obj = sum(model.c2[g]*(model.baseMVA*model.pG[g])**2+model.c1[g]*model.baseMVA*model.pG[g]+ model.c0[g] for g in model.G)+\
      sum(model.VOLL[d]*(1-model.alpha[d])*model.baseMVA*model.PD[d] for d in model.D)+\
      model.WV*sum((1-model.v[b])**2 for b in model.B)
      return obj

Note that we have added a penalty in the objective function that penalises the violation of the voltages from 1 p.u. 'WV' is a weighting on the voltage deviation part of the objective function. 'b' represents a demand in 'model.B' set of demands. 'model.v[b]' represents the voltage at bus 'b'.

Adding/Modifying constraints
----------------------------
Constraints in OATS are implemented as function calls for each member of a set. For example, line limits in DCOPF are implemented as follows:

.. code-block:: python

  def line_lim1_def(model,l):
      return model.pL[l] <= model.SLmax[l]
  def line_lim2_def(model,l):
      return model.pL[l] >= -model.SLmax[l]


The line limit constraints are applied for each member of the set of lines 'L'. The following code snippet presents an example where the line limits are relaxed by 10%. 'pL[l]' represents the active power flow in line 'l' and 'SLmax[l]' represents the continuous line rating of line 'l'.


.. code-block:: python

  def line_lim1_def(model,l):
      return model.pL[l] <= 1.10*model.SLmax[l]
  def line_lim2_def(model,l):
      return model.pL[l] >= -1.10*model.SLmax[l]

Consider a case when the relaxation of 10% is required to be penalised in the objective function. This could be achieved by defining new variables (a variable for each line) that captures line violations up to 10% and then penalises it in the objective function.

The first step is to define new variables as follows:


.. code-block:: python

  model.relaxL = Var(model.L, domain= NonNegativeReals)

The line limit constraints are modified as follows:

.. code-block:: python

  def line_lim1_def(model,l):
      return model.pL[l] <= model.SLmax[l]+model.relaxL[l]
  def line_lim2_def(model,l):
      return model.pL[l] >= model.SLmax[l]-model.relaxL[l]

The line_lim1_def constraint ensures that the active power flow 'model.pL[l]' through line 'l' is less than or equal to the continuous line rating 'model.SLmax' plus the relaxation variable 'model.relaxL[l]'.
The line_lim2_def constraint ensures that the active power flow 'model.pL[l]' through line 'l' is more than or equal to the continuous line rating 'model.SLmax' minus the relaxation variable 'model.relaxL[l]'.

The variable 'relaxL' needs to be bounded so that the line violations are limited to 10%. This can be achieved using the following constraint:

.. code-block:: python

  def relaxL_bound(model,l):
      return model.relaxL[l] <= 0.1*model.SLmax[l]

The final step is to penalise variable 'relaxL' in the objective function:

.. code-block:: python
  def objective(model):
      obj = sum(model.c2[g]*(model.baseMVA*model.pG[g])**2+model.c1[g]*model.baseMVA*model.pG[g]+ model.c0[g] for g in model.G)+\
      sum(model.VOLL[d]*(1-model.alpha[d])*model.baseMVA*model.PD[d] for d in model.D)+\
      model.WR*sum(model.relaxL[l] for l in model.L)
      return obj

The objective function now puts a cost on relaxation of the line power flow constraint, 'WR' is the weighting of the cost. 

Solving user defined models
---------------------------


A user can solve a new model by called oats function ‘model’. Here is an example of solving DCOPF_BM model:

.. code-block:: python

      import oats
      oats.model(model='DCOPF_BM')

The DCOPF_BM model is a balancing optimisation model where the objective function is to minimise the cost of redispatching generation from their set points; to balance supply and demand, and/or due to thermal and voltage constraints.
