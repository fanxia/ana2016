# include utility functions
import os
import sys
import ROOT
import math

def Fun_deltaR(eta1,eta2,phi1,phi2):
    if phi1-phi2>math.pi: d_phi=2*math.pi-(phi1-phi2)
    elif phi1-phi2<-math.pi: d_phi=2*math.pi+(phi1-phi2)
    else: d_phi=phi1-phi2
    result = ((eta1-eta2)**2+(d_phi)**2)**0.5
    return result



def Fun_pileupweight(truepu):
    # for singleEle_2016D:  copy from script/pileup/puweight.txt
#    pileuplist=[7.307961557716201e-05, 0.015002786730374045, 0.014880853104122462, 0.02472307807752863, 0.03542337295963161, 0.029629388339403994, 0.03488229769083586, 0.030939157285156345, 0.025137410364424243, 0.033646968524553594, 0.10202497901440581, 0.39406684353278487, 0.9003830808250708, 1.2443901454546464, 1.3370273900135166, 1.2314321458566726, 1.1045087788899957, 1.1374426788861207, 1.0899540002697605, 1.1711940675512875, 1.051371000755816, 0.9966869844322822, 1.04183771465863, 1.1222863624418296, 1.123858016839053, 1.258641683171495, 1.1695670767522006, 1.2218373232426374, 1.0835810210337282, 1.036876319132205, 0.9313981206714996, 0.8166960182181352, 0.9169402661870983, 0.9177911222357165, 1.2533991567099991, 1.9984945864175763, 4.1361303576025445, 5.655823763391954, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # for singleEle_2016BCD
    pileuplist=[0.000195449881692361, 0.009983816709908574, 0.014035935214231705, 0.023663235335656, 0.03933534466126411, 0.03099676161908973, 0.03364718765567334, 0.06954812762006521, 0.1646511451998625, 0.31738069626953475, 0.4966641508995886, 0.7211565072650534, 0.9726808021437985, 1.159591622637084, 1.2652828804851273, 1.2200834187603156, 1.1418351898565373, 1.2134897464154377, 1.1814708883989518, 1.273972830527228, 1.135973376331179, 1.0563869406739776, 1.070197997960957, 1.1103394700312263, 1.069445130035759, 1.1492443288784953, 1.0178382899351954, 1.0046780041969057, 0.8370452007540007, 0.7526252704468067, 0.638690716373535, 0.5332492532951655, 0.5748982523745999, 0.557567721241006, 0.7453295698534931, 1.1756638096097398, 2.4303621242720443, 3.343505142122782, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    return pileuplist[int(truepu)]



def Fun_btagweight(jets,sys="central"):
#    jetlist[[btagged,btageff,btagsf],[]..]
    Pmc1=1.0
    Pdata1=1.0
    PmcErr2=0.0     # acturally, it's (d(Pmc)/Pmc)^2
    PdataErr2=0.0
    for jet in jets:
        btagged=jet[0]
        btageff=jet[1]
        btageff_err=jet[2]
        if sys=='central':    btagsf=jet[3]
        elif sys=='up':    btagsf=jet[4]
        elif sys=='down':    btagsf=jet[5]

        if btageff==0.0 or btageff==1.0:continue

        if btagged: 
            Pmc1*=btageff
            Pdata1*=btageff*btagsf
            PmcErr2+=(btageff_err/btageff)**2
            PdataErr2+=(btageff_err/btageff)**2
        else: 
            Pmc1*=(1-btageff)
            Pdata1*=(1-btageff*btagsf)
            PmcErr2+=(btageff_err)**2/(1.0-btageff)**2
            PdataErr2+=(btagsf*btageff_err)**2/(1.0-btagsf*btageff)**2

    weight1=Pdata1/Pmc1
    weight1_err=((PdataErr2/Pdata1)**2+(PmcErr2/Pmc1)**2)**0.5*weight1


    return [weight1,weight1_err]



def Fun_invmass_dilep(scanmode,lep,tree):
    TLVlepton1=ROOT.TLorentzVector() 
    TLVlepton2=ROOT.TLorentzVector()

    lep1=lep[0][0]
    lep2=lep[1][0]

    if scanmode in ["eeTree","eeQCDTree"]:
        TLVlepton1.SetPtEtaPhiE(tree.elePt[lep1],tree.eleEta[lep1],tree.elePhi[lep1],tree.eleEn[lep1])
        TLVlepton2.SetPtEtaPhiE(tree.elePt[lep2],tree.eleEta[lep2],tree.elePhi[lep2],tree.eleEn[lep2])

    if scanmode in ["mumuTree","mmQCDTree"]:
        TLVlepton1.SetPtEtaPhiE(tree.muPt[lep1],tree.muEta[lep1],tree.muPhi[lep1],tree.muEn[lep1])
        TLVlepton2.SetPtEtaPhiE(tree.muPt[lep2],tree.muEta[lep2],tree.muPhi[lep2],tree.muEn[lep2])

    return (TLVlepton1+TLVlepton2).M()
