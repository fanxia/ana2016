#!/bin/python
#This script works on mc_step1_output.root
#Will add the pilepu weight, eff,... branches

import os
import sys
import time
import datetime
import ROOT
from ROOT import *
from array import array
from ana2016.susy import *
from ana2016.susy.ana_muon import *
from ana2016.susy.ana_ele import *
from ana2016.susy.ana_jet import *
from ana2016.susy.ana_photon import *
from ana2016.susy.Utilfunc import *
from ana2016.susy.Utilfunc_sig import *

ROOT.gSystem.Load('libCondFormatsBTauObjects') 
ROOT.gSystem.Load('libCondToolsBTau') 


sw = ROOT.TStopwatch()
sw.Start()
print "------------Start--------------"

#---------------btagweight input files-------------------
file_btagEff = TFile.Open("btag/TT_BtagEff.root")
l_btageff=file_btagEff.Get("lEff")
c_btageff=file_btagEff.Get("cEff")
b_btageff=file_btagEff.Get("bEff")

#--------------------------
v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')

file_btagSF = ROOT.BTagCalibration("csvv2","btag/CSVv2_Moriond17_B_H.csv")
#file_btagSF = ROOT.BTagCalibration("~/work/private/2016SUSY/CMSSW_8_0_24/src/ana2016/susy/script/btag/CSVv2_ichep.csv")
#bc_btagsfReader = ROOT.BTagCalibrationReader(file_btagSF,1,"mujets") # 1 for medium working point, mujets for c and b quark
#l_btagsfReader = ROOT.BTagCalibrationReader(file_btagSF,1,"comb") # 1 for medium working point, comb for light quark

btagSFreader = ROOT.BTagCalibrationReader(
    1,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
    "central",      # central systematic type
    v_sys,          # vector of other sys. types
)    

measure_type="comb"
#if sys.argv[2]=="TT_powheg": measure_type="mujets"
print measure_type
btagSFreader.load(
    file_btagSF, 
    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
    measure_type      # measurement type
)
btagSFreader.load(file_btagSF, 1, measure_type  )
btagSFreader.load(file_btagSF, 2, "incl"  ) #eta:0~2.4
#------------------------------------

file_btagCF_fastsim = ROOT.BTagCalibration("csvv","btag/CSVv2_fastsim_ttbar_26_1_2017.csv")
btagCFreader_fastsim = ROOT.BTagCalibrationReader(
    1,              # 0 is for loose op, 1: medium, 2: tight, 3: discr. reshaping
    "central",      # central systematic type
    v_sys,          # vector of other sys. types
)    
btagCFreader_fastsim.load(
    file_btagCF_fastsim, 
    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
    "fastsim"      # measurement type
)
btagCFreader_fastsim.load(file_btagCF_fastsim, 1, "fastsim"  )
btagCFreader_fastsim.load(file_btagCF_fastsim, 2, "fastsim"  ) 
#-------------------------------------

def Fun_bEffaSF(eta,pt,btagflvr,effhist):
    eff=effhist.GetBinContent(effhist.FindBin(pt,eta))
    eff_err=effhist.GetBinError(effhist.FindBin(pt,eta))
    if btagflvr==2: eta=abs(eta)
    sf=btagSFreader.eval_auto_bounds('central',btagflvr,eta,pt)
    sf_up=btagSFreader.eval_auto_bounds('up',btagflvr,eta,pt)
    sf_down=btagSFreader.eval_auto_bounds('down',btagflvr,eta,pt)
    return [eff,eff_err,sf,sf_up,sf_down]

def Fun_bEffaSF_fastsim(eta,pt,btagflvr,effhist):
    cf=btagCFreader_fastsim.eval_auto_bounds('central',btagflvr,eta,pt)

    eff=effhist.GetBinContent(effhist.FindBin(pt,eta))*cf
    eff_err=effhist.GetBinError(effhist.FindBin(pt,eta))*cf
    if btagflvr==2: eta=abs(eta)
    sf=btagSFreader.eval_auto_bounds('central',btagflvr,eta,pt)/cf
    sf_up=btagSFreader.eval_auto_bounds('up',btagflvr,eta,pt)/cf
    sf_down=btagSFreader.eval_auto_bounds('down',btagflvr,eta,pt)/cf
    return [eff,eff_err,sf,sf_up,sf_down]

