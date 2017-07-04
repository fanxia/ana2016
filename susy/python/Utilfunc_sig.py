# include utility functions
# special for fastsim signal mc
# has the function for bino like neutralino's branching ratios!!
import os
import sys
import ROOT
import math


def Fun_pileupweight_fastsim(truepu):


    pileuplist=[0.007886143894340758, 0.018457528871324343, 0.01863155559630011, 0.02096383607316798, 0.032005347957448846, 0.024912595928374328, 0.023496627352485786, 0.03741588618848328, 0.07009385115282743, 0.12634910129372068, 0.227311515961966, 0.3987169537712364, 0.5878015495787806, 0.7425036502486267, 0.8684271448577873, 0.8925405770146807, 0.8623414425532548, 0.9227648136335223, 0.8974838907458019, 0.9729029938841934, 0.8895435739891661, 0.8677012642568253, 0.9327133071800777, 1.0307295073936256, 1.066866710904367, 1.254531338531469, 1.2464301410268261, 1.4207581307155732, 1.409014156658878, 1.5528034565725561, 1.6604924797543752, 1.7960628296877574, 2.582583537218427, 3.4431635455829457, 6.521385095048948, 15.01136679161954, 46.5717794470408, 98.57748728372216, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]


    return pileuplist[int(truepu)]



def Fun_SigFindGen(tree):
    resultstop=[]
    resultnlsp=[]
    ngamma=0
    for genp in range(tree.nMC):
        #-------find nlsp mass
        if tree.mcPID[genp]==1000022 and (tree.mcStatusFlag[genp]&4)==4 and tree.mcMomPID[genp]==1000023:
            resultnlsp.append(tree.mcMomMass[genp])
        #-------find stop mass
        if abs( tree.mcPID[genp])==1000006 and (tree.mcStatusFlag[genp]&4)==4:
            resultstop.append(tree.mcMass[genp])
        #-------find how many final photon, to determin decay modes
        if tree.mcPID[genp]==22 and (tree.mcStatusFlag[genp]&4)==4 and tree.mcMomPID[genp]==1000023:
            ngamma+=1

    return [resultstop,resultnlsp,ngamma]


#pdg2016
sw2=0.23129
cw2=1-sw2
mZ=91.1876

def Fun_SigNLSPBR(mass,decaymode):
    # will get the br:NLSP->photon+G~, and get the event weight according to the decay mode(gg,Zg,ZZ)
    if (mass<mZ): br=1.0
    else:br= cw2/(cw2+sw2*(1.-mZ**2/mass**2)**4)

    if decaymode==99:  # gg
        brweight=(br)**2/0.25
    elif decaymode==29: #Zg
        brweight=2*(br)*(1.0-br)/0.5
    elif decaymode==22: #ZZ
        brweight=(1-br)**2/0.25
    else: brweight=0.0

    return [br,brweight]
