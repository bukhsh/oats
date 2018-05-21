#==================================================================
# runcase.py
# This is a second level OATS script, which is called by the runfile.
# This script receives model,testcase, options as an input to run simulation
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# April 2018
# OATS
# Copyright (c) 2017 by W. Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

#===============Import===============
from __future__ import division
from selecttestcase import selecttestcase
from selectmodel import selectmodel
import os
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition
from printdata import printdata
from printoutput import printoutput


#====================================

def runcase(testcase,mod,solver,opt=None):
    print 'Selected model is: ', mod
    print 'Selected testcase is: ', testcase
    model = selectmodel(mod) #load model
    ptc = selecttestcase(testcase) #read test case
    datfile = 'datafile.dat'

    r = printdata(datfile,ptc,mod,opt)
    r.reducedata()
    r.printheader()
    if 'UC' in mod:
        r.printUCdat()
    else:
        r.printkeysets()
        r.printnetwork()
        #'OPF' or 'LF'
        if 'OPF' in mod:
            r.printOPF()
        elif 'LF' in mod:
            r.printLF()
        #'AC' or 'DC'
        if 'AC' in mod:
            r.printAC()
        elif 'DC' in mod:
            r.printDC()

        if mod=='DCLF':
            r.printDC()
        elif mod=='ACLF':
            r.printACLF()
        elif mod=='DCOPF':
            r.printDCOPF()
        elif mod=='ACOPF':
            r.printACOPF()


    ###############Solver settings####################
    opt = SolverFactory(solver)
    #opt.options['mipgap'] = 0.1
    #################################################

    ############Solve###################
    instance = model.create_instance(datfile)
    instance.dual = Suffix(direction=Suffix.IMPORT)
    results = opt.solve(instance,tee=True)
    instance.solutions.load_from(results)
    # ##################################
    #
    #
    # ############Output###################
    o = printoutput(results, instance,mod)
    o.greet()
    o.solutionstatus()
    if 'UC' in mod:
        o.printUC()
    else:
        o.printsummary()
        o.printoutputxls()
