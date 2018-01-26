#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()


SF_tt=0.818
SF_wjets=1.724
#SF_tt= 1.
#SF_wjets =1.
SF_QCD=0.39
SF_Zjets=1.4
SF_gpurity_tt=0.99
SF_gpurity_ttg=0.81

tag=sys.argv[1]
tag=tag+"_ELE"
LogY=False

AddQCD=True
normaldraw=True
test=False

outdir='step4limit_out'
indir='../ntupleStore'

tree='EventTree_ele'
treeQCD='EventTree_eQCD'


lumi=35.8   #1.731    #4.353 #2016D
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"
#paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(12.88))+" fb^{-1}"

#lumi=lumi*0.96
#metfilter='(Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter)'

cut_pre_bjj="(Bnbjet>0 && BelePt>35)*BbtagWeight " # add it yourself
cut_SR1_bjj="(Bnbjet>0 && BnPho==1 && BelePt>35)*BphoWeight*BbtagWeight " # add it yourself
#cut_SR1_bjj_4gamma="(BelePt>35 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1)*BphoWeight*BbtagWeight" # add it yourself


cut_SR2_bjj="(BelePt>35 && Bnbjet>0 && BnPho>1)*BphoWeight*BbtagWeight" # add it yourself
#cut_CR1_bjj="(BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1)*BbtagWeight" # add it yourself
#cut_CR1_bjj_4fake="(BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1 && BCandPhoTag>>0&1==1)" # add it yourself

#cut_CR2_bjj="BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake>1" # add it yourself

#cut_pre_jjj="BelePt>35 && Bnjet>2 && BelePt>35" # add it yourself
#cut_SR1_jjj="(BelePt>35 && BnPho==1)*BphoWeight" # add it yourself
#cut_SR2_jjj="(BelePt>35 && BnPho>1)*BphoWeight" # add it yourself
#cut_CR1_jjj="BelePt>35 && BnPho==0 && BnFake==1" # add it yourself
#cut_CR2_jjj="BelePt>35 && BnPho==0 && BnFake>1" # add it yourself



#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

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

# vgPlotters=[]
# vgSamples = [['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864]]
# for sample in vgSamples:
#     vgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
# #    SumEvents=vgPlotters[-1].file.Get("H_ele").GetBinContent(1)
# #    vgPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
#     vgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
# #    vgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     vgPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
#     vgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#     vgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
# #    vgPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
#     vgPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
#     allPlotters[sample[0]] = vgPlotters[-1]
# VG = MergedPlotter(vgPlotters)
# VG.setFillProperties(1001,ROOT.kMagenta)


# wjetsPlotters=[]
# wjetsSamples = ['step1p5_WJetsToLNu']
# for sample in wjetsSamples:
#     wjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
# #    SumEvents=wjetsPlotters[-1].file.Get("H_ele").GetBinContent(1)
# #    wjetsPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
#     wjetsPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
#     wjetsPlotters[-1].addCorrectionFactor(61526.7,'xsec')
# #    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
# #    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
# #    wjetsPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
# WJets = MergedPlotter(wjetsPlotters)
# WJets.setFillProperties(1001,ROOT.kBlue-6)

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
#    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    wjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    wjetsPlotters[-1].addCorrectionFactor(SF_wjets,'kfactor')
    allPlotters[sample[0]] = wjetsPlotters[-1]
WJets = MergedPlotter(wjetsPlotters)
WJets.setFillProperties(1001,ROOT.kBlue-6)



zjetsPlotters=[]
zjetsSamples = ['step1p5_DYJetsToLL']
for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    zjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    zjetsPlotters[-1].addCorrectionFactor(6025.2,'xsec')
    zjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    zjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    zjetsPlotters[-1].addCorrectionFactor(SF_Zjets,'efakecorr')
    allPlotters[sample] = zjetsPlotters[-1] 
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kOrange+7)

#for SR1 only
# zjetsPlotters=[]
# zjetsSamples = ['step1p5_DYJetsToLL']
# for sample in zjetsSamples:
#     zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
#     zjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#     zjetsPlotters[-1].addCorrectionFactor(6025.2,'xsec')
#     zjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
# #    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     zjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
#     zjetsPlotters[-1].addCorrectionFactor("(Sum$((BCandPhoTag>>3&1)==1 && BCandphoGenmatch==11)==1)*1.89",'efakedphoton')
#     allPlotters[sample] = zjetsPlotters[-1] 

