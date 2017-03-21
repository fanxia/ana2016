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

def Fun_bEffaSF(eta,pt,btagflvr,effhist):
    eff=effhist.GetBinContent(effhist.FindBin(pt,eta))
    eff_err=effhist.GetBinError(effhist.FindBin(pt,eta))
    if btagflvr==2: eta=abs(eta)
    sf=btagSFreader.eval_auto_bounds('central',btagflvr,eta,pt)
    sf_up=btagSFreader.eval_auto_bounds('up',btagflvr,eta,pt)
    sf_down=btagSFreader.eval_auto_bounds('down',btagflvr,eta,pt)
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
muTrgsf1Hist=file_muSF1_HLT.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio")
muTrgsf2Hist=file_muSF2_HLT.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio")

file_muSF1_id=TFile.Open("lepgammaSF/MuonIDEffi_RunB2F.root")
file_muSF2_id=TFile.Open("lepgammaSF/MuonIDEffi_RunGH.root")
muIDsf1Hist=file_muSF1_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")
muIDsf2Hist=file_muSF2_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")

file_muSF1_iso=TFile.Open("lepgammaSF/MuonIsoEffi_RunB2F.root")
file_muSF2_iso=TFile.Open("lepgammaSF/MuonIsoEffi_RunGH.root")
muIsosf1Hist=file_muSF1_iso.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")
muIsosf2Hist=file_muSF2_iso.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")

file_muSF1_Trk = TFile.Open("lepgammaSF/MuonTrkEffi_RunB2H.root")
file_muSF2_Trk = TFile.Open("lepgammaSF/MuonTrkEffi_RunB2H.root")
muTrksf1Hist=file_muSF1_Trk.Get("ratio_eff_aeta_dr030e030_corr")
muTrksf2Hist=file_muSF2_Trk.Get("ratio_eff_aeta_dr030e030_corr")


def Fun_thisSF(eta,pt,sfhist):
    if pt>=sfhist.GetYaxis().GetXmax(): #above pt range
        result=[sfhist.GetBinContent(sfhist.GetXaxis().FindBin(eta),sfhist.GetYaxis().GetLast()),2.*sfhist.GetBinError(sfhist.GetXaxis().FindBin(eta),sfhist.GetYaxis().GetLast())]
    else: result=[sfhist.GetBinContent(sfhist.FindBin(eta,pt)),sfhist.GetBinError(sfhist.FindBin(eta,pt))]
    return result

def Fun_thisSFTGraph(par,sfhist):
    result=[sfhist.Eval(par)] #don't know how to get the error yet
    return result




#file_muSF = TFile.Open(".root")  
#muTrgsf=file_muSF.Get("")

print "The egamma sf input file is ",file_eleSF_HLT.GetName()
#---------------END lepton sf input files----------------------- 


###################################################################
###################################################################

INPUTFile=sys.argv[1]
file_in=TFile.Open(INPUTFile)
file_out=TFile("../ntupleStore/step1p5_"+sys.argv[2]+"_dilep.root","recreate")

#DoTopPtReweight=False
#if "TT" in sys.argv[2]:
#    DoTopPtReweight=True
#    print "Add top pair pt reweighting info!"

print "input: ",INPUTFile
print "output: ",sys.argv[2]+"_step1p5.root"

Treenames=['EventTree_ee','EventTree_mumu']
Trees_in=[file_in.Get(treename) for treename in Treenames]

#-----------------define the additional branches object--------------
BTotalEventsNumber=array('d',[1.])
BgenWeightTotalEventsNumber=array('d',[1.])
BpileupWeight=array('d',[1.])
BbtagWeight=array('d',[1.])
BbtagWeightUp=array('d',[1.])
BbtagWeightDown=array('d',[1.])
BbtagWeightErr=array('d',[1.])
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


#-----------------define the branches-------------------------------
for tree_in in Trees_in:
    tree_out=tree_in.CloneTree(0)
    tree_out.Branch("BTotalEventsNumber",BTotalEventsNumber,"BTotalEventsNumber/D")
    tree_out.Branch("BgenWeightTotalEventsNumber",BgenWeightTotalEventsNumber,"BgenWeightTotalEventsNumber/D")
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

#    tree_out.Branch("BtopPtWeight",BtopPtWeight,"BtopPtWeight/D")
#----------------ending branches definitions-------------------------

    BTotalEventsNumber[0]=file_in.Get("H_event").GetBinContent(1)
    BgenWeightTotalEventsNumber[0]=file_in.Get("H_event").GetBinContent(2)

    if tree_in.GetName() in ['EventTree_ee']:
        TreeMODE='eeTree'
    elif tree_in.GetName() in ['EventTree_mumu']:
        TreeMODE='mumuTree'
    nprocessed=0
#-----------------Starting loop------------
    for event in tree_in:
        
        nprocessed+=1
#***********************Fill PU weight info***********************
        BpileupWeight[0]=Fun_pileupweight(event.BPUTrue)


#***********************Fill top pair pt reweight info************
#        if DoTopPtReweight:
#            BtopPtWeight[0]=Fun_TopPtWeight(event.BGenTopAPt,event.BGenTopBPt)

