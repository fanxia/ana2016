#!/usr/bin/env python                                                                                                    
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter

lumi=35.87 
doRatio=False
tree='EventTree_eQCD'

tag='qcdplots_ELE'
outdir='qcdplots_out'
indir='../ntupleStore'

if not os.path.exists(outdir): os.system('mkdir '+outdir)
paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"

cut_pre_bjj="Bnbjet>0 && BelePt>35" # add it yourself  

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C')

allPlotters={}

dataPlotters=[]
dataSamples = [
'step1_SingleEle_Run2016B_FebReminiAOD',
'step1_SingleEle_Run2016C_FebReminiAOD',
'step1_SingleEle_Run2016D_FebReminiAOD',
'step1_SingleEle_Run2016E_FebReminiAOD',
'step1_SingleEle_Run2016F_FebReminiAOD1',
'step1_SingleEle_Run2016F_FebReminiAOD2',
'step1_SingleEle_Run2016G_FebReminiAOD',
'step1_SingleEle_Run2016H_FebReminiAODv2',
'step1_SingleEle_Run2016H_FebReminiAODv3'
]
for sample in dataSamples:
    dataPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
Data = MergedPlotter(dataPlotters)


mcPlotters=[]
mcSamples=[]
mcSamples = [['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523],['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864],['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600],['step1p5_TTGJets',3.697],['step1p5_DYJetsToLL',5765.4],['step1p5_TT',831.76],['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297],['step1p5_ST_tW_antitop_5f_inclusiveDecays',35.85],['step1p5_ST_tW_top_5f_inclusiveDecays',35.85],['step1p5_ST_s-channel_4f_leptonDecays',3.36],['step1p5_ST_t-channel_top_4f_inclusiveDecays',136.02],['step1p5_ST_t-channel_antitop_4f_inclusiveDecays',80.95]]

for sample in mcSamples:
    mcPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    mcPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    mcPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    mcPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#    mcPlotters[-1].addCorrectionFactor('0.5/BgenWeightTotalEventsNumber','norm')
#    mcPlotters[-1].addCorrectionFactor("BpileupWeight*0.18",'puWeight')
    mcPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    #    mcPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')                                                 
    allPlotters[sample[0]] = mcPlotters[-1]
MC = MergedPlotter(mcPlotters)
MC.setFillProperties(1001,ROOT.kAzure+8)

Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data-driven QCD    ", "data")
#Stack.addPlotter(MC, "QCDmc","QCD selection on MC", "background")

Stack.setLog(True)
Stack.doRatio(doRatio)

#xBins_pfMET=[0,20,40,60,80,100,150,200,300,500,1000]
Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), 100, 0, 500, channel = "eQCD: Pre", titlex = "elePt", units = "GeV",output=tag+'elePt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500, channel = "eQCD: Pre", titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#Stack.drawStack('BelePFRelCombIso', cut_pre_bjj, str(lumi*1000), 10, 0, 1, channel = "eQCD: Pre", titlex = "iso", units = "",output=tag+'eleIso_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#Stack.drawStack('BeleSCEta', cut_pre_bjj, str(lumi*1000), 50, -2.5, 2.5, channel = "eQCD: Pre", titlex = "sceta", units = "",output=tag+'elesceta_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 500, channel = "eQCD: Pre", titlex = "jetM3", units = "GeV",output=tag+'jetm3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

Stack.closePSFile()
