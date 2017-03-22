#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
from TemplateFitter import TemplateFitter

ROOT.gROOT.SetBatch()

tag=sys.argv[1]
tag=tag+"_EE"
LogY=False


normaldraw=False
test=True

outdir='step1_out'
indir='../ntupleStore'

tree='EventTree_ee'


lumi=35.8   #1.731    #4.353 #2016D
#lumi=4.353+2.646
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"

#metfilter='(Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter)'

cut_pre_bjj="Bnbjet>0 && BelePt[0]>35 && BelePt[1]>35 && Bnjet>2 " # add it yourself
cut_pre_jjj="BelePt[1]>35 && BelePt[0]>35 && Bnjet>2" # add it yourself


#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

vvPlotters=[]
vvSamples = [['step1p5_WW',110.8],['step1p5_WZ',47.13],['step1p5_ZZ',16.523]]
for sample in vvSamples:
     vvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
     vvPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#     vvPlotters[-1].addCorrectionFactor(1./sample[1],'norm')
     vvPlotters[-1].addCorrectionFactor(sample[1],'xsec')
     vvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
     vvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
     vvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
     vvPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
     allPlotters[sample[0]] = vvPlotters[-1]
VV = MergedPlotter(vvPlotters)
VV.setFillProperties(1001,ROOT.kCyan-3)

wgPlotters=[]
wgSamples = [['step1p5_WGToLNuG',405.271]]
for sample in wgSamples:
    wgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
    wgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    wgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    wgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    wgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    wgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    wgPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    allPlotters[sample[0]] = wgPlotters[-1]
WG = MergedPlotter(wgPlotters)
WG.setFillProperties(1001,ROOT.kMagenta)

zgPlotters=[]
zgSamples = [['step1p5_ZGTo2LG',117.864]]
for sample in zgSamples:
    zgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
    zgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    zgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    zgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    zgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    zgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    zgPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    allPlotters[sample[0]] = zgPlotters[-1]
ZG = MergedPlotter(zgPlotters)
ZG.setFillProperties(1001,ROOT.kMagenta)

# vgPlotters=[]
# vgSamples = [['step1p5_WGToLNuG',405.271],['step1p5_ZGTo2LG',117.864]]
# for sample in vgSamples:
#     vgPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
# #    SumEvents=vgPlotters[-1].file.Get("H_ele").GetBinContent(1)
# #    vgPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
#     vgPlotters[-1].addCorrectionFactor(sample[1],'xsec')
# #    vgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     vgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
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
#     wjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'_dilep.root',tree))
# #    SumEvents=wjetsPlotters[-1].file.Get("H_ele").GetBinContent(1)
# #    wjetsPlotters[-1].addCorrectionFactor(1./SumEvents,'norm')
#     wjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
#     wjetsPlotters[-1].addCorrectionFactor(61526.7,'xsec')
# #    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
# #    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
# #    wjetsPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
#     wjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
# WJets = MergedPlotter(wjetsPlotters)
# WJets.setFillProperties(1001,ROOT.kBlue-6)

wjetsPlotters=[]
#wjetsSamples = [['step1p5_W3JetsToLNu',1160],['step1p5_W4JetsToLNu',600]]
wjetsSamples = [['step1p5_W4JetsToLNu',600]]
for sample in wjetsSamples:
    wjetsPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
    wjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    wjetsPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    wjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    wjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    wjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    wjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    allPlotters[sample[0]] = wjetsPlotters[-1]
WJets = MergedPlotter(wjetsPlotters)
WJets.setFillProperties(1001,ROOT.kBlue-6)



zjetsPlotters=[]
zjetsSamples = ['step1p5_DYJetsToLL']
for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'_dilep.root',tree))
#    zjetsPlotters[-1].addCorrectionFactor('1./BTotalEventsNumber','norm')
    zjetsPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    zjetsPlotters[-1].addCorrectionFactor(6025.2,'xsec')
    zjetsPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    zjetsPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    zjetsPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    zjetsPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
    allPlotters[sample] = zjetsPlotters[-1] 
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kOrange+7)

