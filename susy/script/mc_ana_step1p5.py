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


sw = ROOT.TStopwatch()
sw.Start()
print "------------Start--------------"

#---------------btagweight input files-------------------
file_btagEff = TFile.Open("~/work/private/2016SUSY/CMSSW_8_0_11/src/ana2016/susy/script/btag/")
l_btageff=btageffile.Get("lEff")
c_btageff=btageffile.Get("cEff")
b_btageff=btageffile.Get("bEff")

file_btagSF = ROOT.BTagCalibration("csvv2","~/work/private/2016SUSY/CMSSW_8_0_11/src/ana2016/susy/script/btag/CSVv2_ichep.csv")
bc_btagsfReader = ROOT.BTagCalibrationReader(file_btagSF,1,"mujets") # 1 for medium working point, mujets for c and b quark
l_btagsfReader = ROOT.BTagCalibrationReader(file_btagSF,1,"comb") # 1 for medium working point, comb for light quark



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


#-----------------define the branches-------------------------------
for tree_in in Trees_in:
    tree_out=tree_in.CloneTree(0)
    tree_out.Branch("BpileupWeight",BpileupWeight,"BpileupWeight/D")
    tree_out.Branch("BbtagWeight",BbtagWeight,"BbtagWeight/D")


#----------------ending branches definitions-------------------------


#-----------------Starting loop------------
    for event in tree_in:
        
        BpileupWeight[0]=Fun_pileupweight(event.BPUTrue)
        BbtagWeight[0]=Fun_btagweight()

        tree_out.Fill()


        BpileupWeight[0]=1.
        BbtagWeight[0]=1.



    tree_out.Write()

file_out.Write()
file_out.Close()

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"
