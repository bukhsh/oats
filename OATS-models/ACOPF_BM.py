#==================================================================
# ACOPF.mod
# PYOMO model file of "AC" optimal power flow problem (ACOPF)
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE license. (see LICENSE file for details).
#==========Import==========
from __future__ import division
from pyomo.environ import *
#==========================

model = AbstractModel()
# --- sets ---
# buses, generators, loads, lines, sections
model.B      = Set()  # set of buses
model.G      = Set()  # set of generators
model.WIND   = Set()  # set of wind generators
model.D      = Set()  # set of demands
model.L      = Set()  # set of lines
model.SHUNT  = Set()  # set of shunts
model.LE     = Set()  # line-to and from ends set (1,2)
model.TRANSF = Set()  # set of transformers
model.b0     = Set(within=model.B)  # set of reference buses
model.Transf2   = Set(within=model.TRANSF)
model.Bvolt     = Set()  # set of bus that connects voltage regulated transformer

# generators, buses, loads linked to each bus b
model.Gbs = Set(within=model.B * model.G)    # generator-bus mapping
model.Dbs = Set(within=model.B * model.D)    # demand-bus mapping
model.Wbs = Set(within=model.B * model.WIND) # wind-bus mapping
model.SHUNTbs = Set(within=model.B * model.SHUNT)# shunt-bus mapping

# --- parameters ---
# --- tap ratio bounds ---
model.TapUB = Param(model.TRANSF, within=NonNegativeReals)
model.TapLB = Param(model.TRANSF, within=NonNegativeReals)
model.Tap = Param(model.TRANSF, within=NonNegativeReals)
model.VTar = Param(model.Bvolt, within=NonNegativeReals)
# line matrix
model.A = Param(model.L*model.LE)       # bus-line
model.AT = Param(model.TRANSF*model.LE) # bus-transformer

# demands
model.PD = Param(model.D, within=Reals)  # real power demand
model.QD = Param(model.D, within=Reals)  # reactive power demand
model.VOLL    = Param(model.D, within=Reals) #value of lost load

# generators
model.PGmax    = Param(model.G, within=NonNegativeReals) # max real power of generator
model.PGmin    = Param(model.G, within=Reals)            # min real power of generator
model.QGmax    = Param(model.G, within=NonNegativeReals) # max reactive power of generator
model.QGmin    = Param(model.G, within=Reals)            # min reactive power of generator

#wind generators
model.WGmax    = Param(model.WIND,  within=NonNegativeReals) # max real power of wind generator
model.WGmin    = Param(model.WIND,  within=NonNegativeReals) # min real power of wind generator
model.WGQmax   = Param(model.WIND,  within=NonNegativeReals) # max reactive power of wind generator
model.WGQmin   = Param(model.WIND,  within=Reals)            # min reactive power of wind generator

# lines
model.SLmax = Param(model.L, within=NonNegativeReals) # max real power limit on flow in a line
model.GL = Param(model.L, within=Reals)
model.BL = Param(model.L, within=Reals)
model.BC = Param(model.L, within=Reals)

#emergency ratings
model.SLmax_E = Param(model.L, within=NonNegativeReals)       # max emergency real power flow limit
model.SLmaxT_E = Param(model.TRANSF, within=NonNegativeReals) # max emergency real power flow limit

#transformers
model.Tap          = Param(model.TRANSF, within=NonNegativeReals)  # turns ratio of a transformer
model.TapLB        = Param(model.TRANSF, within=NonNegativeReals)  # lower bound on turns ratio
model.TapUB        = Param(model.TRANSF, within=NonNegativeReals)  # upper bound on turns ratio
model.Deltashift   = Param(model.TRANSF) #  phase shift of transformer, rad
model.DeltashiftLB = Param(model.TRANSF) #  lower bound on phase shift of transformer, rad
model.DeltashiftUB = Param(model.TRANSF) #  upper bound on phase shift of transformer, rad

model.SLmaxT = Param(model.TRANSF, within=NonNegativeReals) # max real power flow limit
model.GLT    = Param(model.TRANSF, within=Reals)
model.BLT    = Param(model.TRANSF, within=Reals)

