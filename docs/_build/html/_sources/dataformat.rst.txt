Data format
================================
OATS uses a spreadsheet format for specifying network, demand and generation data.

Download a template for OATS from `here <https://github.com/bukhsh/oats/blob/master/OATS-testcases/tempelate.xlsx>`__.

OATS also has a test case library where a number of standard IEEE and some real-world test cases are provided. The test case library is available on the `OATS GitHub page. <https://github.com/bukhsh/oats>`

OATS parameter descriptions
------------------

The parameters required to describe a network in OATS are outlined below, Optional parameters are highlighted by (^);

bus
^^^^^^^^^^^^^^^^^^^^^
+-----------+---------------------------------------------------------------------+
| name      | bus name. string (can contain letters and/or numbers)               | 
+-----------+---------------------------------------------------------------------+
| baseKV    | base voltage (kV)                                                   | 
+-----------+---------------------------------------------------------------------+
| type      |                                                                     | 
+-----------+---------------------------------------------------------------------+
|           | PQ bus = 1                                                          | 
+-----------+---------------------------------------------------------------------+
|           | PV bus = 2                                                          | 
+-----------+---------------------------------------------------------------------+
|           | reference bus = 3                                                   | 
+-----------+---------------------------------------------------------------------+
|           | isolated bus = 4 [1]_                                               | 
+-----------+---------------------------------------------------------------------+
| zone^     | loss zone (positive integer)? [2]_                                 | 
+-----------+---------------------------------------------------------------------+
| VM        | Voltage Magnitude (p.u.)                                           | 
+-----------+---------------------------------------------------------------------+
| VA        | Voltage angle                                                      | 
+-----------+---------------------------------------------------------------------+
| VNLB      | Normal minimum voltage magnitude (p.u.)                            | 
+-----------+---------------------------------------------------------------------+
| VNUB      | Normal maximum voltage magnitude (p.u.)                            | 
+-----------+---------------------------------------------------------------------+
| VELB      | Extreme minimum voltage magnitude (p.u.)   [3]_                    | 
+-----------+---------------------------------------------------------------------+
| VEUB      | Extreme minimum voltage magnitude (p.u.)                           | 
+-----------+---------------------------------------------------------------------+
.. rubric:: Notes
.. [1] An isolated bus is not modelled as electrically connected
.. [2] I'm at a loss to say what a loss zone is    
.. [3] Extreme values are used in the solver in what way?  

demand
^^^^^^^^^^^^^^^^^^^^^
+--------------------+--------------------------------------------------------------+
| name               | Demand name (string)                                         | 
+--------------------+--------------------------------------------------------------+
| busname            | Bus name [1]                                                 | 
+--------------------+--------------------------------------------------------------+
| real               | real power demand (MW)                                       | 
+--------------------+--------------------------------------------------------------+
| reactive           | reactive power demand (MVAr)                                 | 
+--------------------+--------------------------------------------------------------+
| stat               | Status (1- connected, 2-disconnected)                        |
+--------------------+--------------------------------------------------------------+
| VOLL               | Value of Lost Load (£/MW)                                    | 
+--------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a bus name from the bus sheet

branch
^^^^^^^^^^^^^^^^^^^^^
+--------------------+--------------------------------------------------------------+
| name               | branch name (string)                                         | 
+--------------------+--------------------------------------------------------------+
| from_busname       | from bus name [1]                                            |
+--------------------+--------------------------------------------------------------+
| to_busname         | to bus name [1]                                              | 
+--------------------+--------------------------------------------------------------+
| stat               | Status (1-connected, 2-disconnected)                         | 
+--------------------+--------------------------------------------------------------+
| r                  | resistance (p.u.)                                            | 
+--------------------+--------------------------------------------------------------+
| x                  | reactance (p.u.)                                             | 
+--------------------+--------------------------------------------------------------+
| b                  | total line charging susceptance (p.u.)                       | 
+--------------------+--------------------------------------------------------------+
| ShortTermRating    | MVA rating (short term rating), set to 0 for unlimited [2]   |
+--------------------+--------------------------------------------------------------+
| ContinuousRating   | MVA rating (continuous rating), set to 0 for unlimited       | 
+--------------------+--------------------------------------------------------------+
| angLB              | minimum angle difference (degrees) [3]                       | 
+--------------------+--------------------------------------------------------------+
| angUB              | maximum angle difference (degrees) [3]                       | 
+--------------------+--------------------------------------------------------------+
| contingency^       | 1-include in SCOPF contingencies, 2- don't include           | 
+--------------------+--------------------------------------------------------------+
| failure_rate^      | failure rate over user specified time horizon                | 
+--------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a bus name from the bus sheet
.. [2] The short term rating is used in post fault calculation in SCOPF
.. [3] The voltage angle difference is taken to be unbounded below if angLB < -360 and unbounded above if angUB > 360. If both parameters are zero, it is unconstrained.

