#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()
tag="Bwei"
LogY=False

test=True
outdir='plots'

indir='../ntupleStore'

tree='EventTree_ele'

lumi=4.353   #1.731    #4.353 #2016D
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"

metfilter='(Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter)'

cut_pre_bjj="Bnbjet>0" # add it yourself
cut_SR1_bjj="Bnbjet>0 && BnPho==1 " # add it yourself
cut_SR1_bjj_4gamma="Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1" # add it yourself

cut_SR2_bjj="Bnbjet>0 && BnPho>1" # add it yourself
cut_CR1_bjj="Bnbjet>0 && BnPho==0 && BnFake==1" # add it yourself
cut_CR2_bjj="Bnbjet>0 && BnPho==0 && BnFake>1" # add it yourself

cut_pre_jjj="Bnjet>2" # add it yourself
cut_SR1_jjj="BnPho==1" # add it yourself
cut_SR2_jjj="BnPho>1" # add it yourself
cut_CR1_jjj="BnPho==0 && BnFake==1" # add it yourself
cut_CR2_jjj="BnPho==0 && BnFake>1" # add it yourself


#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

# starting adding MC bkg
vvPlotters=[]
vvSamples = [['step1p5_WW',993209,110.8],['step1p5_WZ',999994,47.13]]
for sample in vvSamples:
     vvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#     vvPlotters[-1].addCorrectionFactor('1./SumWeights','norm')
     vvPlotters[-1].addCorrectionFactor(1./sample[1],'norm')
     vvPlotters[-1].addCorrectionFactor(sample[2],'xsec')
#     vvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     vvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#     vvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     vvPlotters[-1].addCorrectionFactor("trg*id*iso",'lepsf')
     allPlotters[sample[0]] = vvPlotters[-1]
VV = MergedPlotter(vvPlotters)
VV.setFillProperties(1001,ROOT.kOrange)

vgPlotters=[]
vgSamples = [['step1p5_Wg_MG',5916760,405.271],['step1p5_Zg_aMCatNLO',4391358,117.864]]
for sample in vgSamples:
    vgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    vgPlotters[-1].addCorrectionFactor(1./sample[1],'norm')
    vgPlotters[-1].addCorrectionFactor(sample[2],'xsec')
#    vgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#    vgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    vgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    vgPlotters[-1].addCorrectionFactor("trg*id*iso", 'lepsf')
    allPlotters[sample[0]] = vgPlotters[-1]
VG = MergedPlotter(vgPlotters)
VG.setFillProperties(1001,ROOT.kMagenta)

wjetsPlotters=[]
wjetsSamples = ['step1p5_WJetsToLNu']
for sample in wjetsSamples:
    wjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    wjetsPlotters[-1].addCorrectionFactor(1./9908500,'norm')
    wjetsPlotters[-1].addCorrectionFactor(61526.7,'xsec')
#    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#    wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    wjetsPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
WJets = MergedPlotter(wjetsPlotters)
WJets.setFillProperties(1001,ROOT.kBlue-6)

zjetsPlotters=[]
zjetsSamples = ['step1p5_DYLL']
for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    zjetsPlotters[-1].addCorrectionFactor(1./28696800,'norm')
    zjetsPlotters[-1].addCorrectionFactor(6025.2,'xsec')
#    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#    zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    wjetsPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kGreen+2)

# zjetsPlotters=[]
# zjetsSamples = ['DYJetsToLL_M50_BIG_RcDataB2H33fbinv']
# for sample in zjetsSamples:
#     zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#     zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','norm')
#     zjetsPlotters[-1].addCorrectionFactor('(1.05)','norm')
#     if ZJetsZPtWeight: zjetsPlotters[-1].addCorrectionFactor('ZPtWeight','ZPtWeight')
#     zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec') # FEWZ NNLO.results_z_m
#     zjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     zjetsPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#     zjetsPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
#     allPlotters[sample] = zjetsPlotters[-1]
# ZJets = MergedPlotter(zjetsPlotters)
# ZJets.setFillProperties(1001,ROOT.kGreen+2)

