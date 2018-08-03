#==================================================================
# ACLF.mod
# PYOMO model file of "AC" load flow problem (ACLF)
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==========Import==========
from __future__ import division
from pyomo.environ import *
#==========================

model = AbstractModel()
# --- sets ---
model.B         = Set()  # set of buses
model.G         = Set()  # set of generators
model.WIND      = Set()  # set of wind generators
model.D         = Set()  # set of loads
model.L         = Set()  # set of lines
model.SHUNT     = Set()  # set of shunts
model.LE        = Set()  # line-to and from ends set (1,2)
model.TRANSF    = Set()  # set of transformers
model.Bvolt     = Set()  # set of bus that connects voltage regulated transformer
model.b0        = Set(within=model.B)  # set of reference buses
model.g0        = Set(within=model.G)  # set of generators attached to reference bus
model.Transf2   = Set(within=model.TRANSF)
model.DistSlack = Set(within=model.G)
# generators, buses, loads linked to each bus b
model.Gbs  = Set(within=model.B * model.G)    # bus-generator map
model.Dbs  = Set(within=model.B * model.D)    # bus-demand map
model.Wbs  = Set(within=model.B * model.WIND) # bus-wind map
model.SHUNTbs = Set(within=model.B * model.SHUNT) # bus-shunt map

# --- parameters ---
model.A = Param(model.L*model.LE)        # bus-line
model.AT = Param(model.TRANSF*model.LE)  # bus-transformer

# demands
model.PD = Param(model.D, within=Reals)  # real power demand
model.QD = Param(model.D, within=Reals)  # real power demand
model.VOLL    = Param(model.D, within=Reals) #value of lost load

model.PG  = Param(model.G, within=NonNegativeReals)    # real power set-point of generator
model.WG  = Param(model.WIND, within=NonNegativeReals) # real power set-point of wind generator

# line chracteristics
model.BC = Param(model.L, within=Reals)

#transformers
model.Deltashift   = Param(model.TRANSF) #  phase shift of transformer, rad
model.GLT    = Param(model.TRANSF, within=Reals)
model.BLT    = Param(model.TRANSF, within=Reals)

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

model.g  = Param(model.TRANSF, within=Reals)
model.b  = Param(model.TRANSF, within=Reals)
model.bC = Param(model.TRANSF, within=Reals)

# --- tap ratio bounds ---
model.TapUB = Param(model.TRANSF, within=NonNegativeReals)
model.TapLB = Param(model.TRANSF, within=NonNegativeReals)
model.Tap = Param(model.TRANSF, within=NonNegativeReals)
model.VTar = Param(model.Bvolt, within=NonNegativeReals)
# voltage targets
model.VS = Param(model.G, within=NonNegativeReals) #  voltage target at generator buses

##shunt
model.GB = Param(model.SHUNT, within=Reals) #  shunt conductance
model.BB = Param(model.SHUNT, within=Reals) #  shunt susceptance

model.baseMVA = Param(within=NonNegativeReals)# base MVA

#constants
model.eps = Param(within=NonNegativeReals)

# --- variables ---
model.pG       = Var(model.G, domain= NonNegativeReals)# real power output of generator
model.qG       = Var(model.G, domain= Reals)    # reactive power output of generator
model.pW       = Var(model.WIND, domain= Reals) #real power generation from wind
model.qW       = Var(model.WIND, domain= Reals) #reactive power generation from wind
model.pD       = Var(model.D, domain= Reals) # real power absorbed by demand
model.qD       = Var(model.D, domain= Reals) # reactive power absorbed by demand
model.pLfrom   = Var(model.L, domain= Reals) # real power injected at b onto line
model.pLto     = Var(model.L, domain= Reals) # real power injected at b' onto line
model.qLfrom   = Var(model.L, domain= Reals) # reactive power injected at b onto line
model.qLto     = Var(model.L, domain= Reals) # reactive power injected at b' onto line
model.pLfromT  = Var(model.TRANSF, domain= Reals) # real power injected at b onto transformer
model.pLtoT    = Var(model.TRANSF, domain= Reals) # real power injected at b' onto transformer
model.qLfromT  = Var(model.TRANSF, domain= Reals) # reactive power injected at b onto transformer
model.qLtoT    = Var(model.TRANSF, domain= Reals) # reactive power injected at b' onto transformer
model.delta    = Var(model.B, domain= Reals, initialize=0.0) # voltage phase angle at bus b, rad
model.v        = Var(model.B, domain= NonNegativeReals, initialize=1.0) # voltage magnitude at bus b, rad
model.tap      = Var(model.TRANSF,initialize=1.0, within=NonNegativeReals)  # turns ratio of a transformer

