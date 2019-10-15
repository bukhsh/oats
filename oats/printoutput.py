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
        print ("========================")
        print ("\n Output from the OATS")
        print ("========================")
    def solutionstatus(self):
        self.instance.solutions.load_from(self.results)
        print ("------Solver Message------")
        print (self.results.solver)
        print ("--------------------------")
        if (self.results.solver.status == SolverStatus.ok) \
        and (self.results.solver.termination_condition == TerminationCondition.optimal):
            print ("Optimization Converged!")
        elif self.results.solver.termination_condition == TerminationCondition.infeasible:
            sys.exit("Problem is infeasible!\nOats terminated. No output is written on the results file.")
        else:
            print (sys.exit("Problem is infeasible!\nOats terminated. No output is written on the results file."))
    def printsummary(self):
        if 'LF' not in self.mod:
            print ("Cost of the objective function:", str(float(self.instance.OBJ())))
        print ("***********")
        print ("\n Summary")
        print ("***********")
        tab_summary = []
        tab_summary.append(['Conventional generation (MW)','Wind generation (MW)', 'Demand (MW)'])
        tab_summary.append([sum(self.instance.pG[g].value for g in self.instance.G)*self.instance.baseMVA,\
        sum(self.instance.pW[w].value for w in self.instance.WIND)*self.instance.baseMVA,sum(self.instance.PD[d] for d in self.instance.D)*self.instance.baseMVA])
        print (tabulate(tab_summary, headers="firstrow", tablefmt="grid"))
        print ("==============================================")
    def printoutputxls(self):
        #===initialise pandas dataframes
        cols_summary    = ['Conventional generation (MW)', 'Wind generation (MW)', 'Demand (MW)','Objective function value']
        cols_bus        = ['name', 'angle(degs)']
        cols_demand     = ['name', 'busname', 'PD(MW)']

        if ('DC' in self.mod) or ('SC' in self.mod):
            cols_branch     = ['name', 'from_busname', 'to_busname', 'pL(MW)']
            cols_transf     = ['name', 'from_busname', 'to_busname', 'pLT(MW)']
            if 'LF' in self.mod:
                cols_generation = ['name', 'busname', 'PG(MW)', 'pG(MW)']
                cols_wind       = ['name', 'busname', 'PG(MW)', 'pG(MW)']
            elif 'OPF' in self.mod:
                cols_demand.append('alpha')
                cols_branch.append('SLmax(MW)')
                cols_transf.append('SLmax(MW)')
                cols_generation = ['name', 'busname', 'PGLB(MW)','PG(MW)', 'pG(MW)','PGUB(MW)']
                cols_wind       = ['name', 'busname', 'PGLB(MW)','PG(MW)', 'pG(MW)','PGUB(MW)']
        elif 'AC' in self.mod:
            cols_bus.append('Voltage(p.u.)')
            cols_demand.append('QD(MVar)')
            cols_branch     = ['name', 'from_busname', 'to_busname', 'pLto(MW)', 'pLfrom(MW)', 'loss(MW)']
            cols_transf     = ['name', 'from_busname', 'to_busname', 'pLTto(MW)', 'pLTfrom(MW)', 'loss(MW)']
            if 'LF' in self.mod:
                cols_transf.append('tap')
                cols_generation = ['name', 'busname', 'PG(MW)', 'pG(MW)', 'qG(MVar)']
                cols_wind       = ['name', 'busname', 'PG(MW)', 'pG(MW)', 'qG(MVar)']
            elif 'OPF' in self.mod:
                cols_demand.append('alpha')
                cols_generation = ['name', 'busname', 'PGLB(MW)', 'PG(MW)', 'pG(MW)','PGUB(MW)', 'QGLB(MVar)', 'qG(MVar)','QGUB(MVar)']
                cols_wind       = ['name', 'busname', 'PGLB(MW)', 'PG(MW)', 'pG(MW)','PGUB(MW)', 'QGLB(MVar)', 'qG(MVar)','QGUB(MVar)']

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
        'Demand (MW)':sum(self.instance.PD[d] for d in self.instance.D)*self.instance.baseMVA,\
        'Objective function value': self.instance.OBJ()})

        if ('DC' in self.mod) or ('SC' in self.mod):
            #bus data
            ind=0
            for b in self.instance.B:
                bus.loc[ind] = pd.Series({'name': b,'angle(degs)':self.instance.delta[b].value*180/math.pi})
                ind += 1
            if 'LF' in self.mod:
                #line data
                ind=0
                for b in self.instance.L:
                    branch.loc[ind] = pd.Series({'name': b, 'from_busname':self.instance.A[b,1], 'to_busname':self.instance.A[b,2],\
                    'pL(MW)':self.instance.pL[b].value*self.instance.baseMVA})
                    ind += 1
                #transformer data
                ind = 0
                for b in self.instance.TRANSF:
                    transformer.loc[ind] = pd.Series({'name': b, 'from_busname':self.instance.AT[b,1],
                    'to_busname':self.instance.AT[b,2], 'pLT(MW)':self.instance.pLT[b].value*self.instance.baseMVA})
                ind += 1
                #demand data
                ind = 0
                for d in self.instance.Dbs:
                    demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA})
                    ind += 1
                #generator data
                ind = 0
                for g in self.instance.Gbs:
                    generation.loc[ind] = pd.Series({'name': g[0], 'busname':g[1],\
                    'PG(MW)':self.instance.PG[g[1]]*self.instance.baseMVA,'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3)})
                    ind += 1
                ind = 0
                #wind data
                for w in self.instance.Wbs:
                    wind.loc[ind] = pd.Series({'name': w[0], 'busname':w[1],\
                    'PG(MW)':self.instance.WG[w[1]]*self.instance.baseMVA, 'pG(MW)':round(self.instance.pW[w[1]].value*self.instance.baseMVA,3)})
                    ind += 1
            elif 'BM' in self.mod:
                #demand data
                ind = 0
                for d in self.instance.Dbs:
                    demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                    'alpha':round(self.instance.alpha[d[1]].value,3)})
                    ind += 1
                #generator data
                ind = 0
                for g in self.instance.Gbs:
                    generation.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                    'PG(MW)':round(self.instance.PG[g[1]]*self.instance.baseMVA,3),\
                    'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA})
                    ind += 1
                #wind data
                ind = 0
                for g in self.instance.Wbs:
                    wind.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.WGmin[g[1]]*self.instance.baseMVA,\
                    'PG(MW)':round(self.instance.PW[g[1]]*self.instance.baseMVA,3),\
                    'pG(MW)':round(self.instance.pW[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.WGmax[g[1]]*self.instance.baseMVA})
                    ind += 1

            elif 'OPF' in self.mod:
                #line data
                ind=0
                for b in self.instance.L:
                    branch.loc[ind] = pd.Series({'name': b, 'from_busname':self.instance.A[b,1], 'to_busname':self.instance.A[b,2],\
                    'pL(MW)':self.instance.pL[b].value*self.instance.baseMVA,'SLmax(MW)':self.instance.SLmax[b]*self.instance.baseMVA})
                    ind += 1
                #transformer data
                ind = 0
                for b in self.instance.TRANSF:
                    transformer.loc[ind] = pd.Series({'name': b, 'from_busname':self.instance.AT[b,1],
                    'to_busname':self.instance.AT[b,2], 'pLT(MW)':self.instance.pLT[b].value*self.instance.baseMVA,\
                    'SLmax(MW)':self.instance.SLmaxT[b]*self.instance.baseMVA})
                    ind += 1

                #demand data
                ind = 0
                for d in self.instance.Dbs:
                    demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                    'alpha':round(self.instance.alpha[d[1]].value,3)})
                    ind += 1
                #generator data
                ind = 0
                for g in self.instance.Gbs:
                    generation.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                    'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA})
                    ind += 1

                #wind data
                ind = 0
                for g in self.instance.Wbs:
                    wind.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.WGmin[g[1]]*self.instance.baseMVA,\
                    'PG(MW)':round(self.instance.PW[g[1]]*self.instance.baseMVA,3),\
                    'pG(MW)':round(self.instance.pW[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.WGmax[g[1]]*self.instance.baseMVA})
                    ind += 1
        elif 'AC' in self.mod:
            #bus data
            ind=0
            for b in self.instance.B:
                bus.loc[ind] = pd.Series({'name': b,'angle(degs)':self.instance.delta[b].value*180/math.pi,\
                'Voltage(p.u.)':self.instance.v[b].value})
                ind += 1
            #line data
            ind = 0
            for l in self.instance.L:
                branch.loc[ind] = pd.Series({'name': l, 'from_busname':self.instance.A[l,1], 'to_busname':self.instance.A[l,2],\
                'pLto(MW)':self.instance.pLto[l].value*self.instance.baseMVA,\
                'pLfrom(MW)':self.instance.pLfrom[l].value*self.instance.baseMVA,\
                'loss(MW)':(self.instance.pLto[l].value+self.instance.pLfrom[l].value)*self.instance.baseMVA})
                ind += 1
            ind = 0
            if 'LF' in self.mod:
                #transformer data
                for l in self.instance.TRANSF:
                    transformer.loc[ind] = pd.Series({'name': l, 'from_busname':self.instance.AT[l,1],
                    'to_busname':self.instance.AT[l,2], 'pLTto(MW)':self.instance.pLtoT[l].value*self.instance.baseMVA,\
                    'pLTfrom(MW)':self.instance.pLfromT[l].value*self.instance.baseMVA,\
                    'loss(MW)':(self.instance.pLfromT[l].value+self.instance.pLtoT[l].value)*self.instance.baseMVA,\
                    'tap':self.instance.tap[l].value})
                    ind += 1
                #demand data
                ind = 0
                for d in self.instance.Dbs:
                    demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                    'QD(MVar)':self.instance.QD[d[1]]*self.instance.baseMVA})
                    ind += 1
                #generator data
                ind = 0
                for g in self.instance.Gbs:
                    generation.loc[ind] = pd.Series({'name': g[0], 'busname':g[1],\
                    'PG(MW)':self.instance.PG[g[1]]*self.instance.baseMVA,'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3),\
                    'qG(MVar)':round(self.instance.qG[g[1]].value*self.instance.baseMVA,3)})
                    ind += 1
                #wind data
                ind = 0
                for g in self.instance.Wbs:
                    wind.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PG(MW)':self.instance.PG[g[1]]*self.instance.baseMVA,\
                    'pG(MW)':round(self.instance.pW[g[1]].value*self.instance.baseMVA,3)})
                    ind += 1
            elif 'BM' in self.mod:
                ind = 0
                #transformer data
                for l in self.instance.TRANSF:
                    transformer.loc[ind] = pd.Series({'name': l, 'from_busname':self.instance.AT[l,1],
                    'to_busname':self.instance.AT[l,2], 'pLTto(MW)':self.instance.pLtoT[l].value*self.instance.baseMVA,\
                    'pLTfrom(MW)':self.instance.pLfromT[l].value*self.instance.baseMVA,\
                    'loss(MW)':(self.instance.pLfromT[l].value+self.instance.pLtoT[l].value)*self.instance.baseMVA})
                    ind += 1
                #demand data
                ind = 0
                for d in self.instance.Dbs:
                    demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                    'QD(MVar)':self.instance.QD[d[1]]*self.instance.baseMVA,\
                    'alpha':round(self.instance.alpha[d[1]].value,3)})
                    ind += 1
                #generator data
                ind=0
                for g in self.instance.Gbs:
                    generation.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                    'PG(MW)':round(self.instance.PG[g[1]]*self.instance.baseMVA,3),\
                    'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA,\
                    'QGLB(MVar)':self.instance.QGmin[g[1]]*self.instance.baseMVA,\
                    'qG(MVar)':round(self.instance.qG[g[1]].value*self.instance.baseMVA,3),\
                    'QGUB(MVar)':self.instance.QGmax[g[1]]*self.instance.baseMVA})
                    ind += 1
                #wind data
                ind = 0
                for g in self.instance.Wbs:
                    wind.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                    'pG(MW)':round(self.instance.pW[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA,\
                    'QGLB(MVar)':self.instance.QGmin[g[1]]*self.instance.baseMVA,\
                    'qG(MVar)':round(self.instance.qW[g[1]].value*self.instance.baseMVA,3),\
                    'QGUB(MVar)':self.instance.QGmax[g[1]]*self.instance.baseMVA})
                    ind += 1
            elif 'OPF' in self.mod:
                ind = 0
                #transformer data
                for l in self.instance.TRANSF:
                    transformer.loc[ind] = pd.Series({'name': l, 'from_busname':self.instance.AT[l,1],
                    'to_busname':self.instance.AT[l,2], 'pLTto(MW)':self.instance.pLtoT[l].value*self.instance.baseMVA,\
                    'pLTfrom(MW)':self.instance.pLfromT[l].value*self.instance.baseMVA,\
                    'loss(MW)':(self.instance.pLfromT[l].value+self.instance.pLtoT[l].value)*self.instance.baseMVA})
                    ind += 1
                #demand data
                ind = 0
                for d in self.instance.Dbs:
                    demand.loc[ind] = pd.Series({'name': d[1],'busname':d[0],'PD(MW)':self.instance.PD[d[1]]*self.instance.baseMVA,\
                    'QD(MVar)':self.instance.QD[d[1]]*self.instance.baseMVA,\
                    'alpha':round(self.instance.alpha[d[1]].value,3)})
                    ind += 1
                #generator data
                ind=0
                for g in self.instance.Gbs:
                    generation.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                    'pG(MW)':round(self.instance.pG[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA,\
                    'QGLB(MVar)':self.instance.QGmin[g[1]]*self.instance.baseMVA,\
                    'qG(MVar)':round(self.instance.qG[g[1]].value*self.instance.baseMVA,3),\
                    'QGUB(MVar)':self.instance.QGmax[g[1]]*self.instance.baseMVA})
                    ind += 1
                #wind data
                ind = 0
                for g in self.instance.Wbs:
                    wind.loc[ind] = pd.Series({'name':g[0], 'busname':g[1],\
                    'PGLB(MW)':self.instance.PGmin[g[1]]*self.instance.baseMVA,\
                    'pG(MW)':round(self.instance.pW[g[1]].value*self.instance.baseMVA,3),\
                    'PGUB(MW)':self.instance.PGmax[g[1]]*self.instance.baseMVA,\
                    'QGLB(MVar)':self.instance.QGmin[g[1]]*self.instance.baseMVA,\
                    'qG(MVar)':round(self.instance.qW[g[1]].value*self.instance.baseMVA,3),\
                    'QGUB(MVar)':self.instance.QGmax[g[1]]*self.instance.baseMVA})
                    ind += 1


        #----------------------------------------------------------
        #===write output on xlsx file===
        #
        bus = bus.sort_values(['name'])
        generation = generation.sort_values(['name'])
        demand = demand.sort_values(['name'])
        writer = pd.ExcelWriter('results.xlsx', engine ='xlsxwriter')
        summary.to_excel(writer, sheet_name = 'summary',index=False)
        bus.to_excel(writer, sheet_name = 'bus',index=False)
        demand.to_excel(writer, sheet_name = 'demand',index=False)
        generation.to_excel(writer, sheet_name = 'generator',index=False)
        wind.to_excel(writer, sheet_name = 'wind',index=False)
        branch.to_excel(writer, sheet_name = 'branch',index=False)
        transformer.to_excel(writer, sheet_name = 'transformer',index=False)
        writer.save()
    def printUC(self):
        print ("Cost of the objective function:", str(float(self.instance.OBJ())))
        print ("***********")
        print ("\n Summary")
        print ("***********")
        tab_summary = []
        tab_summary.append(['Time Period','Units on','Conventional generation (MW)','Wind generation (MW)', 'Demand (MW)','Cost'])
        for t in self.instance.T:
            tab_summary.append([t,sum(self.instance.u[g,t].value for g in self.instance.G),\
            sum(self.instance.pG[g,t].value for g in self.instance.G)*self.instance.baseMVA,\
            sum(self.instance.pW[w,t].value for w in self.instance.WIND)*self.instance.baseMVA,sum(self.instance.PD[d,t] for d in self.instance.D)*self.instance.baseMVA,\
            self.instance.costfunc[t].value/(sum(self.instance.PD[d,t] for d in self.instance.D)*self.instance.baseMVA)])
        print (tabulate(tab_summary, headers="firstrow", tablefmt="grid"))

        print ("***************\n")
        print ("Zonal Flows\n")
        print ("***************")
        zoneflow = []
        zoneflow.append(['Time Period','Fr','To','Zone Fr (MW)','Zone To (MW)'])
        for t in self.instance.T:
            for l in self.instance.ICT:
                zoneflow.append([t,self.instance.A[l,1],self.instance.A[l,2], self.instance.pICTto[l,t].value*self.instance.baseMVA,\
                self.instance.pICTfrom[l,t].value*self.instance.baseMVA])
        print (tabulate(zoneflow, headers="firstrow", tablefmt="grid"))


        print ("***************\n")
        print ("Storage\n")
        print ("***************")
        storage = []
        storage.append(['Storage','Time Period','Charge(MWh)','Discharge(MWh)','State(MWh)'])
        for t in self.instance.T:
            for s in self.instance.S:
                storage.append([s,t,self.instance.pSIn[s,t].value*self.instance.baseMVA,\
                self.instance.pSOut[s,t].value*self.instance.baseMVA,\
                self.instance.pS[s,t].value*self.instance.baseMVA])


        print (tabulate(storage, headers="firstrow", tablefmt="grid"))

        print ("==============================================")

        cols_summary    = ['Time Period','Conventional generation (MW)', 'Wind generation (MW)', 'Demand (MW)']
        cols_zone       = ['Time Period','Zone', 'Conventional generation (MW)', 'Wind generation (MW)', 'Demand (MW)']
        cols_ict        = ['Time Period','From', 'To', 'Power flow To(MW)', 'Power flow Fr(MW)']
        cols_gen        = ['Time Period','Generator', 'on/off', 'start', 'stop','pG(MW)']

        summary         = pd.DataFrame(columns=cols_summary)
        zone            = pd.DataFrame(columns=cols_zone)
        interconnect    = pd.DataFrame(columns=cols_ict)
        generation      = pd.DataFrame(columns=cols_gen)
        ind = 0
        for t in self.instance.T:
            summary.loc[ind] = pd.Series({'Time Period':t,'Conventional generation (MW)':sum(self.instance.pG[g,t].value for g in self.instance.G)*self.instance.baseMVA,\
            'Wind generation (MW)':sum(self.instance.pW[w,t].value for w in self.instance.WIND)*self.instance.baseMVA,\
            'Demand (MW)':sum(self.instance.PD[d,t] for d in self.instance.D)*self.instance.baseMVA})
            ind += 1
        ind = 0
        for t in self.instance.T:
            for z in self.instance.Z:
                zone.loc[ind] = pd.Series({'Time Period':t,'Zone':z,'Conventional generation (MW)':sum(self.instance.pG[g,t].value for (g,z) in self.instance.GZ)*self.instance.baseMVA,\
                'Wind generation (MW)':sum(self.instance.pW[w,t].value for (w,z) in self.instance.WZ)*self.instance.baseMVA,\
                'Demand (MW)':sum(self.instance.PD[d,t] for (d,z) in self.instance.DZ)*self.instance.baseMVA})
                ind += 1
        ind = 0
        for t in self.instance.T:
            for l in self.instance.ICT:
                interconnect.loc[ind] = pd.Series({'Time Period':t,'From':self.instance.A[l,1],'To':self.instance.A[l,2],\
                'Power flow To(MW)':self.instance.pICTto[l,t].value*self.instance.baseMVA,'Power flow Fr(MW)':self.instance.pICTfrom[l,t].value*self.instance.baseMVA})
                ind += 1
        ind = 0
        for t in self.instance.T:
            for g in self.instance.G:
                generation.loc[ind] = pd.Series({'Time Period':t,'Generator':g, 'on/off':self.instance.u[g,t].value,\
                'start':self.instance.ustart[g,t].value, 'stop':self.instance.ustop[g,t].value,\
                'pG(MW)':self.instance.pG[g,t].value*self.instance.baseMVA})
                ind += 1
        #===write output on xlsx file===
        #
        writer = pd.ExcelWriter('results.xlsx', engine ='xlsxwriter')
        summary.to_excel(writer, sheet_name = 'summary',index=False)
        zone.to_excel(writer, sheet_name = 'zone',index=False)
        interconnect.to_excel(writer, sheet_name = 'interconnection',index=False)
        generation.to_excel(writer, sheet_name = 'generator',index=False)
        writer.save()
