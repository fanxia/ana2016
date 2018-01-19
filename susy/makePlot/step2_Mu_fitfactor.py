#!/usr/bin/env python                                                                                                                                        # Using the resulting hists from step1, to calculate some scale factors: QCD factor, wjets,ttbar sfs....                                                     # can jump to the bottom lines for config 

import math,sys
import ROOT
from ROOT import *
import os, string,  pickle
from TemplateFitter import TemplateFitter
from PlotterMET import PlotterMET

#################Functions#######################
def doQCD():
    print "#####################################################"
    print "*****************Calculate QCD sf********************"
    hdata=fin.Get(tag+"_Mu_pfMET_pre_mu_bjj_4qcd_data_obs")
    ndata=hdata.Integral()

    summc=0.
    mcnamelist=['TTV','TTG','VV','Wgamma','Zgamma','ST','ZJets','WJets','TT']
    #mcnamelist=['TTG','VV','Zgamma','Wgamma','WJets']
    for mcname in mcnamelist:
        hmc=fin.Get(tag+"_Mu_pfMET_pre_mu_bjj_4qcd_"+mcname)
        nmc=hmc.Integral()
        summc+=nmc

    hqcd=fin.Get(tag+"_Mu_pfMET_pre_mu_bjj_4qcd_QCD")
    nqcd=hqcd.Integral()

    k_qcd=(ndata-summc)/nqcd
    print "k_QCD = ",k_qcd
    print "*******************************************************\n\n\n"

    log.write("\n###############################################################")
    log.write("\n############Get QCD scale factor###############################")
    log.write("\n###############################################################")
    log.write("\nNdata=%s;NsummedMC=%s;NQCD=%s"%(ndata,summc,nqcd))
    log.write("\nk_qcd = %s"%k_qcd)
    log.write("\n###############################################################")
    log.write("\n###############################################################\n")
    return k_qcd

def doJetM3fit(k_qcd):
    print "#####################################################"
    print "M3 templit fit for wjets and tt bkgs"
    JetM3Fitter=TemplateFitter()
    JetM3histname=tag+"_Mu_BjetM3_pre_mu_bjj_"
    JetM3Fitter.pushdata("SingleMu 2016 Data",fin.Get(JetM3histname+"data_obs"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"VV"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"ZJets"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"TTG"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"TTV"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"Wgamma"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"Zgamma"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"ST"))
    JetM3Fitter.subdata(fin.Get(JetM3histname+"QCD"),scal=k_qcd)

    JetM3Fitter.pushmc("wjets",fin.Get(JetM3histname+"WJets"))
    JetM3Fitter.pushmc("ttbar",fin.Get(JetM3histname+"TT"))
    #JetM3Fitter.pushmc("ttbar",fin.Get(JetM3histname+"TT"))
    #JetM3Fitter.addmc("ttbar",fin.Get(JetM3histname+"TTG"))

    JetM3Fitter.tempfit()
    JetM3Fitter_result=JetM3Fitter.result
    k_wjets=JetM3Fitter_result['wjets'][2]
    k_wjets_err=JetM3Fitter_result['wjets'][3]
    k_ttbar=JetM3Fitter_result['ttbar'][2]
    k_ttbar_err=JetM3Fitter_result['ttbar'][3]
    log.write("\n\n###############################################################")
    log.write("\n####################JetM3Fitter##################################")
    log.write("\n####################JetM3Fitter##################################")
    log.write("\n%s\n"%JetM3Fitter_result)
    log.write("\n The scale factor for wjets is %s"%k_wjets)
    log.write("\n The scale factor ERR for wjets is %s"%k_wjets_err)
    log.write("\n The scale factor for ttbar is %s"%k_ttbar)
    log.write("\n The scale factor ERR for ttbar is %s"%k_ttbar_err)
    log.write("\n#################################################################")
    log.write("\n#################################################################\n\n\n")
    JetM3Fitter.tempfitplot(foutname,"JetM3","Jet_M3(GeV)","Events/bin")


    print "The scale factor for wjets is",k_wjets,", and err is ",k_wjets_err
    print "The scale factor for ttbar is",k_ttbar,", and err is ",k_ttbar_err
    print "*******************************************************\n\n\n"

    return [k_wjets,k_wjets_err,k_ttbar,k_ttbar_err]

