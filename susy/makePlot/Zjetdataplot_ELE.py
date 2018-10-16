#!/usr/bin/env python
import math,sys
import ROOT
import os, string, math, pickle
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from StackPlotter import StackPlotter
ROOT.gROOT.SetBatch()

SF_QCD=0.39
SF_tt=0.818
SF_wjets=1.72
SF_Zjets=1.4
SF_gpurity_tt=1.
SF_gpurity_ttg=1.

tag=sys.argv[1]
tag=tag+"_ELEZjet"
LogY=False

AddQCD=True
#AddQCD=False
normaldraw=True
test=False

outdir='extraplot_out'
indir='../ntupleStore'

tree='EventTree_ele'
treeQCD='EventTree_eQCD'


lumi=35.87   #1.731    #4.353 #2016D
doRatio=False
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


Stack = StackPlotter(outTag=tag, outDir=outdir)
Stack.setPaveText(paveText)
Stack.addPlotter(Data, "data_obs", "Data", "data")


Stack.addPlotter(TTV, "TTV","TTV", "background")
Stack.addPlotter(TTG, "TTG","TT#gamma", "background")
Stack.addPlotter(VV, "VV","ZZ WZ WW.", "background")
Stack.addPlotter(VG, "Vgamma","V#gamma", "background")

#Stack.addPlotter(ZJets, "ZJets","ZJets", "background")
Stack.addPlotter(ST, "ST","single top", "background")
Stack.addPlotter(WJets, "WJets","WJets", "background")
Stack.addPlotter(TT, "TT","TT", "background")
#Stack.addPlotter(QCD,"QCD","QCD","background")


Stack.setLog(LogY)
Stack.doRatio(doRatio)

#Stackpre=Stack   # only for pre region where consider the qcd contributes
#if AddQCD: Stackpre.addPlotter(QCD,"QCD","QCD","background")

tag+='_'


xBins_pfMET=[0,20,60,100,150,300,500,1000]
xBins_Pt=[0,20,40,60,80,100,120,160,200,250,300,400,500,600,800,1000,1250]
xBins2_pfMET=[0,50,100,250,500,1000]
#print cuts

if normaldraw: 

     Stack.drawStack('BCandphoLepInvMass', cut_SR1_bjj_4gamma, str(lumi*1000), 10, 70, 120, channel = "ele_bjj: SR1", titlex = "Invmass(ele,#gamma)", units = "GeV",output=tag+'Invlepgamma_SR1_ele_bjj',outDir=outdir)#,separateSignal=sepSig)


 
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


