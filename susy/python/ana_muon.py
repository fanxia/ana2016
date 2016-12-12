# include functions for muon selection
import os
import sys
import ROOT


def Fun_findmu(tree):
    result=[]

#-----------------
    def Fun_muPFRelCombIso(ind):
        return (tree.muPFChIso[ind]+max(0.,tree.muPFNeuIso[ind]+tree.muPFPhoIso[ind]-0.5*tree.muPFPUIso[ind]))/tree.muPt[ind]

    def Fun_tight_mu_antiIso(ind):
        if tree.muPt[ind]>30 and abs(tree.muEta[ind])<2.1 and iso>0.25 and abs(tree.muD0[ind])<0.2 and abs(tree.muDz[ind])<0.5 and tree.muChi2NDF[ind]<10 and tree.muMuonHits[ind]>0 and tree.muStations[ind]>1  and tree.muTrkLayers[ind]>5:
            return True
        else: return False

#-----------------

    for m in range(tree.nMu):

        iso=Fun_muPFRelCombIso(m)

        if tree.muPt[m]>30 and abs(tree.muEta[m])<2.1 and iso<0.15 and tree.muIsTightID[m]:
            mu=[m,1,iso]
        elif  tree.muPt[m]>10 and abs(tree.muEta[m])<2.5 and iso<0.25 and tree.muIsLooseID[m]:
            mu=[m,0,iso]
        elif tree.muPt[m]>30 and abs(tree.muEta[m])<2.1 and iso>0.25 and tree.muIsTightID[m]:
            mu=[m,3,iso]
        else: continue

        result.append(mu)

    return result        
        

