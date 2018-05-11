#==================================================================
# printout.py
# A Python script to write output to xls and on screen
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================
from pyomo.opt import SolverStatus, TerminationCondition
from tabulate import tabulate
import pandas as pd
import math
import sys
class printoutput(object):

    def __init__(self, results, instance,mod):
        self.results   = results
        self.instance  = instance
        self.mod       = mod
    def greet(self):
        print "========================"
        print "\n Output from the OATS"
        print "========================"
    def solutionstatus(self):
        self.instance.solutions.load_from(self.results)
        print "------Solver Message------"
        print self.results.solver
        print "--------------------------"
        if (self.results.solver.status == SolverStatus.ok) \
        and (self.results.solver.termination_condition == TerminationCondition.optimal):
            print "Optimization Converged!"
        elif self.results.solver.termination_condition == TerminationCondition.infeasible:
            sys.exit("Problem is infeasible!\nOats terminated. No output is written on the results file.")
        else:
            print sys.exit("Problem is infeasible!\nOats terminated. No output is written on the results file.")
    def printsummary(self):
        print "Cost of the objective function:", str(float(self.instance.OBJ()))
        print "***********"
        print "\n Summary"
        print "***********"
        tab_summary = []
        tab_summary.append(['Conventional generation (MW)','Wind generation (MW)', 'Demand (MW)'])
        tab_summary.append([sum(self.instance.pG[g].value for g in self.instance.G)*self.instance.baseMVA,\
        sum(self.instance.pW[w].value for w in self.instance.WIND)*self.instance.baseMVA,sum(self.instance.PD[d] for d in self.instance.D)*self.instance.baseMVA])
        print tabulate(tab_summary, headers="firstrow", tablefmt="grid")
        print "=============================================="
    def printoutputxls(self):
        #===initialise pandas dataframes
        cols_summary    = ['Conventional generation (MW)', 'Wind generation (MW)', 'Demand (MW)']
        cols_bus        = ['name', 'angle(degs)']
        cols_demand     = ['name', 'busname', 'PD(MW)','alpha']
        cols_wind       = ['name', 'busname', 'PW(MW)', 'pW(MW)']


        if 'LF' in self.mod:
            cols_generation = ['name', 'busname', 'PG(MW)', 'pG(MW)']
            if self.mod=='ACLF':
                cols_generation.append('qG(MW)')
                cols_bus.append('Voltage(p.u.)')
        if 'OPF' in self.mod:
            cols_generation = ['name', 'busname', 'PGLB(MW)', 'pG(MW)', 'PGUB(MW)']
            if self.mod=='ACOPF':
                cols_generation.append(('QGLB(MW)', 'qG(MW)', 'QGUB(MW)'))
                cols_bus.append('Voltage(p.u.)')

        if 'DC' in self.mod:
            cols_branch     = ['name', 'from_busname', 'to_busname', 'pL(MW)']
            cols_transf     = ['name', 'from_busname', 'to_busname', 'pLT(MW)']
        elif 'AC' in self.mod:
            cols_branch     = ['name', 'from_busname', 'to_busname', 'pLto(MW)', 'pLfrom(MW)', 'loss(MW)']
            cols_transf     = ['name', 'from_busname', 'to_busname', 'pLTto(MW)', 'pLTfrom(MW)', 'loss(MW)']
            cols_demand.append('QD(MW)')

        summary         = pd.DataFrame(columns=cols_summary)
        bus             = pd.DataFrame(columns=cols_bus)
        demand          = pd.DataFrame(columns=cols_demand)
        wind            = pd.DataFrame(columns=cols_wind)
        generation      = pd.DataFrame(columns=cols_generation)
        branch          = pd.DataFrame(columns=cols_branch)
        transformer     = pd.DataFrame(columns=cols_transf)

        #-----write Data Frames

        summary.loc[0] = pd.Series({'Conventional generation (MW)': sum(self.instance.pG[g].value for g in self.instance.G)*self.instance.baseMVA,\
        'Wind generation (MW)':sum(self.instance.pW[w].value for w in self.instance.WIND)*self.instance.baseMVA,\
        'Demand (MW)':sum(self.instance.PD[d] for d in self.instance.D)*self.instance.baseMVA})
        ind = 0
        if 'DC' in self.mod:
            for b in self.instance.B:
                bus.loc[ind] = pd.Series({'name': b,'angle(degs)':self.instance.delta[b].value*180/math.pi})
                ind += 1
            ind = 0
            for b in self.instance.L:
                branch.loc[ind] = pd.Series({'name': b, 'from_busname':self.instance.A[b,1], 'to_busname':self.instance.A[b,2],\
                'pL(MW)':self.instance.pL[b].value*self.instance.baseMVA})
                ind += 1
            ind = 0
            for b in self.instance.TRANSF:
                transformer.loc[ind] = pd.Series({'name': b, 'from_busname':self.instance.AT[b,1],
                'to_busname':self.instance.AT[b,2], 'pLT(MW)':self.instance.pLT[b].value*self.instance.baseMVA})
                ind += 1
            ind = 0
            for d in self.instance.Dbs:
                demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                'alpha':round(self.instance.alpha[d[1]].value,3)})
                ind += 1
        elif 'AC' in self.mod:
            for b in self.instance.B:
                bus.loc[ind] = pd.Series({'name': b,'angle(degs)':self.instance.delta[b].value*180/math.pi,\
                'Voltage(p.u.)':self.instance.v[b].value})
                ind += 1
            ind = 0
            for l in self.instance.L:
                branch.loc[ind] = pd.Series({'name': l, 'from_busname':self.instance.A[l,1], 'to_busname':self.instance.A[l,2],\
                'pLto(MW)':self.instance.pLto[l].value*self.instance.baseMVA,\
                'pLfrom(MW)':self.instance.pLfrom[l].value*self.instance.baseMVA,\
                'loss(MW)':(self.instance.pLto[l].value+self.instance.pLfrom[l].value)*self.instance.baseMVA})
                ind += 1
            ind = 0
            for l in self.instance.TRANSF:
                transformer.loc[ind] = pd.Series({'name': l, 'from_busname':self.instance.AT[l,1],
                'to_busname':self.instance.AT[l,2], 'pLTto(MW)':self.instance.pLtoT[l].value*self.instance.baseMVA,\
                'pLTfrom(MW)':self.instance.pLfromT[l].value*self.instance.baseMVA,\
                'loss(MW)':(self.instance.pLfromT[l].value+self.instance.pLtoT[l].value)*self.instance.baseMVA})
                ind += 1
            ind = 0
            for d in self.instance.Dbs:
                demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                'QD(MW)':self.instance.QD[d[1]]*self.instance.baseMVA,\
                'alpha':round(self.instance.alpha[d[1]].value,3)})
                ind += 1

        ind = 0
        for i in self.instance.Wbs:
            wind.loc[ind] = pd.Series({'name': i[1], 'busname':i[0], 'PW(MW)':self.instance.WG[i[1]]*instance.baseMVA,\
            'pW(MW)':self.instance.pW[i[1]].value*self.instance.baseMVA})
            ind += 1
        ind = 0
        if self.mod=='DCLF':
            for g in self.instance.Gbs:
                generation.loc[ind] = pd.Series({'name': g[1], 'busname':g[0], 'PG(MW)':self.instance.PG[g[1]]*self.instance.baseMVA,\
                'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3)})
                ind += 1
        elif self.mod=='DCOPF':
            for g in self.instance.Gbs:
                generation.loc[ind] = pd.Series({'name': g[1], 'busname':g[0], 'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3),\
                'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA})
                ind += 1
        ind = 0

        #----------------------------------------------------------
        #===write output on xlsx file===
        #
        writer = pd.ExcelWriter('results/results.xlsx', engine ='xlsxwriter')
        summary.to_excel(writer, sheet_name = 'summary',index=False)
        bus.to_excel(writer, sheet_name = 'bus',index=False)
        demand.to_excel(writer, sheet_name = 'demand',index=False)
        generation.to_excel(writer, sheet_name = 'generator',index=False)
        wind.to_excel(writer, sheet_name = 'wind',index=False)
        branch.to_excel(writer, sheet_name = 'branch',index=False)
        transformer.to_excel(writer, sheet_name = 'transformer',index=False)
