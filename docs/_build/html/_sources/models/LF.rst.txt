

Load flow problem
==================

The load flow problem can be stated as: for a given power network,
with known complex power loads, and a set of specifications on
power generation and voltages, determine bus voltages, any unspecified generation set point and finally the complex power flow in the
network components. Load flow (or power flow) problem forms the
core of power system analysis. This problem is at the heart of system
planning, operation, contingency analysis and the implementation of
real-time monitoring systems.

Load flow analysis is commonly used for following applications:

* Identify real and reactive power flow
* Identify proper transformer tap settings
* Identify transformer and circuit loadings
* Contingency analysis

The following two tables provide information about the generator and transformers types modelled in OATS.

+-------------------------+
| Generator Types in OATS |
+=========================+
|1=   PV bus              |
+-------------------------+
| 2= Distributed slack bus|
+-------------------------+
| 3= Reference bus        |
+-------------------------+


+---------------------------+
| Transformer Types in OATS |
+===========================+
|1=   2-winding transformer |
+---------------------------+
|2= Tap-changing transformer|
+---------------------------+




Mathematical formulation
------------------------
The load flow problem in OATS is solved as a constrained OPF
problem. The fixed parameters of PV, PQ and Vδ buses are modelled
using hard constraints. The detailed mathematical formulation is provided in the following technical note.


Bukhsh, W. (2018). On Solving the Load Flow Problem as an Optimization Problem. Glasgow: University of Strathclyde. [Online] Available: https://pureportal.strath.ac.uk/en/publications/on-solving-the-load-flow-problem-as-an-optimization-problem



Distributed slack
-----------------
The load flow problem in OATS allow a user to model a distributed
slack. The user can specify the number of slack buses in a system by
changing the generator type from ’1’ to ’2’.



Tap-changing transformer
------------------------
OATS allow a user to determine tap setting of the transformers connecting a high voltage bus to a lower voltage bus. The tap-changing
transformers can be specified using ’2’ in the type field of the transformers. The target voltage at the lower-voltage side is specified in
column VM in the bus sheet. The turn ratios are determined at the high-voltage side of the transformer.


Solving DC and AC load flow problems in OATS
---------------------------------------------

.. automodule:: oats
    :members: dclf


.. automodule:: oats
    :members: aclf