# variables that model the violations (to help with the convergence)
model.epsPG_up    = Var(model.DistSlack, initialize=0.0, domain= NonNegativeReals)
model.epsPG_down  = Var(model.DistSlack, initialize=0.0, domain= NonNegativeReals)
model.epsV_up     = Var(model.G, initialize=0.0, domain= NonNegativeReals)
model.epsV_down   = Var(model.G, initialize=0.0, domain= NonNegativeReals)
# --- cost function ---
def objective(model):
    obj = 1*sum(model.epsV_up[g]+model.epsV_down[g] for g in model.G)+\
    1*sum(model.baseMVA*(model.pLto[l]+model.pLfrom[l]) for l in model.L)+\
    sum(model.baseMVA*(model.epsPG_up[g]+model.epsPG_down[g]) for g in model.DistSlack)
    return obj
model.OBJ = Objective(rule=objective, sense=minimize)

# --- Kirchoff's current law at each bus b ---
def KCL_real_def(model, b):
    return sum(model.pG[g] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.pW[w] for w in model.WIND if (b,w) in model.Wbs)==\
    sum(model.PD[d] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.pLfrom[l] for l in model.L if model.A[l,1]==b)+ \
    sum(model.pLto[l] for l in model.L if model.A[l,2]==b)+\
    sum(model.pLfromT[l] for l in model.TRANSF if model.AT[l,1]==b)+ \
    sum(model.pLtoT[l] for l in model.TRANSF if model.AT[l,2]==b)+\
    sum(model.GB[s]*model.v[b]**2 for s in model.SHUNT if (b,s) in model.SHUNTbs)
def KCL_reactive_def(model, b):
    return sum(model.qG[g] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.qW[w] for w in model.WIND if (b,w) in model.Wbs)== \
    sum(model.QD[d] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.qLfrom[l] for l in model.L if model.A[l,1]==b)+ \
    sum(model.qLto[l] for l in model.L if model.A[l,2]==b)+\
    sum(model.qLfromT[l] for l in model.TRANSF if model.AT[l,1]==b)+ \
    sum(model.qLtoT[l] for l in model.TRANSF if model.AT[l,2]==b)-\
    sum(model.BB[s]*model.v[b]**2 for s in model.SHUNT if (b,s) in model.SHUNTbs)
model.KCL_real     = Constraint(model.B, rule=KCL_real_def)
model.KCL_reactive = Constraint(model.B, rule=KCL_reactive_def)