def doSigmaIEIEfit(k_wjets,k_ttbar,k_zjets=1.0):
    print "#####################################################"
    print "SigmaIetaIeta templit fit for TT and TTgamma in SR1"
    SigmaIEIEFitter=TemplateFitter()
    SigmaIEIEhistname=tag+"_Mu_SigmaIEtaIEta_mu_bjj_"
    SigmaIEIEFitter.pushdata("SingleMu 2016 Data",fin.Get(SigmaIEIEhistname+"data_obs"))
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"TTV"))
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"WJets"),scal=k_wjets)
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"ZJets"),scal=k_zjets)
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"VV"))
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"ST"))
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"Wgamma"))
    SigmaIEIEFitter.subdata(fin.Get(SigmaIEIEhistname+"Zgamma"))

    SigmaIEIEFitter.pushmc("Bkgs",fin.Get(SigmaIEIEhistname+"gammagenjet_TT"),scal=k_ttbar)
    SigmaIEIEFitter.addmc("Bkgs",fin.Get(SigmaIEIEhistname+"gammagenjet_TTG"))

    SigmaIEIEFitter.pushmc("Prompt TT#gamma",fin.Get(SigmaIEIEhistname+"gammagennojet_TTG"))
    SigmaIEIEFitter.addmc("Prompt TT#gamma",fin.Get(SigmaIEIEhistname+"gammagennojet_TT"),scal=k_ttbar)

#    OriginSigmaIEIE=SigmaIEIEFitter.mcsample[1].Integral(2,20)/(SigmaIEIEFitter.mcsample[0].Integral(2,20)+SigmaIEIEFitter.mcsample[1].Integral(2,20))# the original photon purity in mc before fitting
    SigmaIEIEFitter.tempfit()
    SigmaIEIEFitter_result=SigmaIEIEFitter.result
    k_bkgs_gammagenjet=SigmaIEIEFitter_result['Bkgs'][2]
    k_bkgs_gammagenjet_err=SigmaIEIEFitter_result['Bkgs'][3]
    k_promptgamma=SigmaIEIEFitter_result['Prompt TT#gamma'][2]
    k_promptgamma_err=SigmaIEIEFitter_result['Prompt TT#gamma'][3]
    #FitSigmaIEIE=SigmaIEIEFitter_result['Prompt TT#gamma'][0] #photon purity after fitting
#    FitSigmaIEIE=SigmaIEIEFitter.mcsample[1].Integral(2,20)*k_promptgamma/(SigmaIEIEFitter.mcsample[0].Integral(2,20)*k_bkgs_gammagenjet+SigmaIEIEFitter.mcsample[1].Integral(2,20)*k_promptgamma)

    log.write("\n\n####################################################################")
    log.write("\n####################For Photon Purity fitter (SR1)##################################")
    log.write("\n####################SigmaIetaIeta Fitter##################################")
    log.write("\n%s\n"%SigmaIEIEFitter_result)
    log.write("\n the scale factor for prompt photon is %s"%k_promptgamma)
    log.write("\n the scale factor for photon like jet Bkgs is %s"%k_bkgs_gammagenjet)
    log.write("\n#################################################################")
    log.write("\n#################################################################\n\n\n")
    SigmaIEIEFitter.tempfitplot(foutname,"SigmaIEIE","#sigma_{i#etai#eta}(GeV)","Events/bin")

    print 'the scale factor for prompt photon is ',k_promptgamma
    print 'the scale factor ERR for prompt photon is ',k_promptgamma_err
    print "The scale factor for bkgs is",k_bkgs_gammagenjet
    print "The scale factor ERR for bkgs is",k_bkgs_gammagenjet_err
