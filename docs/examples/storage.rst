

Modelling Storage in OATS
=========================
In the current version of OATS, storage is modelled as part of the unit commitment (UC) problem.

The UC problem is a time-linked problem where the time-periods are coupled via ramp rate constraints. The following power balance equation is imposed for each time period t and for each zone z:


.. math::
  \sum_{g \in G} p^{\text{G}}_{g,t} + \sum_{s \in S} \left(p^{\text{Out}}_{s,t}-p^{\text{In}}_{s,t}\right) = \sum_{d \in D}P^{\text{D}}_{d,t}+\sum_{l \in L}p^{\text{L}}_{l,t}


where pIn and pOut represents the charging and discharging of energy storage, respectively. The energy storage is modelled using the following equation:

.. math::
  p^S_{s,t} =\eta^{D}_s p^{\text{Out}}_{s,t}-\frac{1}{\eta^{C}_s} p^{\text{In}}_{s,t}

where :math:`\eta^{C}_s, \eta^{D}_s` are the charging and discharging efficiencies of the storage asset s, respectively.

For details about specifying storage data type, see the explanation of fields `here <https://oats.readthedocs.io/en/latest/dataformat.html#storage>`_. The following command will run the unit commitment model and display results for storage that has been modelled in the network data test.xlsx.


.. code-block:: python

  oats.uc(neos=False,solver='cplex', tc = 'test.xlsx')
