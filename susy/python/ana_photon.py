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





def Fun_findCandpho(Scanmode,muonlist,electronlist,tree):
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

        if tree.phoPFChIso[f]<20 and (tree.phoSigmaIEtaIEta[f]>1.0102 or tree.phoPFChIso[f]>3.32):     # loose fake 
            return True
        else:
            return False

    def Fun_loose_woIEtaIEta(f):
        if  tree.phoHoverE[f]>0.05:
            return False
        if (1.92+0.014*tree.phoEt[f]+0.000019*tree.phoEt[f]**2)<NeuIso_corrected(f) or (0.81+0.0053*tree.phoEt[f])<PhoIso_corrected(f):
            return False

        if tree.phoPFChIso[f]<20 and tree.phoPFChIso[f]<=3.32:
            return True   # loosepho w/o sigmaIetaIeta cut
        else:
            return False

    def Fun_loose_woChHadIso(f):
        if  tree.phoHoverE[f]>0.05:
            return False
        if (1.92+0.014*tree.phoEt[f]+0.000019*tree.phoEt[f]**2)<NeuIso_corrected(f) or (0.81+0.0053*tree.phoEt[f])<PhoIso_corrected(f):
            return False

        if tree.phoPFChIso[f]<20 and tree.phoSigmaIEtaIEta[f]<=1.010:
             # loosepho w/o chIso cut
            return True  
        else:
            return False


    def Fun_phoGenmatch(f):
        genMatchpho=False
        genMatchele=False
        for genPar in range(tree.nMC):
            if tree.mcPID[genPar]==22:
                if Fun_deltaR(tree.phoEta[f],tree.mcEta[genPar],tree.phoPhi[f],tree.mcPhi[genPar])<0.01 and abs(tree.phoEta[f]-tree.mcEta[genPar])<0.005 and abs(tree.phoEt[f]-tree.mcPt[genPar])/tree.mcPt[genPar]<0.1:
                    genMatchpho=True
                    break
            elif tree.mcPID[genPar]==11 or tree.mcPID[genPar]==-11:
                if Fun_deltaR(tree.phoEta[f],tree.mcEta[genPar],tree.phoPhi[f],tree.mcPhi[genPar])<0.04 and abs(tree.phoEta[f]-tree.mcEta[genPar])<0.005 and abs(tree.phoEt[f]-tree.mcPt[genPar])/tree.mcPt[genPar]<0.1:
                    genMatchele=True
                    break
        
        if genMatchpho: return 22
        elif genMatchele: return 11
        else: return -99

#--------------------------------

        


    for p in range(tree.nPho):

#----------get the dr for lep and photon--------
        if Scanmode in ["eleTree","eQCDTree"]: #for electron channel
            lep=electronlist[0][0]
            dR_lep=Fun_deltaR(tree.eleEta[lep],tree.phoEta[p],tree.elePhi[lep],tree.phoPhi[p])
        if Scanmode in ["muTree","mQCDTree"]: # for mu channel
            lep=muonlist[0][0]
            dR_lep=Fun_deltaR(tree.muEta[lep],tree.phoEta[p],tree.muPhi[lep],tree.phoPhi[p])


        if dR_lep<0.3: continue # this pho overlaps to lepton


        if tree.phoEt[p]>20 and abs(tree.phoEta[p])<1.4442 and tree.phoEleVeto[p]:
            phoTag=0
            if tree.phoIDbit[p]>>0&1==1: 
                phoTag |= (1<<3)
            elif tree.phoIDbit[p]>>0&1==0 and Fun_loosefake(p): 
                phoTag |= (1<<0)

            if  Fun_loose_woIEtaIEta(p): 
                phoTag |= (1<<1)
            if  Fun_loose_woChHadIso(p): 
                phoTag |= (1<<2)

            if phoTag>0:
                cand_step1.append([p,phoTag,dR_lep])
       


#---------loop the whole photon and fake

    for pp in cand_step1:
        overlaps_pp=False
        for otherpp in cand_step1:
            dR_pp=Fun_deltaR(tree.phoEta[pp[0]],tree.phoEta[otherpp[0]],tree.phoPhi[pp[0]],tree.phoPhi[otherpp[0]])
            if dR_pp<0.3 and pp[0] != otherpp[0]:
                overlaps_pp=True
                break


        if not overlaps_pp:
            if not tree.isData:  pp.append(Fun_phoGenmatch(pp[0]))
            candpho.append(pp)
            
#    if len(candpho)>0:print candpho

    

        
    return candpho
