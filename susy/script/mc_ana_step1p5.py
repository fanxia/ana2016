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
file_btagEff = TFile.Open("btag/"+sys.argv[2]+"_BtagEff.root")
l_btageff=file_btagEff.Get("lEff")
c_btageff=file_btagEff.Get("cEff")
b_btageff=file_btagEff.Get("bEff")

v_sys = getattr(ROOT, 'vector<string>')()
v_sys.push_back('up')
v_sys.push_back('down')

file_btagSF = ROOT.BTagCalibration("csvv2","btag/CSVv2_ichep.csv")
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
#---------------END btagweight input files-------------------


#----------------lepton sf input files-----------------------
file_eleSF = TFile.Open("lepSF/egammaEffi.root")
eleTrgsf=file_eleSF.Get("efficiency_dt")

file_muSF = TFile.Open(".root")  
muTrgsf=file_muSF.Get("")

print "The egamma sf input file is######### ",file_eleSF.GetName()
#---------------END lepton sf input files----------------------- 


###################################################################
###################################################################

INPUTFile=sys.argv[1]
file_in=TFile.Open(INPUTFile)
file_out=TFile("../ntupleStore/step1p5_"+sys.argv[2]+".root","recreate")

print "input: ",INPUTFile
print "output: ",sys.argv[2]+"_step1p5.root"

Treenames=['EventTree_ele','EventTree_eQCD','EventTree_mu','EventTree_mQCD']
Trees_in=[file_in.Get(treename) for treename in Treenames]

#-----------------define the additional branches object--------------
BTotalEventsNumber=array('d',[1.])# used to save the totaleventsnumbers that have been processed
BpileupWeight=array('d',[1.])
BbtagWeight=array('d',[1.])
BbtagWeightUp=array('d',[1.])
BbtagWeightDown=array('d',[1.])
BbtagWeightErr=array('d',[1.])
BlepIDsf=array('d',[1.])
BlepIsosf=array('d',[1.])
BlepTrgsf=array('d',[1.])
BlepWeight=array('d',[1.])  # for the total weight=lepidSF*isoSF*trgSF


#-----------------define the branches-------------------------------
for tree_in in Trees_in:
    tree_out=tree_in.CloneTree(0)
    tree_out.Branch("BTotalEventsNumber",BTotalEventsNumber,"BTotalEventsNumber/D")
    tree_out.Branch("BpileupWeight",BpileupWeight,"BpileupWeight/D")
    tree_out.Branch("BbtagWeight",BbtagWeight,"BbtagWeight/D")
    tree_out.Branch("BbtagWeightUp",BbtagWeightUp,"BbtagWeightUp/D")
    tree_out.Branch("BbtagWeightDown",BbtagWeightDown,"BbtagWeightDown/D")
    tree_out.Branch("BbtagWeightErr",BbtagWeightErr,"BbtagWeightErr/D")
    
    tree_out.Branch("BlepIDsf",BlepIDsf,"BlepIDsf/D")
    tree_out.Branch("BlepIsosf",BlepIsosf,"BlepIsosf/D")
    tree_out.Branch("BlepTrgsf",BlepTrgsf,"BlepTrgsf/D")
    tree_out.Branch("BlepWeight",BlepWeight,"BlepWeight/D")

#----------------ending branches definitions-------------------------
    BTotalEventsNumber[0]=file_in.Get("H_ele").GetBinContent(1)

    if tree_in.GetName() in ['EventTree_ele','EventTree_eQCD']:
        TreeMODE=12
        lepTrgsf=eleTrgsf
    elif tree_in.GetName() in ['EventTree_mu','EventTree_mQCD']:
        TreeMODE=34
        lepTrgsf=muTrgsf

#-----------------Starting loop------------
    for event in tree_in:
        

#***********************Fill PU weight info***********************
        BpileupWeight[0]=Fun_pileupweight(event.BPUTrue)

#***********************Fill Btag weight info***********************
        Jetlist=[]
        for j in range(len(event.BjetPt)):
            Jet_pt=event.BjetPt[j]
            Jet_eta=event.BjetEta[j]
            Jet_SFeta=Jet_eta # sometimes, the eta range in SF file only has abs value, like for light quarks
            Jet_flavor=event.BjetHadFlvr[j]
            if abs(Jet_flavor)==0: #light
                JetBTagFlav=2
                Jet_SFeta=abs(Jet_eta)
                Jet_eff_hist=l_btageff
            elif abs(Jet_flavor)==4: #c
                JetBTagFlav=1
                Jet_eff_hist=c_btageff
            elif abs(Jet_flavor)==5: #b
                JetBTagFlav=0
                Jet_eff_hist=b_btageff
            else: continue

            Jet_eff=Jet_eff_hist.GetBinContent(Jet_eff_hist.FindBin(Jet_pt,Jet_eta))
            Jet_eff_err=Jet_eff_hist.GetBinError(Jet_eff_hist.FindBin(Jet_pt,Jet_eta))
            Jet_sf=btagSFreader.eval_auto_bounds('central',JetBTagFlav,Jet_SFeta,Jet_pt)
            Jet_sf_up=btagSFreader.eval_auto_bounds('up',JetBTagFlav,Jet_SFeta,Jet_pt)
            Jet_sf_down=btagSFreader.eval_auto_bounds('down',JetBTagFlav,Jet_SFeta,Jet_pt)
            Jet=[event.Bbtagged[j],Jet_eff,Jet_eff_err,Jet_sf,Jet_sf_up,Jet_sf_down]
            Jetlist.append(Jet)
        btagWeightCentral=Fun_btagweight(Jetlist,'central')
        BbtagWeight[0]=btagWeightCentral[0]
        BbtagWeightErr[0]=btagWeightCentral[1]
        BbtagWeightUp[0]=Fun_btagweight(Jetlist,'up')[0]
        BbtagWeightDown[0]=Fun_btagweight(Jetlist,'down')[0]



#***********************Fill lepton sf & weight info*********************** 

        if TreeMODE==12:
            lep_pt=event.BelePt
            lep_eta=event.BeleEta  # will use sc_eta later
        elif TreeMODE==34:
            lep_pt=event.BmuPt
            lep_eta=event.BmuEta
        BlepTrgsf[0]=lepTrgsf.GetBinContent(lepTrgsf.FindBin(lep_eta,lep_pt))
        


        tree_out.Fill()


        BpileupWeight[0]=1.
        BbtagWeight[0]=1.
        BbtagWeightUp[0]=1.
        BbtagWeightDown[0]=1.
        BbtagWeightErr[0]=1.
        BlepIDsf[0]=1.
        BlepIsosf[0]=1.
        BlepTrgsf[0]=1.
        BlepWeight[0]=1.


    tree_out.Write()

file_out.Write()
file_out.Close()

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
