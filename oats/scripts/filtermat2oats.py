#==================================================================
#A Python script that reads Matpower test case and converts into OATS test case
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2017 by W. Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

import pandas as pd

buscol    = ['name','baseKV','type','zone','VM','VA','VNLB','VNUB','VELB','VEUB']
demcol    = ['name','busname','real','reactive','stat','VOLL']
brncol    = ['name','from_busname','to_busname','stat','r','x','b','ShortTermRating','ContinousRating','angLB','angUB','contingency','probability']
trncol    = ['name','from_busname','to_busname','stat','type','r','x','ShortTermRating','ContinousRating','angLB','angUB','PhaseShift','TapRatio','TapLB','TapUB','contingency','probability']
wndcol    = ['busname','name','stat','PG','QG','PGLB','PGUB','QGLB','QGUB','VS','contingency','probability']
shtcol    = ['busname','name','GL','BL','stat']
zneNTCcol = ['interconnection_ID', 'from_zone', 'to_zone', 'TransferCapacityTo(MW)', 'TransferCapacityFr(MW)']
znecol    = ['zone', 'reserve(MW)']
gencol    = ['busname','name','stat','type','PG','QG','PGLB','PGUB','QGLB','QGUB','VS','RampDown(MW/hr)','RampUp(MW/hr)','MinDownTime(hr)','MinUpTime(hr)','FuelType','contingency','probability','startup','shutdown','costc2','costc1','costc0']


dfbus    = pd.DataFrame(columns=buscol)
dfdem    = pd.DataFrame(columns=demcol)
dfbrn    = pd.DataFrame(columns=brncol)
dftrn    = pd.DataFrame(columns=trncol)
dfwnd    = pd.DataFrame(columns=wndcol)
dfsht    = pd.DataFrame(columns=shtcol)
dfzne    = pd.DataFrame(columns=znecol)
dfzneNTC = pd.DataFrame(columns=znecol)
dfgen    = pd.DataFrame(columns=gencol)
dfts     = pd.DataFrame()
baseMVA  = pd.DataFrame(columns={'baseMVA'})
baseMVA.loc[0]=pd.Series({'baseMVA':100})

filepath = 'matpowercases/case300.m'

#value of lost load
VOLL = str(100000)

flag = 0
ind = 0
ind_sht = 0
with open(filepath,"r") as myfile:
    #read mpc.bus data
    for line in myfile:
        if 'mpc.bus' in line:
            flag = 1
            continue
        if flag==1 and '];' in line:
            break
        if flag == 1:
            temp = line[:-2].split('\t')[1:]
            dfbus.loc[ind] = pd.Series({'name':temp[0],'baseKV':temp[9],'type':temp[1],\
            'zone':temp[10],'VM':temp[7],'VA':temp[8],'VNLB':temp[12],'VNUB':temp[11],'VELB':temp[12],'VEUB':temp[11]})
            dfdem.loc[ind] = pd.Series({'name':'D'+temp[0],'busname':temp[0],'real':temp[2],'reactive':temp[3],'stat':str(1),'VOLL':VOLL})
            if float(temp[4])!=0 or float(temp[5])!=0:
                dfsht.loc[ind_sht] = pd.Series({'busname':temp[0],'name':'S'+temp[0],'GL':temp[4],'BL':temp[5],'stat':str(1)})
                ind_sht += 1
            ind += 1
    flag = 0
    ind_br  = 0
    ind_tr  = 0
    #read mpc.branch data
