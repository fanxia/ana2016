#!/usr/bin/env python
import math,sys
import ROOT
from ROOT import *
import os, string, math, pickle
from TemplateFitter import TemplateFitter

fin=TFile.Open("plots/Feb2_PFIsolepgammasf.root")
foutname="Templatefitplots/tempfit"
frootout=TFile.Open(foutname+".root","recreate")
frootout.Close()
log=open(foutname+".log","w")


JetM3Fitter=TemplateFitter()
JetM3histname="Feb2_PFIsolepgammasf_BjetM3_pre_ele_bjj_"
JetM3Fitter.pushdata("SingleEle 2016 Data",fin.Get(JetM3histname+"data_step1_SingleEle_Run2016B_SepRereco"))

JetM3Fitter.pushmc("wjets",fin.Get(JetM3histname+"WJets_step1p5_WJetsToLNu"))
JetM3Fitter.pushmc("ttbar",fin.Get(JetM3histname+"TT_step1p5_TT_powheg"))
JetM3Fitter.addmc("ttbar",fin.Get(JetM3histname+"TTG_step1p5_TTGJets"))

JetM3Fitter.tempfit()
log.write("\n####################JetM3Fitter####################")
log.write("\n%s\n"%JetM3Fitter.result)

JetM3Fitter.tempfitplot(foutname,"JetM3","Jet_M3(GeV)","Events/bin")





log.close()
