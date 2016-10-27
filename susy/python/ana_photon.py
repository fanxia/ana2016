# include functions for photon selection                             
import os
import sys
import ROOT
from ana2016.susy.Utilfunc import *

# get ea from https://github.com/cms-sw/cmssw/tree/CMSSW_8_0_X/RecoEgamma/PhotonIdentification/data/Spring15
def Fun_getPho_NeuEA(sceta):
    if abs(sceta)<1.0: return 0.0599
    elif abs(sceta)<1.479: return 0.0819
    elif abs(sceta)<2.0: return 0.0696
    elif abs(sceta)<2.2: return 0.0360
    elif abs(sceta)<2.3: return 0.0360
    elif abs(sceta)<2.4: return 0.0462
    elif abs(sceta)<5.0: return 0.0656

def Fun_getPho_PhoEA(sceta):
    if abs(sceta)<1.0: return 0.1271
    elif abs(sceta)<1.479: return 0.1101
    elif abs(sceta)<2.0: return 0.0756
    elif abs(sceta)<2.2: return 0.1175
    elif abs(sceta)<2.3: return 0.1498
    elif abs(sceta)<2.4: return 0.1857
    elif abs(sceta)<5.0: return 0.2183





def Fun_findCandpho(Chan,lep,tree):
    cand_step1=[]
    candpho=[]

    def NeuIso_corrected(ind):
        return max(tree.phoPFNeuIso[ind]-tree.rho*Fun_getPho_NeuEA(tree.phoSCEta[ind]),0.0)
    def PhoIso_corrected(ind):
        return max(tree.phoPFPhoIso[ind]-tree.rho*Fun_getPho_PhoEA(tree.phoSCEta[ind]),0.0)

#------------------------------
    def Fun_loosefake(f):
        if  tree.phoHoverE[f]>0.05:
            return False

        if (1.92+0.014*tree.phoEt[f]+0.000019*tree.phoEt[f]**2)<NeuIso_corrected(f) or (0.81+0.0053*tree.phoEt[f])<PhoIso_corrected(f):

            return False

        if tree.phoPFChIso[f]<20 and (tree.phoSigmaIEtaIEta[f]>1.0102 or tree.phoPFChIso[f]>3.32):
            return True
        else:
            print "check"
            return False
#--------------------------------

        


    for p in range(tree.nPho):

#----------get the dr for lep and photon--------
        if Chan==111: #for electron channel
            dR_lep=Fun_deltaR(tree.eleEta[lep],tree.phoEta[p],tree.elePhi[lep],tree.phoPhi[p])
        if Chan==222: # for mu channel
            dR_lep=Fun_deltaR(tree.muEta[lep],tree.phoEta[p],tree.muPhi[lep],tree.phoPhi[p])


        if dR_lep<0.3: continue # this pho overlaps to lepton


        if tree.phoEt[p]>20 and abs(tree.phoEta[p])<1.4442 and tree.phoEleVeto[p]:
            if tree.phoIDbit[p]>>0&1==1: cand_step1.append([p,1,dR_lep])
            elif tree.phoIDbit[p]>>0&1==0 and Fun_loosefake(p): cand_step1.append([p,0,dR_lep])
       


#---------loop the whole photon and fake

    for pp in cand_step1:
        overlaps_pp=False
        for otherpp in cand_step1:
            dR_pp=Fun_deltaR(tree.phoEta[pp[0]],tree.phoEta[otherpp[0]],tree.phoPhi[pp[0]],tree.phoPhi[otherpp[0]])
            if dR_pp<0.3 and pp[0] != otherpp[0]:
                overlaps_pp=True
                break


        if not overlaps_pp:
            candpho.append(pp)
            
#    if len(candpho)>0:print candpho
        
    return candpho
