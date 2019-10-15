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
import sys
deltaT = 1.0
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
        self.data["storage"]     = self.data["storage"].drop(self.data["storage"][self.data["storage"]['stat'] == 0].index.tolist())
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
        slackbus = self.data["generator"]["busname"][self.data["generator"]["type"]==3].tolist()
        for i in slackbus:
            f.write(str(i)+""+"\n")
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
        f.close()
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
        f.close()
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
        f.close()
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
        f.close()
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
        f.close()
    def printACLF(self):
        f = open(self.datfile, 'a')
        Slack     = self.data["generator"][["name"]][self.data["generator"]["type"]==3]
        f.write('set g0:=\n')
        for i in Slack.index.tolist():
            f.write(str(Slack["name"][i])+"\n")
        f.write(';\n')
        DistSlac  = self.data["generator"][["name"]][self.data["generator"]["type"]==2]
        bustransf = self.data["transformer"][["name","from_busname","to_busname"]][self.data["transformer"]["type"]==2]
        if not DistSlac.empty:
            f.write('set DistSlac:=\n')
            for i in DistSlac.index.tolist():
                f.write(str(DistSlac["name"][i])+"\n")
            f.write(';\n')
        if not bustransf.empty:
            Bvolt   = []
            Transf2 = []
            for i in bustransf.index.tolist():
                Transf2.append(bustransf["name"][i])
                frombus = self.data["bus"]["baseKV"][self.data["bus"]["name"]==bustransf["from_busname"][i]].item()
                tobus   = self.data["bus"]["baseKV"][self.data["bus"]["name"]==bustransf["to_busname"][i]].item()
                if frombus > tobus:
                    Bvolt.append(self.data["bus"]["name"][self.data["bus"]["name"]==bustransf["to_busname"][i]].item())
                else:
                    Bvolt.append(self.data["bus"]["name"][self.data["bus"]["name"]==bustransf["from_busname"][i]].item())
            f.write('set Transf2:=\n')
            for i in Transf2:
                f.write(str(i)+"\n")
            f.write(';\n')
            f.write('set Bvolt:=\n')
            for i in Bvolt:
                f.write(str(i)+"\n")
            f.write(';\n')
            f.write('param VTar:=\n')
            for i in Bvolt:
                f.write(str(i)+' '+str(self.data["bus"]["VM"][self.data["bus"]["name"]==i].item())+"\n")
            f.write(';\n')
        #---Voltage targets---
        f.write('param VS:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["VS"][i]))+"\n")
        f.write(';\n')
        if len(self.data["transformer"]["name"])!=0:
            #---Transformer tap bounds---
            f.write('param TapLB:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapLB"][i]))+"\n")
            f.write(';\n')
            f.write('param TapUB:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapUB"][i]))+"\n")
            f.write(';\n')
            f.write('param bC:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(self.data["transformer"]["b"][i])+"\n")
            f.write(';\n')
            f.write('param g:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2))+"\n")
            f.write(';\n')
            f.write('param b:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(-self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2))+"\n")
            f.write(';\n')
        f.close()
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
        f.close()
    def printBM(self):
        f = open(self.datfile, 'a')
        #---Reactive power generation bounds---
        f.write('param PG:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PG"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param QG:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["QG"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param bid:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["bid"][i]))+"\n")
        f.write(';\n')
        f.write('param offer:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["offer"][i]))+"\n")
        f.write(';\n')


        bustransf = self.data["transformer"][["name","from_busname","to_busname"]][self.data["transformer"]["type"]==2]
        if not bustransf.empty:
            Bvolt   = []
            Transf2 = []
            for i in bustransf.index.tolist():
                Transf2.append(bustransf["name"][i])
                frombus = self.data["bus"]["baseKV"][self.data["bus"]["name"]==bustransf["from_busname"][i]].item()
                tobus   = self.data["bus"]["baseKV"][self.data["bus"]["name"]==bustransf["to_busname"][i]].item()
                if frombus > tobus:
                    Bvolt.append(self.data["bus"]["name"][self.data["bus"]["name"]==bustransf["to_busname"][i]].item())
                else:
                    Bvolt.append(self.data["bus"]["name"][self.data["bus"]["name"]==bustransf["from_busname"][i]].item())
            f.write('set Transf2:=\n')
            for i in Transf2:
                f.write(str(i)+"\n")
            f.write(';\n')
            f.write('set Bvolt:=\n')
            for i in Bvolt:
                f.write(str(i)+"\n")
            f.write(';\n')
            f.write('param VTar:=\n')
            for i in Bvolt:
                f.write(str(i)+' '+str(self.data["bus"]["VM"][self.data["bus"]["name"]==i].item())+"\n")
            f.write(';\n')
        #---Voltage targets---
        if len(self.data["transformer"]["name"])!=0:
            #---Transformer tap bounds---
            f.write('param Tap:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapRatio"][i]))+"\n")
            f.write(';\n')
            f.write('param TapLB:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapLB"][i]))+"\n")
            f.write(';\n')
            f.write('param TapUB:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(float(self.data["transformer"]["TapUB"][i]))+"\n")
            f.write(';\n')
            f.write('param bC:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(self.data["transformer"]["b"][i])+"\n")
            f.write(';\n')
            f.write('param g:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(self.data["transformer"]["r"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2))+"\n")
            f.write(';\n')
            f.write('param b:=\n')
            for i in self.data["transformer"].index.tolist():
                f.write(str(self.data["transformer"]["name"][i])+" "+str(-self.data["transformer"]["x"][i]/(self.data["transformer"]["r"][i]**2+self.data["transformer"]["x"][i]**2))+"\n")
            f.write(';\n')

        f.close()

    def printDCBM(self):
        f = open(self.datfile, 'a')
        #---Reactive power generation bounds---
        f.write('param PG:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["PG"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param bidG:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["bid"][i]))+"\n")
        f.write(';\n')
        f.write('param offerG:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(self.data["generator"]["offer"][i]))+"\n")
        f.write(';\n')
        if len(self.data["wind"]["name"])!=0:
            f.write('param PW:=\n')
            for i in self.data["wind"].index.tolist():
                f.write(str(self.data["wind"]["name"][i])+" "+str(float(self.data["wind"]["PG"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')

            f.write('param bidW:=\n')
            for i in self.data["wind"].index.tolist():
                f.write(str(self.data["wind"]["name"][i])+" "+str(float(self.data["wind"]["offer"][i]))+"\n")
            f.write(';\n')
        f.close()
    def printUCdat(self):
        f = open(self.datfile, 'a')
        ##===sets===
        f.write('set LE:=\n 1 \n 2;\n')
        #---set of zones---
        f.write('set Z:=\n')
        for i in set(self.data["bus"]["zone"]):
            f.write(str(i)+"\n")
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
        #---set of interconnections between zones
        if len(set(self.data["bus"]["zone"]))>1:
            f.write('set ICT:=\n')
            for i in self.data["zonalNTC"].index.tolist():
                f.write(str(self.data["zonalNTC"]["interconnection_ID"][i])+"\n")
            f.write(';\n')
         ###---set of storage---
        if len(self.data["storage"]["name"])!=0:
            f.write('set S:=\n')
            for i in self.data["storage"]["name"].unique():
                f.write(str(i)+"\n")
            f.write(';\n')
        #---set of time-periods---
        f.write('set T:= \n')
        for i in self.data["timeseries"]["Demand"].index.tolist():
            f.write(str(i) + "\n")
        f.write(';\n')
        f.write('set TRed:= \n')
        for i in self.data["timeseries"]["Demand"].index.tolist()[1:]:
            f.write(str(i) + "\n")
        f.write(';\n')
        #---storage-bus mapping---
        if len(self.data["storage"]["name"])!=0:
            f.write('set Sbs:=\n')
            for i in self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["zone"][i]) + " "+str(self.data["storage"]["name"][i])+"\n")
            f.write(';\n')
        ##---set of GZ(generator zone mapping---
        f.write('set GZ:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(self.data["bus"]["zone"][self.data["bus"]["name"]== self.data["generator"]["busname"][i]].item())+"\n")
        f.write(';\n')
        ###---set of wind zone mapping---
        if len(self.data["wind"]["name"].index.tolist())!=0:
            f.write('set WZ:=\n')
            for i in self.data["wind"]["name"].index.tolist():
                f.write(str(self.data["wind"]["name"][i])+" "+str(self.data["bus"]["zone"][self.data["bus"]["name"]== self.data["wind"]["busname"][i]].item())+"\n")
            f.write(';\n')
        ###---set of DZ(load zone mapping---
        f.write('set DZ:=\n')
        for i in self.data["demand"]["name"].index.tolist():
            f.write(str(self.data["demand"]["name"][i])+" "+str(self.data["bus"]["zone"][self.data["bus"]["name"]==self.data["demand"]["busname"][i]].item())+"\n")
        f.write(';\n')
        #===parameters===
        #---Real power demand---
        f.write('param PD:=\n')
        for i in self.data["timeseries"]["Demand"]:
            for j in self.data["timeseries"]["Demand"].index.tolist():
                f.write(str(i)+" "+str(j)+" "+str(float(self.data["timeseries"]["Demand"][i][j])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param VOLL:=\n')
        for i in self.data["demand"].index.tolist():
            f.write(str(self.data["demand"]["name"][i])+" "+str(float(self.data["demand"]["VOLL"][i]))+"\n")
        f.write(';\n')
        f.write('param baseMVA:=\n')
        f.write(str(self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')

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
            for i in self.data["timeseries"]["Wind"]:
                for j in self.data["timeseries"]["Wind"].index.tolist():
                    f.write(str(i)+" "+str(j)+" "+str(0)+"\n")
            f.write(';\n')
            f.write('param WGmax:=\n')
            for i in self.data["timeseries"]["Wind"]:
                for j in self.data["timeseries"]["Wind"].index.tolist():
                    f.write(str(i)+" "+str(j)+" "+str(float(self.data["timeseries"]["Wind"][i][j])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')

        if len(self.data["storage"]["name"])!=0:
            f.write('param ChargeEff:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["ChargingEfficieny(%)"][i])/100.0)+"\n")
            f.write(';\n')
            f.write('param DischargeEff:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["DischargingEfficieny(%)"][i])/100.0)+"\n")
            f.write(';\n')
            f.write('param StoreUB:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["capacity(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param StoreLB:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["Minoperatingcapacity(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param StoreInitial:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["InitialStoredPower(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param StoreFinal:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["FinalStoredPower(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param rampCharge:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["chargingrate(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param rampDischarge:=\n')
            for i in  self.data["storage"].index.tolist():
                f.write(str(self.data["storage"]["name"][i])+" "+str(float(self.data["storage"]["dischargingrate(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')


        #--zonal data--
        f.write('param ResReq:=\n')
        for i in self.data["zone"].index.tolist():
            f.write(str(self.data["zone"]["zone"][i])+" "+str(float(self.data["zone"]["reserve(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        if len(self.data["zonalNTC"].index.tolist())!=0:
            f.write('param A:=\n')
            for i in self.data["zonalNTC"].index.tolist():
                f.write(str(self.data["zonalNTC"]["interconnection_ID"][i])+" "+"1"+" "+str(self.data["zonalNTC"]["from_zone"][i])+"\n")
            for i in self.data["zonalNTC"].index.tolist():
                f.write(str(self.data["zonalNTC"]["interconnection_ID"][i])+" "+"2"+" "+str(self.data["zonalNTC"]["to_zone"][i])+"\n")
            f.write(';\n')

            f.write('param NTCto:=\n')
            for i in self.data["zonalNTC"].index.tolist():
                f.write(str(self.data["zonalNTC"]["interconnection_ID"][i])+" "+str(float(self.data["zonalNTC"]["TransferCapacityTo(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')
            f.write('param NTCfr:=\n')
            for i in self.data["zonalNTC"].index.tolist():
                f.write(str(self.data["zonalNTC"]["interconnection_ID"][i])+" "+str(float(self.data["zonalNTC"]["TransferCapacityFr(MW)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
            f.write(';\n')

        #---ramp rates---
        f.write('param RampUp:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(deltaT*self.data["generator"]["RampUp(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param RampDown:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(deltaT*self.data["generator"]["RampDown(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')

        # #---minimum up and down times---
        f.write('param MinUpTime:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float((1.0/deltaT)*self.data["generator"]["MinUpTime(hr)"][i]))+"\n")
        f.write(';\n')
        f.write('param MinDownTime:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float((1.0/deltaT)*self.data["generator"]["MinDownTime(hr)"][i]))+"\n")
        f.write(';\n')

        #---cost data---
        f.write('param c2:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(self.data["generator"]["costc2"][i])+"\n")
        f.write(';\n')
        f.write('param c1:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(self.data["generator"]["costc1"][i])+"\n")
        f.write(';\n')
        f.write('param c0:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(self.data["generator"]["costc0"][i])+"\n")
        f.write(';\n')
        f.write('param SDcosts:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(self.data["generator"]["shutdown"][i])+"\n")
        f.write(';\n')
        f.write('param SUcosts:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(self.data["generator"]["startup"][i])+"\n")
        f.write(';\n')

        f.write('set UCMinUpT:=\n')
        for i in self.data["generator"].index.tolist():
            if int(self.data["generator"]["MinUpTime(hr)"][i])>1:
                for j in range(int(self.data["generator"]["MinUpTime(hr)"][i]),int(self.data["timeseries"]["Demand"].index[-1]+1)):
                    f.write(str(self.data["generator"]["name"][i])+" "+str(j)+" "+str(self.data["timeseries"]["Demand"].index[-1])+"\n")
        f.write(';\n')
        f.write('set UCMinDownT:=\n')
        for i in self.data["generator"].index.tolist():
            if int(self.data["generator"]["MinDownTime(hr)"][i])>1:
                for j in range(int(self.data["generator"]["MinDownTime(hr)"][i]),int(self.data["timeseries"]["Demand"].index[-1]+1)):
                    f.write(str(self.data["generator"]["name"][i])+" "+str(j)+" "+str(self.data["timeseries"]["Demand"].index[-1])+"\n")
        f.write(';\n')
        f.close()
    def printSCdat(self):
        flag_C = 0
        contingencies_id = 1
        contingencies_set = []
        ##--Security constrained data--
        f = open(self.datfile, 'a')
        ##--Generator contingencies--
        for i in self.data["generator"].index.tolist():
            if int(self.data["generator"]["contingency"][i])==1:
                if flag_C==0:
                    f.write('set CG:=\n')
                    flag_C=1
                f.write(str(contingencies_id)+" "+str(self.data["generator"]["name"][i])+"\n")
                contingencies_set.append(contingencies_id)
                contingencies_id += 1
        if flag_C==1:
            f.write(';\n')
        ##--Branch contingencies--
        flag_C = 0
        for i in self.data["branch"].index.tolist():
            if int(self.data["branch"]["contingency"][i])==1:
                if flag_C==0:
                    f.write('set CL:=\n')
                    flag_C=1
                f.write(str(contingencies_id)+" "+str(self.data["branch"]["name"][i])+"\n")
                contingencies_set.append([contingencies_id,str(self.data["branch"]["probability"][i])])
                contingencies_id += 1
        if flag_C==1:
            f.write(';\n')
        ##--Transformer contingencies--
        flag_C = 0
        for i in self.data["transformer"].index.tolist():
            if int(self.data["transformer"]["contingency"][i])==1:
                if flag_C==0:
                    f.write('set CT:=\n')
                    flag_C=1
                f.write(str(contingencies_id)+" "+str(self.data["transformer"]["name"][i])+"\n")
                contingencies_set.append([contingencies_id,str(self.data["transformer"]["probability"][i])])
                contingencies_id += 1
        if flag_C==1:
            f.write(';\n')
        ##--Wind contingencies--
        flag_C = 0
        for i in self.data["wind"].index.tolist():
            if int(self.data["wind"]["contingency"][i])==1:
                if flag_C==0:
                    f.write('set CWIND:=\n')
                    flag_C=1
                f.write(str(contingencies_id)+" "+str(self.data["wind"]["name"][i])+"\n")
                contingencies_set.append([contingencies_id,str(self.data["wind"]["probability"][i])])
                contingencies_id += 1
        if flag_C==1:
            f.write(';\n')
        ##--set of contingencies--
        f.write('set C:=\n')
        for i in contingencies_set:
            f.write(str(i[0])+"\n")
        f.write(';\n')
        if contingencies_set:
            f.write('param probC:=\n')
            for i in contingencies_set:
                f.write(str(i[0])+" "+str(i[1])+"\n")
            f.write(';\n')
        #---ramp rates---
        f.write('param RampUp:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(deltaT*self.data["generator"]["RampUp(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')
        f.write('param RampDown:=\n')
        for i in self.data["generator"].index.tolist():
            f.write(str(self.data["generator"]["name"][i])+" "+str(float(deltaT*self.data["generator"]["RampDown(MW/hr)"][i])/self.data["baseMVA"]["baseMVA"][0])+"\n")
        f.write(';\n')

        f.close()
