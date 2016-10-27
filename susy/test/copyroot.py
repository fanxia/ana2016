import ROOT
import sys
import os

from ROOT import *

sw=ROOT.TStopwatch()
sw.Start()

  #get old file, old tree and set top branch address
#oldfile=TFile.Open('~/eos/cms/store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016D_PRv2.root')
oldfile=TFile.Open('~/eos/cms/store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_DYJetsToLL_m50_aMCatNLO.root')
oldtree=oldfile.Get('ggNtuplizer/EventTree')
oldtree.SetBranchStatus("*",1)
nEntries=oldtree.GetEntries()
#new file to store some entries
#newfile=ROOT.TFile("photon_data_example.root","recreate")
newfile=ROOT.TFile("Sample_job_spring16_DYJetsToLL_m50_aMCatNLO.root","recreate")
newdir=newfile.mkdir("ggNtuplizer")
newdir.cd()
newtree=oldtree.CloneTree(100000)
newfile.Write()
newfile.Close()


sw.Stop()
print "Real time:"+ str(sw.RealTime()/60.0) + " min"
print "CPU time:"+ str(sw.CpuTime()/60.0) + " min"