#---------------END btagweight input files-------------------


#----------------lepton sf input files-----------------------
file_eleSF_HLT = TFile.Open("lepgammaSF/cutAcountEffi_eleHLT.root")
eleTrgsfHist=file_eleSF_HLT.Get("efficiency_dt")
file_eleSF_reco = TFile.Open("lepgammaSF/eleEffi-reco.root")
eleRecosfHist=file_eleSF_reco.Get("EGamma_SF2D")
file_eleSF_id = TFile.Open("lepgammaSF/eleEffi-tightID.root")
eleIDsfHist=file_eleSF_id.Get("EGamma_SF2D")

file_muSF1_HLT = TFile.Open("lepgammaSF/MuonHLTEffi_RunB2F.root")
file_muSF2_HLT = TFile.Open("lepgammaSF/MuonHLTEffi_RunGH.root")
muTrgsf1Hist=file_muSF1_HLT.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA")
muTrgsf2Hist=file_muSF2_HLT.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA")

file_muSF1_id=TFile.Open("lepgammaSF/MuonIDEffi_RunB2F.root")
file_muSF2_id=TFile.Open("lepgammaSF/MuonIDEffi_RunGH.root")
muIDsf1Hist=file_muSF1_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")
muIDsf2Hist=file_muSF2_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")

file_muSF1_iso=TFile.Open("lepgammaSF/MuonIsoEffi_RunB2F.root")
file_muSF2_iso=TFile.Open("lepgammaSF/MuonIsoEffi_RunGH.root")
muIsoSf1Hist=file_muSF1_iso.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")
muIsosf2Hist=file_muSF2_iso.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")

file_muSF1_Trk = TFile.Open("lepgammaSF/MuonTrkEffi_RunB2H.root")
file_muSF2_Trk = TFile.Open("lepgammaSF/MuonTrkEffi_RunB2H.root")
muTrksf1Hist=file_muSF1_Trk.Get("ratio_eff_aeta_dr030e030_corr")
muTrksf2Hist=file_muSF2_Trk.Get("ratio_eff_aeta_dr030e030_corr")

def Fun_thisSF(eta,pt,sfhist):
    if pt>=sfhist.GetYaxis().GetXmax(): #above pt range            
        result=[sfhist.GetBinContent(sfhist.GetXaxis().FindBin(eta),sfhist.GetYaxis().GetLast()),2.*sfhist.GetBinError(sfhist.GetXaxis().FindBin(eta),sfhist.GetYaxis().GetLast())]
    elif pt<sfhist.GetYaxis().GetXmin(): #below pt range            
        result=[sfhist.GetBinContent(sfhist.GetXaxis().FindBin(eta),1),2.*sfhist.GetBinError(sfhist.GetXaxis().FindBin(eta),1)]

    else: result=[sfhist.GetBinContent(sfhist.FindBin(eta,pt)),sfhist.GetBinError(sfhist.FindBin(eta,pt))]
    return result

def Fun_thisSFTGraph(par,sfhist):
    result=[sfhist.Eval(par)] #don't know how to get the error yet                                               
    return result


print "The egamma sf input file is ",file_eleSF_HLT.GetName()
#---------------END lepton sf input files----------------------- 

#---------------pho sf input files----------------------------
file_phoSF=TFile.Open("lepgammaSF/gammaIDsf.root")
file_phoPixSF=TFile.Open("lepgammaSF/gammaPixelvetosf.root")
phosfHist=file_phoSF.Get("EGamma_SF2D")
phoPixsfHist=file_phoPixSF.Get("Scaling_Factors_HasPix_R9 Inclusive")


###------------find stop xsec from .dat file-------------------
#stopxsfile="sigxsec/stop_pair_13TeVxs.dat"
stopxslist=[[float(element) for element in line.strip().split()] for line in open("sigxsec/stop_pair_13TeVxs.dat").read().strip().split('\n')]
stopxsdic={i[0]:i[1:] for i in stopxslist}


###################################################################
###################################################################

INPUTFile=sys.argv[1]
file_in=TFile.Open(INPUTFile)
file_out=TFile("../ntupleStore/step1p5_"+sys.argv[2]+".root","recreate")

DoTopPtReweight=False
if "TT" in sys.argv[2]:
    DoTopPtReweight=True
    print "Add top pair pt reweighting info!"

