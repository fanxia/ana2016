#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()

SF_QCD=0.37
SF_tt=1.
SF_wjets=1.
SF_Zjets=1.
SF_gpurity_tt=1.
SF_gpurity_ttg=1.


tag=sys.argv[1]
tag=tag+"_MuJetM3"
LogY=True

AddQCD=True
AddSig=False
normaldraw=True
test=False

outdir='extraplot_out'
indir='../ntupleStore'

tree='EventTree_mu'
treeQCD='EventTree_mQCD'

lumi=35.87   #1.731    #4.353 #2016D
lumisf1=19.714/lumi   #2016BCDEF
lumisf2=16.146/lumi   #2016GH
doRatio=False
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"
#paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(12.88))+" fb^{-1}"

execfile('cut_config_Mu.txt')

#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

execfile('plotter_config_Mu.txt')

####################################

Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")

Stack.addPlotter(TTV, "TTV","TTV", "background")
Stack.addPlotter(TTG, "TTG","TT#gamma", "background")
Stack.addPlotter(VV, "VV","ZZ WZ WW.", "background")
Stack.addPlotter(VG, "Vgamma","V#gamma", "background")

Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(ST, "ST","single top", "background")
#Stack.addPlotter(WJets, "WJets","WJets", "background")
#Stack.addPlotter(TT, "TT","TT", "background")
Stack.addPlotter(QCD,"QCD","QCD","background")

Stack.setLog(LogY)
Stack.doRatio(doRatio)


tag+='_'

xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]
xBins2_pfMET=[0,50,100,250,500,1000]
#print cuts

if normaldraw: 
     Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_mu_bjj',outDir=outdir)

#--------------------------jjj---------------



if test:
     None
Stack.closePSFile()


