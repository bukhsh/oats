import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import scopf,dcopf,acopf,aclf,uc,dclf

dcopf(neos=False,solver='cplex',tc= 'OATS-testcases/case24_ieee_rts.xlsx')


