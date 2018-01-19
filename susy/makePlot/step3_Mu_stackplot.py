#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()

SF_tt= 0.859
SF_wjets =1.612
SF_QCD=0.42

tag=sys.argv[1]
tag=tag+"_Mu"
LogY=True

AddQCD=True
AddSig=False
#AddQCD=False
normaldraw=True
test=False

outdir='step3_out'
indir='../ntupleStore'

tree='EventTree_mu'
treeQCD='EventTree_mQCD'

lumi=35.86   #1.731    #4.353 #2016D
lumisf1=19.714/lumi   #2016BCDEF
lumisf2=16.146/lumi   #2016GH
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"
#paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(12.88))+" fb^{-1}"


cut_pre_bjj="(Bnbjet>0 && BmuPt>30)*BbtagWeight " # add it yourself
cut_SR1_bjj="(Bnbjet>0 && BnPho==1 && BmuPt>30)*BphoWeight*BbtagWeight " # add it yourself
cut_SR1_bjj_4gamma="(BmuPt>30 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1)*BphoWeight*BbtagWeight" # add it yourself


cut_SR2_bjj="(BmuPt>30 && Bnbjet>0 && BnPho>1)*BphoWeight*BbtagWeight" # add it yourself
cut_CR1_bjj="(BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake==1)*BbtagWeight" # add it yourself
cut_CR1_bjj_4fake="(BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake==1 && BCandPhoTag>>0&1==1)*BbtagWeight" # add it yourself

cut_CR2_bjj="(BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake>1)*BbtagWeight" # add it yourself

cut_pre_jjj="BmuPt>30 && Bnjet>2 && BmuPt>30" # add it yourself
cut_SR1_jjj="(BmuPt>30 && BnPho==1)*BphoWeight" # add it yourself
cut_SR2_jjj="(BmuPt>30 && BnPho>1)*BphoWeight" # add it yourself
cut_CR1_jjj="BmuPt>30 && BnPho==0 && BnFake==1" # add it yourself
cut_CR2_jjj="BmuPt>30 && BnPho==0 && BnFake>1" # add it yourself


# adding cut for qcd scale factor calculation
#cut_pre_bjj_4qcd="Bnbjet>0 && BmuPt>30 && BpfMET<20"

# adding cut for egamma scale factor calculation
cut_SR1_bjj_4gammamatchmu="(BmuPt>30 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1 && BCandphoGenmatch==11)*BphoWeight"
cut_SR1_bjj_4gammamatchnonmu="(BmuPt>30 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1 && BCandphoGenmatch!=11)*BphoWeight"


# adding cut for loosepho_woChiso/woSigmaIetaIeta in 'SR1'
cut_bjj_1phowoIEtaIEta="Bnbjet>0 && BmuPt>30 && BCandPhoTag>>1&1==1 && Sum$(BCandPhoTag>>1&1==1)==1 && BpfMET<50"
cut_bjj_1phowoChHadIso="Bnbjet>0 && BmuPt>30 && BCandPhoTag>>2&1==1 && Sum$(BCandPhoTag>>2&1==1)==1 && BpfMET<50"

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
     vvPlotters[-1].addCorrectionFactor("BmuWeight",'lepsf')
     allPlotters[sample[0]] = vvPlotters[-1]
VV = MergedPlotter(vvPlotters)
VV.setFillProperties(1001,ROOT.kCyan-3)

# wgPlotters=[]
# wgSamples = [['step1p5_WGToLNuG',405.271]]
# for sample in wgSamples:
#     wgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#     wgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#     wgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     wgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#     wgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
# #    wgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     wgPlotters[-1].addCorrectionFactor("BmuWeight", 'lepsf')
#     allPlotters[sample[0]] = wgPlotters[-1]

# WG = MergedPlotter(wgPlotters)
# WG.setFillProperties(1001,ROOT.kMagenta)

# zgPlotters=[]
# zgSamples = [['step1p5_ZGTo2LG',117.864]]
# for sample in zgSamples:
#     zgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
#     zgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
#     zgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     zgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#     zgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
# #    zgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#     zgPlotters[-1].addCorrectionFactor("BmuWeight", 'lepsf')
#     allPlotters[sample[0]] = zgPlotters[-1]
# ZG = MergedPlotter(zgPlotters)
# ZG.setFillProperties(1001,ROOT.kMagenta)

