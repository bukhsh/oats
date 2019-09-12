

Installation
================================
OATS can be installed using pip;

.. code-block:: python

      pip install oatspower

The pip installation is most suited to users wishing to solve standard 'off-the-shelf' power flow problems without the need for full access to the OATS scripts. The ipopt solver is included in the oatspower package along with the following key dependencies:


OATS can also be installed directly from the source available `here <https://github.com/bukhsh/oats/>`__.

Installing OATS from the source offers the advantage of full access to customise to the OATS scripts. This is recommended for advanced users comfortable with coding (or learning) in pyomo.

If installing directly from source, users must also install solvers such as ipopt, cplex or others unless using the online 'Neos' solver method. Details of how to install solvers can be found in;

