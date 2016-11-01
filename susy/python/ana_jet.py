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
                jet=[j,1]
            else: jet=[j,0]

            result.append(jet)

    return result