transformer
^^^^^^^^^^^^^^^^^^^^^
+--------------------+--------------------------------------------------------------+
| name               | transformer name (string)                                    | 
+--------------------+--------------------------------------------------------------+
| from_busname       | from bus name [1]                                            | 
+--------------------+--------------------------------------------------------------+
| to_busname         | to bus name [1]                                              | 
+--------------------+--------------------------------------------------------------+
| stat               | Status (1-connected, 2-disconnected)                         |
+--------------------+--------------------------------------------------------------+
| type^              | 1- 2-winding transformer with fixed tap ratios               |
|                    | 2- tap-changing transformer                                  |
+--------------------+--------------------------------------------------------------+
| r                  | resistance (p.u.)                                            | 
+--------------------+--------------------------------------------------------------+
| x                  | reactance (p.u.)                                             | 
+--------------------+--------------------------------------------------------------+
| ShortTermRating    | MVA rating (short term rating), set to 0 for unlimited [2]   |
+--------------------+--------------------------------------------------------------+
| ContinuousRating   | MVA rating (continuous rating), set to 0 for unlimited       | 
+--------------------+--------------------------------------------------------------+
| angLB              | minimum angle difference (degrees) [3]                       | 
+--------------------+--------------------------------------------------------------+
| angUB              | minimum angle difference (degrees) [3]                       | 
+--------------------+--------------------------------------------------------------+
| PhaseShift^        | transformer phase shift angle (degrees), positive => delay   | 
+--------------------+--------------------------------------------------------------+
| TapRatio^          | Transformer turns ratio                                      | 
+--------------------+--------------------------------------------------------------+
| TapLB              | Transformer minimum turns ratio                              | 
+--------------------+--------------------------------------------------------------+
| TapUB              | Transformer maximum turns ratio                              | 
+--------------------+--------------------------------------------------------------+
| contingency^       | 1-include in SCOPF contingencies, 2- don't include           | 
+--------------------+--------------------------------------------------------------+
| failure_rate^      | failure rate over user specified time horizon                | 
+--------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a bus name from the bus sheet
.. [2] The short term rating is used in post fault calculation in SCOPF
.. [3] The voltage angle difference is taken to be unbounded below if angLB < -360 and unbounded above if angUB > 360. If both parameters are zero, it is unconstrained.

wind
^^^^^^^^^^^^^^^^^^^^^
The wind sheet is included to separate variable generation from fixed capacity 
+--------------------+--------------------------------------------------------------+
| busname            | Bus name [1]                                                 |
+--------------------+--------------------------------------------------------------+
| name               | Wind farm name                                               | 
+--------------------+--------------------------------------------------------------+
| stat               | Status (1-connected, 2-disconnected)                         | 
+--------------------+--------------------------------------------------------------+
| PG                 | Real power output (MW)                                       | 
+--------------------+--------------------------------------------------------------+
| QG                 | Reactive power output (MVAr)                                 | 
+--------------------+--------------------------------------------------------------+
| PGLB               | Minimum real power output (MW)                               | 
+--------------------+--------------------------------------------------------------+
| PGUB               | Maximum power output (MW)                                    |
+--------------------+--------------------------------------------------------------+
| QGLB               | Minimum Reactive power output (MW)                           | 
+--------------------+--------------------------------------------------------------+
| QGUB               | Maximum reactive power output (MVAr)                         | 
+--------------------+--------------------------------------------------------------+
| VS                 | Voltage magnitude setpoint (p.u.)                            | 
+--------------------+--------------------------------------------------------------+
| contingency^       | 1-include in SCOPF contingencies, 2- don't include           | 
+--------------------+--------------------------------------------------------------+
| failure_rate^      | failure rate over user specified time horizon                | 
+--------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a bus name from the bus sheet