model.g  = Param(model.TRANSF, within=Reals)
model.b  = Param(model.TRANSF, within=Reals)
model.bC = Param(model.TRANSF, within=Reals)
# derived line parameters
model.G11 = Param(model.L, within=Reals)
model.G12 = Param(model.L, within=Reals)
model.G21 = Param(model.L, within=Reals)
model.G22 = Param(model.L, within=Reals)
model.B11 = Param(model.L, within=Reals)
model.B12 = Param(model.L, within=Reals)
model.B21 = Param(model.L, within=Reals)
model.B22 = Param(model.L, within=Reals)
## derived transformer parameters
model.G11T = Param(model.TRANSF, within=Reals)
model.G12T = Param(model.TRANSF, within=Reals)
model.G21T = Param(model.TRANSF, within=Reals)
model.G22T = Param(model.TRANSF, within=Reals)
model.B11T = Param(model.TRANSF, within=Reals)
model.B12T = Param(model.TRANSF, within=Reals)
model.B21T = Param(model.TRANSF, within=Reals)
model.B22T = Param(model.TRANSF, within=Reals)

# buses
model.Vmax = Param(model.B, within=NonNegativeReals) #  max voltage angle
model.Vmin = Param(model.B, within=NonNegativeReals) #  min voltage angle

#shunt
model.GB = Param(model.SHUNT, within=Reals) #  shunt conductance
model.BB = Param(model.SHUNT, within=Reals) #  shunt susceptance

# cost
model.c2    = Param(model.G, within=NonNegativeReals)# generator cost coefficient c2 (*pG^2)
model.c1    = Param(model.G, within=NonNegativeReals)# generator cost coefficient c1 (*pG)
model.c0    = Param(model.G, within=NonNegativeReals)# generator cost coefficient c0
model.bid   = Param(model.G, within=Reals)# generator cost coefficient c1 (*pG)
model.offer = Param(model.G, within=NonNegativeReals)# generator cost coefficient c0

model.baseMVA = Param(within=NonNegativeReals)# base MVA

#constants
model.eps = Param(within=NonNegativeReals)

# --- variables ---
model.PG       = Param(model.G, domain= NonNegativeReals)# real power output of generator
model.pG       = Var(model.G, domain= NonNegativeReals)# real power output of generator
model.pGUp     = Var(model.G, domain= NonNegativeReals)# real power output of generator
model.pGDown   = Var(model.G, domain= NonNegativeReals)# real power output of generator

model.QG       = Param(model.G, domain= Reals)# real power output of generator
model.qG       = Var(model.G, domain= Reals)# reactive power output of generator
model.qGUp     = Var(model.G, domain= NonNegativeReals)# reactive power output of generator
model.qGDown   = Var(model.G, domain= NonNegativeReals)# reactive power output of generator

model.pW       = Var(model.WIND, domain= Reals) #real power generation from wind
model.qW       = Var(model.WIND, domain= Reals) #reactive power generation from wind
model.pD       = Var(model.D, domain= Reals)# real power absorbed by demand
model.qD       = Var(model.D, domain= Reals)# reactive power absorbed by demand
model.pLfrom   = Var(model.L, domain= Reals) # real power injected at b onto line
model.pLto     = Var(model.L, domain= Reals) # real power injected at b' onto line
model.qLfrom   = Var(model.L, domain= Reals) # reactive power injected at b onto line
model.qLto     = Var(model.L, domain= Reals) # reactive power injected at b' onto line
model.pLfromT  = Var(model.TRANSF, domain= Reals) # real power injected at b onto transformer
model.pLtoT    = Var(model.TRANSF, domain= Reals) # real power injected at b' onto transformer
model.qLfromT  = Var(model.TRANSF, domain= Reals) # reactive power injected at b onto transformer
model.qLtoT    = Var(model.TRANSF, domain= Reals) # reactive power injected at b' onto transformer
model.tap      = Var(model.TRANSF,initialize=1.0, within=NonNegativeReals)  # turns ratio of a transformer

