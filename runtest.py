# import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import dcopf

dcopf(neos=False,solver='cplex',tc='OATS-testcases/GB_ReducedNetwork.xlsx')
# dcopf(neos=False,solver='cplex',tc='/home/waqquas/Dropbox/NIA-GB-Data/TestCases/GBNetwork_Revised_Reduced.xlsx')