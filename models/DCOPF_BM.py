#==================================================================
# DCOPF.mod
# PYOMO model file of "DC" optimal power flow problem (DCOPF)
# This formulation uses the standard "DC" linearization of the AC power flow equations
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2017 by W Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

#==========Import==========
from __future__ import division
from pyomo.environ import *
#==========================

model = AbstractModel()

# --- SETS ---
model.B      = Set()  # set of buses
model.G      = Set()  # set of generators
model.WIND   = Set()  # set of wind generators
model.D      = Set()  # set of demands
model.L      = Set()  # set of lines
model.SHUNT  = Set()  # set of shunts
model.b0     = Set(within=model.B)  # set of reference buses
model.LE     = Set()  # line-to and from ends set (1,2)
model.TRANSF = Set()  # set of transformers

# generators, buses, loads linked to each bus b
model.Gbs     = Set(within=model.B * model.G)    # set of generator-bus mapping
model.Wbs     = Set(within=model.B * model.WIND) # set of wind-bus mapping
model.Dbs     = Set(within=model.B * model.D)    # set of demand-bus mapping
model.SHUNTbs = Set(within=model.B*model.SHUNT)  # set of shunt-bus mapping

# --- parameters ---
# line matrix
model.A     = Param(model.L*model.LE)       # bus-line matrix
model.AT    = Param(model.TRANSF*model.LE)  # bus-transformer matrix

# demands
model.PD      = Param(model.D, within=Reals)  # real power demand
model.VOLL    = Param(model.D, within=Reals)  # value of lost load
# generators
model.PGmax    = Param(model.G, within=NonNegativeReals) # max real power of generator, p.u.
model.PGmin    = Param(model.G, within=Reals)            # min real power of generator, p.u.
model.WGmax    = Param(model.WIND, within=NonNegativeReals) # max real power of wind generator, p.u.
model.WGmin    = Param(model.WIND, within=NonNegativeReals) # min real power of wind generator, p.u.

# lines and transformer chracteristics and ratings
model.SLmax  = Param(model.L, within=NonNegativeReals)      # real power line limit
model.SLmaxT = Param(model.TRANSF, within=NonNegativeReals) # real power transformer limit
model.BL     = Param(model.L, within=Reals)       # susceptance of a line
model.BLT    = Param(model.TRANSF, within=Reals)  # susceptance of a transformer

# shunt
model.GB = Param(model.SHUNT, within=Reals) #  shunt conductance
model.BB = Param(model.SHUNT, within=Reals) #  shunt susceptance

# cost data
model.bidG      = Param(model.G, within=Reals)    # generator bid price
model.offerG    = Param(model.G, within=Reals)    # generator offer price
model.bidW      = Param(model.WIND, within=Reals) # wind bid price
model.c2    = Param(model.G, within=NonNegativeReals)# generator cost coefficient c2 (*pG^2)
model.c1    = Param(model.G, within=NonNegativeReals)# generator cost coefficient c1 (*pG)
model.c0    = Param(model.G, within=NonNegativeReals)# generator cost coefficient c0

#FPNs
model.PG      = Param(model.G, within=NonNegativeReals)    # FPN
model.PW      = Param(model.WIND, within=NonNegativeReals) # FPN

model.baseMVA = Param(within=NonNegativeReals)# base MVA

#constants
model.eps = Param(within=NonNegativeReals)

# --- control variables ---
model.pG     = Var(model.G,  domain= Reals)  #real power generation
model.pGUp   = Var(model.G,  domain= NonNegativeReals)  #re-dispatch upwards
model.pGDown = Var(model.G,  domain= NonNegativeReals)  #re-dispatch downwards

model.pW     = Var(model.WIND, domain= Reals) #real power generation from wind
model.pWDown = Var(model.WIND, domain= NonNegativeReals) #re-dispatch downwards


model.pD    = Var(model.D, domain= Reals) #real power demand delivered
model.alpha = Var(model.D, domain= NonNegativeReals) #propotion of real power demand delivered
# --- state variables ---
model.deltaL  = Var(model.L, domain= Reals)      # angle difference across lines
model.deltaLT = Var(model.TRANSF, domain= Reals) # angle difference across transformers
model.delta   = Var(model.B, domain= Reals, initialize=0.0) # voltage phase angle at bus b, rad
model.pL      = Var(model.L, domain= Reals) # real power injected at b onto line l, p.u.
model.pLT     = Var(model.TRANSF, domain= Reals) # real power injected at b onto transformer line l, p.u.

