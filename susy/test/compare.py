#!/bin/python
from ROOT import *

# data15=TFile.Open("../ntupleStore/step1_SingleEle_Run2015D.root")
# data16=TFile.Open("../ntupleStore/step1_SingleEleRun2016D.root")

# t1=data15.Get("EventTree_ele")
# t2=data16.Get("EventTree_ele")

# t1.Draw("BelePt>>h1")
# t2.Draw("BelePt>>h2")
# h3=h1.Clone("h3")
# h3.Divide(h2)


# h1.Draw()
# gPad.SetLogy()
# h2.Draw("Same")
# h3.Draw("Same")

# h1.Print("cop.png")


data16=TFile.Open('~/eos/cms/store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016D_PRv2.root')
wjetsmc=TFile.Open("~/eos/cms/store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_WJetsToLNu_aMCatNLO.root")

t1=data16.Get("ggNtuplizer/EventTree")
t2=wjetsmc.Get("ggNtuplizer/EventTree")

t1.Draw("nJet:nVtx>>h1","","prof")
t2.Draw("nJet:nVtx>>h2","","prof")

h3=h1.Clone("h3")
h1.Draw()
h2.Draw("Same")
h3.Divide(h2)
h3.Draw("Same")
