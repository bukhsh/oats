#==================================================================
# SCOPF.mod
# PYOMO model file of "DC" Security constrained-optimal power flow problem (SCOPF)
# This formulation uses the standard "DC" model of AC power flow equations
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
model.B      = Set()  # set of buses, as a list of positive integers
model.G      = Set()  # set of generators, as a list of positive integers
model.WIND   = Set()  # set of wind generators, as a list of positive integers
model.D      = Set()  # set of demands, as a list of positive integers
model.L      = Set()  # set of lines, as a list of positive integers
model.TRANSF = Set()  # set of transformers, as a list of positive integers
model.SHUNT  = Set()  # set of shunts, as a list of positive integers
model.LE     = Set()  # line-to and from ends set (1,2)
model.b0     = Set(within=model.B)  # set of reference buses
model.C      = Set()  # set of contigencies

# set of contingencies
model.CL     = Set(within=model.C * model.L)# set of line contigencies
model.CG     = Set(within=model.C * model.G)# set of generator contigencies
model.CT     = Set(within=model.C * model.TRANSF)# set of transformer contigencies
model.CWIND  = Set(within=model.C * model.WIND)# set of wind generator contigencies

# generators, buses, loads linked to each bus b
model.Gbs     = Set(within=model.B * model.G)    # set of generator-node mapping
model.Wbs     = Set(within=model.B * model.WIND) # set of wing-node mapping
model.Dbs     = Set(within=model.B * model.D)    # set of demand-node mapping
model.SHUNTbs = Set(within=model.B*model.SHUNT)  # set of shunt-node mapping

# --- parameters ---
# line matrix
model.A     = Param(model.L*model.LE)       # bus-line (node-arc) matrix
model.AT    = Param(model.TRANSF*model.LE)  # bus-transformer (node-arc) matrix

# demands
model.PD      = Param(model.D, within=Reals)  # real power demand at load d, p.u.
model.VOLL    = Param(model.D, within=Reals)
# generators
model.PGmax    = Param(model.G, within=Reals)# max real power of generator, p.u.
model.PGmin    = Param(model.G, within=Reals)# min real power of generator, p.u.
model.WGmax    = Param(model.WIND, within=NonNegativeReals)# max real power of wind generator, p.u.
model.WGmin    = Param(model.WIND, within=NonNegativeReals)# min real power of wind generator, p.u.
model.RampUp   = Param(model.G, within=NonNegativeReals) # ramp up of generator g, p.u.
model.RampDown = Param(model.G, within=NonNegativeReals) # ramp down of generator g, p.u.

# lines and transformer chracteristics and ratings
model.SLmax  = Param(model.L, within=NonNegativeReals) # max real power limit on flow in a line, p.u.
model.SLmaxT = Param(model.TRANSF, within=NonNegativeReals) # max real power limit on flow in line l, p.u.
model.BL     = Param(model.L, within=Reals)  # susceptance of a line, p.u.
model.BLT    = Param(model.TRANSF, within=Reals)  # susceptance of line l, p.u.
#emergency ratings
model.SLmax_E  = Param(model.L, within=NonNegativeReals) # max emergency real power limit on flow in a line, p.u.
model.SLmaxT_E = Param(model.TRANSF, within=NonNegativeReals) # max emergency real power limit on flow in a line, p.u.

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
model.PG      = Param(model.G, within=Reals)    # FPN
model.PW      = Param(model.WIND, within=NonNegativeReals) # FPN

model.baseMVA = Param(within=NonNegativeReals)# base MVA

#constants
model.eps = Param(within=NonNegativeReals)
model.nT = Param(within=NonNegativeReals) #total time horizon
model.probC = Param(model.C, domain=NonNegativeReals) #total time horizon

# === Pre-contigency variables ===
# --- control variables ---
model.pG      = Var(model.G, domain= Reals)  #real power generation
model.pGUp    = Var(model.G,  domain= NonNegativeReals)  #re-dispatch upwards
model.pGDown  = Var(model.G,  domain= NonNegativeReals)  #re-dispatch downwards

model.pW      = Var(model.WIND, domain= Reals) #real power generation from wind
model.pWDown  = Var(model.WIND, domain= NonNegativeReals) #re-dispatch downwards