vgPlotters=[]
vgSamples = [['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864]]
for sample in vgSamples:
    vgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    vgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    vgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    vgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    vgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    vgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    vgPlotters[-1].addCorrectionFactor("BmuWeight", 'lepsf')
    allPlotters[sample[0]] = vgPlotters[-1]
VG = MergedPlotter(vgPlotters)
VG.setFillProperties(1001,ROOT.kMagenta)


wjetsPlotters=[]
wjetsSamples = [['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600]]
#wjetsSamples = [['step1p5_W4JetsToLNu',600]]
for sample in wjetsSamples:
    wjetsPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',tree))
    wjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    wjetsPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    wjetsPlotters[-1].addCorrectionFactor("BmuWeight",'lepsf')
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
    zjetsPlotters[-1].addCorrectionFactor("BmuWeight",'lepsf')
    allPlotters[sample] = zjetsPlotters[-1] 

ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kOrange+7)


ttPlotters=[]
ttSamples = ['step1p5_TT']
for sample in ttSamples:
    ttPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
    ttPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttPlotters[-1].addCorrectionFactor(831.76,'xsec')
    ttPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
#    ttPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttPlotters[-1].addCorrectionFactor("BmuWeight",'lepsf')
    ttPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    ttPlotters[-1].addCorrectionFactor(SF_tt,'tt_kfactor')
    allPlotters[sample] = ttPlotters[-1]

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
    ttgPlotters[-1].addCorrectionFactor("BmuWeight",'lepsf')
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
    ttvPlotters[-1].addCorrectionFactor("BmuWeight", 'lepsf')
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
    stPlotters[-1].addCorrectionFactor("BmuWeight", 'lepsf')
    allPlotters[sample[0]] = stPlotters[-1]

ST = MergedPlotter(stPlotters)
ST.setFillProperties(1001,ROOT.kRed-10)
# Adding MC bkg ends here



# Starting adding data
dataPlotters=[]
dataSamples = [
'step1_SingleMu_Run2016B_FebReminiAOD',
'step1_SingleMu_Run2016C_FebReminiAOD',
'step1_SingleMu_Run2016D_FebReminiAOD',
'step1_SingleMu_Run2016E_FebReminiAOD',
'step1_SingleMu_Run2016F_FebReminiAOD1',
'step1_SingleMu_Run2016F_FebReminiAOD2',
'step1_SingleMu_Run2016G_FebReminiAOD',
'step1_SingleMu_Run2016H_FebReminiAODv2',
'step1_SingleMu_Run2016H_FebReminiAODv3'
]
for sample in dataSamples:
    dataPlotters.append(TreePlotter(sample, indir+'/'+sample+'.root',tree))
Data = MergedPlotter(dataPlotters)

Data.setAlias("BphoWeight","1.*1")
Data.setAlias("BCandphoGenmatch","1.*0")
Data.setAlias("BCandphoGenmatch","1.*0") 
Data.setAlias("BbtagWeight","1.*1") 




# start Adding QCD here#################
qcdPlotters=[]
#qcdSamples = [['step1_SingleMu_Run2016B_FebReminiAOD'],['step1_SingleMu_Run2016C_FebReminiAOD'],['step1_SingleMu_Run2016D_FebReminiAOD'],['step1_SingleMu_Run2016E_FebReminiAOD'],['step1_SingleMu_Run2016F_FebReminiAOD1'],['step1_SingleMu_Run2016F_FebReminiAOD2'],['step1_SingleMu_Run2016G_FebReminiAOD'],['step1_SingleMu_Run2016H_FebReminiAODv2'],['step1_SingleMu_Run2016H_FebReminiAODv3'],['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523],['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864],['step1p5_W4JetsToLNu',600],['step1p5_W3JetsToLNu',1160],['step1p5_TTGJets',3.697],['step1p5_DYJetsToLL',6025.2],['step1p5_TT',831.76],['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297],['step1p5_ST_tW_antitop_5f_inclusiveDecays',35.85],['step1p5_ST_tW_top_5f_inclusiveDecays',35.85],['step1p5_ST_s-channel_4f_leptonDecays',3.36],['step1p5_ST_t-channel_top_4f_inclusiveDecays',136.02],['step1p5_ST_t-channel_antitop_4f_inclusiveDecays',80.95]]
qcdSamples = [['step1_SingleMu_Run2016B_FebReminiAOD'],['step1_SingleMu_Run2016C_FebReminiAOD'],['step1_SingleMu_Run2016D_FebReminiAOD'],['step1_SingleMu_Run2016E_FebReminiAOD'],['step1_SingleMu_Run2016F_FebReminiAOD1'],['step1_SingleMu_Run2016F_FebReminiAOD2'],['step1_SingleMu_Run2016G_FebReminiAOD'],['step1_SingleMu_Run2016H_FebReminiAODv2'],['step1_SingleMu_Run2016H_FebReminiAODv3']]
for sample in qcdSamples:
    qcdPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'.root',treeQCD))
    if len(sample)==1: 
         qcdPlotters[-1].addCorrectionFactor(1./(lumi*1000),'lumi')
         qcdPlotters[-1].setAlias("BphoWeight","(1*1.)")
         qcdPlotters[-1].setAlias("BCandphoGenmatch","(1*1.)")
         qcdPlotters[-1].setAlias("BCandphoGenmatch","(1*1.)")
         qcdPlotters[-1].setAlias("BbtagWeight","(1*1.)")  
    if len(sample)>1:
         qcdPlotters[-1].addCorrectionFactor(sample[1],'xsec')
         qcdPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
         qcdPlotters[-1].addCorrectionFactor('-1./BgenWeightTotalEventsNumber','norm')
         qcdPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    #    qcdPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    qcdPlotters[-1].addCorrectionFactor(SF_QCD,'kfactor')
    allPlotters[sample[0]] = qcdPlotters[-1]
QCD = MergedPlotter(qcdPlotters)
QCD.setFillProperties(1001,ROOT.kRed)



# End Adding QCD here#################


##### Add Signal Samples, for all the mass points in one input file############  
sigPlotters=[]
sigSamples=["step1p5_SMS-T6ttZg"]
sigin=ROOT.TFile.Open(indir+'/'+sigSamples[0]+'.root')
scanpoints=[[600,200,ROOT.kRed,'T6ttZg(600_200)'],[800,400,ROOT.kBlue,'T6ttZg(800_400)']]
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
          #    sigPlotters[-1].addCorrectionFactor('genWeight','genWeight')                                                       
          #    sigPlotters[-1].addCorrectionFactor(puWeight,'puWeight')                                                           
          #    sigPlotters[-1].addCorrectionFactor(lepsf,'lepsf')                                                                 
          #    sigPlotters[-1].addCorrectionFactor(mc_scale,'mc_scale')                                                           
          sigPlotters[-1].setFillProperties(0,ROOT.kWhite)
####################################    




####################################

Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")

Stack.addPlotter(TTV, "TTV","TTV", "background")
Stack.addPlotter(TTG, "TTG","TT#gamma", "background")
Stack.addPlotter(VV, "VV","ZZ WZ WW.", "background")
Stack.addPlotter(VG, "Vgamma","V#gamma", "background")
#Stack.addPlotter(WG, "Wgamma","W#gamma", "background")
#Stack.addPlotter(ZG, "Zgamma","Z#gamma", "background")
Stack.addPlotter(ST, "ST","single top", "background")
#Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(WJets, "WJets","WJets", "background")
Stack.addPlotter(TT, "TT","TT", "background")
#if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")

if AddSig==True:
     sepSig=True
     for i in range(len(scanpoints)):
          sigPlotters[i].setLineProperties(2,scanpoints[i][2],2)
#  Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[sigSamples[i]],'signal')                                
          Stack.addPlotter(sigPlotters[i],'',scanpoints[i][3],'signal')


Stack.setLog(True)
Stack.doRatio(doRatio)


tag+='_'

xBins_pfMET=[0,20,40,100,150,200,250,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 
     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "mu_bjj: CR2", titlex = "pfMET", units = "GeV",output=tag+'pfMETbin_CR2_mu_bjj',outDir=outdir)#,separateSignal=sepSig) 

     if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")
     Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "mu_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMETbin_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, channel = "mu_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BmuPt', cut_CR1_bjj, str(lumi*1000), xBins_Pt, 0, 800, channel = "mu_bjj: CR1", titlex = "mu_Pt", units = "GeV",output=tag+'muPt_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BMHT', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: CR1", titlex = "MHT", units = "GeV",output=tag+'MHT_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BHT', cut_CR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: CR1", titlex = "HT_jets", units = "GeV",output=tag+'HT_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoEt', cut_CR1_bjj_4fake, str(lumi*1000), xBins_Pt, 0, 1000, channel = "mu_bjj: CR1", titlex = "fake E_{T}", units = "GeV",output=tag+'fakeEt_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)



     #following part for pre region with qcd contributes
     # if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")

     # Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: Pre", titlex = "pfMET", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: Pre", titlex = "pfMET", units = "GeV",blinding=False, blindingCut=100,output=tag+'pfMET_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     # Stack.drawStack('BnVtx', cut_pre_bjj, str(lumi*1000), 100, 0, 100, channel = "mu_bjj: Pre", titlex = "nVtx", units = "",output=tag+'nVtx_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BmuPt', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: pre", titlex = "mu_Pt", units = "GeV",output=tag+'BmuPt_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BmuEta', cut_pre_bjj, str(lumi*1000), 30, -3, 3, channel = "mu_bjj: pre", titlex = "mu_Eta", units = "GeV",output=tag+'muEta_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     # Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000), 20, 0, 20, channel = "mu_bjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     # Stack.drawStack('BMHT', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: pre", titlex = "MHT", units = "GeV",output=tag+'MHT_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BHT', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: pre", titlex = "HT_jets", units = "GeV",output=tag+'HT_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)



#--------------------------jjj---------------



if test:
#     Stack.drawStack('BpfMET', cut_pre_bjj_4qcd, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_mu_bjj_4qcd',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: SR1", titlex = "Invmass(mu,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
#     if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: CR1", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BmuPt', cut_CR1_bjj, str(lumi*1000), xBins_Pt, 0, 800, channel = "mu_bjj: CR1", titlex = "mu_Pt", units = "GeV",output=tag+'muPt_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BMHT', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: CR1", titlex = "MHT", units = "GeV",output=tag+'MHT_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BHT', cut_CR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: CR1", titlex = "HT_jets", units = "GeV",output=tag+'HT_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoEt', cut_CR1_bjj_4fake, str(lumi*1000), xBins_Pt, 0, 1000, channel = "mu_bjj: CR1", titlex = "fake E_{T}", units = "GeV",output=tag+'fakeEt_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: CR2", titlex = "pfMET", units = "GeV",output=tag+'pfMET_CR2_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
Stack.closePSFile()


