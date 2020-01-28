

Security constrained optimal power flow problem
================================================

Secure operation of a power system requires that no breach of operating standards
take place following a credible contingency. This is achieved by solving a
security-constrained optimal power flow. A DC version of SCOPF is implemented in
OATS. A set of credible contingencies can be specified in the test case. The
credible contingencies in OATS are outages of single circuits, transformers or
generating units.


Mathematical formulation
------------------------

The mathematical formulation of the SCOPF implemented in OATS takes the following form:

.. math::
   \min_{u_c,x_c: \forall c \in \{0\} \cup C} ~~f(u_0,x_0)~~~~~~~~~~~~~~~~~~\\
   \text{subject to}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\\
   h_c(u_c,x_c)=0,~~~~~~~~~~~~ \forall c \in \{0\} \cup C\\
   g_c(u_c,x_c)\le 0,~~~~~~~~~~~~ \forall c \in \{0\} \cup C\\
   |u_c-u_0|\le R_c, ~~~~~~~~~~~~~~\forall c \in C~~~~~~~~~~

where :math:`C` is the set of contingencies. OATS allow a user to build the set of
contingencies by selecting generators, branches and transformers to be included in the
contingency list. The user is referred to the data format section for information
regarding selecting a contingency. The equality constraints (:math:`h_c`) and
inequality constraints (:math:`g_C`) are imposed on the set of contingencies :math:`C` and
on the pre-fault operating state :math:`\{0\}`. The last constraint is a coupling constraint
that couples pre-fault and post-fault state of operation.


SCOPF problem with pre-fault AC and post-fault DC
-------------------------------------------------
The traditional implementations of the SCOPF problem model the pre-fault and post-fault operation
of a system using DC-model of power flow. OATS allow a user to model the pre-fault operation of a system
using AC power flow (hence giving information regarding voltage and reactive power) and post-fault
operation using DC equations. The mathematical formulation of such problem is given as follows.

.. math::
   \min_{u_c,x_c: \forall c \in \{0\} \cup C} ~~f(u_0,x_0)~~~~~~~~~~~~~~~~~~\\
   \text{subject to}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\\
   h^{\text{AC}}_0(u_c,x_c)=0,~~~~~~~~~~~~ c \in \{0\}\\
   g^{\text{AC}}_0(u_c,x_c)\le 0,~~~~~~~~~~~~ c \in \{0\}\\
   h^{\text{DC}}_c(u_c,x_c)=0,~~~~~~~~~~~~ \forall c \in C\\
   g^{\text{DC}}_c(u_c,x_c)\le 0,~~~~~~~~~~~~ \forall c \in C\\
   |u_c-u_0|\le R_c, ~~~~~~~~~~~\forall c \in C


As noted above, the AC power flow equations are only used to model the pre-fault operation of a system.
The post-fault operation of a system is modelled using DC power flow equations.

Solving SCOPF problems in OATS
------------------------------

.. automodule:: oats
    :members: scopf
