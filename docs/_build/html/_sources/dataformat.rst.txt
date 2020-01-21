Data format
================================
OATS uses a spreadsheet format for specifying network, demand and generation data.


OATS also has a test case library where a number of standard IEEE and some real-world test cases are provided. The test case library is available on the `OATS GitHub page <https://github.com/bukhsh/oats>`__.


OATS data template
--------------------
A blank template of OATS data format can be downloaded from this `link <https://github.com/bukhsh/oats/blob/master/OATS-testcases/tempelate.xlsx>`__.


.. image:: /pics/testcase.png
		:width: 35em
		:align: center

Description of sheets in the OATS data format
---------------------------------------------

Following tables provide information about each sheet of the OATS dataformat.

The parameters required to describe a network in OATS are outlined below. Optional parameters are highlighted by (^);

bus
~~~~
+-----------+-------------------------------------------------------+
| name      | bus name. string (can contain letters and/or numbers) |
+-----------+-------------------------------------------------------+
| baseKV    | base voltage (kV)                                     |
+-----------+-------------------------------------------------------+
| zone^     | zone (positive integer) [#bus1]_                      |
+-----------+-------------------------------------------------------+
| VM        | Voltage Magnitude (p.u.)                              |
+-----------+-------------------------------------------------------+
| VA        | Voltage angle                                         |
+-----------+-------------------------------------------------------+
| VNLB      | Normal minimum voltage magnitude (p.u.)               |
+-----------+-------------------------------------------------------+
| VNUB      | Normal maximum voltage magnitude (p.u.)               |
+-----------+-------------------------------------------------------+
| VELB      | Extreme minimum voltage magnitude (p.u.)   [#bus2]_   |
+-----------+-------------------------------------------------------+
| VEUB      | Extreme minimum voltage magnitude (p.u.)              |
+-----------+-------------------------------------------------------+

.. rubric:: Notes
.. [#bus1] Zone is used in unit commitment problem to define inter zonal transfer constraints
.. [#bus2] Extreme values columns are provided as an option for security constrained optimal power flow when relaxed post-fault voltage bounds are desired

demand
~~~~~~~
+--------------------+---------------------------------------+
| name               | Demand name (string)                  |
+--------------------+---------------------------------------+
| busname            | Bus name [#dem1]_                     |
+--------------------+---------------------------------------+
| real               | real power demand (MW)                |
+--------------------+---------------------------------------+
| reactive           | reactive power demand (MVAr)          |
+--------------------+---------------------------------------+
| stat               | Status (1- connected, 2-disconnected) |
+--------------------+---------------------------------------+
| VOLL               | Value of Lost Load (£/MW)             |
+--------------------+---------------------------------------+

.. rubric:: Notes
.. [#dem1] Must match a bus name from the bus sheet

branch
~~~~~~~~
+--------------------+-------------------------------------------------------------------+
| name               | branch name (string)                                              |
+--------------------+-------------------------------------------------------------------+
| from_busname       | from bus name [#branch1]_                                         |
+--------------------+-------------------------------------------------------------------+
| to_busname         | to bus name [#branch1]_                                           |
+--------------------+-------------------------------------------------------------------+
| stat               | Status (1-connected, 0-disconnected)                              |
+--------------------+-------------------------------------------------------------------+
| r                  | resistance (p.u.)                                                 |
+--------------------+-------------------------------------------------------------------+
| x                  | reactance (p.u.)                                                  |
+--------------------+-------------------------------------------------------------------+
| b                  | total line charging susceptance (p.u.)                            |
+--------------------+-------------------------------------------------------------------+
| ShortTermRating    | MVA rating (short term rating), set to 0 for unlimited [#branch2]_|
+--------------------+-------------------------------------------------------------------+
| ContinuousRating   | MVA rating (continuous rating), set to 0 for unlimited            |
+--------------------+-------------------------------------------------------------------+
| angLB              | minimum angle difference (degrees) [#branch3]_                    |
+--------------------+-------------------------------------------------------------------+
| angUB              | maximum angle difference (degrees) [#branch3]_                    |
+--------------------+-------------------------------------------------------------------+
| contingency^       | 1-include in SCOPF contingencies, 0- don't include                |
+--------------------+-------------------------------------------------------------------+
| failure_rate^      | failure rate over user specified time horizon                     |
+--------------------+-------------------------------------------------------------------+

.. rubric:: Notes
.. [#branch1] Must match a bus name from the bus sheet
.. [#branch2] The short term rating is used in post fault calculation in SCOPF
.. [#branch3] The voltage angle difference is taken to be unbounded below if angLB < -360 and unbounded above if angUB > 360. If both parameters are zero, it is unconstrained.

transformer
~~~~~~~~~~~~
+--------------------+-------------------------------------------------------------------+
| name               | transformer name (string)                                         |
+--------------------+-------------------------------------------------------------------+
| from_busname       | from bus name [#tranf1]_                                          |
+--------------------+-------------------------------------------------------------------+
| to_busname         | to bus name [#tranf1]_                                            |
+--------------------+-------------------------------------------------------------------+
| stat               | Status (1-connected, 0-disconnected)                              |
+--------------------+-------------------------------------------------------------------+
| type^              | 1- 2-winding transformer with fixed tap ratios                    |
|                    | 2- tap-changing transformer                                       |
+--------------------+-------------------------------------------------------------------+
| r                  | resistance (p.u.)                                                 |
+--------------------+-------------------------------------------------------------------+
| x                  | reactance (p.u.)                                                  |
+--------------------+-------------------------------------------------------------------+
| ShortTermRating    | MVA rating (short term rating), set to 0 for unlimited [#tranf2]_ |
+--------------------+-------------------------------------------------------------------+
| ContinuousRating   | MVA rating (continuous rating), set to 0 for unlimited            |
+--------------------+-------------------------------------------------------------------+
| angLB              | minimum angle difference (degrees) [#tranf3]_                     |
+--------------------+-------------------------------------------------------------------+
| angUB              | minimum angle difference (degrees) [#tranf3]_                     |
+--------------------+-------------------------------------------------------------------+
| PhaseShift^        | transformer phase shift angle (degrees), positive => delay        |
+--------------------+-------------------------------------------------------------------+
| TapRatio^          | Transformer turns ratio                                           |
+--------------------+-------------------------------------------------------------------+
| TapLB              | Transformer minimum turns ratio                                   |
+--------------------+-------------------------------------------------------------------+
| TapUB              | Transformer maximum turns ratio                                   |
+--------------------+-------------------------------------------------------------------+
| contingency^       | 1-include in SCOPF contingencies, 2- don't include                |
+--------------------+-------------------------------------------------------------------+
| failure_rate^      | failure rate over user specified time horizon                     |
+--------------------+-------------------------------------------------------------------+

.. rubric:: Notes
.. [#tranf1] Must match a bus name from the bus sheet
.. [#tranf2] The short term rating is used in post fault calculation in SCOPF
.. [#tranf3] The voltage angle difference is taken to be unbounded below if angLB < -360 and unbounded above if angUB > 360. If both parameters are zero, it is unconstrained.

wind
~~~~~~~~
The wind sheet is included to separate variable generation from fixed capacity

+--------------------+----------------------------------------------------+
| busname            | Bus name [#wind1]_                                 |
+--------------------+----------------------------------------------------+
| name               | Wind farm name                                     |
+--------------------+----------------------------------------------------+
| stat               | Status (1-connected, 0-disconnected)               |
+--------------------+----------------------------------------------------+
| PG                 | Real power output (MW)                             |
+--------------------+----------------------------------------------------+
| QG                 | Reactive power output (MVAr)                       |
+--------------------+----------------------------------------------------+
| PGLB               | Minimum real power output (MW)                     |
+--------------------+----------------------------------------------------+
| PGUB               | Maximum power output (MW)                          |
+--------------------+----------------------------------------------------+
| QGLB               | Minimum Reactive power output (MW)                 |
+--------------------+----------------------------------------------------+
| QGUB               | Maximum reactive power output (MVAr)               |
+--------------------+----------------------------------------------------+
| VS                 | Voltage magnitude setpoint (p.u.)                  |
+--------------------+----------------------------------------------------+
| contingency^       | 1-include in SCOPF contingencies, 0- don't include |
+--------------------+----------------------------------------------------+
| failure_rate^      | failure rate over user specified time horizon      |
+--------------------+----------------------------------------------------+

.. rubric:: Notes
.. [#wind1] Must match a bus name from the bus sheet

shunt
~~~~~~~~

+--------------------+--------------------------------------------------+
| busname            | Bus name [#shunt1]_                              |
+--------------------+--------------------------------------------------+
| name               | Shunt name (string)                              |
+--------------------+--------------------------------------------------+
| GL                 | Shunt conductance (MW demanded at V = 1.0 p.u.)  |
+--------------------+--------------------------------------------------+
| BL                 | Shunt susceptance (MVAr injected at V = 1.0 p.u.)|
+--------------------+--------------------------------------------------+
| stat               | Status (1- connected, 0-disconnected)            |
+--------------------+--------------------------------------------------+

.. rubric:: Notes
.. [#shunt1] Must match a bus name from the bus sheet

zone
~~~~~~~~

+---------------------+----------------------------------------------------+
| interconnection_ID  | ID for interconnector between zones                |
+---------------------+----------------------------------------------------+
| from_zone           | from zone [#zone1]_                                |
+---------------------+----------------------------------------------------+
| to_zone             | to zone [#zone1]_                                  |
+---------------------+----------------------------------------------------+
| TransferCapacity(MW)| Transfer capacity between 'from_zone' and 'to_zone'|
+---------------------+----------------------------------------------------+

.. rubric:: Notes
.. [#zone1] Must match a zone name from the bus sheet


generators
~~~~~~~~~~~~
+--------------------+-------------------------------------------------------------+
| busname            | Bus name [#gen1]_                                           |
+--------------------+-------------------------------------------------------------+
| name               | Generator name (string)                                     |
+--------------------+-------------------------------------------------------------+
| stat               | Status (1-connected, 0-disconnected)                        |
+--------------------+-------------------------------------------------------------+
| PG                 | Real power output (MW)                                      |
+--------------------+-------------------------------------------------------------+
| QG                 | Reactive power output (MVAr)                                |
+--------------------+-------------------------------------------------------------+
| PGLB               | Minimum real power output (MW)                              |
+--------------------+-------------------------------------------------------------+
| PGUB               | Maximum power output (MW)                                   |
+--------------------+-------------------------------------------------------------+
| QGLB               | Minimum Reactive power output (MW)                          |
+--------------------+-------------------------------------------------------------+
| QGUB               | Maximum reactive power output (MVAr)                        |
+--------------------+-------------------------------------------------------------+
| VS                 | Voltage magnitude setpoint (p.u.)                           |
+--------------------+-------------------------------------------------------------+
| RampDown (MW/hr)^  | Ramp down rate (MW/hr) [#gen2]_                             |
+--------------------+-------------------------------------------------------------+
| RampUp (MW/hr)^    | Ramp up rate (MW/hr) [#gen2]_                               |
+--------------------+-------------------------------------------------------------+
| MinDownTime(hr)^   | Minimum down time (hr) [#gen3]_                             |
+--------------------+-------------------------------------------------------------+
| MinupTime(hr)^     | Minimum up time (hr) [#gen3]_                               |
+--------------------+-------------------------------------------------------------+
| FuelType^          | Coal, Nuke - nuclear, CCGT, OCGT, Unknown                   |
+--------------------+-------------------------------------------------------------+
| contingency        | 1-include in SCOPF contingencies, 0- don't include          |
+--------------------+-------------------------------------------------------------+
| startup^           | Start up cost (£) [#gen3]_                                  |
+--------------------+-------------------------------------------------------------+
| shutdown^          | Shut down cost	(£) [#gen3]_                               |
+--------------------+-------------------------------------------------------------+
| costc2             | Quadratic cost coefficient                                  |
+--------------------+-------------------------------------------------------------+
| costc1             | Linear cost coefficient                                     |
+--------------------+-------------------------------------------------------------+
| costc0             | Constant cost coefficient                                   |
+--------------------+-------------------------------------------------------------+
| bid^               | Bid in balancing mechanism to reduce generation [#gen4]_    |
+--------------------+-------------------------------------------------------------+
| offer^             | Offer in balancing mechanism to increase generation [#gen4]_|
+--------------------+-------------------------------------------------------------+

.. rubric:: Notes
.. [#gen1] Must match a bus name from the bus sheet
.. [#gen2] Ramp rates required for security constrained OPF or unit commitment problems
.. [#gen3] Minimum up/down times, startup and shutdown costs are required in the unit commitment models
.. [#gen4] These parameters are part of the balancing market extension model that is available as an extension to OATS



storage
~~~~~~~~
+--------------------------+-------------------------------------------------------+
| name                     | Name for the storage device                           |
+--------------------------+-------------------------------------------------------+
| zone                     | Name of the zone                                      |
+--------------------------+-------------------------------------------------------+
| stat                     | Status                                                |
+--------------------------+-------------------------------------------------------+
| Minoperatingcapacity(MW) | Min operating capacity 		                   |
+--------------------------+-------------------------------------------------------+
| capacity(MW)             | Total capacity of the storage                         |
+--------------------------+-------------------------------------------------------+
| chargingrate(MW/hr)      | charging rate                                         |
+--------------------------+-------------------------------------------------------+
| dischargingrate(MW/hr)   | discharging rate                                      |
+--------------------------+-------------------------------------------------------+
| ChargingEfficieny(%)     | charging efficiency                                   |
+--------------------------+-------------------------------------------------------+
| DischargingEfficieny(%)  | discharging efficiency                                |
+--------------------------+-------------------------------------------------------+
| InitialStoredPower(MW)   | Initial stored energy                                 |
+--------------------------+-------------------------------------------------------+
| FinalStoredPower(MW)     | Final stored energy at the end of the planning horizon|
+--------------------------+-------------------------------------------------------+



Filter Matpower2Oats
---------------------

A Python script is provided that can be used to convert Matpower test-cases into equivalent OATS test-cases. This script is available on the `OATS GitHub page <https://github.com/bukhsh/oats>`__.
