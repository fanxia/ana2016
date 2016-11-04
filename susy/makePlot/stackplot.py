#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()
tag="tag_"
LogY=False

test=True
outdir='plots'

indir='../ntupleStore'

tree='EventTree_ele'

lumi=4.353 #2016D
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"

metfilter='(Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter)'

cut_pre_bjj="Bnbjet>0" # add it yourself
cut_SR1_bjj="Bnbjet>0 && BnPho==1" # add it yourself
cut_SR2_bjj="Bnbjet>0 && BnPho>1" # add it yourself
cut_CR1_bjj="Bnbjet>0 && BnPho==0 && BnFake==1" # add it yourself
cut_CR2_bjj="Bnbjet>0 && BnPho==0 && BnFake>1" # add it yourself

cut_SR1_jjj="BnPho==1" # add it yourself
cut_SR2_jjj="BnPho>1" # add it yourself
cut_CR1_jjj="BnPho==0 && BnFake==1" # add it yourself
cut_CR2_jjj="BnPho==0 && BnFake>1" # add it yourself


#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

# starting adding MC bkg
# wwPlotters=[]
# wwSamples = ['WWTo2L2Nu']
# for sample in wwSamples:
#     wwPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#     wwPlotters[-1].addCorrectionFactor('1./SumWeights','norm')
#     wwPlotters[-1].addCorrectionFactor('xsec','xsec')
#     wwPlotters[-1].addCorrectionFactor('genWeight','genWeight')
#     wwPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#     wwPlotters[-1].addCorrectionFactor("trg*id*iso",'lepsf')
#     allPlotters[sample] = wwPlotters[-1]
# WW = MergedPlotter(wwPlotters)
# WW.setFillProperties(1001,ROOT.kOrange)

vgPlotters=[]
vgSamples = ['step1_Wg_MG']
for sample in vgSamples:
    vgPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    vgPlotters[-1].addCorrectionFactor(1./5916760,'norm')
    vgPlotters[-1].addCorrectionFactor(0.,'xsec')
#    vgPlotters[-1].addCorrectionFactor('genWeight','genWeight')
#    vgPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#    vgPlotters[-1].addCorrectionFactor("trg*id*iso", 'lepsf')
    allPlotters[sample] = vgPlotters[-1]
VG = MergedPlotter(vgPlotters)
VG.setFillProperties(1001,ROOT.kMagenta)

wjetsPlotters=[]
wjetsSamples = ['step1_WJetsToLNu']
for sample in wjetsSamples:
    wjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    wjetsPlotters[-1].addCorrectionFactor(1./9908500,'norm')
    wjetsPlotters[-1].addCorrectionFactor(61526.7,'xsec')
#    wjetsPlotters[-1].addCorrectionFactor('genWeight','genWeight')
#    wjetsPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#    wjetsPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
WJets = MergedPlotter(wjetsPlotters)
WJets.setFillProperties(1001,ROOT.kBlue-6)

# zjetsPlotters=[]
# zjetsSamples = ['DYJetsToLL_M50_BIG_RcDataB2H33fbinv']
# for sample in zjetsSamples:
#     zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#     zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','norm')
#     zjetsPlotters[-1].addCorrectionFactor('(1.05)','norm')
#     if ZJetsZPtWeight: zjetsPlotters[-1].addCorrectionFactor('ZPtWeight','ZPtWeight')
#     zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec') # FEWZ NNLO.results_z_m
#     zjetsPlotters[-1].addCorrectionFactor('genWeight','genWeight')
#     zjetsPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#     zjetsPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
#     allPlotters[sample] = zjetsPlotters[-1]
# ZJets = MergedPlotter(zjetsPlotters)
# ZJets.setFillProperties(1001,ROOT.kGreen+2)

ttPlotters=[]
ttSamples = ['step1_TT_powheg']

for sample in ttSamples:
    ttPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    ttPlotters[-1].addCorrectionFactor(1./93120500,'norm')
    ttPlotters[-1].addCorrectionFactor(831.76,'xsec')
#    ttPlotters[-1].addCorrectionFactor('genWeight','genWeight')
#    ttPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#    ttPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
    allPlotters[sample] = ttPlotters[-1]

TT = MergedPlotter(ttPlotters)
TT.setFillProperties(1001,ROOT.kAzure-9)
# Adding MC bkg ends here

# Starting adding data
dataPlotters=[]
dataSamples = [
'step1_SingleEleRun2016D', 
]
for sample in dataSamples:
    dataPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#    dataPlotters[0].addCorrectionFactor('(HLT_MUv2||HLT_ELEv2)','HLT')
Data = MergedPlotter(dataPlotters)


Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")

#Stack.addPlotter(WW, "NonReso","WW/WZ/WJets non-reson.", "background")
Stack.addPlotter(TT, "TT","TT", "background")
#Stack.addPlotter(VV, "VVZReso","ZZ WZ reson.", "background")
#Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(WJets, "WJets","WJets", "background")
Stack.addPlotter(VG, "Vgamma","Vgamma", "background")

Stack.setLog(True)
Stack.doRatio(doRatio)


tag+='_'
#print cuts
if test: 
    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), 100, 0, 500, titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


Stack.closePSFile()