#    print 'In mc, The original photon purity before fitting', OriginSigmaIEIE
#    print 'In mc, The photon purity after fitting', FitSigmaIEIE

    print "*******************************************************\n\n\n"

    return [k_promptgamma,k_promptgamma_err,k_bkgs_gammagenjet,k_bkgs_gammagenjet_err]


def doChHadIsofit(k_wjets,k_ttbar,k_zjets=1.0):
    print "#####################################################"
    print "ChHadIso templit fit for TT and TTgamma"
    ChHadIsoFitter=TemplateFitter()
    ChHadIsohistname=tag+"_Mu_PFChIso_mu_bjj_"
    ChHadIsoFitter.pushdata("SingleMu 2016 Data",fin.Get(ChHadIsohistname+"data_obs"))
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"TTV"))
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"WJets"),scal=k_wjets)
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"ZJets"),scal=k_zjets)
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"VV"))
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"ST"))
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"Wgamma"))
    ChHadIsoFitter.subdata(fin.Get(ChHadIsohistname+"Zgamma"))

    ChHadIsoFitter.pushmc("Bkgs",fin.Get(ChHadIsohistname+"gammagenjet_TT"),scal=k_ttbar)
    ChHadIsoFitter.addmc("Bkgs",fin.Get(ChHadIsohistname+"gammagenjet_TTG"))

    ChHadIsoFitter.pushmc("Prompt TT#gamma",fin.Get(ChHadIsohistname+"gammagennojet_TTG"))
    ChHadIsoFitter.addmc("Prompt TT#gamma",fin.Get(ChHadIsohistname+"gammagennojet_TT"),scal=k_ttbar)

#    OriginChHadIso=ChHadIsoFitter.mcsample[1].Integral(1,13)/(ChHadIsoFitter.mcsample[0].Integral(1,13)+ChHadIsoFitter.mcsample[1].Integral(1,13))# the original photon purity in mc before fitting
    ChHadIsoFitter.tempfit()
    ChHadIsoFitter_result=ChHadIsoFitter.result
    k_bkgs_gammagenjet=ChHadIsoFitter_result['Bkgs'][2]
    k_bkgs_gammagenjet_err=ChHadIsoFitter_result['Bkgs'][3]
    k_promptgamma=ChHadIsoFitter_result['Prompt TT#gamma'][2]
    k_promptgamma_err=ChHadIsoFitter_result['Prompt TT#gamma'][3]
    #FitChHadIso=ChHadIsoFitter_result['Prompt TT#gamma'][0] #photon purity after fitting
#    FitChHadIso=ChHadIsoFitter.mcsample[1].Integral(1,13)*k_promptgamma/(ChHadIsoFitter.mcsample[0].Integral(1,13)*k_bkgs_gammagenjet+ChHadIsoFitter.mcsample[1].Integral(1,13)*k_promptgamma)

    log.write("\n\n####################################################################")
    log.write("\n####################For Photon Purity fitter (SR1)##################################")
    log.write("\n####################ChHadIso Fitter##################################")
    log.write("\n%s\n"%ChHadIsoFitter_result)
    log.write("\n the scale factor for prompt photon is %s"%k_promptgamma)
    log.write("\n the scale factor for photon like jet Bkgs is %s"%k_bkgs_gammagenjet)
    log.write("\n#################################################################")
    log.write("\n#################################################################\n\n\n")
    ChHadIsoFitter.tempfitplot(foutname,"ChHadIso","ChHadIso","Events/bin")

    print 'the scale factor for prompt photon is ',k_promptgamma
    print 'the scale factor ERR for prompt photon is ',k_promptgamma_err
    print "The scale factor for bkgs is",k_bkgs_gammagenjet
    print "The scale factor ERR for bkgs is",k_bkgs_gammagenjet_err
