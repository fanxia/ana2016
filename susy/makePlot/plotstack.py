#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()
tag="Feb21_test"
LogY=False

normaldraw=False
test=True
outdir='plots'

indir='../ntupleStore'

tree='EventTree_ele'
#tree='EventTree_eQCD'

lumi=35.8   #1.731    #4.353 #2016D
#lumi=4.353+2.646
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"
#paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(12.88))+" fb^{-1}"

#metfilter='(Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter)'

cut_pre_bjj="Bnbjet>0 && BelePt>35 " # add it yourself
cut_SR1_bjj="(Bnbjet>0 && BnPho==1 && BelePt>35)*BphoWeight " # add it yourself
cut_SR1_bjj_4gamma="(BelePt>35 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1)*BphoWeight" # add it yourself


cut_SR2_bjj="(BelePt>35 && Bnbjet>0 && BnPho>1)*BphoWeight" # add it yourself
cut_CR1_bjj="BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1" # add it yourself
cut_CR1_bjj_4fake="(BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1 && BCandPhoTag>>0&1==1)" # add it yourself

cut_CR2_bjj="BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake>1" # add it yourself

cut_pre_jjj="BelePt>35 && Bnjet>2 && BelePt>35" # add it yourself
cut_SR1_jjj="(BelePt>35 && BnPho==1)*BphoWeight" # add it yourself
cut_SR2_jjj="(BelePt>35 && BnPho>1)*BphoWeight" # add it yourself
cut_CR1_jjj="BelePt>35 && BnPho==0 && BnFake==1" # add it yourself
cut_CR2_jjj="BelePt>35 && BnPho==0 && BnFake>1" # add it yourself


# adding cut for loosepho_woChiso/woSigmaIetaIeta in 'SR1'
cut_bjj_1phowoIEtaIEta="Bnbjet>0 && BelePt>35 && BCandPhoTag>>1&1==1 && Sum$(BCandPhoTag>>1&1==1)==1 && BpfMET<50"
cut_bjj_1phowoChHadIso="Bnbjet>0 && BelePt>35 && BCandPhoTag>>2&1==1 && Sum$(BCandPhoTag>>2&1==1)==1 && BpfMET<50"

#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