model.pD      = Var(model.D, domain= Reals) #real power demand delivered
model.alpha   = Var(model.D, domain= NonNegativeReals) #propotion of real power demand delivered
# --- state variables ---
model.deltaL  = Var(model.L, domain= Reals) # angle difference across lines
model.deltaLT = Var(model.TRANSF, domain= Reals) # angle difference across transformers
model.delta   = Var(model.B, domain= Reals, initialize=0.0) # voltage phase angle at bus b, rad
model.pL      = Var(model.L, domain= Reals) # real power injected at b onto line l, p.u.
model.pLT     = Var(model.TRANSF, domain= Reals) # real power injected at b onto transformer line l, p.u.

# === Post-contigency variables ===
# --- control variables ---
model.pGC          = Var(model.G,model.C, domain= Reals)  #post-fault generation set point
model.pGCUp        = Var(model.G,model.C, domain= NonNegativeReals)  #post-fault generation set point
model.pGCDown      = Var(model.G,model.C, domain= NonNegativeReals)  #post-fault generation set point

model.DeltapG      = Var(model.G,model.C, domain= Reals)  #change in pre-fault generation set point following a contingency
model.DeltapGUp    = Var(model.G,model.C, domain= NonNegativeReals)  #positive change in pre-fault generation set point
model.DeltapGDown  = Var(model.G,model.C, domain= NonNegativeReals)  #negative change in pre-fault generation set point

model.pWC          = Var(model.WIND,model.C, domain= Reals) #post-fault wind generation
model.pWCDown      = Var(model.WIND,model.C, domain= NonNegativeReals) #post-fault wind generation

model.DeltapW      = Var(model.WIND,model.C, domain= Reals) #change in pre-fault generation set point following a contingency
model.DeltapWDown  = Var(model.WIND,model.C, domain= NonNegativeReals) #negative change in pre-fault generation set point(wind can only move downwards)

model.pDC    = Var(model.D,model.C, domain= Reals) #real power demand delivered post-contingency
model.alphaC = Var(model.D,model.C, domain= NonNegativeReals) #propotion of real power demand delivered post-contingency

# --- state variables ---
model.pLC      = Var(model.L,model.C, domain= Reals) # real power injected at b onto line l, p.u.
model.pLTC     = Var(model.TRANSF,model.C, domain= Reals) # real power injected at b onto transformer l, p.u.
model.deltaLC  = Var(model.L,model.C, domain= Reals) # angle difference across lines
model.deltaLTC = Var(model.TRANSF,model.C, domain= Reals) # angle difference across transformers
model.deltaC   = Var(model.B,model.C, domain= Reals, initialize=0.0) # voltage phase angle at bus b, rad

# --- pre- and post- contingency costs
model.FPreCont  = Var() # Objective function component for pre-contingency operation
model.FPostCont = Var(model.C) # Objective function component for post-contingency operation
# --- cost function ---
def objective(model):
    obj = model.FPreCont + 0.0*sum(model.FPostCont[c] for c in model.C)
    return obj
model.OBJ = Objective(rule=objective, sense=minimize)

# --- cost components of the objective function ---
def precontingency_cost(model):
    return model.FPreCont == sum(model.offerG[g]*(model.baseMVA*model.pGUp[g])+model.bidG[g]*(model.baseMVA*model.pGDown[g]) for g in model.G) +\
    sum(model.bidW[w]*(model.baseMVA*model.pWDown[w]) for w in model.WIND) +\
    sum(model.VOLL[d]*(1-model.alpha[d])*model.baseMVA*model.PD[d] for d in model.D)
model.precontingency_cost_const = Constraint(rule=precontingency_cost)

def postcontingency_cost(model,c):
    return model.FPostCont[c] == sum(model.offerG[g]*(model.baseMVA*model.pGCUp[g,c])+model.bidG[g]*(model.baseMVA*model.pGCDown[g,c]) for g in model.G) +\
    sum(model.bidW[w]*(model.baseMVA*model.pWCDown[w,c]) for w in model.WIND) +\
    sum(model.VOLL[d]*(1-model.alphaC[d,c])*model.baseMVA*model.PD[d] for d in model.D)
