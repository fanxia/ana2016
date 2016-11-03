#!/bin/python
#To calculate the MC btag eff using the whole loose jets
import os
import sys
import time
import datetime
import ROOT
from ROOT import *

from ana2016.susy import *
from ana2016.susy.ana_muon import *
from ana2016.susy.ana_ele import *
from ana2016.susy.ana_jet import *
from ana2016.susy.ana_photon import *
from ana2016.susy.Utilfunc import *



chain_in = ROOT.TChain("ggNtuplizer/EventTree")
#chain_in.Add("../preselected/reduced_Muchannel_dataSingleMu.root")
chain_in.Add(sys.argv[1])
chain_in.SetBranchStatus("AK8*",0)
print"Total events for processing: ",chain_in.GetEntries()

file_out = ROOT.TFile("btageff_"+sys.argv[2]+".root","recreate")
file_out.cd()

ptNBins=200
ptMin=0
ptMax=1000
etaNBins=24
etaMin=-2.4
etaMax=2.4

num_bjets = ROOT.TH2D("bjets", "bjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_bjets.Sumw2();
num_btags = ROOT.TH2D("btags", "btags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_btags.Sumw2();
num_cjets = ROOT.TH2D("cjets", "cjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_cjets.Sumw2();
num_ctags = ROOT.TH2D("ctags", "ctags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ctags.Sumw2();
num_ljets = ROOT.TH2D("ljets", "ljets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ljets.Sumw2();
num_ltags = ROOT.TH2D("ltags", "ltags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ltags.Sumw2();

#num_tempjets = ROOT.TH2D("tempjets", "tempjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_tempjets.Sumw2();
#num_temptags = ROOT.TH2D("temptags", "temptags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_temptags.Sumw2();


processevent = 0
for event in chain_in:
    processevent+=1
    if processevent%10000==0: print "processing event ",processevent


    jetlist=Fun_findjet([],event)
    for jet in jetlist:
        jetInd=jet[0]
        if jet[1]==1: btagged=True
        else: btagged=False


#        ---------The following using jet hadron flavor(recommanded by BTV POG) which was not included in ggNtuplizer7-14
        flavor=event.jetHadFlvr[jetInd]

        if flavor==0:        #light
                num_ljets.Fill(event.jetPt[jetInd],event.jetEta[jetInd])
                if btagged: num_ltags.Fill(event.jetPt[jetInd],event.jetEta[jetInd])
        elif flavor==4:      #charm
                num_cjets.Fill(event.jetPt[jetInd],event.jetEta[jetInd])
                if btagged: num_ctags.Fill(event.jetPt[jetInd],event.jetEta[jetInd])
        elif flavor==5:     #bottom
                num_bjets.Fill(event.jetPt[jetInd],event.jetEta[jetInd])
                if btagged: num_btags.Fill(event.jetPt[jetInd],event.jetEta[jetInd])
        else: continue


lEff=num_ltags.Clone("lEff")
lEff.Divide(num_ljets)

cEff=num_ctags.Clone("cEff")
cEff.Divide(num_cjets)

bEff=num_btags.Clone("bEff")
bEff.Divide(num_bjets)

#tempEff=num_temptags.Clone("tempEff")
#tempEff.Divide(num_tempjets)
    

file_out.Write()
file_out.Close()
