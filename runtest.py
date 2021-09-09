import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import scopf,dcopf,acopf,aclf

aclf(neos=False,solver='ipopt',tc='/home/waqquas/Downloads/LFAtest_pypower.xlsx')
