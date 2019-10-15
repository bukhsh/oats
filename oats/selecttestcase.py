#==================================================================
# select_testcase.py
# This Python script loads the test case file from the library
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================

import pandas as pd

def selecttestcase(test):
    xl = pd.ExcelFile(test)

    df_bus         = xl.parse("bus")
    df_demand      = xl.parse("demand")
    df_branch      = xl.parse("branch")
    df_generators  = xl.parse("generator")
    df_shunt       = xl.parse("shunt")
    df_transformer = xl.parse("transformer")
    df_wind        = xl.parse("wind")
    df_baseMVA     = xl.parse("baseMVA")
    df_zone        = xl.parse("zone")
    df_zonalNTC    = xl.parse("zonalNTC")
    df_ts          = xl.parse("timeseries",header=[0,1])


    data = {
    "bus": df_bus,
    "demand": df_demand,
    "branch": df_branch,
    "generator": df_generators,
    "shunt": df_shunt,
    "transformer": df_transformer,
    "wind": df_wind,
    "baseMVA": df_baseMVA,
    "zone": df_zone,
    "timeseries": df_ts,
    "zone":df_zone,
    "zonalNTC":df_zonalNTC
    }
    try:
        df_storage   = xl.parse("storage")
        data['storage'] = df_storage
    except:
        print ('Storage not defined')

    return data
