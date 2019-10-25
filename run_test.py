# import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import uc

# uc(neos=False,solver='cplex',tc='/Users/waqquasbukhsh/testing/caseGB.xlsx')
uc(neos=False,solver='cplex',tc='/home/waqquas/Dropbox/caseGB.xlsx')