# zjetsPlotters=[]
# zjetsSamples = ['DYJetsToLL_M50_BIG_RcDataB2H33fbinv']
# for sample in zjetsSamples:
#     zjetsPlotters.append(TreePlotter(sample, indir+'/'+sample+'_dilep.root',tree))
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
ttSamples = ['step1p5_TT']
for sample in ttSamples:
    ttPlotters.append(TreePlotter(sample, indir+'/'+sample+'_dilep.root',tree))
    ttPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttPlotters[-1].addCorrectionFactor(831.76,'xsec')
    ttPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    ttPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
#    ttPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample] = ttPlotters[-1]
TT = MergedPlotter(ttPlotters)
TT.setFillProperties(1001,ROOT.kAzure-9)


ttgPlotters=[]
ttgSamples = ['step1p5_TTGJets']
for sample in ttgSamples:
    ttgPlotters.append(TreePlotter(sample, indir+'/'+sample+'_dilep.root',tree))
    ttgPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttgPlotters[-1].addCorrectionFactor(3.697,'xsec')
    ttgPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttgPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    ttgPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttgPlotters[-1].addCorrectionFactor("BeleWeight",'lepsf')
#    ttgPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample] = ttgPlotters[-1]
TTG = MergedPlotter(ttgPlotters)
TTG.setFillProperties(1001,ROOT.kGreen-3)


ttvPlotters=[]
ttvSamples = [['step1p5_TTWJetsToLNu',0.2043],['step1p5_TTWJetsToQQ',0.4062],['step1p5_TTZToLLNuNu',0.2529],['step1p5_TTZToQQ',0.5297]]
for sample in ttvSamples:
    ttvPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
    ttvPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    ttvPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    ttvPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    ttvPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    ttvPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
    ttvPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
#    ttvPlotters[-1].addCorrectionFactor("BtopPtWeight",'ttreweight')
    allPlotters[sample[0]] = ttvPlotters[-1]
TTV = MergedPlotter(ttvPlotters)
TTV.setFillProperties(1001,ROOT.kYellow)

stPlotters=[]
#stSamples = [['step1p5_ST_tW_antitop_5f_inclus',35.85],['step1p5_ST_tW_top_5f_inclus',35.85],['step1p5_ST_t-channel_top_4f_leptonDecays',44.33],['step1p5_ST_t-channel_antitop_4f_leptonDecays',26.38],['step1p5_ST_s-channel_4f_leptonDecays',3.36]]
stSamples = [['step1p5_ST_tW_antitop_5f_inclusiveDecays',35.85],['step1p5_ST_tW_top_5f_inclusiveDecays',35.85],['step1p5_ST_s-channel_4f_leptonDecays',3.36]]
for sample in stSamples:
    stPlotters.append(TreePlotter(sample[0], indir+'/'+sample[0]+'_dilep.root',tree))
    stPlotters[-1].addCorrectionFactor(sample[1],'xsec')
    stPlotters[-1].addCorrectionFactor('BgenWeight','genWeight')
    stPlotters[-1].addCorrectionFactor('1./BgenWeightTotalEventsNumber','norm')
    stPlotters[-1].addCorrectionFactor("BpileupWeight",'puWeight')
    stPlotters[-1].addCorrectionFactor("BbtagWeight",'btagWeight')
#    stPlotters[-1].addCorrectionFactor("BlepTrgsf",'trgWeight')
    stPlotters[-1].addCorrectionFactor("BeleWeight", 'lepsf')
    allPlotters[sample[0]] = stPlotters[-1]
ST = MergedPlotter(stPlotters)
ST.setFillProperties(1001,ROOT.kRed-10)


# Adding MC bkg ends here
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
    dataPlotters.append(TreePlotter(sample, indir+'/'+sample+'_dilep.root',tree))
Data = MergedPlotter(dataPlotters)

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

Stack.setLog(True)
Stack.doRatio(doRatio)


tag+='_'