#model.deltaL = Var(model.L, domain= Reals) # angle difference across lines
model.delta  = Var(model.B, domain= Reals, initialize=0.0) # voltage phase angle at bus b, rad
model.v      = Var(model.B, domain= NonNegativeReals, initialize=1.0) # voltage magnitude at bus b, rad
model.alpha  = Var(model.D, initialize=1.0, domain= NonNegativeReals)# proportion to supply of load d

# --- cost function ---
def objective(model):
    obj = sum(model.bid[g]*model.baseMVA*model.pGDown[g]+ model.offer[g]*model.baseMVA*model.pGUp[g] for g in model.G)+\
    0.0*sum(model.baseMVA*model.qGDown[g]+ model.baseMVA*model.qGUp[g] for g in model.G)+\
    sum(999*(model.PD[d]-model.pD[d])*100 for d in model.D)
    return obj
model.OBJ = Objective(rule=objective, sense=minimize)

# --- Kirchoff's current law at each bus b ---
def KCL_real_def(model, b):
    return sum(model.pG[g] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.pW[w] for w in model.WIND if (b,w) in model.Wbs)==\
    sum(model.pD[d] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.pLfrom[l] for l in model.L if model.A[l,1]==b)+ \
    sum(model.pLto[l] for l in model.L if model.A[l,2]==b)+\
    sum(model.pLfromT[l] for l in model.TRANSF if model.AT[l,1]==b)+ \
    sum(model.pLtoT[l] for l in model.TRANSF if model.AT[l,2]==b)+\
    sum(model.GB[s]*model.v[b]**2 for s in model.SHUNT if (b,s) in model.SHUNTbs)
def KCL_reactive_def(model, b):
    return sum(model.qG[g] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.qW[w] for w in model.WIND if (b,w) in model.Wbs)== \
    sum(model.qD[d] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.qLfrom[l] for l in model.L if model.A[l,1]==b)+ \
    sum(model.qLto[l] for l in model.L if model.A[l,2]==b)+\
    sum(model.qLfromT[l] for l in model.TRANSF if model.AT[l,1]==b)+ \
    sum(model.qLtoT[l] for l in model.TRANSF if model.AT[l,2]==b)-\
    sum(model.BB[s]*model.v[b]**2 for s in model.SHUNT if (b,s) in model.SHUNTbs)
model.KCL_real     = Constraint(model.B, rule=KCL_real_def)
model.KCL_reactive = Constraint(model.B, rule=KCL_reactive_def)


# --- FPN constraints for P and Q---
def FPN_P(model,g):
    return model.pG[g] == model.PG[g] + model.pGUp[g] - model.pGDown[g]
def FPN_Q(model,g):
    return model.qG[g] == model.QG[g] + model.qGUp[g] - model.qGDown[g]
model.FPN_Pconst = Constraint(model.G, rule=FPN_P)
model.FPN_Qconst = Constraint(model.G, rule=FPN_Q)


