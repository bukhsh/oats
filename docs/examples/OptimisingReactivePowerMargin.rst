

Optimising Reactive Power Margin
================================

The traditional objective function of an optimal power flow problem (OPF) is to
minimise the active power generation subject to meeting system demand and
network constraints. In OATS, it is quite straight forward to modify the objective
function depending on the needs of the problem. In this example, we demonstrate
modifying the objective function of an OPF to optimise reactive power margin.

The traditional objective function of an OPF is given as:

.. math::
  \sum_{g \in G} c_g(p^{G}_{g})

where :math:`c_g` defines a function, which is normally a monotonically increasing
quadratic or a linear function of active power generation.

Let :math:`Q^{min}_g, Q^{max}_g` be the minimum and maximum reactive power generation bounds of
a generator :math:`g`. Let :math:`q_g` be reactive power generation from generator :math:`g`.
The following quadratic term is the square of the distance from the mid-point of each generation
reactive power capability.

.. math::
  m_g = \sum_{g \in G} \left(q_g - \left(\frac{Q^{min}_g+ Q^{max}_g}{2}\right)\right)^2

Now we can modify the objective function in the OPF as follows:

.. math::
  \gamma_1\sum_{g \in G}c_g(p^{G}_{g}) + \gamma_2\sum_{g \in G} m_g(q^{G}_{g})

where :math:`\gamma_i, (i=1,2)` are weights and can be changed depending on the
importance associated to the active power cost and reactive power margins.


Now, the question is that how can we achieve all the above within OATS. The first step is to
define new parameters, set and variables. In this problem, we only need to define
the following two new parameters.

.. code-block:: python

  model.gamma1 = Param(within=NonNegativeReals) # weight for active power
  model.gamma2 = Param(within=NonNegativeReals) # weight for reactive power

Once the above two parameters are defined, we can modify the objective function as follows:

  .. code-block:: python

    def objective(model):
        obj = model.gamma1*sum(model.c2[g]*(model.baseMVA*model.pG[g])**2+model.c1[g]*model.baseMVA*model.pG[g]+ model.c0[g] for g in model.G)+\
        sum(model.VOLL[d]*(1-model.alpha[d])*model.baseMVA*model.PD[d] for d in model.D)+\
        model.gamma2*sum(model.qG[g]-0.5*(model.QGmin[g]+model.QGmax[g]))^2
        return obj