with open(filepath,"r") as myfile:
    for line in myfile:
        if 'mpc.branch' in line:
            flag = 1
            continue
        if flag==1 and '];' in line:
            break
        if flag == 1:
            temp = line[:-2].split('\t')[1:]
            if float(temp[8])==0: #transformer or not
                if float(temp[5])==0: #in matpower '0' means no line capacity constraint
                    dfbrn.loc[ind_br] = pd.Series({'name':'L'+str(ind_br+1)+'-'+temp[0]+temp[1],\
                    'from_busname':temp[0],'to_busname':temp[1],'stat':temp[10],\
                    'r':temp[2],'x':temp[3],'b':temp[4],'ShortTermRating':str(9999),\
                    'ContinousRating':str(9999),'angLB':temp[11],'angUB':temp[12],'contingency':str(1),'probability':str(0.0001)})
                    ind_br += 1
                else:
                    dfbrn.loc[ind_br] = pd.Series({'name':'L'+str(ind_br+1)+'-'+temp[0]+temp[1],\
                    'from_busname':temp[0],'to_busname':temp[1],'stat':temp[10],\
                    'r':temp[2],'x':temp[3],'b':temp[4],'ShortTermRating':temp[7],\
                    'ContinousRating':temp[5],'angLB':temp[11],'angUB':temp[12],'contingency':str(1),'probability':str(0.0001)})
                    ind_br += 1
            else:
                if float(temp[5])==0: #in matpower '0' means no line capacity constraint
                    dftrn.loc[ind_tr] = pd.Series({'name':'T'+str(ind_tr+1)+'-'+temp[0]+temp[1],\
                    'from_busname':temp[0],'to_busname':temp[1],'stat':temp[10],'type':str(1),\
                    'r':temp[2],'x':temp[3],'ShortTermRating':str(9999),'ContinousRating':str(9999),\
                    'angLB':temp[11],'angUB':temp[12],'PhaseShift':temp[9],'TapRatio':temp[8],\
                    'TapLB':str(float(temp[8])*(1-0.05)),'TapUB':str(float(temp[8])*(1+0.05)),\
                    'contingency':str(1),'probability':str(0.0001)})
                    ind_tr += 1
                else:
                    dftrn.loc[ind_tr] = pd.Series({'name':'T'+str(ind_tr+1)+'-'+temp[0]+temp[1],\
                    'from_busname':temp[0],'to_busname':temp[1],'stat':temp[10],\
                    'r':temp[2],'x':temp[3],'ShortTermRating':temp[7],'ContinousRating':temp[5],\
                    'angLB':temp[11],'angUB':temp[12],'PhaseShift':temp[9],'TapRatio':temp[8],\
                    'TapLB':str(float(temp[8])*(1-0.05)),'TapUB':str(float(temp[8])*(1+0.05)),\
                    'contingency':str(1),'probability':str(0.0001)})
                    ind_tr += 1
    #read mpc.gencost data
    flag    = 0
    costdat = pd.DataFrame(columns={'gen', 'start', 'shut' ,'c2', 'c1', 'c0'})
    ind_gen = 0
with open(filepath,"r") as myfile:
    for line in myfile:
        if 'mpc.gencost' in line:
            flag = 1
            continue
        if flag==1 and '];' in line:
            break
        if flag == 1:
            temp = line[:-2].split('\t')[1:]
            costdat.loc[ind_gen] = pd.Series({'gen':ind_gen, 'start':temp[1], 'shut':temp[2] ,'c2':temp[4], 'c1':temp[5], 'c0':temp[6].strip(';')})
            ind_gen += 1
    #read mpc.generator
    flag = 0
    ind  = 0
with open(filepath,"r") as myfile:
    for line in myfile:
        if 'mpc.gen' in line:
            flag = 1
            continue
        if flag==1 and '];' in line:
            break
        if flag == 1:
            temp = line[:-2].split('\t')[1:]
            dfgen.loc[ind] = pd.Series({'busname':temp[0],'name':'G'+str(ind+1),'stat':temp[7],'type':str(1),'PG':temp[1],\
            'QG':temp[2],'PGLB':temp[9],'PGUB':temp[8],'QGLB':temp[4],'QGUB':temp[3],\
            'VS':temp[5],'RampDown(MW/hr)':temp[18],'RampUp(MW/hr)':temp[18],'MinDownTime(hr)':str(1),\
            'MinUpTime(hr)':str(1),'FuelType':'NA','contingency':str(0),'probability':str(0.0001),'startup':costdat['start'][costdat['gen']==ind].item(),\
            'shutdown':costdat['shut'][costdat['gen']==ind].item(),'costc2':costdat['c2'][costdat['gen']==ind].item(),\
            'costc1':costdat['c1'][costdat['gen']==ind].item(),'costc0':costdat['c0'][costdat['gen']==ind].item()})
            ind += 1


#----------------------------------------------------------
#===write oats test case===
#
writer = pd.ExcelWriter('oats/'+filepath.split('/')[1].split('.')[0]+'.xlsx', engine ='xlsxwriter')
dfbus[buscol].to_excel(writer, sheet_name = 'bus',index=False , header=True)
dfdem[demcol].to_excel(writer, sheet_name = 'demand',index=False, header=True)
dfbrn[brncol].to_excel(writer, sheet_name = 'branch',index=False, header=True)
dftrn[trncol].to_excel(writer, sheet_name = 'transformer',index=False, header=True)
dfwnd[wndcol].to_excel(writer, sheet_name = 'wind',index=False, header=True)
dfsht[shtcol].to_excel(writer, sheet_name = 'shunt',index=False, header=True)
dfzne[znecol].to_excel(writer, sheet_name = 'zone',index=False, header=True)
dfzneNTC[znecol].to_excel(writer, sheet_name = 'zonalNTC',index=False, header=True)
dfgen[gencol].to_excel(writer, sheet_name = 'generator',index=False, header=True)
dfts.to_excel(writer, sheet_name = 'timeseries',index=False, header=True)
baseMVA.to_excel(writer, sheet_name = 'baseMVA',index=False, header=True)