#    print 'In mc, The original photon purity before fitting', OriginChHadIso
#    print 'In mc, The photon purity after fitting', FitChHadIso

    print "*******************************************************\n\n\n"
    return [k_promptgamma,k_promptgamma_err,k_bkgs_gammagenjet,k_bkgs_gammagenjet_err]

def doCombTT(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma):
    print "#####################################################"
    print "plot SR1 MET comparison before/after TT sfs"
    PlotMETTT=PlotterMET()
    PlotMETTT.pushbef("before",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),col=kBlue)
    PlotMETTT.addbef(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"))
    PlotMETTT.pushaft("after",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),col=kRed,scal=sf_promptgamma)
    PlotMETTT.addaft(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma)

    PlotMETTT.syserror(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"),sferr_promptgamma,sferr_nonpromptgamma)
    PlotMETTT.plotMETcompare(foutname,"combTT_pfMET","pfMET(GeV)","")
    print "In SR1, TT samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTT.ratio
    print "And the ratio Error is ",PlotMETTT.ratioErr
    print "And the ratio Sys. Error is ",PlotMETTT.ratiosysErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"
    print "*******************************************************\n\n\n"

    log.write("\n\n####################################################################")
    log.write("Combine the sfs for TT(prompt and non-prompt photons) into one sf")
    log.write("This sf is additional to the jetM3 k_ttbar, apply both in SR1")
    log.write("\n For SR1, the scale factor for TT is %s"%PlotMETTT.ratio)
    log.write("\n For SR1, the scale factor for TT Err is %s"%PlotMETTT.ratioErr)
    log.write("\n For SR1, the scale factor for TT Sys. Err is %s"%PlotMETTT.ratiosysErr)
    log.write("\n#################################################################\n\n\n")


def doCombTTSR2(sf_promptgamma,sf_nonpromptgamma):
    print "#####################################################"
    print "plot SR1 MET comparison before/after TT sfs"
    PlotMETTT=PlotterMET()
    PlotMETTT.pushbef("before",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),col=kBlue)
    PlotMETTT.addbef(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"))
    PlotMETTT.pushaft("after",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),col=kRed,scal=sf_promptgamma)
    PlotMETTT.addaft(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma)

    PlotMETTT.plotMETcompare(foutname,"combTT_pfMET","pfMET(GeV)","")
    print "In SR1, TT samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTT.ratio
    print "And the ratio Error is ",PlotMETTT.ratioErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"
    print "*******************************************************\n\n\n"

    log.write("\n\n####################################################################")
    log.write("Combine the sfs for TT(prompt and non-prompt photons) into one sf")
    log.write("This sf is additional to the jetM3 k_ttbar, apply both in SR1")
    log.write("\n For SR1, the scale factor for TT is %s"%PlotMETTT.ratio)
    log.write("\n For SR1, the scale factor for TT Err is %s"%PlotMETTT.ratioErr)
    log.write("\n#################################################################\n\n\n")