# starting adding MC bkg
vvPlotters=[]
vvSamples = [['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523]]
for sample in vvSamples:
     vvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#     SumEvents=vvPlotters[-1].file.Get("H_ele").GetBinContent(1)
#     print "SumEvents=",SumEvents
#     vvPlotters[-1].addCorrectionFactor('1./SumWeights','norm')
     vvPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
#     vvPlotters[-1].addCorrectionFactor(1./sample[1],'norm')
     vvPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#     vvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
     vvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
     vvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     vvPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
     vvPlotters[-1].addCorrectionFactor("BlepWeight",'lepsf')
     allPlotters[sample[0]] = vvPlotters[-1]
VV = MergedPlotter(vvPlotters)
VV.setFillProperties(1001,ROOT.kCyan-3)

vgPlotters=[]
vgSamples = [['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864]]
for sample in vgSamples:
    vgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#    SumEvents=vgPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    vgPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    vgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#    vgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    vgPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    vgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    vgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    vgPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    vgPlotters[-1].addCorrectionFactor("BlepWeight", 'lepsf')
    allPlotters[sample[0]] = vgPlotters[-1]
VG = MergedPlotter(vgPlotters)
VG.setFillProperties(1001,ROOT.kMagenta)

wjetsPlotters=[]
wjetsSamples = ['step1p5_WJetsToLNu']
for sample in wjetsSamples:
    wjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#    SumEvents=wjetsPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    wjetsPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    wjetsPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    wjetsPlotters[-1].addCorrectionFactor(61526.7,'xsec')
#    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    wjetsPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    wjetsPlotters[-1].addCorrectionFactor("BlepWeight",'lepsf')
WJets = MergedPlotter(wjetsPlotters)
WJets.setFillProperties(1001,ROOT.kBlue-6)

# wjetsPlotters=[]
# wjetsSamples = [['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600]]
# for sample in wjetsSamples:
#     wjetsPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
# #    SumEvents=wjetsPlotters[-1].file.Get("H_ele").GetBinContent(1)
# #    wjetsPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
#     wjetsPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
#     wjetsPlotters[-1].addCorrectionFactor(sample[1],'xsec')
# #    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
# #    wjetsPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BlepWeight",'lepsf')
#     allPlotters[sample[0]] = vgPlotters[-1]
# WJets = MergedPlotter(wjetsPlotters)
# WJets.setFillProperties(1001,ROOT.kBlue-6)



zjetsPlotters=[]
zjetsSamples = ['step1p5_DYLL']
for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#    SumEvents=zjetsPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    zjetsPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    zjetsPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    zjetsPlotters[-1].addCorrectionFactor(6025.2,'xsec')
#    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    zjetsPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    zjetsPlotters[-1].addCorrectionFactor("BlepWeight",'lepsf')
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kOrange+7)

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
#    SumEvents=ttPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    ttPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    ttPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    ttPlotters[-1].addCorrectionFactor(831.76,'xsec')
#    ttPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    ttPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttPlotters[-1].addCorrectionFactor("BlepWeight",'lepsf')
    ttPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
#    ttPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    allPlotters[sample] = ttPlotters[-1]
TT = MergedPlotter(ttPlotters)
TT.setFillProperties(1001,ROOT.kAzure-9)


ttgPlotters=[]
ttgSamples = ['step1p5_TTGJets']

for sample in ttgSamples:
    ttgPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#    SumEvents=ttgPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    ttgPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    ttgPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    ttgPlotters[-1].addCorrectionFactor(3.697,'xsec')
#    ttgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#    ttgPlotters[-1].addCorrectionFactor(puWeight,'puWeight')
    ttgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    ttgPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    ttgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttgPlotters[-1].addCorrectionFactor("BlepWeight",'lepsf')
    ttgPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample] = ttgPlotters[-1]

TTG = MergedPlotter(ttgPlotters)
TTG.setFillProperties(1001,ROOT.kGreen-3)


ttvPlotters=[]
ttvSamples = [['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297]]
for sample in ttvSamples:
    ttvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#    SumEvents=ttvPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    ttvPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    ttvPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#    ttvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttvPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    ttvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    ttvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    ttvPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    ttvPlotters[-1].addCorrectionFactor("BlepWeight", 'lepsf')
    ttvPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample[0]] = ttvPlotters[-1]
TTV = MergedPlotter(ttvPlotters)
TTV.setFillProperties(1001,ROOT.kYellow)

stPlotters=[]
stSamples = [['step1p5_ST_tW_antitop_5f_inclus',35.85],['step1p5_ST_tW_top_5f_inclus',35.85],['step1p5_ST_t-channel_top_4f_leptonDecays',44.33],['step1p5_ST_t-channel_antitop_4f_leptonDecays',26.38],['step1p5_ST_s-channel_4f_leptonDecays',3.36]]
for sample in stSamples:
    stPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#    SumEvents=stPlotters[-1].file.Get("H_ele").GetBinContent(1)
#    stPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
    stPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#    stPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    stPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    stPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    stPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    stPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    stPlotters[-1].addCorrectionFactor("BlepWeight", 'lepsf')
    allPlotters[sample[0]] = stPlotters[-1]
ST = MergedPlotter(stPlotters)
ST.setFillProperties(1001,ROOT.kRed-10)


# Adding MC bkg ends here

# Starting adding data
dataPlotters=[]
dataSamples = [
#'step1_SingleMuRun2016D',
#'step1_SingleEleRun2016B',
#'step1_SingleEleRun2016C', 
#'step1_SingleEleRun2016D'
'step1_SingleEle_Run2016B_SepRereco',
'step1_SingleEle_Run2016C_SepRereco',
'step1_SingleEle_Run2016D_SepRereco',
'step1_SingleEle_Run2016E_SepRereco',
'step1_SingleEle_Run2016F_SepRereco',
'step1_SingleEle_Run2016G_sepRereco',
'step1_SingleEle_Run2016H_PRv2',
'step1_SingleEle_Run2016H_PRv3'
#'step1_SingleEle_Run2015D'
]
for sample in dataSamples:
    dataPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#    dataPlotters[0].addCorrectionFactor('(HLT_MUv2||HLT_ELEv2)','HLT')
Data = MergedPlotter(dataPlotters)

Data.setAlias("BphoWeight","1.*1")

Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")

#Stack.addPlotter(VV, "NonReso","VV/WZ/WJets non-reson.", "background")


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


tag+='_'

xBins_pfMET=[0,20,40,60,80,100,150,200,250,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 
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

#    Stack.drawStack('BlepMt', cut_pre_bjj, str(lumi*1000), 20, 0, 1000, channel = "ele_bjj: Pre", titlex = "Mt", units = "GeV",output=tag+'lepMt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 50, 0, 500, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET1_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500, channel = "eleQCD_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000,  channel = "ele_bjj: SR1", titlex = "pfMET", units a= "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 50, 0, 500,  channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 50, 0, 500,  channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',blinding=True, blindingCut=100,outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 50, 0, 500,  channel = "ele_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000,  channel = "ele_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BjetM3', cut_pre_jjj, str(lumi*1000), 100, 0, 1000, channel = "ele_jjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('Bnjet', cut_pre_jjj, str(lumi*1000), 20, 0, 20, channel = "ele_jjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000), 20, 0, 20, channel = "ele_bjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), xBins_Pt[:-1], 0, 1000, channel = "ele_bjj: pre", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_SR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_CR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: CR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


    Stack.drawStack('BeleEta', cut_pre_bjj, str(lumi*1000), 30, -3, 3, channel = "ele_bjj: pre", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BeleEta', cut_SR1_bjj, str(lumi*1000), 30, -3, 3, channel = "ele_bjj: SR1", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BeleEta', cut_CR1_bjj, str(lumi*1000), 30, -3, 3, channel = "ele_bjj: CR1", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BCandphoEt', cut_SR1_bjj_4gamma, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "photon E_{T}", units = "GeV",output=tag+'PhoEt_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BCandphoEta', cut_SR1_bjj_4gamma, str(lumi*1000), 20, -2, 2, channel = "ele_bjj: SR1", titlex = "photon #eta", units = "",output=tag+'PhoEta_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_SR1_bjj_4gamma, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj: SR1", titlex = "photon #sigma_{i#etai#eta}", units = "",output=tag+'phoSigmaIEtaIEta_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BCandphoPFChIso', cut_SR1_bjj_4gamma, str(lumi*1000), 20, 0, 2, channel = "ele_bjj: SR1", titlex = "photon chargedHadIso", units = "",output=tag+'phoPFChIso_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)



#--------------------------jjj---------------

    Stack.drawStack('BelePt', cut_pre_jjj, str(lumi*1000), 100, 0, 1000, channel = "ele_jjj: pre", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_pre_jjj, str(lumi*1000), 100, 0, 1000, channel = "eleQCD_jjj: pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BelePt', cut_SR1_jjj, str(lumi*1000), 100, 0, 1000, channel = "ele_jjj: SR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_SR1_ele_jjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('BeleEta', cut_pre_jjj, str(lumi*1000), 30, -3, 3, channel = "ele_jjj: pre", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BeleEta', cut_SR1_jjj, str(lumi*1000), 30, -3, 3, channel = "ele_jjj: SR1", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_SR1_ele_jjj',outDir=outdir)#,separateSignal=sepSig)



if test:

#    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStackSketch('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch>0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchpho_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStackSketch('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch>0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchpho_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch<0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchjet_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStackSketch('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch<0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchjet_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoPFChIso', cut_bjj_1phowoChHadIso, str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoPFChIso', cut_bjj_1phowoChHadIso+" && BCandphoGenmatch>0", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_matchpho_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoPFChIso', cut_bjj_1phowoChHadIso+" && BCandphoGenmatch<0", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_matchjet_ele_bjj',outDir=outdir)#,separateSignal=sepSig)



Stack.closePSFile()


