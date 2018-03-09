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

outdir='step4limit_out'
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
ZJets.addCorrectionFactor(SF_Zjets,'efakecorr')

execfile('plotter_config_ELE.txt')

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
Stack.addPlotter(VG, "Vgamma","V#gamma", "background")
#Stack.addPlotter(WG, "Wgamma","W#gamma", "background")
#Stack.addPlotter(ZG, "Zgamma","Z#gamma", "background")
Stack.addPlotter(ST, "ST","single top", "background")
Stack.addPlotter(ZJets, "ZJets","ZJets", "background")

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
xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 


     TT.addCorrectionFactor(SF_gpurity_tt,"photon purity")
     TTG.addCorrectionFactor(SF_gpurity_ttg,"photon purity")

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


     ZJets.addCorrectionFactor('BgenWeight>0',"clear")
     TT.addCorrectionFactor(SF_gpurity_tt,"photon purity")
     TTG.addCorrectionFactor(SF_gpurity_ttg,"photon purity")


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


