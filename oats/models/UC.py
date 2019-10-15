#==================================================================
# UC.py
# PYOMO model file of unit commitment problem
# ---Author---
# W. Bukhsh,
# wbukhsh@gmail.com
# OATS
# Copyright (c) 2015 by W. Bukhsh, Glasgow, Scotland
# OATS is distributed under the GNU GENERAL PUBLIC LICENSE v3. (see LICENSE file for details).
#==================================================================

#==========Import==========
from __future__ import division
from pyomo.environ import *
#==========================

model = AbstractModel()

# --- SETS ---
model.Z      = Set()  # set of zones
model.G      = Set()  # set of generators
model.WIND   = Set()  # set of wind generators
model.D      = Set()  # set of loads
model.T      = Set()  # set of time periods, as a list of positive integers
model.ICT    = Set()  # set of interconnections between zone
model.TRed   = Set()  # set of time periods T={1,...,N-1} ignoring last time period-req for ramp
model.SHUNT  = Set()  # set of shunts
model.LE     = Set()  # line-to and from ends set (1,2)
model.S      = Set()  # set of storage

## mapping sets
model.GZ  = Set(within=model.G*model.Z)     # set of generators and zones
model.WZ  = Set(within=model.WIND*model.Z)  # set of WIND abd zones
model.DZ  = Set(within=model.D*model.Z)     # set of demand and zones
model.SZ  = Set(within=model.SHUNT*model.Z) # set of shunts and zones
model.Sbs = Set(within=model.Z*model.S)    # set of storage-zone mapping

# UC Min Up and Min Down indexing sets
model.UCMinDownT   = Set(within=model.G*model.T*model.T) #indexing set for min down constraints
model.UCMinUpT     = Set(within=model.G*model.T*model.T) #indexing set for min up constraints
model.MinDownTime  = Param(model.G)
model.MinUpTime    = Param(model.G)

# --- parameters ---

# storage
model.StoreUB       = Param(model.S, within=NonNegativeReals)# max real power capacity of storage, p.u.
model.StoreLB       = Param(model.S, within=NonNegativeReals)# max real power capacity of storage, p.u.
model.StoreInitial  = Param(model.S, within=NonNegativeReals)# charging efficieny of storage
model.StoreFinal    = Param(model.S, within=NonNegativeReals)# charging efficieny of storage
model.ChargeEff     = Param(model.S, within=NonNegativeReals)# charging efficieny of storage
model.DischargeEff  = Param(model.S, within=NonNegativeReals)# charging efficieny of storage
model.RateCharge    = Param(model.S, within=NonNegativeReals)# rate of charging of storage
model.RateDischarge = Param(model.S, within=NonNegativeReals)# rate of charging of storage
model.rampCharge    = Param(model.S, within=NonNegativeReals)# storage cost for discharging
model.rampDischarge = Param(model.S, within=NonNegativeReals)# storage cost for discharging

# interconnector matrix
model.A = Param(model.ICT*model.LE)  # bus-line (node-arc) matrix
# demands
model.PD    = Param(model.D,model.T, within=Reals)  #real power demand
model.VOLL  = Param(model.D, within=Reals)          # Value of lost load
# generators
model.PGmax = Param(model.G, within=NonNegativeReals)# max real power of generator, p.u.
model.PGmin = Param(model.G, within=Reals)# min real power of generator, p.u.

#RES
model.WGmax = Param(model.WIND,model.T, within=NonNegativeReals)# max real power of wind generator, p.u.
model.WGmin = Param(model.WIND,model.T, within=NonNegativeReals)# min real power of wind generator, p.u.

# inter-connector
model.NTCto = Param(model.ICT, within=NonNegativeReals) # to NTC
model.NTCfr = Param(model.ICT, within=NonNegativeReals) # from NTC

#ramping rates
model.RampUp   = Param(model.G, within=NonNegativeReals)
model.RampDown = Param(model.G, within=NonNegativeReals)

# cost
model.c2 = Param(model.G, within=NonNegativeReals)# generator cost coefficient c2 (*pG^2)
model.c1 = Param(model.G, within=NonNegativeReals)# generator cost coefficient c1 (*pG)
model.c0 = Param(model.G, within=NonNegativeReals)# generator cost coefficient c0
model.SUcosts = Param(model.G, within=NonNegativeReals)# generator start-up cost
model.SDcosts = Param(model.G, within=NonNegativeReals)# generator shut-down cost

model.baseMVA = Param(within=NonNegativeReals)# base MVA

#constants
model.eps  = Param(within=NonNegativeReals)


#reserve requirements
model.ResReq = Param(model.Z, within=NonNegativeReals)

model.nT     = Param(within=NonNegativeReals) #total time horizon

#params and sets for boundary conditions
model.UCBoundaryConditions = Param(model.G,model.T) #boundary conditions for the UC problem
model.UCBCGenSet     = Set(within=model.G)  # set of reference buses
model.UCBCTimeSet    = Set(within=model.T)  # set of reference buses