model.postcontingency_cost_const = Constraint(model.C, rule=postcontingency_cost)


# --- Kirchoff's current law Definition at each bus b ---
def KCL_def(model, b):
    return sum(model.pG[g] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.pW[w] for w in model.WIND if (b,w) in model.Wbs) == \
    sum(model.pD[d] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.pL[l] for l in model.L if model.A[l,1]==b)- \
    sum(model.pL[l] for l in model.L if model.A[l,2]==b)+\
    sum(model.pLT[l] for l in model.TRANSF if model.AT[l,1]==b)- \
    sum(model.pLT[l] for l in model.TRANSF if model.AT[l,2]==b)+\
    sum(model.GB[s] for s in model.SHUNT if (b,s) in model.SHUNTbs)
# the next line creates one KCL constraint for each bus
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
#the next two lines creates KVL constraints for each line and transformer, respectively.
model.KVL_line_const     = Constraint(model.L, rule=KVL_line_def)
model.KVL_trans_const    = Constraint(model.TRANSF, rule=KVL_trans_def)

# --- demand model ---
def demand_model(model,d):
    return model.pD[d] == model.alpha[d]*model.PD[d]
def demand_LS_bound_Max(model,d):
    return model.alpha[d] <= 1
#the next two lines creates constraints for demand model
model.demandmodelC = Constraint(model.D, rule=demand_model)
model.demandalphaC = Constraint(model.D, rule=demand_LS_bound_Max)

# --- generator power limits ---
def Real_Power_Max(model,g):
    return model.pG[g] <= model.PGmax[g]
def Real_Power_Min(model,g):
    return model.pG[g] >= model.PGmin[g]
#the next two lines creates generation bounds for each generator.
model.PGmaxC = Constraint(model.G, rule=Real_Power_Max)
model.PGminC = Constraint(model.G, rule=Real_Power_Min)

# ---wind generator power limits ---
def Wind_Real_Power_Max(model,w):
    return model.pW[w] <= model.WGmax[w]
def Wind_Real_Power_Min(model,w):
    return model.pW[w] >= model.WGmin[w]
#the next two lines creates generation bounds for each generator.
model.WGmaxC = Constraint(model.WIND, rule=Wind_Real_Power_Max)
model.WGminC = Constraint(model.WIND, rule=Wind_Real_Power_Min)

# --- line power limits ---
def line_lim1_def(model,l):
    return model.pL[l] <= model.SLmax[l]
def line_lim2_def(model,l):
    return model.pL[l] >= -model.SLmax[l]
#the next two lines creates line flow constraints for each line.
model.line_lim1 = Constraint(model.L, rule=line_lim1_def)
model.line_lim2 = Constraint(model.L, rule=line_lim2_def)

# --- power flow limits on transformer lines---
def transf_lim1_def(model,l):
    return model.pLT[l] <= model.SLmaxT[l]
def transf_lim2_def(model,l):
    return model.pLT[l] >= -model.SLmaxT[l]
#the next two lines creates line flow constraints for each transformer.
model.transf_lim1 = Constraint(model.TRANSF, rule=transf_lim1_def)
model.transf_lim2 = Constraint(model.TRANSF, rule=transf_lim2_def)

# --- phase angle constraints ---
def phase_angle_diff1(model,l):
    return model.deltaL[l] == model.delta[model.A[l,1]] - \
    model.delta[model.A[l,2]]
model.phase_diff1 = Constraint(model.L, rule=phase_angle_diff1)

# --- phase angle constraints ---
def phase_angle_diff2(model,l):
    return model.deltaLT[l] == model.delta[model.AT[l,1]] - \
    model.delta[model.AT[l,2]]
model.phase_diff2 = Constraint(model.TRANSF, rule=phase_angle_diff2)

# --- reference bus constraint ---
def ref_bus_def(model,b):
    return model.delta[b]==0
model.refbus = Constraint(model.b0, rule=ref_bus_def)

