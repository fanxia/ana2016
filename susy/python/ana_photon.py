# include functions for photon selection                             
import os
import sys
import ROOT
from ana2016.susy.Utilfunc import *

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedPhotonIdentificationRun2#Recommended_Working_points_for_2

def Fun_getPho_NeuEA(sceta):
    if abs(sceta)<1.0: return 0.0597
    elif abs(sceta)<1.479: return 0.0807
    elif abs(sceta)<2.0: return 0.0629
    elif abs(sceta)<2.2: return 0.0197
    elif abs(sceta)<2.3: return 0.0184
    elif abs(sceta)<2.4: return 0.0284
    elif abs(sceta)<5.0: return 0.0591


def Fun_getPho_PhoEA(sceta):
    if abs(sceta)<1.0: return 0.1210
    elif abs(sceta)<1.479: return 0.1107
    elif abs(sceta)<2.0: return 0.0699
    elif abs(sceta)<2.2: return 0.1056
    elif abs(sceta)<2.3: return 0.1457
    elif abs(sceta)<2.4: return 0.1719
    elif abs(sceta)<5.0: return 0.1998

def Fun_getPho_ChEA(sceta):
    if abs(sceta)<1.0: return 0.0360
    elif abs(sceta)<1.479: return 0.0377
    elif abs(sceta)<2.0: return 0.0306
    elif abs(sceta)<2.2: return 0.0283
    elif abs(sceta)<2.3: return 0.0254
    elif abs(sceta)<2.4: return 0.0217
    elif abs(sceta)<5.0: return 0.0167




def Fun_findCandpho(scanmode,muonlist,electronlist,tree):
    cand_step1=[]
    candpho=[]

    def NeuIso_corrected(ind):
        return max(tree.phoPFNeuIso[ind]-tree.rho*Fun_getPho_NeuEA(tree.phoSCEta[ind]),0.0)
    def PhoIso_corrected(ind):
        return max(tree.phoPFPhoIso[ind]-tree.rho*Fun_getPho_PhoEA(tree.phoSCEta[ind]),0.0)
    def ChIso_corrected(ind):
        return max(tree.phoPFChIso[ind]-tree.rho*Fun_getPho_ChEA(tree.phoSCEta[ind]),0.0)


#------------------------------
    def Fun_loosepho(f):
        if  tree.phoHoverE[f]<0.0597 and NeuIso_corrected(f)<(10.91+0.0148*tree.phoEt[f]+0.000017*tree.phoEt[f]**2) and PhoIso_corrected(f)<(3.63+0.0047*tree.phoEt[f]) and tree.phoSigmaIEtaIEtaFull5x5[f]<=0.01031 and ChIso_corrected(f)<=1.295:     # loose photon
            return True
        else:
            return False

    def Fun_loosefake(f):
        if  tree.phoHoverE[f]<0.0597 and NeuIso_corrected(f)<(10.91+0.0148*tree.phoEt[f]+0.000017*tree.phoEt[f]**2) and PhoIso_corrected(f)<(3.63+0.0047*tree.phoEt[f]) and ChIso_corrected(f)<20 and tree.phoSigmaIEtaIEtaFull5x5[f]<0.02:   
            if (tree.phoSigmaIEtaIEtaFull5x5[f]>0.01031 and ChIso_corrected(f)<=1.295) or (tree.phoSigmaIEtaIEtaFull5x5[f]<=0.01031 and ChIso_corrected(f)>1.295):     # loose fake 
                return True
            else:
                return False
        else: return False

    def Fun_loose_woIEtaIEta(f):
        if  tree.phoHoverE[f]<0.0597 and NeuIso_corrected(f)<(10.91+0.0148*tree.phoEt[f]+0.000017*tree.phoEt[f]**2) and PhoIso_corrected(f)<(3.63+0.0047*tree.phoEt[f]) and ChIso_corrected(f)<=1.295 and tree.phoSigmaIEtaIEtaFull5x5[f]<0.02:   
            return True   # loosepho w/o sigmaIetaIeta cut
        else:
            return False

    def Fun_loose_woChHadIso(f):
        if  tree.phoHoverE[f]<0.0597 and NeuIso_corrected(f)<(10.91+0.0148*tree.phoEt[f]+0.000017*tree.phoEt[f]**2) and PhoIso_corrected(f)<(3.63+0.0047*tree.phoEt[f]) and tree.phoSigmaIEtaIEtaFull5x5[f]<=0.01031 and ChIso_corrected(f)<20:    
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
        if scanmode in ["eleTree","eQCDTree"]: #for electron channel
            lep=electronlist[0][0]
            dR_lep=Fun_deltaR(tree.eleEta[lep],tree.phoEta[p],tree.elePhi[lep],tree.phoPhi[p])
            
        if scanmode in ["muTree","mQCDTree"]: # for mu channel
            lep=muonlist[0][0]
            dR_lep=Fun_deltaR(tree.muEta[lep],tree.phoEta[p],tree.muPhi[lep],tree.phoPhi[p])

        if scanmode in ["eeTree","eeQCDTree"]: #for di-electron 
            lep1=electronlist[0][0]
            lep2=electronlist[1][0]
            dR_lep=min(Fun_deltaR(tree.eleEta[lep1],tree.phoEta[p],tree.elePhi[lep1],tree.phoPhi[p]),Fun_deltaR(tree.eleEta[lep2],tree.phoEta[p],tree.elePhi[lep2],tree.phoPhi[p]))

        if scanmode in ["mumuTree","mmQCDTree"]: #for di-muon 
            lep1=muonlist[0][0]
            lep2=muonlist[1][0]
            dR_lep=min(Fun_deltaR(tree.muEta[lep1],tree.phoEta[p],tree.muPhi[lep1],tree.phoPhi[p]),Fun_deltaR(tree.muEta[lep2],tree.phoEta[p],tree.muPhi[lep2],tree.phoPhi[p]))


        if dR_lep<0.3: continue # this pho overlaps to lepton


        if tree.phoEt[p]>20 and abs(tree.phoEta[p])<1.4442 and abs(tree.phoSCEta[p])<1.479 and not tree.phohasPixelSeed[p]:
            phoTag=0
#            if Fun_loosepho(p): 
            if tree.phoIDbit[p]&1==1:  #loose photon
                phoTag |= (1<<3)
            elif Fun_loosefake(p): 
                phoTag |= (1<<0)
            

            if  Fun_loose_woIEtaIEta(p): 
                phoTag |= (1<<1)
            if  Fun_loose_woChHadIso(p): 
                phoTag |= (1<<2)

            if phoTag>0:
                cand_step1.append([p,phoTag,dR_lep,ChIso_corrected(p)])

                

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



def Fun_invmass_pholep(scanmode,lep,pho,tree):
    TLVlepton=ROOT.TLorentzVector()
    TLVphoton=ROOT.TLorentzVector()
    TLVphoton.SetPtEtaPhiM(tree.phoEt[pho],tree.phoEta[pho],tree.phoPhi[pho],0.)

    if scanmode in ["eleTree","eQCDTree"]:
        TLVlepton.SetPtEtaPhiE(tree.elePt[lep],tree.eleEta[lep],tree.elePhi[lep],tree.eleEn[lep])
    if scanmode in ["muTree","mQCDTree"]:
        TLVlepton.SetPtEtaPhiE(tree.muPt[lep],tree.muEta[lep],tree.muPhi[lep],tree.muEn[lep])


    return (TLVlepton+TLVphoton).M()



