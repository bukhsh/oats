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
from oats.runcase import runcase

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='oatslog.log',
                    filemode='w')
logging.info("OATS log file")
logging.info("Program started")

#----------------------------------------------------------------------
def dcopf():
    #options
    opt=({'neos':False,\
    'solver':'cplex'})
    # =====Test cases=====
    #give a path to the testcase file under the 'testcase' folder
    testcase = 'case24_ieee_rts.xlsx'

    model ='DCOPF'
    # ==log==
    logging.info("Solver selected: "+opt['solver'])
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,opt)
    logging.info("Done!")
