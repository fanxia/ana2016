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
tag=tag+"_MuCR"
LogY=True

AddQCD=True
AddSig=False
normaldraw=True
test=False

outdir='step3_out'
indir='../ntupleStore'

tree='EventTree_mu'
treeQCD='EventTree_mQCD'

lumi=35.87   #1.731    #4.353 #2016D
lumisf1=19.714/lumi   #2016BCDEF
lumisf2=16.146/lumi   #2016GH
doRatio=True
Blind=True
UseMETFilter=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)
if not Blind: tag = tag+'unblind_'

paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi))+" fb^{-1}"
#paveText="#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(12.88))+" fb^{-1}"

execfile('cut_config_Mu.txt')

#if UseMETFilter:
#    cuts = '('+cuts+'&&'+metfilter+')'

ROOT.gROOT.ProcessLine('.x ./tdrstyle.C') 

allPlotters = {}

execfile('plotter_config_Mu.txt')
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
Stack.addPlotter(ST, "ST","single top", "background")
#Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(WJets, "WJets","WJets", "background")
Stack.addPlotter(TT, "TT","TT", "background")

if AddSig==True:
     sepSig=True
     for i in range(len(scanpoints)):
          sigPlotters[i].setLineProperties(2,scanpoints[i][2],2)
#  Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[sigSamples[i]],'signal')                                
          Stack.addPlotter(sigPlotters[i],'',scanpoints[i][3],'signal')


Stack.setLog(True)
Stack.doRatio(doRatio)


tag+='_'

xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 
     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "mu_bjj: CR2", titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMETbin_CR2_mu_bjj',outDir=outdir)#,separateSignal=sepSig) 

     if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")
     Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "mu_bjj: CR1", titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMETbin_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, channel = "mu_bjj: CR1", titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BmuPt', cut_CR1_bjj, str(lumi*1000), xBins_Pt, 0, 800, channel = "mu_bjj: CR1", titlex = "mu_Pt", units = "GeV",output=tag+'muPt_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BMHT', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: CR1", titlex = "MHT", units = "GeV",output=tag+'MHT_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BHT', cut_CR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: CR1", titlex = "HT_jets", units = "GeV",output=tag+'HT_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoEt', cut_CR1_bjj_4fake, str(lumi*1000), xBins_Pt, 0, 1000, channel = "mu_bjj: CR1", titlex = "fake E_{T}", units = "GeV",output=tag+'fakeEt_CR1_mu_bjj',outDir=outdir)#,separateSignal=sepSig)



     #following part for pre region with qcd contributes
     # if AddQCD: Stack.addPlotter(QCD,"QCD","QCD","background")

     # Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: Pre", titlex = "E_{T}^{miss}", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "mu_bjj: Pre", titlex = "E_{T}^{miss}", units = "GeV",blinding=False, blindingCut=100,output=tag+'pfMET_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: Pre", titlex = "E_{T}^{miss}", units = "GeV",output=tag+'pfMET_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     # Stack.drawStack('BnVtx', cut_pre_bjj, str(lumi*1000), 100, 0, 100, channel = "mu_bjj: Pre", titlex = "nVtx", units = "",output=tag+'nVtx_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BmuPt', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: pre", titlex = "mu_Pt", units = "GeV",output=tag+'BmuPt_pre_mu_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BmuEta', cut_pre_bjj, str(lumi*1000), 30, -3, 3, channel = "mu_bjj: pre", titlex = "mu_Eta", units = "GeV",output=tag+'muEta_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     # Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000), 20, 0, 20, channel = "mu_bjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)

     # Stack.drawStack('BMHT', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: pre", titlex = "MHT", units = "GeV",output=tag+'MHT_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BHT', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "mu_bjj: pre", titlex = "HT_jets", units = "GeV",output=tag+'HT_pre_mu_bjj',outDir=outdir)#,separateSignal=sepSig)



#--------------------------jjj---------------



if test:
     None
Stack.closePSFile()


