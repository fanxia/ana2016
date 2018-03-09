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
tag=tag+"_ELE"
LogY=False

AddQCD=True
normaldraw=True
test=False

outdir='step5uncert_out'
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

#lumi=lumi*0.96
#metfilter='(Flag_EcalDeadCellTriggerPrimitiveFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_HBHENoiseFilter&&Flag_globalTightHalo2016Filter&&Flag_eeBadScFilter)'

execfile('cut_config_ELE.txt')

#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

execfile('plotter_config_ELE.txt')


##### Add two Signal Samples
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
Stack.addPlotter(VG, "Vgamma","V#gamma", "background")
Stack.addPlotter(ST, "ST","single top", "background")
#Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(WJets, "WJets","WJets", "background")
Stack.addPlotter(TT, "TT","TT", "background")

for i in range(len(scanpoints)):
  sigPlotters[i].setLineProperties(2,scanpoints[i][2],2)
#  Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[sigSamples[i]],'signal')                                
  Stack.addPlotter(sigPlotters[i],'',scanpoints[i][3],'signal')


Stack.setLog(True)
Stack.doRatio(doRatio)

#Stackpre=Stack   # only for pre region where consider the qcd contributes
#if AddQCD: Stackpre.addPlotter(QCD,"QCD","QCD","background")

tag+='_'

xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 

     sepSig=True
     TT.addCorrectionFactor(SF_gpurity_tt**2,"photon purity")
     TTG.addCorrectionFactor(SF_gpurity_ttg**2,"photon purity")

     Stack.drawStack('BpfMET', cut_SR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",blinding=True,blindingCut=60,output=tag+'pfMET_SR2_ele_bjj',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BbtagWeightUp',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "pfMET", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BbtagWeightDown',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1.+BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BeleWeightUp',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1.-BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BeleWeightDown',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BtopPtWeightDown',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(2.-1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BtopPtWeightUp',outDir=outdir,separateSignal=sepSig)


     Stack.drawStack('BpfMeT1JESUp', cut_SR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BJESUp',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMeT1JESDo', cut_SR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BJESDown',outDir=outdir,separateSignal=sepSig)

     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BphoWeightDown',outDir=outdir,separateSignal=sepSig)                                                                     
     Stack.drawStack('BpfMET', cut_SR2_bjj+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj_BphoWeightUp',outDir=outdir,separateSignal=sepSig)

     Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
     TT.addCorrectionFactor(1./SF_gpurity_tt,"photon purity")
     TTG.addCorrectionFactor(1./SF_gpurity_ttg,"photon purity")

     Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",blinding=True,blindingCut=60,output=tag+'pfMET_SR1_ele_bjj',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*BbtagWeightUp/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BbtagWeightUp',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*BbtagWeightDown/BbtagWeight", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BbtagWeightDown',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1.+BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BeleWeightUp',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1.-BeleWeightErr)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BeleWeightDown',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BtopPtWeightDown',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(2.-1./BtopPtWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BtopPtWeightUp',outDir=outdir,separateSignal=sepSig)


     Stack.drawStack('BpfMeT1JESUp', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BJESUp',outDir=outdir,separateSignal=sepSig)
     Stack.drawStack('BpfMeT1JESDo', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BJESDown',outDir=outdir,separateSignal=sepSig)


     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1-BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BphoWeightDown',outDir=outdir,separateSignal=sepSig)                                                          
     Stack.drawStack('BpfMET', cut_SR1_bjj+"*(1.+BphoWeightErr/BphoWeight)", str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj_BphoWeightUp',outDir=outdir,separateSignal=sepSig)


#     Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: SR1",titlex = "E_{T}^{miss}", units = "GeV",blinding=True, blindingCut=50,output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#     Stack.drawStack('BpfMET', cut_SR2_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: SR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_SR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: CR1",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: CR2",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_CR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


     Stack.addPlotter(QCD,"QCD","QCD","background")

#     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500,channel = "ele_bjj: Pre",titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500,channel = "ele_bjj: Pre",titlex = "E_{T}^{miss}", units = "GeV",blinding=T

     Stack.closePSFile()
     sys.exit()


#--------------------------jjj---------------




if test:

     Stack.closePSFile()