# --- cost function ---
def objective(model):
    obj = sum(model.offerG[g]*(model.baseMVA*model.pGUp[g])+model.bidG[g]*(model.baseMVA*model.pGDown[g]) for g in model.G) +\
    sum(model.bidW[w]*(model.baseMVA*model.pWDown[w]) for w in model.WIND) +\
    sum(model.VOLL[d]*(1-model.alpha[d])*model.baseMVA*model.PD[d] for d in model.D)
    return obj
model.OBJ = Objective(rule=objective, sense=minimize)

# --- Kirchoff's current law at each bus b ---
def KCL_def(model, b):
    return sum(model.pG[g] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.pW[w] for w in model.WIND if (b,w) in model.Wbs) == \
    sum(model.pD[d] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.pL[l] for l in model.L if model.A[l,1]==b)- \
    sum(model.pL[l] for l in model.L if model.A[l,2]==b)+\
    sum(model.pLT[l] for l in model.TRANSF if model.AT[l,1]==b)- \
    sum(model.pLT[l] for l in model.TRANSF if model.AT[l,2]==b)+\
    sum(model.GB[s] for s in model.SHUNT if (b,s) in model.SHUNTbs)
model.KCL_const = Constraint(model.B, rule=KCL_def)


# --- FPN model ---
def Generator_redispatch(model,g):
    return model.pG[g] == model.PG[g]+model.pGUp[g]-model.pGDown[g]
def Wind_redispatch(model,w):
    return model.pW[w] == model.PW[w]-model.pWDown[w]

model.RedispatcG = Constraint(model.G, rule=Generator_redispatch)
model.RedispatcW = Constraint(model.WIND, rule=Wind_redispatch)


# --- Kirchoff's voltage law on each line and transformer---
def KVL_line_def(model,l):
    return model.pL[l] == (-model.BL[l])*model.deltaL[l]
def KVL_trans_def(model,l):
    return model.pLT[l] == (-model.BLT[l])*model.deltaLT[l]
model.KVL_line_const     = Constraint(model.L, rule=KVL_line_def)
model.KVL_trans_const    = Constraint(model.TRANSF, rule=KVL_trans_def)

# --- demand model ---
def demand_model(model,d):
    return model.pD[d] == model.alpha[d]*model.PD[d]
def demand_LS_bound_Max(model,d):
    return model.alpha[d] <= 1
model.demandmodelC = Constraint(model.D, rule=demand_model)
model.demandalphaC = Constraint(model.D, rule=demand_LS_bound_Max)

# --- generator power limits ---
def Real_Power_Max(model,g):
    return model.pG[g] <= model.PGmax[g]
def Real_Power_Min(model,g):
    return model.pG[g] >= model.PGmin[g]

model.PGmaxC = Constraint(model.G, rule=Real_Power_Max)
model.PGminC = Constraint(model.G, rule=Real_Power_Min)

# ---wind generator power limits ---
def Wind_Real_Power_Max(model,w):
    return model.pW[w] <= model.WGmax[w]
def Wind_Real_Power_Min(model,w):
    return model.pW[w] >= model.WGmin[w]
model.WGmaxC = Constraint(model.WIND, rule=Wind_Real_Power_Max)
model.WGminC = Constraint(model.WIND, rule=Wind_Real_Power_Min)

# --- line power limits ---
def line_lim1_def(model,l):
    return model.pL[l] <= model.SLmax[l]
def line_lim2_def(model,l):
    return model.pL[l] >= -model.SLmax[l]
model.line_lim1 = Constraint(model.L, rule=line_lim1_def)
model.line_lim2 = Constraint(model.L, rule=line_lim2_def)

# --- power flow limits on transformer lines---
def transf_lim1_def(model,l):
    return model.pLT[l] <= model.SLmaxT[l]
def transf_lim2_def(model,l):
    return model.pLT[l] >= -model.SLmaxT[l]
model.transf_lim1 = Constraint(model.TRANSF, rule=transf_lim1_def)
model.transf_lim2 = Constraint(model.TRANSF, rule=transf_lim2_def)

# --- phase angle constraints ---
def phase_angle_diff1(model,l):
    return model.deltaL[l] == model.delta[model.A[l,1]] - \
    model.delta[model.A[l,2]]
model.phase_diff1 = Constraint(model.L, rule=phase_angle_diff1)

# --- reference bus constraint ---
def ref_bus_def(model,b):
    return model.delta[b]==0
model.refbus = Constraint(model.b0, rule=ref_bus_def)
