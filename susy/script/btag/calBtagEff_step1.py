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
from array import array

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
for inputf in INPUTFile.split():
    chain_in.Add(inputf)
chain_in.SetBranchStatus("AK8*",0)
print"Total events for processing: ",chain_in.GetEntries()
event=chain_in

if len(sys.argv)>4:
    fileID=int(sys.argv[3])
    startEntryNumber=int(sys.argv[4])
    endEntryNumber=int(sys.argv[5])
elif len(sys.argv)==4:
    fileID=int(sys.argv[3])
    startEntryNumber=0
    endEntryNumber=chain_in.GetEntries()
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
#log = open("logstep1_"+OUTPUTName+"_"+str(fileID)+".txt","w")
file_out = ROOT.TFile("BtagEff_step1_"+OUTPUTName+"_"+str(fileID)+".root","recreate")
file_out.cd()

ptNBins=17
ptMin=0
ptMax=1000
etaNBins=6
etaMin=-2.4
etaMax=2.4

ptBin=array('d',[20,30,40,50,60,70,80,100,120,160,210,260,320,400,500,600,800,99999])
etaBin=array('d',[-2.4,-1.6,-0.8,0.0,0.8,1.6,2.4])
num_bjets = ROOT.TH2D("bjets", "bjets", ptNBins, ptBin, etaNBins, etaBin); num_bjets.Sumw2();
num_btags = ROOT.TH2D("btags", "btags", ptNBins, ptBin, etaNBins, etaBin); num_btags.Sumw2();
num_cjets = ROOT.TH2D("cjets", "cjets", ptNBins, ptBin, etaNBins, etaBin); num_cjets.Sumw2();
num_ctags = ROOT.TH2D("ctags", "ctags", ptNBins, ptBin, etaNBins, etaBin); num_ctags.Sumw2();
num_ljets = ROOT.TH2D("ljets", "ljets", ptNBins, ptBin, etaNBins, etaBin); num_ljets.Sumw2();
num_ltags = ROOT.TH2D("ltags", "ltags", ptNBins, ptBin, etaNBins, etaBin); num_ltags.Sumw2();

#num_tempjets = ROOT.TH2D("tempjets", "tempjets", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_tempjets.Sumw2();
#num_temptags = ROOT.TH2D("temptags", "temptags", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_temptags.Sumw2();


processevent = 0
for entrynumber in range(startEntryNumber,endEntryNumber):
    event.GetEntry(entrynumber)

    processevent+=1
    if processevent%10000==0: print "processing event ",processevent

    if not event.isPVGood: continue
    # elelist:[[index,ID,iso],[]...]
    # mulist: [[index,ID,iso],[]...]
    # mulist=Fun_findmu(event)
    # elelist=Fun_findele(event)

    # if len(elelist)==1 and elelist[0][1]==1 and len(mulist)==0: 
    #     Scanmode="eleTree"
    #     lep_ind=elelist[0][0]
    # elif len(elelist)==0  and len(mulist)==1 and mulist[0][1]==1: 
    #     Scanmode="muTree"
    #     lep_ind=mulist[0][0]
    # else: continue


#--------------1.HLT cut-------------

#    if Channel==111 : hlt=event.HLTEleMuX>>55&1
#    if Channel==222 : hlt=(event.HLTEleMuX>>31&1 and event.HLTEleMuX>>32&1)

#    if not hlt: continue


#    Candpholist=Fun_findCandpho(Channel,lep_ind,event)

    jetlist=Fun_findjetbtag(event)
    for jet in jetlist:
        jetInd=jet[0]
        if jet[1]==1: btagged=True
        else: btagged=False


#        ---------The following using jet hadron flavor(recommanded by BTV POG) which was not included in ggNtuplizer7-14
        flavor=jet[2]

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