ttPlotters=[]
ttSamples = ['step1p5_TT_powheg']

for sample in ttSamples:
    ttPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    ttPlotters[-1].addCorrectionFactor(1./93120500,'norm')
    ttPlotters[-1].addCorrectionFactor(831.76,'xsec')
#    ttPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#    ttPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
#    ttPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    ttPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    ttPlotters[-1].addCorrectionFactor(lepsf,'lepsf')
    allPlotters[sample] = ttPlotters[-1]

TT = MergedPlotter(ttPlotters)
TT.setFillProperties(1001,ROOT.kAzure-9)
# Adding MC bkg ends here

# Starting adding data
dataPlotters=[]
dataSamples = [
#'step1_SingleMuRun2016D', 
'step1_SingleEleRun2016D'
#'step1_SingleEle_Run2015D'
]
for sample in dataSamples:
    dataPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#    dataPlotters[0].addCorrectionFactor('(HLT_MUv2||HLT_ELEv2)','HLT')
Data = MergedPlotter(dataPlotters)


Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")

#Stack.addPlotter(VV, "NonReso","VV/WZ/WJets non-reson.", "background")

Stack.addPlotter(VV, "VV","ZZ WZ WW.", "background")
Stack.addPlotter(VG, "Vgamma","Vgamma", "background")
Stack.addPlotter(ZJets, "ZJets","ZJets", "background")

Stack.addPlotter(WJets, "WJets","WJets", "background")

Stack.addPlotter(TT, "TT","TT", "background")

Stack.setLog(True)
Stack.doRatio(doRatio)


tag+='_'

xBins_pfMET=[0,20,40,60,80,100,150,200,250,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250]

#print cuts

if test: 
#    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_SR2_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), 100, 0, 500, titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR2_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BmuPt', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, titlex = "mu_Pt", units = "GeV",output=tag+'muPt_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BmuPt', cut_SR1_bjj, str(lumi*1000), 100, 0, 1000, titlex = "mu_Pt", units = "GeV",output=tag+'muPt_SR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BelePt', cut_SR1_bjj, str(lumi*1000), 100, 0, 1000, titlex = "ele_Pt", units = "GeV",output=tag+'elePt_SR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)


    Stack.drawStack('BnVtx', cut_pre_bjj, str(lumi*1000), 100, 0, 100, channel = "ele_bjj: Pre", titlex = "nVtx", units = "",output=tag+'nVtx_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BlepMt', cut_pre_bjj, str(lumi*1000), 20, 0, 1000, channel = "ele_bjj: Pre", titlex = "Mt", units = "GeV",output=tag+'lepMt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 100, 0, 500,  channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500,  channel = "ele_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000), 20, 0, 20, channel = "ele_bjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), xBins_Pt[:-1], 0, 1000, channel = "ele_bjj: pre", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_SR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_CR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: CR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


    Stack.drawStack('BeleEta', cut_pre_bjj, str(lumi*1000), 30, -3, 3, channel = "ele_bjj: pre", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BeleEta', cut_SR1_bjj, str(lumi*1000), 30, -3, 3, channel = "ele_bjj: SR1", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "Inv_{ele,gamma}", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)



#--------------------------jjj---------------

    Stack.drawStack('BelePt', cut_pre_jjj, str(lumi*1000), 100, 0, 1000, channel = "ele_jjj: pre", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_SR1_jjj, str(lumi*1000), 100, 0, 1000, channel = "ele_jjj: SR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_SR1_ele_jjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BeleEta', cut_pre_jjj, str(lumi*1000), 30, -3, 3, channel = "ele_jjj: pre", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BeleEta', cut_SR1_jjj, str(lumi*1000), 30, -3, 3, channel = "ele_jjj: SR1", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_SR1_ele_jjj',outDir=outdir)#,separateSignal=sepSig)


Stack.closePSFile()


