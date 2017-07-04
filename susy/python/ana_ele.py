# include functions for ele selection
import os
import sys
import ROOT


# update to 80x https://indico.cern.ch/event/482673/contributions/2187022/attachments/1282446/1905912/talk_electron_ID_spring16.pdf
def Fun_getEle_EA(sceta):
    if abs(sceta)<1.0: return 0.1703
    elif abs(sceta)<1.479: return 0.1715
    elif abs(sceta)<2.0: return 0.1213
    elif abs(sceta)<2.2: return 0.1230
    elif abs(sceta)<2.3: return 0.1635
    elif abs(sceta)<2.4: return 0.1937
    elif abs(sceta)<5.0: return 0.2393
    else: return 0.0





def Fun_findele(tree):
    result=[]

#----------------------
    def Fun_ele_relCombIsoWithEA(ind):
        return (tree.elePFChIso[ind] + max( 0.0, tree.elePFNeuIso[ind]+tree.elePFPhoIso[ind]-Fun_getEle_EA(tree.eleSCEta[ind])*tree.rho) )/tree.elePt[ind]

    def Fun_loose_ele(ind,pfiso):
        if abs(tree.eleSCEta[ind])<=1.479 and pfiso<0.0994 and tree.eledEtaseedAtVtx[ind]<0.00477 and tree.eledPhiAtVtx[ind]<0.222 and tree.eleHoverE[ind]<0.298 and tree.eleEoverPInv[ind]<0.241 and tree.eleConvVeto[ind]==1 and tree.eleSigmaIEtaIEtaFull5x5[ind]<0.011 and tree.eleMissHits[ind]<=1:
            return True
        elif abs(tree.eleSCEta[ind])>1.479 and pfiso<0.107 and tree.eledEtaseedAtVtx[ind]<0.00868  and tree.eledPhiAtVtx[ind]<0.213 and tree.eleHoverE[ind]<0.101 and tree.eleEoverPInv[ind]<0.14 and tree.eleSigmaIEtaIEtaFull5x5[ind]<0.0314 and tree.eleMissHits[ind]<=1 and tree.eleConvVeto[ind]==1: 
            return True
        else: return False
        

    def Fun_tight_ele(ind,pfiso):
        if abs(tree.eleSCEta[ind])<=1.479 and pfiso<0.0588 and tree.eledEtaseedAtVtx[ind]<0.00308 and tree.eledPhiAtVtx[ind]<0.0816 and tree.eleHoverE[ind]<0.0414 and tree.eleEoverPInv[ind]<0.0129 and tree.eleConvVeto[ind]==1 and tree.eleSigmaIEtaIEtaFull5x5[ind]<0.00998 and tree.eleMissHits[ind]<=1:
            return True
        elif abs(tree.eleSCEta[ind])>1.479 and pfiso<0.0292 and tree.eledEtaseedAtVtx[ind]<0.00605  and tree.eledPhiAtVtx[ind]<0.0394 and tree.eleHoverE[ind]<0.0641 and tree.eleEoverPInv[ind]<0.0129 and tree.eleSigmaIEtaIEtaFull5x5[ind]<0.0292 and tree.eleMissHits[ind]<=1 and tree.eleConvVeto[ind]==1: 
            return True
        else: return False

        
    def Fun_tight_ele_antiIso(ind,pfiso):
        if abs(tree.eleSCEta[ind])<=1.479 and pfiso>0.0994 and pfiso<1. and tree.eledEtaseedAtVtx[ind]<0.00308 and tree.eledPhiAtVtx[ind]<0.0816 and tree.eleHoverE[ind]<0.0414 and tree.eleEoverPInv[ind]<0.0129 and tree.eleConvVeto[ind]==1 and tree.eleSigmaIEtaIEtaFull5x5[ind]<0.00998 and tree.eleMissHits[ind]<=1:
            return True
        elif abs(tree.eleSCEta[ind])>1.479 and pfiso>0.107 and pfiso<1. and tree.eledEtaseedAtVtx[ind]<0.00605  and tree.eledPhiAtVtx[ind]<0.0394 and tree.eleHoverE[ind]<0.0641 and tree.eleEoverPInv[ind]<0.0129 and tree.eleSigmaIEtaIEtaFull5x5[ind]<0.0292 and tree.eleMissHits[ind]<=1 and tree.eleConvVeto[ind]==1: 
            return True
        else: return False
        



#----------------------------





    for e in range(tree.nEle):
        if abs(tree.eleSCEta[e])>1.4442 and abs(tree.eleSCEta[e])<1.566: continue

        PFiso=Fun_ele_relCombIsoWithEA(e)
        # if tree.elePt[e]>30 and abs(tree.eleEta[e])<2.1 and Fun_tight_ele(e,PFiso):
        #     ele=[e,1]
        # elif tree.elePt[e]>10 and abs(tree.eleEta[e])<2.5 and Fun_loose_ele(e,PFiso):
        #     ele=[e,0]
        # elif tree.elePt[e]>30 and abs(tree.eleEta[e])<2.1 and Fun_tight_ele_antiIso(e,PFiso):
        #     ele=[e,3]

        if tree.elePt[e]>35 and abs(tree.eleEta[e])<2.1 and (tree.eleIDbit[e]>>3&1)==1:
            ele=[e,1]
        elif tree.elePt[e]>10 and abs(tree.eleEta[e])<2.5 and (tree.eleIDbit[e]>>1&1)==1:
            ele=[e,0]
        elif tree.elePt[e]>35 and abs(tree.eleEta[e])<2.1 and Fun_tight_ele_antiIso(e,PFiso):
            ele=[e,3]
        
        else: continue
        
        ele.append(PFiso)
        result.append(ele)

    
    return result
