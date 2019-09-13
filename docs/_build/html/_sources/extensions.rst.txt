

Extending models in OATS
========================

A salient feature of OATS is its ease of extending a model to define a new class of problem.

No modelling tool is capable of capturing all the extensions in constraint handling, or extension in objective function so it is important to give the user freedom to define their problems.

Knowledge of PYOMO modelling language is required to defined OATS models. The GitHub page of OATS includes a range of models that are extended for specific applications.



Modifying objective function
----------------------------


Adding/Modifying constraints
----------------------------

Adding new variables
--------------------

Adding parameters
-----------------

Getting output results on new parameters
----------------------------------------

Reporting marginal prices
--------------------------




A user can solve a new model by called oats function ‘model’. Here is an example of solving DCOPF_BM model:

.. code-block:: python

      import oats
      oats.model(model='DCOPF_BM')

The DCOPF_BM model is a balancing optimisation model where the objective function is to minimise the cost of redispatching generation from their set points; to balance supply and demand, and/or due to thermal and voltage constraints.
