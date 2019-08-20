

Models
=========

OATS include implementation of the following steady-state power system optimisation models:


.. toctree::
    :maxdepth: 1

    models/LF
    models/OPF
    models/SCOPF
    models/UC



Extending models
----------------

A salient feature of OATS is its ease of extending a model to define a new class of problem.

No modelling tool is capable of capturing all the extensions in constraint handling, or extension in objective function so it is important to give the user freedom to define their problems.

Knowledge of PYOMO modelling language is required to defined OATS models. The GitHub page of OATS includes a range of models that are extended for specific applications.
A user can solve a new model by called oats function ‘model’. Here is an example of solving DCOPF_BM model:

.. code-block:: python

      import oats
      oats.model(model='DCOPF_BM')
