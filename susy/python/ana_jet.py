# include functions for jet selection                                
import os
import sys
import ROOT
from ana2016.susy.Utilfunc import *


def Fun_findjet(Scanmode,muonlist,electronlist,pholist,tree):
    result=[]
    for j in range(tree.nJet):

        if Scanmode in ["eleTree","eQCDTree"]: #for electron channel
            lep=electronlist[0][0]
            dR_lep=Fun_deltaR(tree.eleEta[lep],tree.jetEta[j],tree.elePhi[lep],tree.jetPhi[j])
        if Scanmode in ["muTree","mQCDTree"]: # for mu channel
            lep=muonlist[0][0]
            dR_lep=Fun_deltaR(tree.muEta[lep],tree.jetEta[j],tree.muPhi[lep],tree.jetPhi[j])
    
        if Scanmode in ["eeTree","eeQCDTree"]: #for di-electron 
            lep1=electronlist[0][0]
            lep2=electronlist[1][0]
            dR_lep=min(Fun_deltaR(tree.eleEta[lep1],tree.jetEta[j],tree.elePhi[lep1],tree.jetPhi[j]),Fun_deltaR(tree.eleEta[lep2],tree.jetEta[j],tree.elePhi[lep2],tree.jetPhi[j]))

        if Scanmode in ["mumuTree","mmQCDTree"]: #for di-muon 
            lep1=muonlist[0][0]
            lep2=muonlist[1][0]
            dR_lep=min(Fun_deltaR(tree.muEta[lep1],tree.jetEta[j],tree.muPhi[lep1],tree.jetPhi[j]),Fun_deltaR(tree.muEta[lep2],tree.jetEta[j],tree.muPhi[lep2],tree.jetPhi[j]))

        if dR_lep<0.4: continue # this jet overlaps to lepton


        jetOverpho=False
        for pho in pholist:
            dR_jetpho=Fun_deltaR(tree.phoEta[pho[0]],tree.jetEta[j],tree.phoPhi[pho[0]],tree.jetPhi[j])
            if dR_jetpho<0.4: 
                jetOverpho=True
                break
        if jetOverpho: continue



        if tree.jetPt[j]>30 and abs(tree.jetEta[j])<2.4 and tree.jetPFLooseId[j]:
            if tree.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[j]>0.8:
                jet=[j,1,dR_lep]
            else: jet=[j,0,dR_lep]

            result.append(jet)
    
#    if len(result)==3:
#        print "---"
#        for jet in result:        
#            if jet[2]<0.4:
#                    print jet[2],"loose" #,"d_Pt:",(tree.jetPt[jet[0]]-tree.elePt[lep])/tree.jetPt[jet[0]]
    return result




def Fun_JetM3(Jetlist,tree):
    # calculate the highst 3jets invmass combination
    maxSumPt = 0.
    maxM3 = 0.
    nj=len(Jetlist) #number of jets
    for comb in range(1<<nj):
        npicked=0
        for j in range(nj):
            if ((comb>>j)&1) ==1: npicked +=1


        if npicked != 3: continue
        
        thisCombination=ROOT.TLorentzVector(0.,0.,0.,0.)
        for j in range(nj):
            if ((comb>>j)&1) ==1:
                thisjet=ROOT.TLorentzVector()
                thisjet.SetPtEtaPhiE(tree.jetPt[Jetlist[j][0]],tree.jetEta[Jetlist[j][0]],tree.jetPhi[Jetlist[j][0]],tree.jetEn[Jetlist[j][0]])
                thisCombination += thisjet

        if thisCombination.Pt()>maxSumPt:
            maxSumPt = thisCombination.Pt()
            maxM3= thisCombination.M()

    return maxM3


    
    