print "input: ",INPUTFile
print "output: ",sys.argv[2]+"_step1p5.root"

H_sigscan=file_in.Get('H_sigscan').Clone()

Treenames=['EventTree_ele','EventTree_eQCD','EventTree_mu','EventTree_mQCD']
Trees_in=[file_in.Get(treename) for treename in Treenames]

#-----------------define the additional branches object--------------
BTotalEventsNumber=array('d',[1.])
BgenWeightTotalEventsNumber=array('d',[1.])
BpileupWeight=array('d',[1.])
BbtagWeight=array('d',[1.])
BbtagWeightUp=array('d',[1.])
BbtagWeightDown=array('d',[1.])
BbtagWeightErr=array('d',[1.])
BphoWeight=array('d',[1.])
BphoWeightErr=array('d',[1.])
BtopPtWeight=array('d',[1.])

BeleRecosf=array('d',[1.])
BeleIDsf=array('d',[1.])
BeleIsosf=array('d',[1.])
BeleTrgsf=array('d',[1.])
BeleWeight=array('d',[1.])  # for the total weight=eleidSF*isoSF*trgSF
#BtopPtWeight=array('d',[1.])

BmuID1sf=array('d',[1.]) # These are for 2016RunBCDEF~period1 
BmuIso1sf=array('d',[1.])
BmuTrg1sf=array('d',[1.])
BmuTrk1sf=array('d',[1.])
BmuWeight1=array('d',[1.])  # for the total weight=muidSF*isoSF*trgSF

BmuID2sf=array('d',[1.]) # These are for 2016RunGH~period2
BmuIso2sf=array('d',[1.])
BmuTrg2sf=array('d',[1.])
BmuTrk2sf=array('d',[1.])
BmuWeight2=array('d',[1.])  # for the total weight=muidSF*isoSF*trgSF


################# branches for fastsim SUSY signal
#BmasspointEventsNumber=array('d',[-99])
Bstopxsec=array('d',[-99.])
BstopxsecErr=array('d',[-99.])
BnlspBr=array('d',[-99.])
Bnlspdecayweight=array('d',[-99.])
BTotalScanpointEventsNumber=array('d',[-99.])

#-----------------define the branches-------------------------------
for tree_in in Trees_in:
    tree_out=tree_in.CloneTree(0)
    tree_out.Branch("BTotalEventsNumber",BTotalEventsNumber,"BTotalEventsNumber/D")
    tree_out.Branch("BgenWeightTotalEventsNumber",BgenWeightTotalEventsNumber,"BgenWeightTotalEventsNumber/D")
    tree_out.Branch("BTotalScanpointEventsNumber",BTotalScanpointEventsNumber,"BTotalScanpointEventsNumber/D")
    tree_out.Branch("BpileupWeight",BpileupWeight,"BpileupWeight/D")
    tree_out.Branch("BbtagWeight",BbtagWeight,"BbtagWeight/D")
    tree_out.Branch("BbtagWeightUp",BbtagWeightUp,"BbtagWeightUp/D")
    tree_out.Branch("BbtagWeightDown",BbtagWeightDown,"BbtagWeightDown/D")
    tree_out.Branch("BbtagWeightErr",BbtagWeightErr,"BbtagWeightErr/D")
    
    tree_out.Branch("BeleRecosf",BeleRecosf,"BeleRecosf/D")
    tree_out.Branch("BeleIDsf",BeleIDsf,"BeleIDsf/D")
    tree_out.Branch("BeleIsosf",BeleIsosf,"BeleIsosf/D")
    tree_out.Branch("BeleTrgsf",BeleTrgsf,"BeleTrgsf/D")
    tree_out.Branch("BeleWeight",BeleWeight,"BeleWeight/D")