xBins_pfMET=[0,20,40,60,80,100,150,200,250,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,140,160,180,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 

    Stack.drawStack('BnVtx', cut_pre_bjj, str(lumi*1000), 100, 0, 100, channel = "ele_bjj: Pre", titlex = "nVtx", units = "",output=tag+'nVtx_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 50, 0, 500, channel = "ele_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET1_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500, channel = "eleQCD_bjj: Pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BjetM3', cut_pre_jjj, str(lumi*1000), 100, 0, 1000, channel = "ele_jjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
    Stack.drawStack('Bnjet', cut_pre_jjj, str(lumi*1000), 20, 0, 20, channel = "ele_jjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)

    Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000), 20, 0, 20, channel = "ele_bjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)



#--------------------------jjj---------------


#    Stack.drawStack('BpfMET', cut_pre_jjj, str(lumi*1000), 100, 0, 1000, channel = "eleQCD_jjj: pre", titlex = "pfMET", units = "GeV",output=tag+'pfMET_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)


if test:
     Stack.drawStack('BeeInvMass', cut_pre_bjj, str(lumi*1000),40 , 0, 200, channel = "ee_bjj", titlex = "m_{ee}", units = "GeV",output=tag+'Mass_ee_ee_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BeeInvMass', cut_pre_jjj, str(lumi*1000),40 , 0, 200, channel = "ee_jjj", titlex = "m_{ee}", units = "GeV",output=tag+'Mass_ee_ee_jjj',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000),10 , 0, 10, channel = "ee_bjj", titlex = "N_jets", units = "GeV",output=tag+'njet_ee_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('Bnjet', cut_pre_jjj, str(lumi*1000),10 , 0, 10, channel = "ee_jjj", titlex = "N_jets", units = "GeV",output=tag+'njet_ee_ee_jjj',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000),50 , 0, 1000, channel = "ee_bjj", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_ee_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BjetM3', cut_pre_jjj, str(lumi*1000),50 , 0, 1000, channel = "ee_jjj", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_ee_jjj',outDir=outdir)#,separateSignal=sepSig)

     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000),50 , 0, 500, channel = "ee_bjj", titlex = "pfMET", units = "GeV",output=tag+'BpfMET_ee_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_pre_jjj, str(lumi*1000),50 , 0, 500, channel = "ee_jjj", titlex = "pfMET", units = "GeV",output=tag+'BpfMET_ee_jjj',outDir=outdir)#,separateSignal=sepSig)





Stack.closePSFile()


sys.exit()
tag="Mar16_EE"
#############################################
fin=ROOT.TFile.Open("step1p5_out/"+tag+".root")
print fin.GetName()

foutname="step1p5_out/fit"+tag
frootout=ROOT.TFile.Open(foutname+".root","recreate")
frootout.Close()
log=open(foutname+".log","w")

print "Invmass(ee) templit fit for DY and Zgamma Bkgs"
InvEEFitter=TemplateFitter()
InvEEhistname=tag+"_Mass_ee_ee_bjj_"
InvEEFitter.pushdata("SingleEle 2016 Data",fin.Get(InvEEhistname+"data"))

InvEEFitter.pushmc("Bkgs",fin.Get(InvEEhistname+"VV"))
InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"TTG"))
InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"Wgamma"))
InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"WJets"))

InvEEFitter.pushmc("DY/Z#gamma",fin.Get(InvEEhistname+"Zgamma"))

# InvEEFitter.pushmc("Bkgs",fin.Get(InvEEhistname+"TTV"))
# InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"TTG"))
# InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"TT"))
# #InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"TT"),scal=k_ttbar)
# #InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"WJets"),scal=k_wjets)
# InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"WJets"))
# InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"VV"))
# InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"ST"))
# InvEEFitter.addmc("Bkgs",fin.Get(InvEEhistname+"WG"))


# InvEEFitter.pushmc("DY/Z#gamma",fin.Get(InvEEhistname+"ZJets"))
# InvEEFitter.addmc("DY/Z#gamma",fin.Get(InvEEhistname+"ZG"))

InvEEFitter.tempfit()
InvEEFitter_result=InvEEFitter.result
k_bkgs=InvEEFitter_result['Bkgs'][2]
k_ee=InvEEFitter_result['DY/Z#gamma'][2]

log.write("\n\n####################################################################")
log.write("\n####################InvmassEE Fitter##################################")
log.write("\n####################InvmassEE Fitter##################################")
log.write("\n%s\n"%InvEEFitter_result)
log.write("\n In Ele channel, the scale factor for DY&Vgamma is %s"%k_ee)
log.write("\n In Ele channel, the scale factor for Bkgs is %s"%k_bkgs)
log.write("\n#################################################################")
log.write("\n#################################################################\n\n\n")
InvEEFitter.tempfitplot(foutname,"invmass(ee)","Invmass(ee)(GeV)","Events/bin")

print "The scale factor for DY&Zgamma  is",k_ee
print "The scale factor for bkgs is",k_bkgs
print "*******************************************************\n\n\n"

log.close()
