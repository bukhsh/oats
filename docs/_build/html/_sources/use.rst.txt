

Getting Started with OATS
================================
OATS is a powerful power systems optimisation toolbox. OATS include implementation of the following steady-state analysis models:

* DC/AC load flow problem
* DC/AC optimal power flow problem
* Security constrained optimal power flow problem
* Unit comittment problem

.. automodule:: oats
    :members: aclf
    :exclude-members: dclf

.. autofunction:: dclf(tc=default_testcase,solver='ipopt',neos=False,out=0)
