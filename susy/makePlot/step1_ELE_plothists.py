#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()

tag=sys.argv[1]
tag=tag+"_ELE"
LogY=False

AddQCD=True
#AddQCD=False
normaldraw=False
test=True

outdir='step1_out'
indir='../ntupleStore'

tree='EventTree_ele'
treeQCD='EventTree_eQCD'
#tree='EventTree_eQCD'

lumi=35.87   #1.731    #4.353 #2016D

doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"



#############

execfile("cut_config_ELE.txt")

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

# starting adding MC bkg
vvPlotters=[]
vvSamples = [['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523]]
for sample in vvSamples:
     vvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
     vvPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
     vvPlotters[-1].addCorrectionFactor(sample[1],'xsec')
     vvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
     vvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#     vvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
     vvPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
     allPlotters[sample[0]] = vvPlotters[-1]
VV = MergedPlotter(vvPlotters)
VV.setFillProperties(1001,ROOT.kCyan-3)

wgPlotters=[]
wgSamples = [['step1p5_WGToLNuG',405.271]]
for sample in wgSamples:
    wgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    wgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    wgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    wgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    wgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    wgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    wgPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    allPlotters[sample[0]] = wgPlotters[-1]
WG = MergedPlotter(wgPlotters)
WG.setFillProperties(1001,ROOT.kMagenta)

zgPlotters=[]
zgSamples = [['step1p5_ZGTo2LG',117.864]]
for sample in zgSamples:
    zgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    zgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    zgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    zgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    zgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    zgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    zgPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    allPlotters[sample[0]] = zgPlotters[-1]
ZG = MergedPlotter(zgPlotters)
ZG.setFillProperties(1001,ROOT.kMagenta)


wjetsPlotters=[]
wjetsSamples = [['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600]]
#wjetsSamples = [['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600],['step1p5_W2JetsToLNu',3841]]
#wjetsSamples = [['step1p5_W4JetsToLNu',600]]
for sample in wjetsSamples:
    wjetsPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    wjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    wjetsPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    wjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    allPlotters[sample[0]] = wjetsPlotters[-1]
WJets = MergedPlotter(wjetsPlotters)
WJets.setFillProperties(1001,ROOT.kBlue-6)



zjetsPlotters=[]
zjetsSamples = ['step1p5_DYJetsToLL']
for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    zjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    zjetsPlotters[-1].addCorrectionFactor(5765.4,'xsec')
    zjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    zjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    allPlotters[sample] = zjetsPlotters[-1] 
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kOrange+7)


ttPlotters=[]
ttSamples = [['step1p5_TT',831.76]]
#ttSamples = [['step1p5_TTJets_DiLept',87.3],['step1p5_TTJets_SingleLeptFromT',182.7],['step1p5_TTJets_SingleLeptFromTbar',182.7]]
for sample in ttSamples:
    ttPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    ttPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    ttPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    ttPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    ttPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample[0]] = ttPlotters[-1]
TT = MergedPlotter(ttPlotters)
TT.setFillProperties(1001,ROOT.kAzure-9)


ttgPlotters=[]
ttgSamples = ['step1p5_TTGJets']
for sample in ttgSamples:
    ttgPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    ttgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttgPlotters[-1].addCorrectionFactor(3.697,'xsec')
    ttgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    ttgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttgPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    ttgPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample] = ttgPlotters[-1]
TTG = MergedPlotter(ttgPlotters)
TTG.setFillProperties(1001,ROOT.kGreen-3)


ttvPlotters=[]
ttvSamples = [['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297]]
for sample in ttvSamples:
    ttvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    ttvPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    ttvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttvPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    ttvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttvPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    ttvPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample[0]] = ttvPlotters[-1]
TTV = MergedPlotter(ttvPlotters)
TTV.setFillProperties(1001,ROOT.kYellow)

stPlotters=[]
stSamples = [['step1p5_ST_tW_antitop_5f_inclusiveDecays',35.85],['step1p5_ST_tW_top_5f_inclusiveDecays',35.85],['step1p5_ST_s-channel_4f_leptonDecays',3.36],['step1p5_ST_t-channel_top_4f_inclusiveDecays',136.02],['step1p5_ST_t-channel_antitop_4f_inclusiveDecays',80.95]]
for sample in stSamples:
    stPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    stPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    stPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    stPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    stPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    stPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    stPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    allPlotters[sample[0]] = stPlotters[-1]
ST = MergedPlotter(stPlotters)
ST.setFillProperties(1001,ROOT.kRed-10)


# Adding MC bkg ends here



# Starting adding data
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

Data.setAlias("BphoWeight","1.*1")
Data.setAlias("BbtagWeight","1.*1")
Data.setAlias("BCandphoGenmatch","1.*0")
Data.setAlias("BtopPtWeight","1.*1")
Data.setAlias("BbtagWeightUp","1.*1")
Data.setAlias("BbtagWeightDown","1.*1")
Data.setAlias("BeleWeightErr","1.*0")
Data.setAlias("BphoWeightErr","1.*0")
Data.setAlias("BpfMeT1JESUp","BpfMET")
Data.setAlias("BpfMeT1JESDo","BpfMET")




# start Adding QCD here#################
qcdPlotters=[]
# qcdSamples = [['step1_SingleEle_Run2016B_FebReminiAOD'],['step1_SingleEle_Run2016C_FebReminiAOD'],['step1_SingleEle_Run2016D_FebReminiAOD'],['step1_SingleEle_Run2016E_FebReminiAOD'],['step1_SingleEle_Run2016F_FebReminiAOD1'],['step1_SingleEle_Run2016F_FebReminiAOD2'],['step1_SingleEle_Run2016G_FebReminiAOD'],['step1_SingleEle_Run2016H_FebReminiAODv2'],['step1_SingleEle_Run2016H_FebReminiAODv3'],['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523],['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864],['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600],['step1p5_TTGJets',3.697],['step1p5_DYJetsToLL',5765.4],['step1p5_TT',831.76],['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297],['step1p5_ST_tW_antitop_5f_inclusiveDecays',35.85],['step1p5_ST_tW_top_5f_inclusiveDecays',35.85],['step1p5_ST_s-channel_4f_leptonDecays',3.36],['step1p5_ST_t-channel_top_4f_inclusiveDecays',136.02],['step1p5_ST_t-channel_antitop_4f_inclusiveDecays',80.95]]
# for sample in qcdSamples:
#     qcdPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',treeQCD))
#     if len(sample)==1: 
#          qcdPlotters[-1].addCorrectionFactor(1./(lumi*1000),'lumi')
#          qcdPlotters[-1].setAlias("BphoWeight","(1*1.)")
#          qcdPlotters[-1].setAlias("BbtagWeight","(1*1.)")
#          qcdPlotters[-1].setAlias("BCandphoGenmatch","(1*1.)")
#     if len(sample)>1:
#          qcdPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#          qcdPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#          qcdPlotters[-1].addCorrectionFactor('-1./BgenWeightTotalEventsNumber','norm')
#          qcdPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#     #    qcdPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     allPlotters[sample[0]] = qcdPlotters[-1]
qcdSamples = [['step1_SingleEle_Run2016B_FebReminiAOD'],['step1_SingleEle_Run2016C_FebReminiAOD'],['step1_SingleEle_Run2016D_FebReminiAOD'],['step1_SingleEle_Run2016E_FebReminiAOD'],['step1_SingleEle_Run2016F_FebReminiAOD1'],['step1_SingleEle_Run2016F_FebReminiAOD2'],['step1_SingleEle_Run2016G_FebReminiAOD'],['step1_SingleEle_Run2016H_FebReminiAODv2'],['step1_SingleEle_Run2016H_FebReminiAODv3']]
for sample in qcdSamples:
    qcdPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',treeQCD))
    if len(sample)==1: 
         qcdPlotters[-1].addCorrectionFactor(1./(lumi*1000),'lumi')
         qcdPlotters[-1].setAlias("BphoWeight","(1*1.)")
         qcdPlotters[-1].setAlias("BbtagWeight","(1*1.)")
         qcdPlotters[-1].setAlias("BCandphoGenmatch","(1*1.)")
    if len(sample)>1:
         qcdPlotters[-1].addCorrectionFactor(sample[1],'xsec')
         qcdPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
         qcdPlotters[-1].addCorrectionFactor('-1./BgenWeightTotalEventsNumber','norm')
         qcdPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    #    qcdPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    allPlotters[sample[0]] = qcdPlotters[-1]

QCD = MergedPlotter(qcdPlotters)
QCD.setFillProperties(1001,ROOT.kRed)
QCD.setAlias("BphoWeight","1.*1")
QCD.setAlias("BbtagWeight","1.*1")
QCD.setAlias("BCandphoGenmatch","1.*0")
QCD.setAlias("BtopPtWeight","1.*1")
QCD.setAlias("BbtagWeightUp","1.*1")
QCD.setAlias("BbtagWeightDown","1.*1")
QCD.setAlias("BeleWeightErr","1.*0")
QCD.setAlias("BphoWeightErr","1.*0")
QCD.setAlias("BpfMeT1JESUp","BpfMET")
QCD.setAlias("BpfMeT1JESDo","BpfMET")



# End Adding QCD here#################


Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")


Stack.addPlotter(TTV, "TTV","TTV", "background")
Stack.addPlotter(TTG, "TTG","TT#gamma", "background")
Stack.addPlotter(VV, "VV","ZZ WZ WW.", "background")
#Stack.addPlotter(VG, "Vgamma","V#gamma", "background")
Stack.addPlotter(WG, "Wgamma","W#gamma", "background")
Stack.addPlotter(ZG, "Zgamma","Z#gamma", "background")
Stack.addPlotter(ST, "ST","single top", "background")
Stack.addPlotter(ZJets, "ZJets","ZJets", "background")

Stack.addPlotter(WJets, "WJets","WJets", "background")

Stack.addPlotter(TT, "TT","TT", "background")
if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")

Stack.setLog(True)
Stack.doRatio(doRatio)


tag+='_'

#xBins_pfMET=[0,20,40,60,80,100,150,200,250,300,500,1000]
xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]

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


##################################################
if test:


     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_pre_jjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_jjj: Pre", titlex = "pfMET", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

     ####FOR QCD FIT###########
     Stack.drawStack('BpfMET', cut_pre_bjj_4qcd, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj_4qcd',outDir=outdir)#,separateSignal=sepSig)


     
     Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


     #######FOR JETM3 TEMPLATE FIT###########
     Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_bjj+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj_BbtagWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_bjj+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj_BbtagWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_bjj+"*(1.+BeleWeightErr)", str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj_BeleWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_bjj+"*(1.-BeleWeightErr)", str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj_BeleWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_bjj+"*(1./BtopPtWeight)", str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj_BtopPtWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_bjj+"*(2.-1./BtopPtWeight)", str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj_BtopPtWeightUp',outDir=outdir)#,separateSignal=sepSig)


     ######FOR ZJET FIT###############
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma, str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele, str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele, str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BbtagWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BbtagWeightUp_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BbtagWeightUp_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BbtagWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BbtagWeightDown_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BbtagWeightDown_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*(1.+BeleWeightErr)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BeleWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*(1.+BeleWeightErr)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BeleWeightUp_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*(1.+BeleWeightErr)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BeleWeightUp_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*(1.-BeleWeightErr)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BeleWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*(1.-BeleWeightErr)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BeleWeightDown_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*(1.-BeleWeightErr)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BeleWeightDown_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*(1./BtopPtWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BtopPtWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*(1./BtopPtWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BtopPtWeightDown_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*(1./BtopPtWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BtopPtWeightDown_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*(2.-1./BtopPtWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BtopPtWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*(2.-1./BtopPtWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BtopPtWeightUp_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*(2.-1./BtopPtWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BtopPtWeightUp_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*(1+BphoWeightErr/BphoWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BphoWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*(1+BphoWeightErr/BphoWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BphoWeightUp_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*(1+BphoWeightErr/BphoWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BphoWeightUp_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BphoWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BphoWeightDown_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_BphoWeightDown_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)



     Stack.drawStack('BpfMET', cut_SR1_bjj_4gammamatchele, str(lumi*1000), xBins_pfMET,0,500, channel = "ele_bjj: SR1", titlex = "pfMET(#gamma-->e)", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj_4gammamatchnonele, str(lumi*1000), xBins_pfMET,0,500, channel = "ele_bjj: SR1", titlex = "pfMET(#gamma-->no e)", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)


     Stack.drawStack('Bnjet', cut_SR1_bjj_4gammamatchele, str(lumi*1000), 15,0,15, channel = "ele_bjj: SR1", titlex = "N_{jets}(#gamma-->e)", units = "",output=tag+'Bnjet_SR1_ele_bjj_gammamatchele',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('Bnjet', cut_SR1_bjj_4gammamatchnonele, str(lumi*1000), 15,0,15, channel = "ele_bjj: SR1", titlex = "N_{jets}(#gamma-->no e)", units = "",output=tag+'Bnjet_SR1_ele_bjj_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: pre", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


     #######FOR PHOTON PURITY FIT##############
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BbtagWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BbtagWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BbtagWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BbtagWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BbtagWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BbtagWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*(1.+BeleWeightErr)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BeleWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*(1.+BeleWeightErr)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BeleWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*(1.+BeleWeightErr)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BeleWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*(1.-BeleWeightErr)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BeleWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*(1.-BeleWeightErr)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BeleWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*(1.-BeleWeightErr)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BeleWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*(1./BtopPtWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BtopPtWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*(1./BtopPtWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BtopPtWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*(1./BtopPtWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BtopPtWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*(2.-1./BtopPtWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BtopPtWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*(2.-1./BtopPtWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BtopPtWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*(2.-1./BtopPtWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BtopPtWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BphoWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BphoWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BphoWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BphoWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchjet+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen jet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BphoWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoSigmaIEtaIEtaFull', cut_bjj_4gammawoietaieta_genmatchnojet+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta} #gamma gen nojet", units = "",output=tag+'SigmaIEtaIEta_ele_bjj_BphoWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)


     Stack.drawStack('BpfMET', cut_SR1_bjj_4gamma_genmatchnojet, str(lumi*1000), xBins_pfMET,0,500, channel = "ele_bjj", titlex ="pfMET #gamma gen nojet", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj_4gamma_genmatchjet, str(lumi*1000), xBins_pfMET,0,500, channel = "ele_bjj", titlex ="pfMET #gamma gen jet", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_gammagenjet',outDir=outdir)#,separateSignal=sepSig)


     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso, str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet, str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet, str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_gammagenjet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj_BbtagWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_BbtagWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_BbtagWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj_BbtagWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_BbtagWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_BbtagWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso+"*(1.+BeleWeightErr)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj_BeleWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet+"*(1.+BeleWeightErr)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_BeleWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet+"*(1.+BeleWeightErr)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_BeleWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso+"*(1.-BeleWeightErr)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj_BeleWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet+"*(1.-BeleWeightErr)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_BeleWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet+"*(1.-BeleWeightErr)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_BeleWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso+"*(1./BtopPtWeight)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj_BtopPtWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet+"*(1./BtopPtWeight)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_BtopPtWeightDown_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet+"*(1./BtopPtWeight)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_BtopPtWeightDown_gammagenjet',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso+"*(2.-1./BtopPtWeight)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj_BtopPtWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchnojet+"*(2.-1./BtopPtWeight)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen nojet", units = "",output=tag+'PFChIso_ele_bjj_BtopPtWeightUp_gammagennojet',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoPFCorChIso', cut_bjj_4gammawochhadiso_genmatchjet+"*(2.-1./BtopPtWeight)", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso #gamma gen jet", units = "",output=tag+'PFChIso_ele_bjj_BtopPtWeightUp_gammagenjet',outDir=outdir)#,separateSignal=sepSig)





Stack.closePSFile()


