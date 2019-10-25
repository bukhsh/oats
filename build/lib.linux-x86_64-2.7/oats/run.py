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
import logging
import os
from oats.runcase import runcase

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='oatslog.log',
                    filemode='w')
logging.info("OATS log file")
logging.info("Program started")
oats_dir = os.path.dirname(os.path.realpath(__file__))
default_testcase = oats_dir+'/testcases/case24_ieee_rts.xlsx'

#----------------------------------------------------------------------
# DC Load flow
def dclf(tc='default',solver='ipopt',neos=True,out=0):
    """
    Solves DC load flow problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #options
    opt=({'neos':neos,\
    'solver':solver,'out':out})
    testcase = tc
    model ='DCLF'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")
# AC Load flow
def aclf(tc='default',solver='ipopt',neos=True,out=0):
    """
    Solves AC load flow problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """
    if tc == 'default':
        tc = default_testcase
    opt=({'neos':neos,\
    'solver':solver,'out':out})
    testcase = tc
    model ='ACLF'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")
# DC optimal power flow problem
def dcopf(tc='default',solver='ipopt',neos=True,out=0):
    """
    Solves DC optimal power flow problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #options
    opt=({'neos':neos,\
    'solver':solver,'out':out})
    testcase = tc
    model ='DCOPF'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")

# AC optimal power flow problem
def acopf(tc='default',solver='ipopt',neos=True,out=0):
    """
    Solves AC optimal power flow problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #options
    opt=({'neos':neos,\
    'solver':solver,'out':out})
    testcase = tc
    model ='ACOPF'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")

# security constrained optimal power flow problem
def scopf(tc='default',solver='ipopt',neos=True,out=0):
    """
    Solves security constrained optimal power flow problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #options
    opt=({'neos':neos,\
    'solver':solver,'out':out})
    testcase = tc
    model ='SCOPF'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")

# unit commitment problem
def uc(tc='default',solver='cplex',neos=True,out=0):
    """
    Solves unit commitment problem

    ARGUMENTS:
        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #options
    opt=({'neos':neos,\
    'solver':solver,'out':out})
    testcase = tc
    model ='UC'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")


# user defined model
def model(model,tc='default',solver='cplex',neos=True,out=0):
    """
    Solves a user defined model

    ARGUMENTS:
        **model** (*.py file)  - A model file that describes the optimisation problem using PYOMO modelling language.

        **tc** (*.xlsx file)  - OATS test case. See OATS data format for details

        **solver** (str)  - name of a solver. Defualt is 'ipopt'

        **neos** (bool) - If True, the problem is solved using NEOS otherwise using a localy install solver.

        **out** (bool) - If True, the output is displayed on screen.
    """

    if tc == 'default':
        tc = default_testcase
    #options
    opt=({'neos':neos,\
    'solver':solver,'out':out,'user_def_model':True})
    testcase = tc
    model =model
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")