#***********************Fill Btag weight info***********************
        Jetlist=[]
        for j in range(event.Bnjet):
            Jet_flavor=event.BjetHadFlvr[j]
            if abs(Jet_flavor)==0: #light
                bEffaSF=Fun_bEffaSF(event.BjetEta[j],event.BjetPt[j],2,l_btageff)
            elif abs(Jet_flavor)==4: #c
                bEffaSF=Fun_bEffaSF(event.BjetEta[j],event.BjetPt[j],1,c_btageff)
            elif abs(Jet_flavor)==5: #b
                bEffaSF=Fun_bEffaSF(event.BjetEta[j],event.BjetPt[j],0,b_btageff)
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

        if TreeMODE=='eeTree':   #eeTree
            ele1trig=Fun_thisSF(abs(event.BeleSCEta[0]),event.BelePt[0],eleTrgsfHist)
            ele2trig=Fun_thisSF(abs(event.BeleSCEta[1]),event.BelePt[1],eleTrgsfHist)
            BeleTrgsf[0]=ele1trig[0]+ele2trig[0]-ele1trig[0]*ele2trig[0]

            ele1reco=Fun_thisSF(event.BeleSCEta[0],event.BelePt[0],eleRecosfHist)
            ele2reco=Fun_thisSF(event.BeleSCEta[1],event.BelePt[1],eleRecosfHist)
            BeleRecosf[0]=ele1reco[0]*ele2reco[0]

            ele1id=Fun_thisSF(event.BeleSCEta[0],event.BelePt[0],eleIDsfHist)
            ele2id=Fun_thisSF(event.BeleSCEta[1],event.BelePt[1],eleIDsfHist)
            BeleIDsf[0]=ele1id[0]*ele2id[0]
            BeleWeight[0]=BeleRecosf[0]*BeleIDsf[0]*BeleIsosf[0]*BeleTrgsf[0]                                          

        elif TreeMODE=='mumuTree':   #mutree and muqcdtree
            mu1trig=[Fun_thisSF(abs(event.BmuEta[0]),event.BmuPt[0],muTrgsf1Hist),Fun_thisSF(abs(event.BmuEta[0]),event.BmuPt[0],muTrgsf2Hist)]  #[[period1SF,period1SFerr],[period2SF,period2SFerr]]
            mu2trig=[Fun_thisSF(abs(event.BmuEta[1]),event.BmuPt[1],muTrgsf1Hist),Fun_thisSF(abs(event.BmuEta[1]),event.BmuPt[1],muTrgsf2Hist)]
            BmuTrg1sf[0]=mu1trig[0][0]+mu2trig[0][0]-mu1trig[0][0]*mu2trig[0][0] #period1 totalSF
            BmuTrg2sf[0]=mu1trig[1][0]+mu2trig[1][0]-mu1trig[1][0]*mu2trig[1][0] #period2 totalSF

            mu1trk=[Fun_thisSFTGraph(abs(event.BmuEta[0]),muTrksf1Hist),Fun_thisSFTGraph(abs(event.BmuEta[0]),muTrksf2Hist)]  #[[period1SF,period1SFerr],[period2SF,period2SFerr]]
            mu2trk=[Fun_thisSFTGraph(abs(event.BmuEta[1]),muTrksf1Hist),Fun_thisSFTGraph(abs(event.BmuEta[1]),muTrksf2Hist)]
            BmuTrk1sf[0]=mu1trk[0][0]*mu2trk[0][0] #period1 totalSF
            BmuTrk2sf[0]=mu1trk[1][0]*mu2trk[1][0] #period2 totalSF



            mu1id=[Fun_thisSF(abs(event.BmuEta[0]),event.BmuPt[0],muIDsf1Hist),Fun_thisSF(abs(event.BmuEta[0]),event.BmuPt[0],muIDsf2Hist)]  #first mu sf
            mu2id=[Fun_thisSF(abs(event.BmuEta[1]),event.BmuPt[1],muIDsf1Hist),Fun_thisSF(abs(event.BmuEta[1]),event.BmuPt[1],muIDsf2Hist)]  #second mu sf
            BmuID1sf[0]=mu1id[0][0]*mu2id[0][0]
            BmuID2sf[0]=mu1id[1][0]*mu2id[1][0]

            mu1iso=[Fun_thisSF(abs(event.BmuEta[0]),event.BmuPt[0],muIsosf1Hist),Fun_thisSF(abs(event.BmuEta[0]),event.BmuPt[0],muIsosf2Hist)]
            mu2iso=[Fun_thisSF(abs(event.BmuEta[1]),event.BmuPt[1],muIsosf1Hist),Fun_thisSF(abs(event.BmuEta[1]),event.BmuPt[1],muIsosf2Hist)]
            BmuIso1sf[0]=mu1iso[0][0]*mu2iso[0][0]
            BmuIso2sf[0]=mu1iso[1][0]*mu2iso[1][0]

            BmuWeight1[0]=BmuTrk1sf[0]*BmuID1sf[0]*BmuIso1sf[0]*BmuTrg1sf[0]                                    
            BmuWeight2[0]=BmuTrk2sf[0]*BmuID2sf[0]*BmuIso2sf[0]*BmuTrg2sf[0]                                                                  

        

     
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


    tree_out.Write()

file_out.Write()
file_out.Close()

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
