# include functions for ele selection
import os
import sys
import ROOT

# get ea from https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_X/RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt
def Fun_getEle_EA(sceta):
    if abs(sceta)<1.0: return 0.1752
    elif abs(sceta)<1.479: return 0.1862
    elif abs(sceta)<2.0: return 0.1411
    elif abs(sceta)<2.2: return 0.1534
    elif abs(sceta)<2.3: return 0.1903
    elif abs(sceta)<2.4: return 0.2243
    elif abs(sceta)<5.0: return 0.2687






def Fun_findele(tree):
    result=[]

#----------------------
    def Fun_ele_relCombIsoWithEA(ind):
        return ( tree.elePFChIso[ind] + max( 0.0, tree.elePFNeuIso[ind]+tree.elePFPhoIso[ind]- Fun_getEle_EA(tree.eleSCEta[ind])*tree.rho) )/tree.elePt[ind]

    def Fun_loose_ele(ind):
        if tree.elePt[ind]>10 and abs(tree.eleEta[ind])<2.5 and tree.eleIDbit[ind]>>1&1==1:
            return True
        else: return False

    def Fun_tight_ele(ind):
        if tree.elePt[ind]>30 and abs(tree.eleEta[ind])<2.5 and tree.eleIDbit[ind]>>3&1==1:
            return True
        else: return False
    
    def Fun_tight_ele_antiIso(ind):
        if tree.elePt[ind]<30: return False

        pfiso=Fun_ele_relCombIsoWithEA(ind)
        antiIso=False
        if abs(tree.eleSCEta[ind])<=1.479 and pfiso>0.0893 and pfiso<1.0 and tree.eledEtaAtVtx[ind]<0.00926 and tree.eledPhiAtVtx[ind]<0.0336 and tree.eleHoverE[ind]<0.0597 and abs(tree.eleD0[ind])<0.0111 and abs(tree.eleDz[ind])<0.0466 and tree.eleConvVeto[ind]==1:
            antiIso=True
        elif abs(tree.eleSCEta[ind])<2.5 and abs(tree.eleSCEta[ind])>1.479 and pfiso>0.121 and pfiso<1.0 and tree.eledEtaAtVtx[ind]<0.00724  and tree.eledPhiAtVtx[ind]<0.0918 and tree.eleHoverE[ind]<0.0615 and abs(tree.eleD0[ind])<0.0351 and abs(tree.eleDz[ind])<0.417 and tree.eleConvVeto[ind]==1:
            antiIso=True
        else: return False


        if antiIso: return True
        else: return False


#----------------------------





    for e in range(tree.nEle):
        if Fun_tight_ele(e):
            ele=[e,1]
        elif Fun_loose_ele(e):
            ele=[e,0]
        elif Fun_tight_ele_antiIso(e):
            ele=[e,3]

        else: continue
        
        ele.append(Fun_ele_relCombIsoWithEA(e))
        result.append(ele)

    
    return result