#    tree_out.Branch("BmuRecosf",BmuRecosf,"BmuRecosf/D")
    tree_out.Branch("BmuID1sf",BmuID1sf,"BmuID1sf/D")
    tree_out.Branch("BmuIso1sf",BmuIso1sf,"BmuIso1sf/D")
    tree_out.Branch("BmuTrg1sf",BmuTrg1sf,"BmuTrg1sf/D")
    tree_out.Branch("BmuTrk1sf",BmuTrk1sf,"BmuTrk1sf/D")
    tree_out.Branch("BmuWeight1",BmuWeight1,"BmuWeight1/D")

    tree_out.Branch("BmuID2sf",BmuID2sf,"BmuID2sf/D")
    tree_out.Branch("BmuIso2sf",BmuIso2sf,"BmuIso2sf/D")
    tree_out.Branch("BmuTrg2sf",BmuTrg2sf,"BmuTrg2sf/D")
    tree_out.Branch("BmuTrk2sf",BmuTrk2sf,"BmuTrk2sf/D")
    tree_out.Branch("BmuWeight2",BmuWeight2,"BmuWeight2/D")


    tree_out.Branch("BphoWeight",BphoWeight,"BphoWeight/D")
    tree_out.Branch("BphoWeightErr",BphoWeightErr,"BphoWeightErr/D")

    tree_out.Branch("BtopPtWeight",BtopPtWeight,"BtopPtWeight/D")

    tree_out.Branch("Bstopxsec",Bstopxsec,"Bstopxsec/D")
    tree_out.Branch("BstopxsecErr",BstopxsecErr,"BstopxsecErr/D")
    tree_out.Branch("BnlspBr",BnlspBr,"BnlspBr/D")
    tree_out.Branch("Bnlspdecayweight",Bnlspdecayweight,"Bnlspdecayweight/D")


#----------------ending branches definitions-------------------------

    BTotalEventsNumber[0]=file_in.Get("H_event").GetBinContent(1)
    BgenWeightTotalEventsNumber[0]=file_in.Get("H_event").GetBinContent(2)

    if tree_in.GetName() in ['EventTree_ele','EventTree_eQCD']:
        TreeMODE=12
    elif tree_in.GetName() in ['EventTree_mu','EventTree_mQCD']:
        TreeMODE=34
#        lepTrgsf=muTrgsf
    nprocessed=0
#-----------------Starting loop------------
    for event in tree_in:
        BTotalScanpointEventsNumber[0]=H_sigscan.GetBinContent(H_sigscan.FindBin(event.BlheStopMass,event.BlheNLSPMass))
        nprocessed+=1
#***********************Fill PU weight info***********************
        BpileupWeight[0]=Fun_pileupweight_fastsim(event.BPUTrue)


#***********************Fill top pair pt reweight info************
        if DoTopPtReweight:
            BtopPtWeight[0]=Fun_TopPtWeight(event.BGenTopAPt,event.BGenTopBPt)

#***********************Fill Btag weight info***********************
        Jetlist=[]
        for j in range(event.Bnjet):
            Jet_flavor=event.BjetHadFlvr[j]
            if abs(Jet_flavor)==0: #light
                bEffaSF=Fun_bEffaSF_fastsim(event.BjetEta[j],event.BjetPt[j],2,l_btageff)
            elif abs(Jet_flavor)==4: #c
                bEffaSF=Fun_bEffaSF_fastsim(event.BjetEta[j],event.BjetPt[j],1,c_btageff)
            elif abs(Jet_flavor)==5: #b
                bEffaSF=Fun_bEffaSF_fastsim(event.BjetEta[j],event.BjetPt[j],0,b_btageff)
            else: continue

            Jet=[event.Bbtagged[j]]
            Jet+=bEffaSF
            Jetlist.append(Jet)
        btagWeightCentral=Fun_btagweight(Jetlist,'central')
        BbtagWeight[0]=btagWeightCentral[0]
        BbtagWeightErr[0]=btagWeightCentral[1]
        BbtagWeightUp[0]=Fun_btagweight(Jetlist,'up')[0]
        BbtagWeightDown[0]=Fun_btagweight(Jetlist,'down')[0]



