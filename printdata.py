#==================================================================
# printdata.py
# A Python script to write data file for PYOMO
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3 (see LICENSE file for details).
#==================================================================
import datetime
import math
class printdata(object):
    def __init__(self,datfile,data,model,options):
        self.datfile = datfile
        self.data    = data
        self.model   = model
        self.options = options
    def reducedata(self):
        self.data["demand"]      = self.data["demand"].drop(self.data["demand"][self.data["demand"]['stat'] == 0].index.tolist())
        self.data["branch"]      = self.data["branch"].drop(self.data["branch"][self.data["branch"]['stat'] == 0].index.tolist())
        self.data["shunt"]       = self.data["shunt"].drop(self.data["shunt"][self.data["shunt"]['stat'] == 0].index.tolist())
        self.data["transformer"] = self.data["transformer"].drop(self.data["transformer"][self.data["transformer"]['stat'] == 0].index.tolist())
        self.data["wind"]        = self.data["wind"].drop(self.data["wind"][self.data["wind"]['stat'] == 0].index.tolist())
        self.data["generator"]   = self.data["generator"].drop(self.data["generator"][self.data["generator"]['stat'] == 0].index.tolist())
    def printheader(self):
        f = open(self.datfile, 'w')
        #####PRINT HEADER--START
        f.write('#This is Python generated data file for Pyomo model DCLF.py\n')
        f.write('#_author_:W. Bukhsh\n')
        f.write('#Time stamp: '+ str(datetime.datetime.now())+'\n')
        f.close()
    def printkeysets(self):
        f = open(self.datfile, 'a')
        ##===sets===
        #---set of buses---
        f.write('set B:=\n')
        for i in self.data["bus"].index.tolist():
            f.write(str(self.data["bus"]["name"][i])+"\n")
        f.write(';\n')
        #---set of generators---
        f.write('set G:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+"\n")
        f.write(';\n')
        #---set of demands---
        f.write('set D:=\n')
        for i in self.data["demand"]["name"].unique():
            f.write(str(i)+"\n")
        f.write(';\n')
        #---set of wind generators---
        if len(self.data["wind"]["name"])!=0:
            f.write('set WIND:=\n')
            for i in self.data["wind"]["name"].unique():
                f.write(str(i)+"\n")
            f.write(';\n')
        #===parameters===
        #---Real power demand---
        f.write('param PD:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["name"][i])+" "+str(float(self.data["demand"]["real"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param VOLL:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["name"][i])+" "+str(float(self.data["demand"]["VOLL"][i]))+"\n")
        f.write(';\n')
        f.write('param baseMVA:=\n')
        f.write(str(self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.close()
    def printnetwork(self):
        f = open(self.datfile, 'a')
        f.write('set LE:=\n 1 \n 2;\n')
        #set of transmission lines
        f.write('set L:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+"\n")
        f.write(';\n')
        #set of transformers
        if len(self.data["transformer"]["name"])!=0:
            f.write('set TRANSF:= \n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+"\n")
            f.write(';\n')
        #---set of generator-bus mapping (gen_bus, gen_ind)---
        f.write('set Gbs:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["busname"][i]) + " "+str(self.data["generator"]["name"][i])+"\n")
        f.write(';\n')
        #---set of wind generator-bus mapping (windgen_bus, gen_ind)---
        if len(self.data["wind"]["name"])!=0:
            f.write('set Wbs:=\n')
            for i in self.data["wind"].index.tolist():
                f.write(str(self.data["wind"]["busname"][i]) + " "+str(self.data["wind"]["name"][i])+"\n")
            f.write(';\n')
        #---set of demand-bus mapping (demand_bus, demand_ind)---
        f.write('set Dbs:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["busname"][i]) + " "+str(self.data["demand"]["name"][i])+"\n")
        f.write(';\n')
        #---set of reference bus---
        f.write('set b0:=\n')
        for i in self.data["bus"].index.tolist():
            if float(self.data["bus"]["type"][i])==3:
                f.write(str(self.data["bus"]["name"][i])+""+"\n")
        f.write(';\n')
        #---param defining system topolgy---
        f.write('param A:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+"1"+" "+str(self.data["branch"]["from_busname"][i])+"\n")
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+"2"+" "+str(self.data["branch"]["to_busname"][i])+"\n")
        f.write(';\n')
        #---Transformers---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param AT:= \n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+"1"+" "+str(self.data["transformer"]["from_busname"][i])+"\n")
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+"2"+" "+str(self.data["transformer"]["to_busname"][i])+"\n")
            f.write(';\n')
        f.close()
    def printLF(self):
        f = open(self.datfile, 'a')
        #---Real power generation bounds---
        f.write('param PG:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PG"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        #---Real power wind generation bounds---
        if len(self.data["wind"]["name"])!=0:
            f.write('param WG:=\n')
            for i in self.data["wind"].index.tolist():
                f.write(str(self.data["wind"]["name"][i])+" "+str(float(self.data["wind"]["PG"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
        if len(self.data["transformer"]["name"])!=0:
            f.write('param Tap:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapRatio"][i]))+"\n")
            f.write(';\n')
    def printDC(self):
        f = open(self.datfile, 'a')
        #---Tranmission line chracteristics for DC load flow---
        f.write('param BL:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-1/float(self.data["branch"]["x"][i]))+"\n")
        f.write(';\n')
        #---Transformer chracteristics---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param BLT:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(-float(1/self.data["transformer"]["x"][i]))+"\n")
            f.write(';\n')
    def printOPF(self):
        f = open(self.datfile, 'a')
        #---Real power generation bounds---
        f.write('param PGmin:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PGLB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param PGmax:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PGUB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        #---Real power wind generation bounds---
        if len(self.data["wind"]["name"])!=0:
            f.write('param WGmin:=\n')
            for i in self.data["wind"].index.tolist():
                f.write(str(self.data["wind"]["name"][i])+" "+str(float(self.data["wind"]["PGLB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param WGmax:=\n')
            for i in self.data["wind"].index.tolist():
                f.write(str(self.data["wind"]["name"][i])+" "+str(float(self.data["wind"]["PGUB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
        #---Tranmission line bounds---
        f.write('param SLmax:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(float(self.data["branch"]["ContinousRating"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        #---Transformer chracteristics---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param SLmaxT:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["ContinousRating"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
        #---cost data---
        f.write('param c2:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["costc2"][i]))+"\n")
        f.write(';\n')
        f.write('param c1:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["costc1"][i]))+"\n")
        f.write(';\n')
        f.write('param c0:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["costc0"][i]))+"\n")
        f.write(';\n')
    def printDCOPF(self):
        f = open(self.datfile, 'a')
        #---Tranmission line chracteristics---
        f.write('param BL:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-1/float(self.data["branch"]["x"][i]))+"\n")
        f.write(';\n')
        #---Transformer chracteristics---
        if len(self.data["transformer"]["name"])!=0:
            f.write('param BLT:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(-float(1/self.data["transformer"]["x"][i]))+"\n")
            f.write(';\n')
            f.write('param Tap:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapRatio"][i]))+"\n")
            f.write(';\n')
    def printAC(self):
        f = open(self.datfile, 'a')
        #set of shunts
        if len(self.data["shunt"]["name"])!=0:
            f.write('set SHUNT:=\n')
            for i in self.data["shunt"].index.tolist():
                f.write(str(self.data["shunt"]["name"][i])+"\n")
            f.write(';\n')
            f.write('set SHUNTbs:=\n')
            for i in self.data["shunt"].index.tolist():
                f.write(str(self.data["shunt"]["busname"][i])+" "+str(self.data["shunt"]["name"][i])+"\n")
            f.write(';\n')
            f.write('param GB:=\n')
            for i in self.data["shunt"].index.tolist():
                f.write(str(self.data["shunt"]["name"][i])+" "+str(float(self.data["shunt"]["GL"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param BB:=\n')
            for i in self.data["shunt"].index.tolist():
                f.write(str(self.data["shunt"]["name"][i])+" "+str(float(self.data["shunt"]["BL"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
        #---Reactive power demand---
        f.write('param QD:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["name"][i])+" "+str(float(self.data["demand"]["reactive"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')

        f.write('param G11:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(self.data["branch"]["r"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2))+"\n")
        f.write(';\n')
        f.write('param G12:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-self.data["branch"]["r"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2))+"\n")
        f.write(';\n')
        f.write('param G21:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-self.data["branch"]["r"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2))+"\n")
        f.write(';\n')
        f.write('param G22:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(self.data["branch"]["r"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2))+"\n")
        f.write(';\n')
        f.write('param B11:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-self.data["branch"]["x"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2)+0.5*self.data["branch"]["b"][i])+"\n")
        f.write(';\n')
        f.write('param B12:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(self.data["branch"]["x"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2))+"\n")
        f.write(';\n')
        f.write('param B21:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(self.data["branch"]["x"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2))+"\n")
        f.write(';\n')
        f.write('param B22:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(-self.data["branch"]["x"][i]/(self.data["branch"]["r"][i]**2+self.data["branch"]["x"][i]**2)+0.5*self.data["branch"]["b"][i])+"\n")
        f.write(';\n')

        #derived transformer parameters
        if len(self.data["transformer"]["name"])!=0:
            f.write('param G11T:=\n')
            for i in self.data["transformer"].index.tolist():
                temp     = self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+str(temp/(self.data["transformer"]["TapRatio"][i]**2))+"\n")
            f.write(';\n')
            f.write('param G12T:=\n')
            for i in self.data["transformer"].index.tolist():
                tempG     = self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                tempB     = -self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+\
                str(-1/(self.data["transformer"]["TapRatio"][i])*(tempG*math.cos(self.data["transformer"]["PhaseShift"][i])-\
                tempB*math.sin(self.data["transformer"]["PhaseShift"][i])))+"\n")
            f.write(';\n')
            f.write('param G21T:=\n')
            for i in self.data["transformer"].index.tolist():
                tempG     = self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                tempB     = -self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+\
                str(-1/(self.data["transformer"]["TapRatio"][i])*(tempG*math.cos(self.data["transformer"]["PhaseShift"][i])+\
                tempB*math.sin(self.data["transformer"]["PhaseShift"][i])))+"\n")
            f.write(';\n')

            f.write('param G22T:=\n')
            for i in self.data["transformer"].index.tolist():
                temp     = self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+str(temp)+"\n")
            f.write(';\n')
            f.write('param B11T:=\n')
            for i in self.data["transformer"].index.tolist():
                temp     = -self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+str(temp/(self.data["transformer"]["TapRatio"][i]**2))+"\n")
            f.write(';\n')
            f.write('param B12T:=\n')
            for i in self.data["transformer"].index.tolist():
                tempG     = self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                tempB     = -self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+\
                str(-1/(self.data["transformer"]["TapRatio"][i])*(tempB*math.cos(self.data["transformer"]["PhaseShift"][i])+\
                tempG*math.sin(self.data["transformer"]["PhaseShift"][i])))+"\n")
            f.write(';\n')
            f.write('param B21T:=\n')
            for i in self.data["transformer"].index.tolist():
                tempG     = self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                tempB     = -self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+\
                str(-1/(self.data["transformer"]["TapRatio"][i])*(-tempG*math.sin(self.data["transformer"]["PhaseShift"][i])+\
                tempB*math.cos(self.data["transformer"]["PhaseShift"][i])))+"\n")
            f.write(';\n')
            f.write('param B22T:=\n')
            for i in self.data["transformer"].index.tolist():
                temp     = -self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2)
                f.write(str(self.data["transformer"]["name"][i])+" "+str(temp)+"\n")
            f.write(';\n')
    def printACLF(self):
        f = open(self.datfile, 'a')
        #---Voltage targets---
        f.write('param VS:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["VS"][i]))+"\n")
        f.write(';\n')

        #---Tranmission line chracteristics for DC load flow---
        f.write('param BC:=\n')
        for i in self.data["branch"].index.tolist():
            f.write(str(self.data["branch"]["name"][i])+" "+str(self.data["branch"]["b"][i])+"\n")
        f.write(';\n')
        #derived line parameters
    def printACOPF(self):
        f = open(self.datfile, 'a')
        #---Reactive power generation bounds---
        f.write('param QGmin:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["QGLB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param QGmax:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["QGUB"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        #---Voltage bounds---
        f.write('param Vmin:=\n')
        for i in self.data["bus"].index.tolist():
            f.write(str(self.data["bus"]["name"][i])+" "+str(self.data["bus"]["VNLB"][i])+"\n")
        f.write(';\n')
        f.write('param Vmax:=\n')
        for i in self.data["bus"].index.tolist():
            f.write(str(self.data["bus"]["name"][i])+" "+str(self.data["bus"]["VNUB"][i])+"\n")
        f.write(';\n')
