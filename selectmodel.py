#==================================================================
# select_model.py
# This Python script loads the model from the model library
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================

import imp #for importing models
def selectmodel(prob):
    mod = imp.load_source(prob, 'models/'+prob+'.py')
    return mod.model