shunt
^^^^^^^^^^^^^^^^^^^^^

+--------------------+--------------------------------------------------------------+
| busname            | Bus name [1]                                                 | 
+--------------------+--------------------------------------------------------------+
| name               | Shunt name (string)                                          | 
+--------------------+--------------------------------------------------------------+
| GL                 | Shunt conductance (MW demanded at V = 1.0 p.u.)              | 
+--------------------+--------------------------------------------------------------+
| BL                 | Shunt susceptance (MVAr injected at V = 1.0 p.u.)            | 
+--------------------+--------------------------------------------------------------+
| stat               | Status (1- connected, 2-disconnected)                        |
+--------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a bus name from the bus sheet

zone
^^^^^^^^^^^^^^^^^^^^^

+---------------------+--------------------------------------------------------------+
| interconnection_ID  | ID for interconnector between zones                          | 
+---------------------+--------------------------------------------------------------+
| from_zone           | from zone [1]                                                | 
+---------------------+--------------------------------------------------------------+
| to_zone             | to zone [1]                                                  | 
+---------------------+--------------------------------------------------------------+
| TransferCapacity(MW)| Transfer capacity betwen 'from_zone' and 'to_zone'           | 
+---------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a zone name from the bus sheet

generators
^^^^^^^^^^^^^^^^^^^^^
+--------------------+--------------------------------------------------------------+
| busname            | Bus name [1]                                                 | 
+--------------------+--------------------------------------------------------------+
| name               | Generator name (string)                                      | 
+--------------------+--------------------------------------------------------------+
| stat               | Status (1-connected, 2-disconnected)                         | 
+--------------------+--------------------------------------------------------------+
| PG                 | Real power output (MW)                                       | 
+--------------------+--------------------------------------------------------------+
| QG                 | Reactive power output (MVAr)                                 | 
+--------------------+--------------------------------------------------------------+
| PGLB               | Minimum real power output (MW)                               | 
+--------------------+--------------------------------------------------------------+
| PGUB               | Maximum power output (MW)                                    |
+--------------------+--------------------------------------------------------------+
| QGLB               | Minimum Reactive power output (MW)                           | 
+--------------------+--------------------------------------------------------------+
| QGUB               | Maximum reactive power output (MVAr)                         | 
+--------------------+--------------------------------------------------------------+
| VS                 | Voltage magnitude setpoint (p.u.)                            | 
+--------------------+--------------------------------------------------------------+
| RampDown (MW/hr)^  | Ramp down rate (MW/hr) [2]                                   | 
+--------------------+--------------------------------------------------------------+
| RampUp (MW/hr)^    | Ramp up rate (MW/hr) [2]                                     | 
+--------------------+--------------------------------------------------------------+
| MinDownTime(hr)^   | Minimum down time (hr) [3]                                   | 
+--------------------+--------------------------------------------------------------+
| MinupTime(hr)^     | Minimum up time (hr) [3]                                     | 
+--------------------+--------------------------------------------------------------+
| FuelType^          | Coal, Nuke - nuclear, CCGT, OCGT, Unknown                    | 
+--------------------+--------------------------------------------------------------+
| contingency        | 1-include in SCOPF contingencies, 2- don't include           | 
+--------------------+--------------------------------------------------------------+
| startup^           | Start up cost (£) [3]                                        | 
+--------------------+--------------------------------------------------------------+
| shutdown^          | Shut down cost	(£) [3]                                       | 
+--------------------+--------------------------------------------------------------+
| costc2             | Quadratic cost coefficient                                   | 
+--------------------+--------------------------------------------------------------+
| costc1             | Linear cost coefficient                                      | 
+--------------------+--------------------------------------------------------------+
| costc0             | Constant cost coefficient                                    |
+--------------------+--------------------------------------------------------------+
| bid^               | Bid in balancing mechanism to reduce generation [4]          | 
+--------------------+--------------------------------------------------------------+
| offer^             | Offer in balancing mechanism to increase generation [4]      |
+--------------------+--------------------------------------------------------------+
.. rubric:: Notes
.. [1] Must match a bus name from the bus sheet
.. [2] Ramp rates required for security constrainted OPF or unit commitment problems
.. [3] Minimum up/down times, startup and shutdown costs are required in the unit commitment models
.. [4] These parameters are part of the balancing market extension model described in XXX