#     zjetsPlotters.append(TreePlotter(sample+"copy", indir+'/'+sample+'.root',tree))
#     zjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#     zjetsPlotters[-1].addCorrectionFactor(6025.2,'xsec')
#     zjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
# #    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     zjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
#     zjetsPlotters[-1].addCorrectionFactor("(Sum$((BCandPhoTag>>3&1)==1 && BCandphoGenmatch!=11)==1)*1.09",'realphoton')
#     allPlotters[sample] = zjetsPlotters[-1] 
# ZJets = MergedPlotter(zjetsPlotters)
# ZJets.setFillProperties(1001,ROOT.kOrange+7)

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
    ttPlotters[-1].addCorrectionFactor(SF_tt,'tt_kfactor')
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
Data.setAlias("BCandphoGenmatch","1.*0")
Data.setAlias("BtopPtWeight","1.*1")
Data.setAlias("BbtagWeight","1.*1")
Data.setAlias("BbtagWeightUp","1.*1")
Data.setAlias("BbtagWeightDown","1.*1")
Data.setAlias("BeleWeightErr","1.*0")
Data.setAlias("BphoWeightErr","1.*0")
Data.setAlias("BpfMeT1JESUp","BpfMET")
Data.setAlias("BpfMeT1JESDo","BpfMET")



# start Adding QCD here#################
qcdPlotters=[]
#qcdSamples = [['step1_SingleEle_Run2016B_FebReminiAOD'],['step1_SingleEle_Run2016C_FebReminiAOD'],['step1_SingleEle_Run2016D_FebReminiAOD'],['step1_SingleEle_Run2016E_FebReminiAOD'],['step1_SingleEle_Run2016F_FebReminiAOD1'],['step1_SingleEle_Run2016F_FebReminiAOD2'],['step1_SingleEle_Run2016G_FebReminiAOD'],['step1_SingleEle_Run2016H_FebReminiAODv2'],['step1_SingleEle_Run2016H_FebReminiAODv3'],['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523],['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864],['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600],['step1p5_TTGJets',3.697],['step1p5_DYJetsToLL',6025.2],['step1p5_TT',831.76],['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297],['step1p5_ST_tW_antitop_5f_inclusiveDecays',35.85],['step1p5_ST_tW_top_5f_inclusiveDecays',35.85],['step1p5_ST_s-channel_4f_leptonDecays',3.36],['step1p5_ST_t-channel_top_4f_inclusiveDecays',136.02],['step1p5_ST_t-channel_antitop_4f_inclusiveDecays',80.95]]
qcdSamples = [['step1_SingleEle_Run2016B_FebReminiAOD'],['step1_SingleEle_Run2016C_FebReminiAOD'],['step1_SingleEle_Run2016D_FebReminiAOD'],['step1_SingleEle_Run2016E_FebReminiAOD'],['step1_SingleEle_Run2016F_FebReminiAOD1'],['step1_SingleEle_Run2016F_FebReminiAOD2'],['step1_SingleEle_Run2016G_FebReminiAOD'],['step1_SingleEle_Run2016H_FebReminiAODv2'],['step1_SingleEle_Run2016H_FebReminiAODv3']]
for sample in qcdSamples:
    qcdPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',treeQCD))
    if len(sample)==1: 
         qcdPlotters[-1].addCorrectionFactor(1./(lumi*1000),'lumi')
         qcdPlotters[-1].setAlias("BphoWeight","(1*1.)")
         qcdPlotters[-1].setAlias("BCandphoGenmatch","(1*1.)")
    if len(sample)>1:
         qcdPlotters[-1].addCorrectionFactor(sample[1],'xsec')
         qcdPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
         qcdPlotters[-1].addCorrectionFactor('-1./BgenWeightTotalEventsNumber','norm')
         qcdPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    #    qcdPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    qcdPlotters[-1].addCorrectionFactor(SF_QCD,'kfactor')
 #   qcdPlotters[-1].addCorrectionFactor('BpfMET<50','metfactor')
    allPlotters[sample[0]] = qcdPlotters[-1]
QCD = MergedPlotter(qcdPlotters)
QCD.setFillProperties(1001,ROOT.kRed)



# End Adding QCD here#################


# ##### Add Signal Samples############  
# sigPlotters=[]
# sigSamples=[["step1_Sig800_550",0.0283338]]
# for sample in sigSamples:
#     sigPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#     SumEvents=sigPlotters[-1].file.Get("H_ele").GetBinContent(1)
#     print "signal sum events is ", SumEvents
#     sigPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
#     sigPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#     sigPlotters[-1].setAlias("BphoWeight","(1*1.)")
# #    sigPlotters[-1].addCorrectionFactor('genWeight','genWeight')                                                       
# #    sigPlotters[-1].addCorrectionFactor(puWeight,'puWeight')                                                           
# #    sigPlotters[-1].addCorrectionFactor(lepsf,'lepsf')                                                                 
# #    sigPlotters[-1].addCorrectionFactor(mc_scale,'mc_scale')                                                           
#     sigPlotters[-1].setFillProperties(0,ROOT.kWhite)
# ####################################    

##### Add Signal Samples, for all the mass points in one input file############  
sigPlotters=[]
sigSamples=["step1p5_SMS-T6ttZg"]
sigin=ROOT.TFile.Open(indir+'/'+sigSamples[0]+'.root')
H_sigscan=sigin.Get("H_sigscan")
scanpoints=[]
scanpointname=[]
for x in range(300,1501):
    for y in range(10,1401):
        scanNumber=H_sigscan.GetBinContent(H_sigscan.FindBin(x,y))
        if scanNumber>0:
            scanpoints.append([x,y])
            scanpointname.append("Mst"+str(x)+"_Mnl"+str(y))
