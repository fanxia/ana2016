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
tag=tag+"_ELECR"
LogY=True

AddQCD=True
#AddQCD=False
normaldraw=True
test=False

outdir='step3_out'
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
#ZJets.addCorrectionFactor(SF_Zjets,'efakecorr')


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



Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")


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

#Stackpre=Stack   # only for pre region where consider the qcd contributes
#if AddQCD: Stackpre.addPlotter(QCD,"QCD","QCD","background")

tag+='_'


xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]

#print cuts

if normaldraw: 
     Stack.drawStack('BpfMET', cut_CR2_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: CR2",titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_CR2_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

     if AddQCD==True:
          Stack.addPlotter(QCD,"QCD","QCD","background")

#     Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), 100, 0, 500, channel = "ele_bjj: CR1", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 500, channel = "ele_bjj: CR1", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMETbin_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BelePt', cut_CR1_bjj, str(lumi*1000), 50, 0, 500, channel = "ele_bjj: CR1", titlex = "ele_Pt", units = "GeV",output=tag+'elePt_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BMHT', cut_CR1_bjj, str(lumi*1000), 50, 0, 500, channel = "ele_bjj: CR1", titlex = "MHT", units = "GeV",output=tag+'MHT_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BHT', cut_CR1_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: CR1", titlex = "HT_jets", units = "GeV",output=tag+'HT_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BCandphoEt', cut_CR1_bjj_4fake, str(lumi*1000), 50, 0, 500, channel = "ele_bjj: CR1", titlex = "fake E_{T}", units = "GeV",output=tag+'fakeEt_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('Bnjet', cut_CR1_bjj, str(lumi*1000), 20, 0, 20, channel = "ele_bjj: CR1", titlex = "NJets", units = "",output=tag+'njets_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)



     #Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500,channel = "ele_bjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir,separateSignal=sepSig)
     #Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 500,channel = "ele_bjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir,separateSignal=sepSig)
     #Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), 100, 0, 500,channel = "ele_bjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",blinding=True, blindingCut=50,output=tag+'pfMET_pre_ele_bjj',outDir=outdir,separateSignal=sepSig)
     #Stack.drawStack('BelePt', cut_pre_bjj, str(lumi*1000), 80, 0, 800, channel = "ele_bjj: Pre",titlex = "ele_Pt", units = "GeV",output=tag+'elePt_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BnVtx', cut_pre_bjj, str(lumi*1000), 100, 0, 100, channel = "ele_bjj: Pre", titlex = "nVtx", units = "",output=tag+'nVtx_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('Bnjet', cut_pre_bjj, str(lumi*1000), 20, 0, 20, channel = "ele_bjj: Pre", titlex = "njet", units = "",output=tag+'Bnjet_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BnPho', cut_pre_bjj, str(lumi*1000), 3, 0, 3, channel = "ele_bjj: Pre", titlex = "N_{#gamma}", units = "",output=tag+'BnPho_pre_ele_bjj',outDir=outdir,separateSignal=sepSig)
     # Stack.drawStack('BeleEta', cut_pre_bjj, str(lumi*1000), 30, -3, 3, channel = "ele_bjj: pre", titlex = "ele_Eta", units = "GeV",output=tag+'eleEta_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BMHT', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: pre", titlex = "MHT", units = "GeV",output=tag+'MHT_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     # Stack.drawStack('BHT', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: pre", titlex = "HT_jets", units = "GeV",output=tag+'HT_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


     Stack.closePSFile()
     sys.exit()


#--------------------------jjj---------------




if test:
     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_pre_jjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_jjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",blinding=True, blindingCut=100,output=tag+'pfMET_pre_ele_jjj',outDir=outdir)#,separateSignal=sepSig)
     Stack.drawStack('BpfMET', cut_pre_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#     Stack.drawStack('BpfMET', cut_pre_bjj_4qcd, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: Pre", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_pre_ele_bjj_4qcd',outDir=outdir)#,separateSignal=sepSig)


#     Stack.drawStack('BpfMET', cut_SR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: SR1", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#     Stack.drawStack('BpfMET', cut_CR1_bjj, str(lumi*1000), xBins_pfMET, 0, 1000, channel = "ele_bjj: CR1", titlex = "E_{T}^{mis}", units = "GeV",output=tag+'pfMET_CR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


#     Stack.drawStack('BjetM3', cut_pre_bjj, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: Pre", titlex = "jet_M3", units = "GeV",output=tag+'BjetM3_pre_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


#     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchele, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_gammamatchele',outDir=outdir)#,separateSignal=sepSig)

#     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gammamatchnonele, str(lumi*1000), 100, 0, 1000, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj_gammamatchnonele',outDir=outdir)#,separateSignal=sepSig)


#    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStackSketch('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta, str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch>0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchpho_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStackSketch('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch>0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchpho_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch<0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchjet_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStackSketch('BCandphoSigmaIEtaIEta', cut_bjj_1phowoIEtaIEta+" && BCandphoGenmatch<0", str(lumi*1000), 20, 0, 0.02, channel = "ele_bjj", titlex = "#sigma_{i#etai#eta}", units = "",output=tag+'SigmaIEtaIEta_matchjet_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoPFChIso', cut_bjj_1phowoChHadIso, str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoPFChIso', cut_bjj_1phowoChHadIso+" && BCandphoGenmatch>0", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_matchpho_ele_bjj',outDir=outdir)#,separateSignal=sepSig)
#    Stack.drawStack('BCandphoPFChIso', cut_bjj_1phowoChHadIso+" && BCandphoGenmatch<0", str(lumi*1000), 20, 0, 2, channel = "ele_bjj", titlex = "chargedHadIso", units = "",output=tag+'PFChIso_matchjet_ele_bjj',outDir=outdir)#,separateSignal=sepSig)



Stack.closePSFile()


