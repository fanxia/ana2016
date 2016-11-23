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
btagSFreader.load(
    file_btagSF, 
    0,          # 0 is for b flavour, 1: FLAV_C, 2: FLAV_UDSG 
    "comb"      # measurement type
)
btagSFreader.load(file_btagSF, 1, "comb"  )
btagSFreader.load(file_btagSF, 2, "incl"  ) #eta:0~2.4



#---------------END btagweight input files-------------------



INPUTFile=sys.argv[1]
file_in=TFile.Open(INPUTFile)
file_out=TFile("../ntupleStore/step1p5_"+sys.argv[2]+".root","recreate")

print "input: ",INPUTFile
print "output: ",sys.argv[2]+"_step1p5.root"

Treenames=['EventTree_ele','EventTree_eQCD','EventTree_mu','EventTree_mQCD']
Trees_in=[file_in.Get(treename) for treename in Treenames]

#-----------------define the additional branches object--------------

BpileupWeight=array('d',[1.])
BbtagWeight=array('d',[1.])
BbtagWeightUp=array('d',[1.])
BbtagWeightDown=array('d',[1.])
BbtagWeightErr=array('d',[1.])


#-----------------define the branches-------------------------------
for tree_in in Trees_in:
    tree_out=tree_in.CloneTree(0)
    tree_out.Branch("BpileupWeight",BpileupWeight,"BpileupWeight/D")
    tree_out.Branch("BbtagWeight",BbtagWeight,"BbtagWeight/D")
    tree_out.Branch("BbtagWeightUp",BbtagWeightUp,"BbtagWeightUp/D")
    tree_out.Branch("BbtagWeightDown",BbtagWeightDown,"BbtagWeightDown/D")
    tree_out.Branch("BbtagWeightErr",BbtagWeightErr,"BbtagWeightErr/D")


#----------------ending branches definitions-------------------------


#-----------------Starting loop------------
    for event in tree_in:
        
        BpileupWeight[0]=Fun_pileupweight(event.BPUTrue)

#-------------------------
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

        tree_out.Fill()


        BpileupWeight[0]=1.
        BbtagWeight[0]=1.
        BbtagWeightUp[0]=1.
        BbtagWeightDown[0]=1.
        BbtagWeightErr[0]=1.



    tree_out.Write()

file_out.Write()
file_out.Close()

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
