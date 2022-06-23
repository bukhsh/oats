import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import scopf,dcopf,acopf,aclf,uc

uc(neos=False,solver='cplex',tc= '/Users/waqquasbukhsh/Downloads/ntdc_2021_oats_v2.xlsx')