# --- Kirchoff's voltage law on each line ---
def KVL_real_fromend(model,l):
    return model.pLfrom[l] == model.G11[l]*(model.v[model.A[l,1]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.B12[l]*sin(model.delta[model.A[l,1]]-\
    model.delta[model.A[l,2]])+model.G12[l]*cos(model.delta[model.A[l,1]]-model.delta[model.A[l,2]]))
def KVL_real_toend(model,l):
    return model.pLto[l] == model.G22[l]*(model.v[model.A[l,2]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.B21[l]*sin(model.delta[model.A[l,2]]-\
    model.delta[model.A[l,1]])+model.G21[l]*cos(model.delta[model.A[l,2]]-model.delta[model.A[l,1]]))
def KVL_reactive_fromend(model,l):
    return model.qLfrom[l] == -model.B11[l]*(model.v[model.A[l,1]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.G12[l]*sin(model.delta[model.A[l,1]]-\
    model.delta[model.A[l,2]])-model.B12[l]*cos(model.delta[model.A[l,1]]-model.delta[model.A[l,2]]))
def KVL_reactive_toend(model,l):
    return model.qLto[l] == (-model.B22[l]*(model.v[model.A[l,2]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.G21[l]*sin(model.delta[model.A[l,2]]-\
    model.delta[model.A[l,1]])-model.B21[l]*cos(model.delta[model.A[l,2]]-model.delta[model.A[l,1]])))
model.KVL_real_from     = Constraint(model.L, rule=KVL_real_fromend)
model.KVL_real_to       = Constraint(model.L, rule=KVL_real_toend)
model.KVL_reactive_from = Constraint(model.L, rule=KVL_reactive_fromend)
model.KVL_reactive_to   = Constraint(model.L, rule=KVL_reactive_toend)

# --- Kirchoff's voltage law on each transformer line ---
def KVL_real_fromendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,2] in model.Bvolt):
        return model.pLfromT[l] == (model.g[l]/(model.tap[l]**2))*(model.v[model.AT[l,1]]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])+model.g[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
    else:
        return model.pLfromT[l] == (model.g[l]/(model.Tap[l]**2))*(model.v[model.AT[l,1]]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])+model.g[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
def KVL_real_toendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,2] in model.Bvolt):
        return model.pLtoT[l] == model.g[l]*(model.v[model.AT[l,2]]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,2]]-\
        model.delta[model.AT[l,1]])+model.g[l]*cos(model.delta[model.AT[l,2]]-model.delta[model.AT[l,1]]))
    else:
        return model.pLtoT[l] == model.g[l]*(model.v[model.AT[l,2]]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,2]]-\
        model.delta[model.AT[l,1]])+model.g[l]*cos(model.delta[model.AT[l,2]]-model.delta[model.AT[l,1]]))
def KVL_reactive_fromendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,2] in model.Bvolt):
        return model.qLfromT[l] == -(model.b[l]+0.5*model.bC[l])*(model.v[model.AT[l,1]]**2)/(model.tap[l]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.g[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])-model.b[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
    else:
        return model.qLfromT[l] == -(model.b[l]+0.5*model.bC[l])*(model.v[model.AT[l,1]]**2)/(model.Tap[l]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.g[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])-model.b[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
def KVL_reactive_toendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,2] in model.Bvolt):
        return model.qLtoT[l] == -(model.b[l]+0.5*model.bC[l])*(model.v[model.AT[l,2]]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.g[l]*sin(model.delta[model.AT[l,2]]-\
        model.delta[model.AT[l,1]])-model.b[l]*cos(model.delta[model.AT[l,2]]-model.delta[model.AT[l,1]]))
    else:
        return model.qLtoT[l] == -(model.b[l])*(model.v[model.AT[l,2]]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.g[l]*sin(model.delta[model.AT[l,2]]-\
        model.delta[model.AT[l,1]])-model.b[l]*cos(model.delta[model.AT[l,2]]-model.delta[model.AT[l,1]]))
model.KVL_real_fromTransf     = Constraint(model.TRANSF, rule=KVL_real_fromendTransf)
model.KVL_real_toTransf       = Constraint(model.TRANSF, rule=KVL_real_toendTransf)
model.KVL_reactive_fromTransf = Constraint(model.TRANSF, rule=KVL_reactive_fromendTransf)
model.KVL_reactive_toTransf   = Constraint(model.TRANSF, rule=KVL_reactive_toendTransf)

# --- tap ratios ---
def tap_max(model,l):
    if l in model.Transf2:
        return model.tap[l] <= model.TapUB[l]
    else:
        return model.tap[l] <= model.Tap[l]
def tap_min(model,l):
    if l in model.Transf2:
        return model.tap[l] >= model.TapLB[l]
    else:
        return model.tap[l] >= model.Tap[l]
model.TapMaxC = Constraint(model.TRANSF, rule=tap_max)
model.TapMinC = Constraint(model.TRANSF, rule=tap_min)

# --- voltage constraint on a voltage regulated transformer---
def volt_reg(model,b):
    return model.v[b] <= model.VTar[b]