splog=open(outdir+"/scanpointname.txt","w")
for spname in scanpointname:
     splog.write("%s\n"%spname)
splog.close()


for sample in sigSamples:
     for mass in scanpoints:
          mstop=mass[0]
          mnlsp=mass[1]
#          sigPlotters.append(TreePlotter(sample+"_Mst"+str(mstop)+"_Mnl"+str(mnlsp), indir+'/'+sample+'.root',tree))
          sigPlotters.append(TreePlotter("SMS_T6ttZg_Mst"+str(mstop)+"_Mnl"+str(mnlsp), indir+'/'+sample+'.root',tree))
          sigPlotters[-1].addCorrectionFactor("1./BTotalScanpointEventsNumber",'norm')
          sigPlotters[-1].addCorrectionFactor('(BlheStopMass=='+str(mstop)+')*(BlheNLSPMass=='+str(mnlsp)+')','masspoint')
          sigPlotters[-1].addCorrectionFactor('Bstopxsec','xsec')
          sigPlotters[-1].addCorrectionFactor('Bnlspdecayweight','br')
          sigPlotters[-1].setAlias("BphoWeight","(1*1.)")
          sigPlotters[-1].setAlias("BeleWeightErr","1.*0")
          sigPlotters[-1].setAlias("BpfMeT1JESUp","BpfMET")
          sigPlotters[-1].setAlias("BpfMeT1JESDo","BpfMET")
          #    sigPlotters[-1].addCorrectionFactor('genWeight','genWeight')                                                       
          #    sigPlotters[-1].addCorrectionFactor(puWeight,'puWeight')                                                           
          #    sigPlotters[-1].addCorrectionFactor(lepsf,'lepsf')                                                                 
          #    sigPlotters[-1].addCorrectionFactor(mc_scale,'mc_scale')                                                           
          sigPlotters[-1].setFillProperties(0,ROOT.kWhite)
####################################    




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
#Stack.addPlotter(ZJets, "ZJets","ZJets", "background")

Stack.addPlotter(WJets, "WJets","WJets", "background")

Stack.addPlotter(TT, "TT","TT", "background")

for i in range(len(scanpoints)):
  sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
#  Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[sigSamples[i]],'signal')                                
  Stack.addPlotter(sigPlotters[i],'',sigPlotters[i].name,'signal')


Stack.setLog(True)
Stack.doRatio(doRatio)

#Stackpre=Stack   # only for pre region where consider the qcd contributes
#if AddQCD: Stackpre.addPlotter(QCD,"QCD","QCD","background")

tag+='_'

#xBins_pfMET=[0,20,40,60,80,100,150,200,250,300,500,1000]
#xBins_pfMET=[0,20,40,60,80,100,150,200,300,500,1000]
xBins_pfMET=[0,20,40,60,80,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 


     TT.addCorrectionFactor(SF_gpurity_tt**2,"photon purity")
     TTG.addCorrectionFactor(SF_gpurity_ttg**2,"photon purity")

     Stack.drawStack('BpfMET', cut_SR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BbtagWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BbtagWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1.+BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BeleWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1.-BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BeleWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BtopPtWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(2.-1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BtopPtWeightUp',outDir=outdir)#,separateSignal=sepSig)


     Stack.drawStack('BpfMeT1JESUp', cut_SR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BJESUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMeT1JESDo', cut_SR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BJESDown',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BphoWeightDown',outDir=outdir)#,separateSignal=sepSig)                                                                     
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BphoWeightUp',outDir=outdir)#,separateSignal=sepSig)

     Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
     TT.addCorrectionFactor(1./SF_gpurity_tt,"photon purity")
     TTG.addCorrectionFactor(1./SF_gpurity_ttg,"photon purity")

     Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BbtagWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BbtagWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1.+BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BeleWeightUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1.-BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BeleWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BtopPtWeightDown',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(2.-1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BtopPtWeightUp',outDir=outdir)#,separateSignal=sepSig)


     Stack.drawStack('BpfMeT1JESUp', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BJESUp',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMeT1JESDo', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BJESDown',outDir=outdir)#,separateSignal=sepSig)


     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BphoWeightDown',outDir=outdir)#,separateSignal=sepSig)                                                          
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BphoWeightUp',outDir=outdir)#,separateSignal=sepSig)


#     Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: SR1",titlex = "pfMET", units = "GeV",blinding=True, blindingCut=50,output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#     Stack.drawStack('BpfMET', cut_SR2_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: SR2", titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: CR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


     Stack.addPlotter(QCD,"QCD","QCD","background")

#     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500,channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500,channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",blinding=T

     Stack.closePSFile()
     sys.exit()


#--------------------------jjj---------------




if test:

     Stack.closePSFile()