#======Post-contingency constraints======
# --- Kirchoff's current law Definition at each bus b ---
def KCL_def_PostCnt(model, b,c):
    return sum(model.pGC[g,c] for g in model.G if (b,g) in model.Gbs) +\
    sum(model.pWC[w,c] for w in model.WIND if (b,w) in model.Wbs) == \
    sum(model.pDC[d,c] for d in model.D if (b,d) in model.Dbs)+\
    sum(model.pLC[l,c] for l in model.L if model.A[l,1]==b)- \
    sum(model.pLC[l,c] for l in model.L if model.A[l,2]==b)+\
    sum(model.pLTC[l,c] for l in model.TRANSF if model.AT[l,1]==b)- \
    sum(model.pLTC[l,c] for l in model.TRANSF if model.AT[l,2]==b)+\
    sum(model.GB[s] for s in model.SHUNT if (b,s) in model.SHUNTbs)
# the next line creates one KCL constraint for each bus
model.KCL_const_PostCnt = Constraint(model.B,model.C, rule=KCL_def_PostCnt)

# --- FPN model ---
def Generator_redispatch_C(model,g,c):
    return model.pGC[g,c] == model.PG[g]+model.pGUp[g]-model.pGDown[g]
def Wind_redispatch_C(model,w,c):
    return model.pWC[w,c] == model.PW[w]-model.pWDown[w]

model.RedispatcGC = Constraint(model.G,model.C, rule=Generator_redispatch_C)
model.RedispatcWC = Constraint(model.WIND,model.C, rule=Wind_redispatch_C)

# --- Kirchoff's voltage law on each line ---
def KVL_line_def_PostCnt(model,l,c):
    if (c,l) in model.CL:
        return model.pLC[l,c] == 0
    else:
        return model.pLC[l,c] == (-model.BL[l])*model.deltaLC[l,c]
def KVL_trans_def_PostCnt(model,l,c):
    if (c,l) in model.CT:
        return model.pLTC[l,c] == 0
    else:
        return model.pLTC[l,c] == (-model.BLT[l])*model.deltaLTC[l,c]
#the next two lines create KVL constraints for each line and transformer, respectively.
model.KVL_line_const_PostCnt     = Constraint(model.L,model.C, rule=KVL_line_def_PostCnt)
model.KVL_trans_const_PostCnt    = Constraint(model.TRANSF,model.C, rule=KVL_trans_def_PostCnt)

# --- change in generation set point---
def change_generation_postcont(model,g,c):
    return model.pGC[g,c] == model.pG[g]+model.DeltapG[g,c]
def change_generation_direction_postcont(model,g,c):
    return model.DeltapG[g,c] == model.DeltapGUp[g,c]-model.DeltapGDown[g,c]
#the next two lines creates constraints for modelling the change in generation from pre-contingency operating point
model.change_generation_postcontC = Constraint(model.G,model.C, rule=change_generation_postcont)
model.change_generation_direction_postcontC = Constraint(model.G,model.C, rule=change_generation_direction_postcont)

# --- change in wind generation set point---
def change_windgeneration_postcont(model,w,c):
    return model.pWC[w,c] == model.pW[w]+model.DeltapW[w,c]
def change_windgeneration_direction_postcont(model,w,c):
    return model.DeltapW[w,c] == -model.DeltapWDown[w,c]
#the next two lines creates constraints for modelling the change in wind generation from pre-contingency operating point
model.change_windgeneration_postcontC = Constraint(model.WIND,model.C, rule=change_windgeneration_postcont)
model.change_windgeneration_direction_postcontC = Constraint(model.WIND,model.C, rule=change_windgeneration_direction_postcont)

# --- demand model (post-contingency)---
def demand_model_postcont(model,d,c):
    return model.pDC[d,c] == model.alphaC[d,c]*model.PD[d]
def demand_LS_bound_Max_postcont(model,d,c):
    return model.alphaC[d,c] <= 1
#the next two lines creates constraints for demand model
model.demandmodel_postcontC = Constraint(model.D,model.C, rule=demand_model_postcont)
model.demandalpha_postcontC = Constraint(model.D,model.C, rule=demand_LS_bound_Max_postcont)

# --- generator power limits ---
def Real_Power_Max_PostCnt(model,g,c):
    if (c,g) in model.CG:
        return model.pGC[g,c] == 0
    else:
        return model.pGC[g,c] <= model.PGmax[g]
