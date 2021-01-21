# import oats
#
# oats.uc()
# import os
# pp_dir = os.path.dirname(os.path.realpath(__file__))
#
from oats.run import dcopf

dcopf(neos=False,solver='cplex',tc='/home/waqquas/Dropbox/NIA-GB-Data/TestCases/GB_ReducedModel_woTransformers_RI.xlsx')