# --- variables ---
model.pG       = Var(model.G,model.T, domain= NonNegativeReals)# real power output of generator g
model.pGResv   = Var(model.G,model.T, domain= NonNegativeReals)# real power reserve from the generator g
model.pW       = Var(model.WIND,model.T, domain= NonNegativeReals)# real power output of RES r
model.pD       = Var(model.D,model.T, domain= Reals)# real power demand delivered at d
model.alpha    = Var(model.D,model.T, domain= NonNegativeReals)# propotion of real power demand delivered at d
model.pICTto   = Var(model.ICT,model.T, domain= Reals) # real power injected at b' onto line l
model.pICTfrom = Var(model.ICT,model.T, domain= Reals) # reactive power injected at b onto line l

#storage variables
model.pS    = Var(model.S,model.T, domain= Reals)  #real power contribution of storage
model.pSIn  = Var(model.S,model.T, domain= NonNegativeReals)  #real power charging
model.pSOut = Var(model.S,model.T, domain= NonNegativeReals)  #real power discharging


#Unit comittment variables
model.u      = Var(model.G,model.T, within=Binary, initialize=1) # unit comittment variables for the generators
model.ustart = Var(model.G,model.T, within=Binary, initialize=1) # unit comittment variables for the generators
model.ustop  = Var(model.G,model.T, within=Binary, initialize=1) # unit comittment variables for the generators

#cost function
model.costfunc  = Var(model.T)

# --- cost function ---
def objective(model):
    obj = sum(model.costfunc[t] for t in model.T)
    return obj
model.OBJ = Objective(rule=objective, sense=minimize)

def cost_def(model, t):
    return model.costfunc[t] == sum((model.c2[g]*(model.pG[g,t])**2+model.c1[g]*model.pG[g,t]+\
    model.c0[g]*model.u[g,t])*model.baseMVA +\
    model.ustart[g,t]*model.SUcosts[g]+\
    model.ustop[g,t]*model.SDcosts[g] for g in model.G)+\
    sum(model.VOLL[d]*(1-model.alpha[d,t])*model.baseMVA*model.PD[d,t] for d in model.D)

# the next line creates one KCL constraint for each bus
model.cost_const = Constraint(model.T, rule=cost_def)

# --- Kirchoff's current law Definition at each bus b ---
def KCL_def(model,z, t):
    return sum(model.pG[g,t] for g in model.G if (g,z) in model.GZ)+\
    sum(model.pW[w,t] for w in model.WIND if (w,z) in model.WZ) +\
    sum(model.pSOut[s,t] for s in model.S if (z,s) in model.Sbs) - \
    sum(model.pSIn[s,t] for s in model.S if (z,s) in model.Sbs)+\
    sum(model.pICTfrom[i,t] for i in model.ICT if model.A[i,1]==z) +\
    sum(model.pICTto[i,t] for i in model.ICT if model.A[i,2]==z) == \
    sum(model.pD[d,t] for d in model.D if (d,z) in model.DZ)+\
    sum(model.GB[s] for s in model.SHUNT if (s,z) in model.SZ)

# the next line creates one KCL constraint for each bus
model.KCL_const = Constraint(model.Z, model.T, rule=KCL_def)

# --- generator power limits ---
def Real_Power_Max(model,g,t):
    return model.pG[g,t]+model.pGResv[g,t] <= model.PGmax[g]*model.u[g,t]
def Real_Power_Min(model,g,t):
    return model.pG[g,t] >= model.PGmin[g]*model.u[g,t]

model.PGmaxC = Constraint(model.G,model.T, rule=Real_Power_Max)
model.PGminC = Constraint(model.G,model.T, rule=Real_Power_Min)

# --- Wind power limits ---
def Wind_Real_Power_Max(model,w,t):
    return model.pW[w,t] <= model.WGmax[w,t]
def Wind_Real_Power_Min(model,w,t):
    return model.pW[w,t] >= model.WGmin[w,t]

model.WindPGmaxC = Constraint(model.WIND,model.T, rule=Wind_Real_Power_Max)
model.WindPGminC = Constraint(model.WIND,model.T, rule=Wind_Real_Power_Min)

# --- Reserve requirements ---
def Reserve_Req(model,z,t):
    return sum(model.pGResv[g,t] for g in model.G if (g,z) in model.GZ) >= model.ResReq[z]
model.ReserveReqC = Constraint(model.Z,model.T, rule=Reserve_Req)

# --- demands and load shedding ---
def Load_Shed_real(model,d,t):
    return model.pD[d,t] == model.alpha[d,t]*model.PD[d,t]

model.LoadShed_real = Constraint(model.D,model.T, rule=Load_Shed_real)

def alpha_BoundUB(model,d,t):
    return model.alpha[d,t] <= 1.0
