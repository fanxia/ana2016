# Using the resulting hists from step1, to calculate some scale factors: QCD factor, wjets,ttbar sfs....
#!/usr/bin/env python
import math,sys
import ROOT
from ROOT import *
import os, string, math, pickle
from TemplateFitter import TemplateFitter


tag="Mar1_QCD"

fin=TFile.Open("step1_out/"+tag+".root")
foutname="step2_out/fitfactor"+tag
frootout=TFile.Open(foutname+".root","recreate")
frootout.Close()
log=open(foutname+".log","w")




#################### QCD scale factor ######################
###,--.             ,-----.     ,-----. ,------.        ####
###|  |,-.         '  .-.  '   '  .--./ |  .-.  \       ####
###|     /         |  | |  |   |  |     |  |  \  :      ####
###|  \  \  ,----. '  '-'  '-. '  '--'\ |  '--'  /      ####
###`--'`--' '----'  `-----'--'  `-----' `-------'       ####
#################### QCD scale factor ######################                                                    

print "*****************Calculate QCD sf********************"
hdata=fin.Get(tag+"_pfMET_pre_ele_bjj_4qcd_data")
ndata=hdata.Integral()

summc=0.
mcnamelist=['TTV','TTG','VV','Vgamma','ST','ZJets','WJets','TT']
for mcname in mcnamelist:
    hmc=fin.Get(tag+"_pfMET_pre_ele_bjj_4qcd_"+mcname)
    nmc=hmc.Integral()
    summc+=nmc

hqcd=fin.Get(tag+"_pfMET_pre_ele_bjj_4qcd_QCD")
nqcd=hqcd.Integral()

k_qcd=(ndata-summc)/nqcd
print "k_QCD = ",k_qcd
print "*******************************************************\n\n\n"

log.write("\n###############################################################")
log.write("\n############Get QCD scale factor###############################")
log.write("\n###############################################################")
log.write("\nNdata=%s;NsummedMC=%s;NQCD=%s"%(ndata,summc,nqcd))
log.write("\n%s"%k_qcd)
log.write("\n###############################################################")
log.write("\n###############################################################\n")


################### M3 templit fit for wjets and tt bkgs ####################
####     ,--.           ,--.          ,--.   ,--. ,----.                ##### 
####     |  |  ,---.  ,-'  '-.        |   `.'   | '.-.  |               #####
####,--. |  | | .-. : '-.  .-'        |  |'.'|  |   .' <                #####
####|  '-'  / \   --.   |  |   ,----. |  |   |  | /'-'  |               #####
#### `-----'   `----'   `--'   '----' `--'   `--' `----'                #####
################### M3 templit fit for wjets and tt bkgs ####################

print "M3 templit fit for wjets and tt bkgs"
JetM3Fitter=TemplateFitter()
JetM3histname=tag+"_BjetM3_pre_ele_bjj_"
JetM3Fitter.pushdata("SingleEle 2016 Data",fin.Get(JetM3histname+"data"))
JetM3Fitter.subdata(fin.Get(JetM3histname+"VV"))
JetM3Fitter.subdata(fin.Get(JetM3histname+"ZJets"))
JetM3Fitter.subdata(fin.Get(JetM3histname+"TTG"))
JetM3Fitter.subdata(fin.Get(JetM3histname+"QCD"),scal=k_qcd)

JetM3Fitter.pushmc("wjets",fin.Get(JetM3histname+"WJets"))
JetM3Fitter.pushmc("ttbar",fin.Get(JetM3histname+"TT"))
#JetM3Fitter.addmc("ttbar",fin.Get(JetM3histname+"TTG"))

JetM3Fitter.tempfit()
JetM3Fitter_result=JetM3Fitter.result
k_wjets=JetM3Fitter_result['wjets'][2]
k_ttbar=JetM3Fitter_result['ttbar'][2]
log.write("\n\n###############################################################")
log.write("\n####################JetM3Fitter##################################")
log.write("\n####################JetM3Fitter##################################")
log.write("\n%s\n"%JetM3Fitter_result)
log.write("\n The scale factor for wjets is %s"%k_wjets)
log.write("\n The scale factor for ttbar is %s"%k_ttbar)
log.write("\n#################################################################")
log.write("\n#################################################################\n\n\n")
JetM3Fitter.tempfitplot(foutname,"JetM3","Jet_M3(GeV)","Events/bin")


print "The scale factor for wjets is",k_wjets
print "The scale factor for ttbar is",k_ttbar
print "*******************************************************\n\n\n"





########################################################################################################
##,--.                     ,--.   ,--.                                                                ##
##`--' ,--,--,  ,--.  ,--. |   `.'   |         ,---.   ,---.   ,--,--. ,--,--,--. ,--,--,--.  ,--,--. ##
##,--. |      \  \  `'  /  |  |'.'|  |        | .-. : | .-. | ' ,-.  | |        | |        | ' ,-.  | ##
##|  | |  ||  |   \    /   |  |   |  | ,----. \   --. ' '-' ' \ '-'  | |  |  |  | |  |  |  | \ '-'  | ##
##`--' `--''--'    `--'    `--'   `--' '----'  `----' .`-  /   `--`--' `--`--`--' `--`--`--'  `--`--' ##
##                                                    `---'                                           ##
########################################################################################################                            ##Only need in elechannel, in SR1, template fit invmass(egamma) to get sfs for DY,Vgamma bkgs                 
print "Invmass(ele_gamma) templit fit for DY and Vgamma Bkgs"
InvEGFitter=TemplateFitter()
InvEGhistname=tag+"_Invlepgamma_SR1_ele_bjj_"
InvEGFitter.pushdata("SingleEle 2016 Data",fin.Get(InvEGhistname+"data"))

InvEGFitter.pushmc("Bkgs",fin.Get(InvEGhistname+"TTV"))
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"TTG"))
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"TT"),scal=k_ttbar)
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"WJets"),scal=k_wjets)
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"VV"))
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"ST"))
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"gammamatchnonele_ZJets"))
InvEGFitter.addmc("Bkgs",fin.Get(InvEGhistname+"gammamatchnonele_Vgamma"))


InvEGFitter.pushmc("DY/V#gamma",fin.Get(InvEGhistname+"gammamatchele_ZJets"))
InvEGFitter.addmc("DY/V#gamma",fin.Get(InvEGhistname+"gammamatchele_Vgamma"))

InvEGFitter.tempfit()
InvEGFitter_result=InvEGFitter.result
k_bkgs=InvEGFitter_result['Bkgs'][2]
k_egamma=InvEGFitter_result['DY/V#gamma'][2]

log.write("\n\n####################################################################")
log.write("\n####################InvmassEG Fitter##################################")
log.write("\n####################InvmassEF Fitter##################################")
log.write("\n%s\n"%InvEGFitter_result)
log.write("\n Only in Ele channel, the scale factor for DY&Vgamma is %s"%k_egamma)
log.write("\n Only in Ele channel, the scale factor for Bkgs is %s"%k_bkgs)
log.write("\n#################################################################")
log.write("\n#################################################################\n\n\n")
InvEGFitter.tempfitplot(foutname,"SR1invEleG","Invmass(ele-gamma)(GeV)","Events/bin")

print "The scale factor for DY&Vgamma  is",k_egamma
print "The scale factor for bkgs is",k_bkgs
print "*******************************************************\n\n\n"





log.close()
