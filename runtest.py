# import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import dcopf

dcopf(neos=False,solver='ipopt',tc='OATS-testcases/GB_ReducedNetwork.xlsx')