#***********************Fill lepton sf & weight info*********************** 

        if TreeMODE==12:   #eTree and eQCDtree
            eletrig=Fun_thisSF(event.BeleSCEta,event.BelePt,eleTrgsfHist)
            elereco=Fun_thisSF(event.BeleSCEta,event.BelePt,eleRecosfHist)
            eleid=Fun_thisSF(event.BeleSCEta,event.BelePt,eleIDsfHist)
            BeleTrgsf[0]=eletrig[0]
            BeleRecosf[0]=elereco[0]
            BeleIDsf[0]=eleid[0]
            BeleWeight[0]=BeleRecosf[0]*BeleIDsf[0]*BeleIsosf[0]*BeleTrgsf[0]                                          
        elif TreeMODE==34:
            mutrk=[Fun_thisSFTGraph(abs(event.BmuEta),muTrksf1Hist),Fun_thisSFTGraph(abs(event.BmuEta),muTrksf2Hist)]  #[[period1SF,period1SFerr],[period2SF,period2SFerr]]
            mutrig=[Fun_thisSF(abs(event.BmuEta),event.BmuPt,muTrgsf1Hist),Fun_thisSF(abs(event.BmuEta),event.BmuPt,muTrgsf2Hist)]  #[[period1SF,period1SFerr],[period2SF,period2SFerr]]
            muid=[Fun_thisSF(abs(event.BmuEta),event.BmuPt,muIDsf1Hist),Fun_thisSF(abs(event.BmuEta),event.BmuPt,muIDsf2Hist)]                  
            muiso=[Fun_thisSF(abs(event.BmuEta),event.BmuPt,muIsoSf1Hist),Fun_thisSF(abs(event.BmuEta),event.BmuPt,muIsosf2Hist)]
            BmuID1sf[0]=muid[0][0]
            BmuID2sf[0]=muid[1][0]
            BmuIso1sf[0]=muiso[0][0]
            BmuIso2sf[0]=muiso[1][0]
            BmuTrg1sf[0]=mutrig[0][0]
            BmuTrg2sf[0]=mutrig[1][0]
            BmuTrk1sf[0]=mutrk[0][0]
            BmuTrk2sf[0]=mutrk[1][0]
            BmuWeight1[0]=BmuID1sf[0]*BmuIso1sf[0]*BmuTrg1sf[0]*BmuTrk1sf[0]
            BmuWeight2[0]=BmuID2sf[0]*BmuIso2sf[0]*BmuTrg2sf[0]*BmuTrk2sf[0]

#***********************Fil photon sf & weight info***********************
        phoWeight=1.
        phoWeightE2=0.
        for p in range(event.BnCandPho):
            if (event.BCandPhoTag[p]>>3&1)==1:  #only consider real loose photon's sf
                pho_pt=event.BCandphoEt[p]
                pho_eta=event.BCandphoSCEta[p]
                
                pho_sf=Fun_thisSF(pho_eta,pho_pt,phosfHist)
                pho_pixsf=Fun_thisSF(abs(pho_eta),pho_pt,phoPixsfHist) #no pt dependance
                phoWeight*=pho_sf[0]*pho_pixsf[0]
                phoWeightE2+=(pho_sf[1])**2/(pho_sf[0])**2+(pho_pixsf[1])**2/(pho_pixsf[0])**2
#                if pho_sf<0.1: print "photon: ",pho_pt,pho_eta
        BphoWeight[0]=phoWeight
        BphoWeightErr[0]=phoWeightE2**0.5*phoWeight
                                                  

#***********************Fill Signal MC info*********************
        stopxs=stopxsdic[event.BlheStopMass]#write a method to read txt file and pick xsec of stop mass
        Bstopxsec[0]=stopxs[0]
        BstopxsecErr[0]=stopxs[1]

        nlspdecay=Fun_SigNLSPBR(event.BlheNLSPMass,event.BNLSPDecay)
        BnlspBr[0]=nlspdecay[0]
        Bnlspdecayweight[0]=nlspdecay[1]


        tree_out.Fill()


        BpileupWeight[0]=1.
        BbtagWeight[0]=1.
        BbtagWeightUp[0]=1.
        BbtagWeightDown[0]=1.
        BbtagWeightErr[0]=1.
        BeleRecosf[0]=1.
        BeleIDsf[0]=1.
        BeleIsosf[0]=1.
        BeleTrgsf[0]=1.
        BeleWeight[0]=1.
        BmuID1sf[0]=1.
        BmuIso1sf[0]=1.
        BmuTrg1sf[0]=1.
        BmuTrk1sf[0]=1.
        BmuWeight1[0]=1.
        BmuID2sf[0]=1.
        BmuIso2sf[0]=1.
        BmuTrg2sf[0]=1.
        BmuTrk2sf[0]=1.
        BmuWeight2[0]=1.

        BphoWeight[0]=1.
        BphoWeightErr[0]=1.

        Bstopxsec[0]=-99.
        BstopxsecErr[0]=-99.
        BnlspBr[0]=-99.
        Bnlspdecayweight[0]=-99.


    tree_out.Write()

file_out.Write()
file_out.Close()

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