def alpha_BoundLB(model,d,t):
    return model.alpha[d,t] >= 0.0

model.alphaBoundUBC = Constraint(model.D,model.T, rule=alpha_BoundUB)
model.alphaBoundLBC = Constraint(model.D,model.T, rule=alpha_BoundLB)

# --- generator ramp limits ---
def Real_Power_RampUp(model,g,t):
    return model.pG[g,t]-model.pG[g,t-1] <= model.RampUp[g]
def Real_Power_RampDown(model,g,t):
    return model.pG[g,t]-model.pG[g,t-1] >= -model.RampDown[g]

model.RampUpC   = Constraint(model.G,model.TRed, rule=Real_Power_RampUp)
model.RampDownC = Constraint(model.G,model.TRed, rule=Real_Power_RampDown)

# --- UC constraints ---
def UC_start_shut_cons(model,g,t):
    return model.ustart[g,t]-model.ustop[g,t]== model.u[g,t]-model.u[g,t-1]
model.UC_start_shunt_def = Constraint(model.G,model.TRed, rule=UC_start_shut_cons)

#---min up and down time constraints---
def UC_Min_UpTime_cons(model,g,t1,t2):
    return sum(model.ustart[g,k] for k in range(t1,t2))  <= model.u[g,t2]
def UC_Min_DownTime_cons(model,g,t1,t2):
    return sum(model.ustop[g,k] for k in range(t1,t2))   <= 1-model.u[g,t2]
model.UC_Min_UpTime_def = Constraint(model.UCMinUpT, rule=UC_Min_UpTime_cons)
model.UC_Min_DownTime_def = Constraint(model.UCMinDownT, rule=UC_Min_DownTime_cons)

# --- UC Boundary constraints ---
def UC_BC_cons(model,g,t):
    return model.u[g,t]== model.UCBoundaryConditions[g,t]

model.UC_BC_def = Constraint(model.UCBCGenSet,model.UCBCTimeSet, rule=UC_BC_cons)

# --- line power limits ---
def ICT_lim_def1(model,i,t):
    return model.pICTto[i,t] <= model.NTCto[i]
def ICT_lim_def2(model,i,t):
    return model.pICTfrom[i,t] <= model.NTCfr[i]
def ICT_lim_def3(model,i,t):
    return model.pICTto[i,t] >= -model.NTCto[i]
def ICT_lim_def4(model,i,t):
    return model.pICTfrom[i,t] >= -model.NTCfr[i]
model.line_lim1 = Constraint(model.ICT,model.T, rule=ICT_lim_def1)
model.line_lim2 = Constraint(model.ICT,model.T, rule=ICT_lim_def2)
model.line_lim4 = Constraint(model.ICT,model.T, rule=ICT_lim_def4)
model.line_lim3 = Constraint(model.ICT,model.T, rule=ICT_lim_def3)
# --- Loss equations ---
def Loss_Approx(model,i,t):
    return model.pICTto[i,t]+model.pICTfrom[i,t] == 0

model.Loss_ApproxC = Constraint(model.ICT,model.T, rule=Loss_Approx)

# --- storage model ---
def storage_model(model,s,t):
    return model.pS[s,t] == (model.pSIn[s,t]*(model.ChargeEff[s])-model.pSOut[s,t]*(1/model.DischargeEff[s]))
#the next two lines creates constraints for demand model
model.StoreModelC = Constraint(model.S,model.T, rule=storage_model)


#===Storage dynamics Constraints
def storage_dynamics_UB(model,s,t):
    return sum(model.pS[s,i] for i in range(1,t+1))  <= model.StoreUB[s]-model.StoreInitial[s]
def storage_dynamics_LB(model,s,t):
    return sum(model.pS[s,i] for i in range(1,t+1))  >= model.StoreLB[s]-model.StoreInitial[s]
#the next two lines creates constraints for demand model
model.StoreModelDynUBC = Constraint(model.S,model.TRed, rule=storage_dynamics_UB)
model.StoreModelDynLBC = Constraint(model.S,model.TRed, rule=storage_dynamics_LB)

def storage_dynamics_UB_firtsperiod(model,s):
    return model.pS[s,0]   <= model.StoreUB[s]-model.StoreInitial[s]
def storage_dynamics_LB_firtsperiod(model,s):
    return model.pS[s,0]  >= model.StoreLB[s]-model.StoreInitial[s]
#the next two lines creates constraints for demand model
model.StoreModelDynUBC_fixed = Constraint(model.S,rule=storage_dynamics_UB_firtsperiod)
model.StoreModelDynLBC_fixed = Constraint(model.S,rule=storage_dynamics_LB_firtsperiod)

# --- boundary constraint for storage ---
def storage_boundary_constraint(model,s):
    return sum(model.pS[s,t] for t in model.T) == model.StoreFinal[s]-model.StoreInitial[s]
model.storageBounddef = Constraint(model.S,rule=storage_boundary_constraint)