def doCombTTG(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma):
    print "#####################################################"
    print "plot MET comparison before/after TTG sfs"
    PlotMETTTG=PlotterMET()
    PlotMETTTG.pushbef("before",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TTG"),col=kBlue)
    PlotMETTTG.addbef(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TTG"))
    PlotMETTTG.pushaft("after",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TTG"),col=kRed,scal=sf_promptgamma)
    PlotMETTTG.addaft(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TTG"),scal=sf_nonpromptgamma)

    PlotMETTTG.syserror(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TTG"),fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TTG"),sferr_promptgamma,sferr_nonpromptgamma)
    PlotMETTTG.plotMETcompare(foutname,"combTTG_pfMET","pfMET(GeV)","")
    print "In TTG samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTTG.ratio
    print "And the ratio Error is ",PlotMETTTG.ratioErr
    print "And the ratio sys. Error is ",PlotMETTTG.ratiosysErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"
    print "*******************************************************\n\n\n"

    log.write("\n\n####################################################################")
    log.write("Combine the sfs for TTG(prompt and non-prompt photons) into one sf")
    log.write("\n For SR1, the scale factor for TTG is %s"%PlotMETTTG.ratio)
    log.write("\n For SR1, the scale factor for TTG Err is %s"%PlotMETTTG.ratioErr)
    log.write("\n For SR1, the scale factor for TTG Sys. Err is %s"%PlotMETTTG.ratiosysErr)
    log.write("\n#################################################################\n\n\n")


def doCombTTaTTG(sf_nonpromptgamma,sf_promptgamma,k_ttbar):
    print "#####################################################"
    print "plot MET comparison before/after TT&TTG sfs, use only plot, don't use the following sf"
    PlotMETTTcom=PlotterMET()
    PlotMETTTcom.pushbef("before",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TTG"),col=kBlue)
    PlotMETTTcom.addbef(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TTG"))
    PlotMETTTcom.addbef(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"),scal=k_ttbar)
    PlotMETTTcom.addbef(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),scal=k_ttbar)
    PlotMETTTcom.pushaft("after",fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TTG"),col=kRed,scal=sf_promptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TTG"),scal=sf_nonpromptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma*k_ttbar)
    PlotMETTTcom.addaft(fin.Get(tag+"_Mu_pfMET_SR1_mu_bjj_gammagennojet_TT"),scal=sf_promptgamma*k_ttbar)

    PlotMETTTcom.plotMETcompare(foutname,"combTTaTTG_pfMET","pfMET(GeV)","")
    print "In TT/TTG samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTTcom.ratio
    print "And the ratio Error is ",PlotMETTTcom.ratioErr
    print "You need to carefully check the comparison ratio hists to make sure the seperate sfs won't affect the MET shape"
    print "*******************************************************\n\n\n"
    log.write("\n\n####################################################################")
    log.write("Combine the sfs for TT&TTG(prompt and non-prompt photons) into one sf")
    log.write("\n For SR1, the scale factor for TT&TTG is %s"%PlotMETTTcom.ratio)
    log.write("\n For SR1, the scale factor for TT&TTG Err is %s"%PlotMETTTcom.ratioErr)
    log.write("\n#################################################################\n\n\n")

######################################################################################
##############Running config area#####################################################
######################################################################################
tag=sys.argv[1]

fin=TFile.Open("step1_out/"+tag+"_Mu.root")  #input of mu channel                                                                                      

foutname="step2_out/fitfactor_Mu_"+tag
frootout=TFile.Open(foutname+".root","recreate")
frootout.Close()
log=open(foutname+".log","w")

# qcd sf for pre-region
k_qcd=doQCD()

# ttbar, wjets sfs for pre-region
[k_wjets,k_wjets_err,k_ttbar,k_ttbar_err]=doJetM3fit(k_qcd)


#In SR1, fit the sfs for prompt non-prompt photons for samples: TT, TTG
SigmaIEIEresult=doSigmaIEIEfit(k_wjets,k_ttbar)
ChHadIsoresult=doChHadIsofit(k_wjets,k_ttbar)

# comb prompt non-prompt photons sfs for TT, TTG
print "Try comb photon purity sfs for TT and TTG, will use the SigmaIEIE templatefit results!"
useSigmaIEIE=True
if useSigmaIEIE:
           [k_promptgamma,k_promptgamma_err,k_bkgs_gammagenjet,k_bkgs_gammagenjet_err]=SigmaIEIEresult
else:
           [k_promptgamma,k_promptgamma_err,k_bkgs_gammagenjet,k_bkgs_gammagenjet_err]=ChHadIsoresult

sf_promptgamma=k_promptgamma
sferr_promptgamma=k_promptgamma_err
sf_nonpromptgamma=k_bkgs_gammagenjet
sferr_nonpromptgamma=k_bkgs_gammagenjet_err

doCombTT(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma)
doCombTTG(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma)
doCombTTaTTG(sf_nonpromptgamma,sf_promptgamma,k_ttbar)

log.close()
