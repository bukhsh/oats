#==================================================================
# DCLF.mod
# PYOMO model file of "DC" load flow problem (DCLF)
# This formulation uses the standard "DC" linearization of the AC power flow equations
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W Bukhsh, Glasgow, Scotland
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
model.A     = Param(model.L*model.LE)       # bus-line (node-arc) matrix
model.AT    = Param(model.TRANSF*model.LE)  # bus-transformer (node-arc) matrix

# demands
model.PD      = Param(model.D, within=Reals)  # real power demand
model.VOLL    = Param(model.D, within=Reals)  # value of lost load

# generators
model.PG    = Param(model.G, within=Reals)    # real power set-point of generator
model.WG    = Param(model.WIND, within=NonNegativeReals) # real power set-point of wind generator

# lines and transformer chracteristics
model.BL  = Param(model.L, within=Reals)        # susceptance of a line
model.BLT = Param(model.TRANSF, within=Reals)  # susceptance of a transformer
model.Tap = Param(model.TRANSF, within=NonNegativeReals)  # turns ratio of transformer

# shunt
model.GB = Param(model.SHUNT, within=Reals) #  shunt conductance
model.BB = Param(model.SHUNT, within=Reals) #  shunt susceptance

model.baseMVA = Param(within=NonNegativeReals)# base MVA

#constants
model.eps = Param(within=NonNegativeReals)


# --- control variables ---
model.pG    = Var(model.G, domain= Reals) #real power generation
model.pW    = Var(model.WIND, domain= Reals)         #real power generation from wind
model.pD    = Var(model.D, domain= Reals)            #real power demand delivered
model.alpha = Var(model.D, domain= NonNegativeReals) #propotion of real power demand delivered
# --- state variables ---
model.deltaL  = Var(model.L, domain= Reals)      # angle difference across lines
model.deltaLT = Var(model.TRANSF, domain= Reals) # angle difference across transformers
model.delta   = Var(model.B, domain= Reals, initialize=0.0) # voltage phase angle at bus b, rad
model.pL      = Var(model.L, domain= Reals)      # real power injected at b onto line l
model.pLT     = Var(model.TRANSF, domain= Reals) # real power injected at b onto transformer line l
# --- variables that model small violations on PG values. this is to help with the convergence
model.epsG_up      = Var(model.G, domain= NonNegativeReals)
model.epsG_down    = Var(model.G, domain= NonNegativeReals)
model.epsW_up      = Var(model.WIND, domain= NonNegativeReals)
model.epsW_down    = Var(model.WIND, domain= NonNegativeReals)

# --- cost function ---
def objective(model):
    obj = sum(model.baseMVA*(model.epsG_down[g]+model.epsG_up[g]) for (b,g) in model.Gbs if b not in model.b0)+\
    sum(model.baseMVA*(model.epsW_down[w]+model.epsW_up[w]) for w in model.WIND)+\
    sum(model.baseMVA*model.VOLL[d]*(1-model.alpha[d])*model.PD[d] for d in model.D)
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

# --- Kirchoff's voltage law at each line and transformer---
def KVL_line_def(model,l):
    return model.pL[l] == (-model.BL[l])*model.deltaL[l]
def KVL_trans_def(model,l):
    return model.pLT[l] == (-model.BLT[l]/model.Tap[l])*model.deltaLT[l]
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
    return model.pG[g] <= model.PG[g]+model.epsG_up[g]
def Real_Power_Min(model,g):
    return model.pG[g] >= model.PG[g]-model.epsG_down[g]
model.PGmaxC = Constraint(model.G, rule=Real_Power_Max)
model.PGminC = Constraint(model.G, rule=Real_Power_Min)

# ---wind generator power limits ---
def Wind_Real_Power_Max(model,w):
    return model.pW[w] <= model.WG[w]+model.epsW_up[w]
def Wind_Real_Power_Min(model,w):
    return model.pW[w] >= model.WG[w]+model.epsW_up[w]
model.WGmaxC = Constraint(model.WIND, rule=Wind_Real_Power_Max)
model.WGminC = Constraint(model.WIND, rule=Wind_Real_Power_Min)

# --- phase angle constraints ---
def phase_angle_diff1(model,l):
    return model.deltaL[l] == model.delta[model.A[l,1]] - \
    model.delta[model.A[l,2]]
model.phase_diff1 = Constraint(model.L, rule=phase_angle_diff1)

# --- reference bus constraint ---
def ref_bus_def(model,b):
    return model.delta[b]==0
model.refbus = Constraint(model.b0, rule=ref_bus_def)
