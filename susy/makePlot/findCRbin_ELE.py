#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()

execfile('sf_config.txt')

tag=sys.argv[1]
tag=tag+"_ELECR"
LogY=True

AddQCD=True
#AddQCD=False
normaldraw=True
test=False

outdir='findCRbin_out'
indir='../ntupleStore'

tree='EventTree_ele'
treeQCD='EventTree_eQCD'


lumi=35.87   #1.731    #4.353 #2016D
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"
#paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(12.88))+" fb^{-1}"


execfile('cut_config_ELE.txt')

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

execfile('plotter_config_ELE.txt')
#ZJets.addCorrectionFactor(SF_Zjets,'efakecorr')


Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")


Stack.addPlotter(TTV, "TTV","TTV", "background")
Stack.addPlotter(TTG, "TTG","TT#gamma", "background")
Stack.addPlotter(VV, "VV","ZZ WZ WW.", "background")
Stack.addPlotter(VG, "Vgamma","V#gamma", "background")
Stack.addPlotter(ST, "ST","single top", "background")
Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(WJets, "WJets","WJets", "background")
Stack.addPlotter(TT, "TT","TT", "background")



Stack.setLog(True)
Stack.doRatio(doRatio)

#Stackpre=Stack   # only for pre region where consider the qcd contributes
#if AddQCD: Stackpre.addPlotter(QCD,"QCD","QCD","background")

tag+='_'


xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]
#xBins2_pfMET=[0,50,100,250,500,1000]
#print cuts
Bins1List=[['BinNo1',[0,100,250,500]],['BinNo2',[0,20,60,100,150,300,500]],['BinNo22',[0,20,50,100,150,300,500]],['BinNo3',[0,20,50,75,100,125,150,300,500]],['BinNo4',5],['BinNo5',10],['BinNo6',50],['Bin7',100]]
Bins2List=[['BinNo1',[0,100,200,500]],['BinNo2',[0,50,150,300,500]],['BinNo3',[0,50,100,250,500]],['BinNo4',[0,25,50,100,150,200,500]],['BinNo5',5]]


if normaldraw: 
     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), 50, 0, 500, channel = "ele_bjj: CR2",titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_CR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     for [binNo,xBins2_pfMET] in Bins2List:
          Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), xBins2_pfMET, 0, 500, channel = "ele_bjj: CR2",titlex = "E_{T}^{mis}", units = "GeV",output=tag+binNo+'pfMET_CR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

     if AddQCD==True:
          Stack.addPlotter(QCD,"QCD","QCD","background")
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: CR1", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     for [binNo,xBins_pfMET] in Bins1List:

          Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: CR1", titlex = "E_{T}^{mis}", units = "GeV",output=tag+binNo+'pfMETbin_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.closePSFile()
     sys.exit()


#--------------------------jjj---------------




if test:


     Stack.closePSFile()


