#==================================================================
# runfile.py
# This is a top level OATS script. Simulations can be ran using this script
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2017 by W. Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

from runcase import runcase #JUST TESTING

opt=({}) #pass options to the runcase script

# give complete path to the solver
solver = 'ipopt'

# =====Test cases=====
#give a path to the testcase file under the 'testcase' folder
testcase = 'case24_ieee_rts.xlsx'
#testcase = 'IrishNetwork.xlsx'
# =====Model=====
#specify a model to solve
#model ='DCLF'
#model ='ACLF'
#model ='ACOPF'
#model ='UC'
model ='DCOPF'
#model ='SCOPF'
runcase(testcase,model,solver,opt)