# --- Kirchoff's voltage law on each line ---
def KVL_real_fromend(model,l):
    return model.pLfrom[l] == (model.G11[l]*(model.v[model.A[l,1]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.B12[l]*sin(model.delta[model.A[l,1]]-\
    model.delta[model.A[l,2]])+model.G12[l]*cos(model.delta[model.A[l,1]]-model.delta[model.A[l,2]])))
def KVL_real_toend(model,l):
    return model.pLto[l] == (model.G22[l]*(model.v[model.A[l,2]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.B21[l]*sin(model.delta[model.A[l,2]]-\
    model.delta[model.A[l,1]])+model.G21[l]*cos(model.delta[model.A[l,2]]-model.delta[model.A[l,1]])))
def KVL_reactive_fromend(model,l):
    return model.qLfrom[l] == (-model.B11[l]*(model.v[model.A[l,1]]**2)+\
    model.v[model.A[l,1]]*model.v[model.A[l,2]]*(model.G12[l]*sin(model.delta[model.A[l,1]]-\
    model.delta[model.A[l,2]])-model.B12[l]*cos(model.delta[model.A[l,1]]-model.delta[model.A[l,2]])))
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
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,1] in model.Bvolt):
        return model.pLfromT[l] == (model.g[l]/(model.tap[l]**2))*(model.v[model.AT[l,1]]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])+model.g[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
    else:
        return model.pLfromT[l] == (model.g[l]/(model.Tap[l]**2))*(model.v[model.AT[l,1]]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])+model.g[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
def KVL_real_toendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,1] in model.Bvolt):
        return model.pLtoT[l] == model.g[l]*(model.v[model.AT[l,2]]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,2]]-\
        model.delta[model.AT[l,1]])+model.g[l]*cos(model.delta[model.AT[l,2]]-model.delta[model.AT[l,1]]))
    else:
        return model.pLtoT[l] == model.g[l]*(model.v[model.AT[l,2]]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.b[l]*sin(model.delta[model.AT[l,2]]-\
        model.delta[model.AT[l,1]])+model.g[l]*cos(model.delta[model.AT[l,2]]-model.delta[model.AT[l,1]]))
def KVL_reactive_fromendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,1] in model.Bvolt):
        return model.qLfromT[l] == -(model.b[l]+0.5*model.bC[l])*(model.v[model.AT[l,1]]**2)/(model.tap[l]**2)-\
        (1/model.tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.g[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])-model.b[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
    else:
        return model.qLfromT[l] == -(model.b[l]+0.5*model.bC[l])*(model.v[model.AT[l,1]]**2)/(model.Tap[l]**2)-\
        (1/model.Tap[l])*model.v[model.AT[l,1]]*model.v[model.AT[l,2]]*(model.g[l]*sin(model.delta[model.AT[l,1]]-\
        model.delta[model.AT[l,2]])-model.b[l]*cos(model.delta[model.AT[l,1]]-model.delta[model.AT[l,2]]))
def KVL_reactive_toendTransf(model,l):
    if (model.AT[l,1] in model.Bvolt) or (model.AT[l,1] in model.Bvolt):
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

# --- generator power limits ---
def Real_Power_up(model,g):
    if g in model.DistSlack:
        return model.pG[g] <= model.PG[g]+model.epsPG_up[g]
    else:
        return model.pG[g] <= model.PG[g]
def Real_Power_down(model,g):
    if g in model.DistSlack:
        return model.pG[g] >= model.PG[g]-model.epsPG_down[g]
    else:
        return model.pG[g] >= model.PG[g]
model.PGmaxC = Constraint(model.G-model.g0, rule=Real_Power_up)
model.PGminC = Constraint(model.G-model.g0, rule=Real_Power_down)

# ---wind generator power limits ---
def Wind_Real_Power_up(model,w):
    return model.pW[w] <= model.WG[w]
def Wind_Real_Power_down(model,w):
    return model.pW[w] >= model.WG[w]
model.WGmaxC  = Constraint(model.WIND, rule=Wind_Real_Power_up)
model.WGminC  = Constraint(model.WIND, rule=Wind_Real_Power_down)


# --- voltage target constraints ---
def bus_max_voltage(model,b,g):
    return model.v[b] <= model.VS[g]+model.epsV_up[g]
def bus_min_voltage(model,b,g):
    return model.v[b] >= model.VS[g]-model.epsV_down[g]
model.Vmaxc = Constraint(model.Gbs, rule=bus_max_voltage)
model.Vminc = Constraint(model.Gbs, rule=bus_min_voltage)

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
model.VoltRegC  = Constraint(model.Bvolt, rule=volt_reg)
model.VoltRegC2 = Constraint(model.Bvolt, rule=volt_reg2)

# --- reference bus constraint ---
def ref_bus_def(model,b):
    return model.delta[b]==0
model.refbus = Constraint(model.b0, rule=ref_bus_def)
