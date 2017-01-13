#!/bin/python
#use cut and count method to roughly estimate the singleEle trigger efficiency

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

def Fun_findeleTag(tree):
    tagele=[]
    for e in range(tree.nEle):
        if tree.eleIDbit[e]>>3&1==1 and tree.elePt[e]>30 and tree.eleSCEta[e]<2.5 and tree.eleFiredSingleTrgs[e]>>13&1==1:
            tagele.append(e)
    return tagele

def Fun_findeleProb(tree):
    probele=[]
    for e in range(tree.nEle):
        if tree.eleIDbit[e]>>3&1==1 and tree.elePt[e]>10 and tree.eleSCEta[e]<2.5:
            probele.append(e)
    return probele

def Fun_PairTagProb(tree,tt,pp):
#    result=[[t,p,invmass],[]]
    Zmass=92
    test=[]
    for t in tt:
        for p in pp:
            Invm=Fun_invmass_dilep('eeTree',[[t],[p]],event)
            if t!=p and Invm<120 and Invm>60:  test.append([t,p,abs(Invm-Zmass)])
    if len(test)<1: return False
    min_dmass=min(l[2] for l in test)
    result=[p for p in test if p[2]==min_dmass]
    return result

INPUTFile=sys.argv[1]
OUTPUTName=sys.argv[2]
print "input: ",INPUTFile
print "output: ",OUTPUTName


chain_in = ROOT.TChain("ggNtuplizer/EventTree")
chain_in.Add(sys.argv[1])
chain_in.SetBranchStatus("AK8*",0)
#print"Total events for processing: ",chain_in.GetEntries()
event=chain_in

if len(sys.argv)>3:
    fileID=int(sys.argv[3])
    startEntryNumber=int(sys.argv[4])
    endEntryNumber=int(sys.argv[5])
else:
    fileID=-999
    startEntryNumber=0
    endEntryNumber=chain_in.GetEntries()
#    endEntryNumber=100000

print "fileID: ",fileID
print "startEntryNumber: ",startEntryNumber
print "endEntryNumber: ",endEntryNumber

dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p lepEff_step1/'+OUTPUTName+'/'+dd)
os.chdir('lepEff_step1/'+OUTPUTName+'/'+dd)
log = open("logstep1_"+OUTPUTName+"_"+str(fileID)+".txt","w")
file_out = ROOT.TFile("lepEff_step1_"+OUTPUTName+"_"+str(fileID)+".root","recreate")
file_out.cd()


ptNBins=200
ptMin=10
ptMax=1000
etaNBins=25
etaMin=-2.5
etaMax=2.5
processevent=0

num_pass = ROOT.TH2F("pass", "pass", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_pass.Sumw2();
num_all = ROOT.TH2F("all", "all", ptNBins, ptMin, ptMax, etaNBins, etaMin, etaMax); num_pass.Sumw2();

for entrynumber in range(startEntryNumber,endEntryNumber):
    event.GetEntry(entrynumber)

    processevent+=1
    if processevent%10000==0: print "processing event ",processevent

    if not event.isPVGood: continue

    TagInd=Fun_findeleTag(event)
    if len(TagInd)<1: continue
    
    ProbeInd=Fun_findeleProb(event)
    if len(ProbeInd)<1: continue

    TnPpair=Fun_PairTagProb(event,TagInd,ProbeInd)

    if not TnPpair: continue

    for pair in TnPpair:
        num_all.Fill(event.elePt[pair[1]],event.eleEta[pair[1]])
        if event.eleFiredSingleTrgs[pair[1]]>>13&1==1:
            num_pass.Fill(event.elePt[pair[1]],event.eleEta[pair[1]])

file_out.Write()
file_out.Close()
