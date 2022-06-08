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
    data_flags = {'storage':1,'ts':1,'shunt':1}
    xl = pd.ExcelFile(test)
                      # ,engine='openpyxl')

    df_bus         = xl.parse("bus")
    df_demand      = xl.parse("demand")
    df_branch      = xl.parse("branch")
    df_generators  = xl.parse("generator")
    df_transformer = xl.parse("transformer")
    df_wind        = xl.parse("wind")
    df_baseMVA     = xl.parse("baseMVA")
    df_zone        = xl.parse("zone")
    df_zonalNTC    = xl.parse("zonalNTC")

    data = {
    "bus": df_bus.dropna(how='all'),
    "demand": df_demand.dropna(how='all'),
    "branch": df_branch.dropna(how='all'),
    "generator": df_generators.dropna(how='all'),
    "transformer": df_transformer.dropna(how='all'),
    "wind": df_wind.dropna(how='all'),
    "baseMVA": df_baseMVA.dropna(how='all'),
    "zone":df_zone.dropna(how='all'),
    "zonalNTC":df_zonalNTC.dropna(how='all'),
    "flags":data_flags
    }
    try:
        df_storage   = xl.parse("storage")
        data.update( {"storage" : df_storage.dropna(how='all')} )
    except:
        print ('Storage not defined')
        data["flags"]['storage'] = 0
    try:
        df_ts    = xl.parse("timeseries",header=[0,1])
        data.update( {"timeseries" : df_ts.dropna(how='all')} )
    except:
        print('Time-series data not defined')
        data["flags"]['ts'] = 0
    try:
        df_ts    = xl.parse("shunt")
        data.update( {"shunt" : df_ts.dropna(how='all')} )
    except:
        print('Shunt data not defined')
        data["flags"]['shunt'] = 0


    return data
