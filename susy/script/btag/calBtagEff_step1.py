#!/bin/python
#To calculate the MC btag eff using the jets in which the event has past the singleLepton cuts
# to run this script alone: python calBtagEff_step1.py inputfilename outputname
# to run this by submitting jobs, refer to submitMC_btag_step1.sh

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



INPUTFile=sys.argv[1]
OUTPUTName=sys.argv[2]
print "input: ",INPUTFile
print "output: ",OUTPUTName


chain_in = ROOT.TChain("ggNtuplizer/EventTree")
chain_in.Add(sys.argv[1])
chain_in.SetBranchStatus("AK8*",0)
print"Total events for processing: ",chain_in.GetEntries()
event=chain_in

if len(sys.argv)>3:
    fileID=int(sys.argv[3])
    startEntryNumber=int(sys.argv[4])
    endEntryNumber=int(sys.argv[5])
else:
    fileID=-999
    startEntryNumber=0
    endEntryNumber=chain_in.GetEntries()

print "fileID: ",fileID
print "startEntryNumber: ",startEntryNumber
print "endEntryNumber: ",endEntryNumber

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p MC_BtagEff_step1/'+OUTPUTName+'/'+dd)
os.chdir('MC_BtagEff_step1/'+OUTPUTName+'/'+dd)
log = open("logstep1_"+OUTPUTName+"_"+str(fileID)+".txt","w")
file_out = ROOT.TFile("BtagEff_step1_"+OUTPUTName+"_"+str(fileID)+".root","recreate")
file_out.cd()

ptNBins=200
ptMin=0
ptMax=1000
etaNBins=24
etaMin=-2.4
etaMax=2.4

num_bjets = ROOT.TH2F("bjets", "bjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_bjets.Sumw2();
num_btags = ROOT.TH2F("btags", "btags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_btags.Sumw2();
num_cjets = ROOT.TH2F("cjets", "cjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_cjets.Sumw2();
num_ctags = ROOT.TH2F("ctags", "ctags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ctags.Sumw2();
num_ljets = ROOT.TH2F("ljets", "ljets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ljets.Sumw2();
num_ltags = ROOT.TH2F("ltags", "ltags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_ltags.Sumw2();

#num_tempjets = ROOT.TH2F("tempjets", "tempjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_tempjets.Sumw2();
#num_temptags = ROOT.TH2F("temptags", "temptags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_temptags.Sumw2();


processevent = 0
for entrynumber in range(startEntryNumber,endEntryNumber):
    event.GetEntry(entrynumber)

    processevent+=1
    if processevent%10000==0: print "processing event ",processevent

    if not event.hasGoodVtx: continue
    # elelist:[[index,ID,iso],[]...]
    # mulist: [[index,ID,iso],[]...]
    mulist=Fun_findmu(event)
    elelist=Fun_findele(event)

    if len(elelist)==1 and elelist[0][1]==1 and len(mulist)==0: 
        Scanmode="eleTree"
        lep_ind=elelist[0][0]
    elif len(elelist)==0  and len(mulist)==1 and mulist[0][1]==1: 
        Scanmode="muTree"
        lep_ind=mulist[0][0]
    else: continue


#--------------1.HLT cut-------------

#    if Channel==111 : hlt=event.HLTEleMuX>>55&1
#    if Channel==222 : hlt=(event.HLTEleMuX>>31&1 and event.HLTEleMuX>>32&1)

#    if not hlt: continue


#    Candpholist=Fun_findCandpho(Channel,lep_ind,event)

    jetlist=Fun_findjet(Scanmode,mulist,elelist,[],event)
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


#lEff=num_ltags.Clone("lEff")
#lEff.Divide(num_ljets)

#cEff=num_ctags.Clone("cEff")
#cEff.Divide(num_cjets)

#bEff=num_btags.Clone("bEff")
#bEff.Divide(num_bjets)


file_out.Write()
file_out.Close()