def Real_Power_Min_PostCnt(model,g,c):
    if (c,g) in model.CG:
        return model.pGC[g,c] == 0
    else:
        return model.pGC[g,c] >= model.PGmin[g]
#the next two lines create constraints on real power generation bounds
model.PGmaxC_PostCnt = Constraint(model.G,model.C, rule=Real_Power_Max_PostCnt)
model.PGminC_PostCnt = Constraint(model.G,model.C, rule=Real_Power_Min_PostCnt)

# --- wind generator power limits ---
def Wind_Real_Power_Max_PostCnt(model,w,c):
    if (c,w) in model.CWIND:
        return model.pWC[w,c] == 0
    else:
        return model.pWC[w,c] <= model.WGmax[w]
def Wind_Real_Power_Min_PostCnt(model,w,c):
    if (c,w) in model.CWIND:
        return model.pWC[w,c] == 0
    else:
        return model.pWC[w,c] >= model.WGmin[w]
#the next two lines create constraints on real power generation bounds
model.WPGmaxC_PostCnt = Constraint(model.WIND,model.C, rule=Wind_Real_Power_Max_PostCnt)
model.WPGminC_PostCnt = Constraint(model.WIND,model.C, rule=Wind_Real_Power_Min_PostCnt)

# --- line power limits ---
def line_lim1_def_PostCnt(model,l,c):
    return model.pLC[l,c] <= model.SLmax[l]
def line_lim2_def_PostCnt(model,l,c):
    return model.pLC[l,c] >= -model.SLmax[l]
#the next two lines create line flow constraints for each line.
model.line_lim1_PostCnt = Constraint(model.L,model.C, rule=line_lim1_def_PostCnt)
model.line_lim2_PostCnt = Constraint(model.L,model.C, rule=line_lim2_def_PostCnt)

# --- power flow limits on transformer lines---
def transf_lim1_def_PostCnt(model,l,c):
    return model.pLTC[l,c] <= model.SLmaxT[l]
def transf_lim2_def_PostCnt(model,l,c):
    return model.pLTC[l,c] >= -model.SLmaxT[l]
#the next two lines create line flow constraints for each transformer.
model.transf_lim1_PostCnt = Constraint(model.TRANSF,model.C, rule=transf_lim1_def_PostCnt)
model.transf_lim2_PostCnt = Constraint(model.TRANSF,model.C, rule=transf_lim2_def_PostCnt)

# --- phase angle constraints ---
def phase_angle_diff1_PostCnt(model,l,c):
    return model.deltaLC[l,c] == model.deltaC[model.A[l,1],c] - \
    model.deltaC[model.A[l,2],c]
#the next line creates a constraint to link angle difference across a line.
model.phase_diff1_PostCnt = Constraint(model.L,model.C, rule=phase_angle_diff1_PostCnt)

# --- phase angle constraints ---
def phase_angle_diff2_PostCnt(model,l,c):
    return model.deltaLTC[l,c] == model.deltaC[model.AT[l,1],c] - \
    model.deltaC[model.AT[l,2],c]
#the next line creates a constraint to link angle difference across a transformer.
model.phase_diff2_PostCnt = Constraint(model.TRANSF,model.C, rule=phase_angle_diff2_PostCnt)

# --- reference bus constraint ---
def ref_bus_def_PostCnt(model,b,c):
    return model.deltaC[b,c]==0
model.refbus_PostCnt = Constraint(model.b0,model.C, rule=ref_bus_def_PostCnt)

#======Pre-contingency and Post-contingency linking constraints======
def generation_link_rampUp_def(model,g,c):
    if (c,g) in model.CG:
        return model.pGC[g,c] == 0
    else:
        return model.DeltapG[g,c]<=model.RampUp[g]
def generation_link_rampDown_def(model,g,c):
    if (c,g) in model.CG:
        return model.pGC[g,c] == 0
    else:
        return model.DeltapG[g,c]>=-model.RampDown[g]
model.generation_link_rampUp_const   = Constraint(model.G,model.C, rule=generation_link_rampUp_def)
model.generation_link_rampDown_const = Constraint(model.G,model.C, rule=generation_link_rampDown_def)
