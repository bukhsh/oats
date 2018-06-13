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

from runcase import runcase
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='oatslog.log',
                    filemode='w')
logging.info("OATS log file")

#----------------------------------------------------------------------
def main():
    logging.info("Program started")
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
    # ==log==
    logging.info("Solver selected: "+solver)
    logging.info("Testcase selected: "+testcase)
    logging.info("Model selected: "+model)
    runcase(testcase,model,solver,opt)
    logging.info("Done!")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.error("Fatal error in main loop", exc_info=True)
        raise
