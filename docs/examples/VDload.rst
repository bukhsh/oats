

Voltage Dependent Loads
=======================

The steady-state analysis models implemented in OATS have a constant power model of electricity load. The ACOPF model in OATS can be easily extended to model voltage dependent loads. In this demonstrative examples, a ZIP model of electricity load consists of constant impedance (Z), constant current (I) and constant power (P) load components and are represented by a second-order polynomial in bus voltage magnitude as follows:



.. math::
  \begin{align}
  p^{\text{D}}_d(v_d) &= \text{P}^{\text{D}}_d \left( a^\text{P}_dv_d^2+b^\text{P}_dv_d+c^\text{P}_d\right)\\
  q^{\text{D}}_d(v_d) &= \text{Q}^{\text{D}}_d \left(a^\text{Q}_dv_d^2+b^\text{Q}_dv_d+c^\text{Q}_d\right)
  \end{align}


where :math:`a^\text{P}_d, b^\text{P}_d, c^\text{P}_d` are the active and reactive power coefficients of the quadratic polynomial, respectively. Parameters :math:`a^\text{P}_d` represent the relative participation of constant impedance load, :math:`b^\text{P}_d` the relative participation of constant load, and :math:`c^\text{P}_d` the relative participation of constant power load.


The real and reactive power demand are modelled as parameters in the ACOPF model of OATS (written in PYOMO syntax) on the set of demands D, as follows:

.. code-block:: python

  model.PD = Param(model.D, within=Reals)
  model.QD = Param(model.D, within=Reals)

In order to model the dependence of electricity demand on voltages, the real and reactive power parameters are modelled as variables pD and qD, as follows.

.. code-block:: python

  model.pD  = Var(model.D, within=Reals)
  model.qD  = Var(model.D, within=Reals)
  model.aPD = Param(model.D, within=NonNegativeReals)
  model.bPD = Param(model.D, within=NonNegativeReals)
  model.cPD = Param(model.D, within=NonNegativeReals)
  model.aQD = Param(model.D, within=NonNegativeReals)
  model.bQD = Param(model.D, within=NonNegativeReals)
  model.cQD = Param(model.D, within=NonNegativeReals)



The coefficients of the quadratic function are defined as parameters given by the user. Equations (2) are implemented in the ACOPF model of OATS to model the ZIP load as follows:

.. code-block:: python

  def real_power_demand(model,d):
    return model.pD[d] == model.PD(model.aPD[d]*model.v[b]**2+model.bPD[d]*model.v[b]+model.cPD[d])

  def reactive_power_demand(model,d):
    return model.qD[d] == model.QD(model.aQD[d]*model.v[b]**2+model.bQD[d]*model.v[b]+model.cQD[d])


The implementation of the above model is provided in the `GitHub folder <https://github.com/bukhsh/oats/tree/master/OATS-models>`_ containing OATS models extensions.