def volt_reg2(model,b):
    return model.v[b] >= model.VTar[b]
# model.VoltRegC  = Constraint(model.Bvolt, rule=volt_reg)
# model.VoltRegC2 = Constraint(model.Bvolt, rule=volt_reg2)

# --- generator power limits ---
def Real_Power_Max(model,g):
    return model.pG[g] <= model.PGmax[g]
def Real_Power_Min(model,g):
    return model.pG[g] >= model.PGmin[g]
def Reactive_Power_Max(model,g):
    return model.qG[g] <= model.QGmax[g]
def Reactive_Power_Min(model,g):
    return model.qG[g] >= model.QGmin[g]
model.PGmaxC = Constraint(model.G, rule=Real_Power_Max)
model.PGminC = Constraint(model.G, rule=Real_Power_Min)
model.QGmaxC = Constraint(model.G, rule=Reactive_Power_Max)
model.QGminC = Constraint(model.G, rule=Reactive_Power_Min)

# ---wind generator power limits ---
def Wind_Real_Power_Max(model,w):
    return model.pW[w] <= model.WGmax[w]
def Wind_Real_Power_Min(model,w,t):
    return model.pW[w] >= model.WGmin[w]
def Wind_Reactive_Power_Max(model,w):
    return model.qW[w] <= model.WGQmax[w]
def Wind_Reactive_Power_Min(model,w):
    return model.qW[w] >= model.WGQmin[w]
model.WGmaxC  = Constraint(model.WIND, rule=Wind_Real_Power_Max)
model.WGminC  = Constraint(model.WIND, rule=Wind_Real_Power_Min)
model.WGQmaxC = Constraint(model.WIND, rule=Wind_Reactive_Power_Max)
model.WGQminC = Constraint(model.WIND, rule=Wind_Reactive_Power_Min)

# --- demand and load shedding ---
def Load_Shed_real(model,d):
    return model.pD[d] == model.alpha[d]*model.PD[d]
def Load_Shed_reactive(model,d):
    return model.qD[d] == model.alpha[d]*model.QD[d]
model.LoadShed_real = Constraint(model.D, rule=Load_Shed_real)
model.LoadShed_reactive = Constraint(model.D, rule=Load_Shed_reactive)

def alpha_BoundUB(model,d):
    return model.alpha[d] <= 1
def alpha_BoundLB(model,d):
    return model.alpha[d] >= 0
model.alphaBoundUBC = Constraint(model.D, rule=alpha_BoundUB)
model.alphaBoundLBC = Constraint(model.D, rule=alpha_BoundLB)

# --- line power limits ---
def line_lim1_def(model,l):
    return model.pLfrom[l]**2+model.qLfrom[l]**2 <= model.SLmax[l]**2
def line_lim2_def(model,l):
    return model.pLto[l]**2+model.qLto[l]**2 <= model.SLmax[l]**2
model.line_lim1 = Constraint(model.L, rule=line_lim1_def)
model.line_lim2 = Constraint(model.L, rule=line_lim2_def)

# --- power flow limits on transformer lines---
def transf_lim1_def(model,l):
    return model.pLfromT[l]**2+model.qLfromT[l]**2 <= model.SLmaxT[l]**2
def transf_lim2_def(model,l):
    return model.pLtoT[l]**2+model.qLtoT[l]**2 <= model.SLmaxT[l]**2
model.transf_lim1 = Constraint(model.TRANSF, rule=transf_lim1_def)
model.transf_lim2 = Constraint(model.TRANSF, rule=transf_lim2_def)

# --- voltage constraints ---
def bus_max_voltage(model,b):
    return model.v[b] <= model.Vmax[b]
def bus_min_voltage(model,b):
    return model.v[b] >= model.Vmin[b]
model.Vmaxc = Constraint(model.B, rule=bus_max_voltage)
model.Vminc = Constraint(model.B, rule=bus_min_voltage)

# --- reference bus constraint ---
def ref_bus_def(model,b):
    return model.delta[b]==0
model.refbus = Constraint(model.b0, rule=ref_bus_def)
