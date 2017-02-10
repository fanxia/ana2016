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
    #for whole data2016 and Moriond17MC
#    pileuplist=[0.36607728367112397, 0.893925224429129, 1.1977164711293022, 0.9626995126421471, 1.1209761161608771, 1.164859138495215, 0.7955992069782198, 0.49582436388980267, 0.7421820181560131, 0.8788562011257953, 0.9642318178900664, 1.0724989149422395, 1.1253355687662896, 1.1760272210091784, 1.2020826475636825, 1.2076435646538353, 1.2001763306015454, 1.1826818134820003, 1.1439985554442524, 1.0966325099375585, 1.0656023419000509, 1.0511664066705138, 1.0515997504290857, 1.0506303621694364, 1.0498618047566595, 1.0581729089685616, 1.0721551494002155, 1.083029806486924, 1.0956935452522283, 1.107870839003214, 1.0946211207988656, 1.0826197557764918, 1.04124703311932, 0.9857518332210599, 0.910807479609711, 0.8209225782064177, 0.7167870987003486, 0.6100130736543593, 0.503118192256282, 0.4048414744758991, 0.30919531102329884, 0.2279203149583453, 0.16368974737145012, 0.11317989130853941, 0.07730047708806811, 0.0509220818594168, 0.031893565774466566, 0.020093554222709423, 0.012263091535772767, 0.007426461028558469, 0.00438028012095721, 0.0026077681562074752, 0.0015659946918537924, 0.0009713583046727934, 0.0007292056402946547, 0.0006727091108798432, 0.0007304586969373182, 0.0009487909835455563, 0.0013553331212479232, 0.0018941913968854134, 0.003082438877965567, 0.00409665052535598, 0.004874493533860768, 0.005256059659392086, 0.005784980601288857, 0.005514678617763402, 0.0050004571391072585, 0.004409828175951356, 0.004012243389524247, 0.0035475435966838345, 0.0031075066784920346, 0.0027021093405185615, 0.002336914444157967, 0.0020252898809134164, 0.0017232814390099108, 0.0, 0.0, 0.0, 0.0, 0.0]


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


def Fun_mht(ml,el,pl,jl,tree):
    TLVall=ROOT.TLorentzVector()
    TLVthis=ROOT.TLorentzVector()
    TLVall.SetPtEtaPhiE(0,0,0,0)

    if len(ml) >0:
        for mu in ml:
            TLVthis.SetPtEtaPhiE(tree.muPt[mu[0]],tree.muEta[mu[0]],tree.muPhi[mu[0]],tree.muEn[mu[0]])
            TLVall+=TLVthis

    if len(el) >0:
        for ele in el:
            TLVthis.SetPtEtaPhiE(tree.elePt[ele[0]],tree.eleEta[ele[0]],tree.elePhi[ele[0]],tree.eleEn[ele[0]])
            TLVall+=TLVthis
            
    if len(pl) >0:
        for pho in pl: 
            TLVthis.SetPtEtaPhiM(tree.phoEt[pho[0]],tree.phoEta[pho[0]],tree.phoPhi[pho[0]],0.)
            TLVall+=TLVthis

    if len(jl) >0:
        for jet in jl:
            TLVthis.SetPtEtaPhiE(tree.jetPt[jet[0]],tree.jetEta[jet[0]],tree.jetPhi[jet[0]],tree.jetEn[jet[0]])
            TLVall+=TLVthis

    return TLVall.Pt()


            
def Fun_FindGenTopPair(tree):
    result=[]
    for genp in range(tree.nMC):
        if abs(tree.mcPID[genp])==6 and tree.mcStatusFlag[genp]>>2&1==1:  # is hardprocess top
            result.append(tree.mcPt[genp])
    return result

def Fun_TopPtWeight(apt,bpt):
    result=(math.exp(0.0615-0.0005*apt)*math.exp(0.0615-0.0005*bpt))**0.5
    return result
