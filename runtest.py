import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import scopf,dcopf,acopf

acopf(neos=False,solver='ipopt',tc='/home/waqquas/Downloads/GBNetwork_Revised_Reduced_S1.xlsx')
