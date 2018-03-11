#!/-Usr/bin/env python                                                                                                                                        # Using the resulting hists from step1, to calculate some scale factors: QCD factor, wjets,ttbar sfs....                                                     # can jump to the bottom lines for config 

import math,sys
import ROOT
from ROOT import *
import os, string,  pickle
from TemplateFitter import TemplateFitter
from PlotterMET import PlotterMET
from Util import CombineSys

#################Functions#######################
def doQCD():
    print "#####################################################"
    print "*****************Calculate QCD sf********************"
    hdata=fin.Get(tag+"_ELE_pfMET_pre_ele_bjj_4qcd_data_obs")
    ndata=hdata.Integral()

    summc=0.
    mcnamelist=['TTV','TTG','VV','Wgamma','Zgamma','ST','ZJets','WJets','TT']
    #mcnamelist=['TTG','VV','Zgamma','Wgamma','WJets']
    for mcname in mcnamelist:
        hmc=fin.Get(tag+"_ELE_pfMET_pre_ele_bjj_4qcd_"+mcname)
        nmc=hmc.Integral()
        summc+=nmc

    hqcd=fin.Get(tag+"_ELE_pfMET_pre_ele_bjj_4qcd_QCD")
    nqcd=hqcd.Integral()

    k_qcd=(ndata-summc)/nqcd
    k_qcd_erratio=(1./(ndata-summc)+1./(nqcd))**0.5
    print "k_QCD = ",k_qcd
    print "*******************************************************\n\n\n"

    log.write("\n###############################################################")
    log.write("\n############Get QCD scale factor###############################")
    log.write("\n###############################################################")
    log.write("\nNdata=%s;NsummedMC=%s;NQCD=%s"%(ndata,summc,nqcd))
    log.write("\nk_qcd = %s"%k_qcd)
    log.write("\n###############################################################")
    log.write("\n###############################################################\n")
    return [k_qcd,k_qcd_erratio*k_qcd]

def doJetM3fit(k_qcd,sys=''):
    print "#####################################################"
    print "M3 templit fit for wjets and tt bkgs"
    JetM3Fitter=TemplateFitter()
    JetM3histname=tag+"_ELE_BjetM3_pre_ele_bjj_"
    JetM3Fitter.pushdata("SingleEle 2016 Data",fin.Get(JetM3histname+"data_obs"))
    if sys!='': JetM3histname=JetM3histname+sys+"_"
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
    log.write("\nThe systematic is %s\n"%sys)
    log.write("\n%s\n"%JetM3Fitter_result)
    log.write("\n The scale factor for wjets is %s"%k_wjets)
    log.write("\n The scale factor ERR for wjets is %s"%k_wjets_err)
    log.write("\n The scale factor for ttbar is %s"%k_ttbar)
    log.write("\n The scale factor ERR for ttbar is %s"%k_ttbar_err)
    log.write("\n#################################################################\n\n\n")

    if sys=='':
        JetM3Fitter.tempfitplot(foutname,"JetM3","Jet_M3(GeV)","Events/bin")

    if sys!='': print "systematic is ",sys
    print "The scale factor for wjets is",k_wjets,", and err is ",k_wjets_err
    print "The scale factor for ttbar is",k_ttbar,", and err is ",k_ttbar_err
    print "*******************************************************\n\n\n"

    return [k_wjets,k_wjets_err,k_ttbar,k_ttbar_err]

def doZJets(k_ttbar,k_wjets,sys=''):
    print "#####################################################"
    print "Invmass(ele_gamma) templit fit for DY and Vgamma Bkgs"
    InvEGFitter=TemplateFitter()
    InvEGhistname=tag+"_ELE_Invlepgamma_SR1_ele_bjj_"
    InvEGFitter.pushdata("SingleEle 2016 Data",fin.Get(InvEGhistname+"data_obs"))
    if sys!='': InvEGhistname=InvEGhistname+sys+'_'
    InvEGFitter.subdata(fin.Get(InvEGhistname+"TTV"))
    InvEGFitter.subdata(fin.Get(InvEGhistname+"TTG"))
    InvEGFitter.subdata(fin.Get(InvEGhistname+"TT"),scal=k_ttbar)
    InvEGFitter.subdata(fin.Get(InvEGhistname+"WJets"),scal=k_wjets)
    InvEGFitter.subdata(fin.Get(InvEGhistname+"VV"))
    InvEGFitter.subdata(fin.Get(InvEGhistname+"ST"))
    InvEGFitter.subdata(fin.Get(InvEGhistname+"Wgamma"))
    InvEGFitter.subdata(fin.Get(InvEGhistname+"Zgamma"))

    InvEGFitter.pushmc("DYgamma",fin.Get(InvEGhistname+"gammamatchnonele_ZJets"))
    InvEGFitter.pushmc("fakeDYgamma",fin.Get(InvEGhistname+"gammamatchele_ZJets"),col=kAzure+1)
    InvEGFitter.tempfit()
    InvEGFitter_result=InvEGFitter.result
    k_egamma=InvEGFitter_result['DYgamma'][2]
    k_egamma_err=InvEGFitter_result['DYgamma'][3]

    k_fake=InvEGFitter_result['fakeDYgamma'][2]
    k_fake_err=InvEGFitter_result['fakeDYgamma'][3]
    log.write("\n\n####################################################################")
    log.write("\n####################InvmassEG Fitter##################################")
    log.write("\n####################InvmassEF Fitter##################################")
    log.write("\nThe systematic is %s\n"%sys)
    log.write("\n%s\n"%InvEGFitter_result)
    log.write("\n Only in Ele channel, the scale factor for DY (non-ele-faked gamma) is %s"%k_egamma)
    log.write("\n Only in Ele channel, the scale factor ERR for DY(non-ele-faked gamma) is %s"%k_egamma_err)
    log.write("\n Only in Ele channel, the scale factor for DY (ele-faked gamma) is %s"%k_fake)
    log.write("\n Only in Ele channel, the scale factor ERR for DY(ele-faked gamma) is %s"%k_fake_err)
    log.write("\n#################################################################\n\n\n")
    if sys=='':
        InvEGFitter.tempfitplot(foutname,"SR1invEleG","Invmass(ele-gamma)(GeV)","Events/bin")
    if sys!='': print "systematic is ",sys
    print "The scale factor for DY(non-ele-faked gamma)  is",k_egamma,", and err is ",k_egamma_err
    print "The scale factor for DY(ele-faked gamma)  is",k_fake,", and err is ",k_fake_err
    print "*******************************************************\n\n\n"

    return[k_egamma,k_egamma_err,k_fake,k_fake_err]

def doCombZJets(sf_zjets_gamma,sferr_zjets_gamma,sf_zjets_efakep,sferr_zjets_efakep,sys=""):
    print "#####################################################"
    print "Will try to comb the SFs for ZJets in previous step to get only one sf, need to check the MET plot before apply it in limitsetting!"
    print "plot MET comparison before/after the sfs for ele-faked gamma and non-ele-faked gamma in Zjets samples "
    PlotMETZjets=PlotterMET()
    PlotMETZjets.pushbef("Before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchnonele_ZJets"),col=kBlack)
    PlotMETZjets.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchele_ZJets"))
    PlotMETZjets.pushaft("After",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchnonele_ZJets"),col=kBlue,scal=sf_zjets_gamma)
    PlotMETZjets.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchele_ZJets"),scal=sf_zjets_efakep)

    PlotMETZjets.syserror(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchnonele_ZJets"),fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchele_ZJets"),sferr_zjets_gamma,sferr_zjets_efakep)
    PlotMETZjets.plotMETcompare(foutname,"combZjets_pfMET","E_{T}^{miss} (GeV)","",sys)
    print "In Zjets samples, SF for non-ele-faked photon events is ",sf_zjets_gamma," and for ele faked gamma is ",sf_zjets_efakep
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETZjets.ratio
    print "And the ratio Fit Error is ",PlotMETZjets.ratioErr
    print "And the ratio Stat. Error is ",PlotMETZjets.ratiosysErr
    fitAstatErr=((PlotMETZjets.ratiosysErr)**2+(PlotMETZjets.ratioErr)**2)**0.5
    print "And the ratio Stat+Fit. Error is ",fitAstatErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape\n\n\n"

    log.write("\n\n####################################################################")
    log.write("Combine the sfs for ZJets(non-ele-faked and ele-faked photons) into one sf")
    log.write("\n Only in Ele channel SR1, the scale factor for DY is %s"%PlotMETZjets.ratio)
    log.write("\n Only in Ele channel SR1, the scale factor for DY Err is %s"%PlotMETZjets.ratioErr)
    log.write("\n Only in Ele channel SR1, the scale factor for DY Sys. Err is %s"%PlotMETZjets.ratiosysErr)
    log.write("\n#################################################################\n\n\n")
    
    return [PlotMETZjets.ratio,fitAstatErr]


def doSigmaIEIEfit(k_wjets,k_ttbar,k_zjets=1.0,sys=''):
    print "#####################################################"
    print "SigmaIetaIeta templit fit for TT and TTgamma in SR1"
    SigmaIEIEFitter=TemplateFitter()
    SigmaIEIEhistname=tag+"_ELE_SigmaIEtaIEta_ele_bjj_"
    SigmaIEIEFitter.pushdata("SingleEle 2016 Data",fin.Get(SigmaIEIEhistname+"data_obs"))
    if sys!='': SigmaIEIEhistname=SigmaIEIEhistname+sys+'_'
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
    log.write("\nThe systematic is %s\n"%sys)
    log.write("\n%s\n"%SigmaIEIEFitter_result)
    log.write("\n the scale factor for prompt photon is %s"%k_promptgamma)
    log.write("\n the scale factor for photon like jet Bkgs is %s"%k_bkgs_gammagenjet)
    log.write("\n#################################################################")
    log.write("\n#################################################################\n\n\n")
    if sys=='':
        SigmaIEIEFitter.tempfitplot(foutname,"SigmaIEIE","#sigma_{i#etai#eta}(GeV)","Events/bin")
    if sys!='': print "systematic is ",sys
    print 'the scale factor for prompt photon is ',k_promptgamma
    print 'the scale factor ERR for prompt photon is ',k_promptgamma_err
    print "The scale factor for bkgs is",k_bkgs_gammagenjet
    print "The scale factor ERR for bkgs is",k_bkgs_gammagenjet_err
#    print 'In mc, The original photon purity before fitting', OriginSigmaIEIE
#    print 'In mc, The photon purity after fitting', FitSigmaIEIE

    print "*******************************************************\n\n\n"

    return [k_promptgamma,k_promptgamma_err,k_bkgs_gammagenjet,k_bkgs_gammagenjet_err]


def doChHadIsofit(k_wjets,k_ttbar,k_zjets=1.0,sys=''):
    print "#####################################################"
    print "ChHadIso templit fit for TT and TTgamma"
    ChHadIsoFitter=TemplateFitter()
    ChHadIsohistname=tag+"_ELE_PFChIso_ele_bjj_"
    ChHadIsoFitter.pushdata("SingleEle 2016 Data",fin.Get(ChHadIsohistname+"data_obs"))
    if sys!='': ChHadIsohistname=ChHadIsohistname+sys+'_'
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
    log.write("\nThe systematic is %s\n"%sys)
    log.write("\n%s\n"%ChHadIsoFitter_result)
    log.write("\n the scale factor for prompt photon is %s"%k_promptgamma)
    log.write("\n the scale factor for photon like jet Bkgs is %s"%k_bkgs_gammagenjet)
    log.write("\n#################################################################")
    log.write("\n#################################################################\n\n\n")

    if sys=='':
        ChHadIsoFitter.tempfitplot(foutname,"ChHadIso","ChHadIso","Events/bin")
    if sys!='': print "systematic is ",sys

    print 'the scale factor for prompt photon is ',k_promptgamma
    print 'the scale factor ERR for prompt photon is ',k_promptgamma_err
    print "The scale factor for bkgs is",k_bkgs_gammagenjet
    print "The scale factor ERR for bkgs is",k_bkgs_gammagenjet_err
#    print 'In mc, The original photon purity before fitting', OriginChHadIso
#    print 'In mc, The photon purity after fitting', FitChHadIso

    print "*******************************************************\n\n\n"
    return [k_promptgamma,k_promptgamma_err,k_bkgs_gammagenjet,k_bkgs_gammagenjet_err]

def doCombTT(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma,sys=""):
    print "#####################################################"
    print "plot SR1 MET comparison before/after TT sfs"
    PlotMETTT=PlotterMET()
    PlotMETTT.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),col=kBlack)
    PlotMETTT.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"))
    PlotMETTT.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),col=kBlue,scal=sf_promptgamma)
    PlotMETTT.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma)

    PlotMETTT.syserror(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),sferr_promptgamma,sferr_nonpromptgamma)
    PlotMETTT.plotMETcompare(foutname,"combTT_pfMET","pfMET(GeV)","",sys)
    print "In SR1, TT samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTT.ratio
    print "And the ratio Error is ",PlotMETTT.ratioErr
    print "And the ratio Sys. Error is ",PlotMETTT.ratiosysErr
    fitAstatErr=((PlotMETTT.ratiosysErr)**2+(PlotMETTT.ratioErr)**2)**0.5
    print "And the ratio Stat+Fit. Error is ",fitAstatErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"
    print "*******************************************************\n\n\n"

    log.write("\n\n####################################################################")
    log.write("Combine the sfs for TT(prompt and non-prompt photons) into one sf")
    log.write("This sf is additional to the jetM3 k_ttbar, apply both in SR1")
    log.write("\n For SR1, the scale factor for TT is %s"%PlotMETTT.ratio)
    log.write("\n For SR1, the scale factor for TT Err is %s"%PlotMETTT.ratioErr)
    log.write("\n For SR1, the scale factor for TT Sys. Err is %s"%PlotMETTT.ratiosysErr)
    log.write("\n#################################################################\n\n\n")
    return [PlotMETTT.ratio,fitAstatErr]


def doCombTTSR2(sf_promptgamma,sf_nonpromptgamma):
    print "#####################################################"
    print "plot SR1 MET comparison before/after TT sfs"
    PlotMETTT=PlotterMET()
    PlotMETTT.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),col=kBlue)
    PlotMETTT.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"))
    PlotMETTT.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),col=kRed,scal=sf_promptgamma)
    PlotMETTT.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma)

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


def doCombTTG(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma,sys=""):
    print "#####################################################"
    print "plot MET comparison before/after TTG sfs"
    PlotMETTTG=PlotterMET()
    PlotMETTTG.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kBlack)
    PlotMETTTG.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"))
    PlotMETTTG.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kBlue,scal=sf_promptgamma)
    PlotMETTTG.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"),scal=sf_nonpromptgamma)

    PlotMETTTG.syserror(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"),sferr_promptgamma,sferr_nonpromptgamma)
    PlotMETTTG.plotMETcompare(foutname,"combTTG_pfMET","pfMET(GeV)","",sys)
    print "In TTG samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTTG.ratio
    print "And the ratio Error is ",PlotMETTTG.ratioErr
    print "And the ratio sys. Error is ",PlotMETTTG.ratiosysErr
    fitAstatErr=((PlotMETTTG.ratiosysErr)**2+(PlotMETTTG.ratioErr)**2)**0.5
    print "And the ratio Stat+Fit. Error is ",fitAstatErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"
    print "*******************************************************\n\n\n"

    log.write("\n\n####################################################################")
    log.write("Combine the sfs for TTG(prompt and non-prompt photons) into one sf")
    log.write("\n For SR1, the scale factor for TTG is %s"%PlotMETTTG.ratio)
    log.write("\n For SR1, the scale factor for TTG Err is %s"%PlotMETTTG.ratioErr)
    log.write("\n For SR1, the scale factor for TTG Sys. Err is %s"%PlotMETTTG.ratiosysErr)
    log.write("\n#################################################################\n\n\n")
    return [PlotMETTTG.ratio,fitAstatErr]


def doCombTTaTTG(sf_nonpromptgamma,sf_promptgamma,k_ttbar,sys=""):
    print "#####################################################"
    print "plot MET comparison before/after TT&TTG sfs, use only plot, don't use the following sf"
    PlotMETTTcom=PlotterMET()
    PlotMETTTcom.pushbef("Before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kBlack)
    PlotMETTTcom.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"))
    PlotMETTTcom.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),scal=k_ttbar)
    PlotMETTTcom.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),scal=k_ttbar)
    PlotMETTTcom.pushaft("After",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kBlue,scal=sf_promptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"),scal=sf_nonpromptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma*k_ttbar)
    PlotMETTTcom.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),scal=sf_promptgamma*k_ttbar)

    PlotMETTTcom.plotMETcompare(foutname,"combTTaTTG_pfMET","E_{T}^{miss} (GeV)","",sys)
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

fin=TFile.Open("step1_out/"+tag+"_ELE.root")  #input of ele channel                                                                                      
#eefin=TFile.Open("step1_out/"+tag+"_EE.root")    #input of ee channel                                                                                       
foutname="step2_out/fitfactor_ELE_"+tag
frootout=TFile.Open(foutname+".root","recreate")
frootout.Close()
log=open(foutname+".log","w")
sumlog=open(foutname+"summary.log","w")

# qcd sf for pre-region
[k_qcd,k_qcd_err]=doQCD()
sumlog.write("\n\n####################################################################")
sumlog.write("\n QCD normalization scale factor")
sumlog.write("\nk_qcd = %s\n"%k_qcd)
sumlog.write("\nk_qcd_err = %s\n\n\n"%k_qcd_err)

# ttbar, wjets sfs for pre-region
[k_wjets,k_wjets_err,k_ttbar,k_ttbar_err]=doJetM3fit(k_qcd)
sumlog.write("\n\n####################################################################")
sumlog.write("\n JetM3 template fit scale factor for wjets and ttbar")
sumlog.write("\nSYSTEMATIC: SF_wjets, SF_wjets_err, SF_ttbar, SF_ttbar_err\n")
sumlog.write("central:%s\n"%[k_wjets,k_wjets_err,k_ttbar,k_ttbar_err])

sys_wjets=CombineSys(k_wjets)
sys_ttbar=CombineSys(k_ttbar)
for sys in ['BbtagWeightUp','BbtagWeightDown','BeleWeightUp','BeleWeightDown','BtopPtWeightDown','BtopPtWeightUp']:
    [sk_wjets,sk_wjets_err,sk_ttbar,sk_ttbar_err]=doJetM3fit(k_qcd,sys)
    sumlog.write("%s:%s\n"%(sys,[sk_wjets,sk_wjets_err,sk_ttbar,sk_ttbar_err]))
    sys_wjets.pushsys(sk_wjets)
    sys_ttbar.pushsys(sk_ttbar)
sumlog.write("estimateJESUp(+5percent):%s\n"%[k_wjets*1.05,'----',k_ttbar*1.05,'---'])
sumlog.write("estimateJESUp(-5percent):%s\n"%[k_wjets*0.95,'----',k_ttbar*0.95,'---'])
sys_wjets.pushsys(sk_wjets*1.05)
sys_wjets.pushsys(sk_wjets*0.95)
sys_ttbar.pushsys(sk_ttbar*1.05)
sys_ttbar.pushsys(sk_ttbar*0.95)
sumlog.write("CombineSYS:--%s--%s\n\n\n"%(sys_wjets.sys(),sys_ttbar.sys()))

# zjets sfs for ELE SR1
[sf_zjets_gamma,sferr_zjets_gamma,sf_zjets_efakep,sferr_zjets_efakep]=doZJets(k_ttbar,k_wjets)
# try to comb the zjets sfs
[k_zjets,kerr_zjets]=doCombZJets(sf_zjets_gamma,sferr_zjets_gamma,sf_zjets_efakep,sferr_zjets_efakep,"")
sumlog.write("\n\n####################################################################")
sumlog.write("\n Zjets template fit scale factor for realgamma and elefakedgamma")
sumlog.write("\nSYSTEMATIC: SF_zjet_gamma, SF_zjet_gamma_err, SF_zjet_efakep, SF_zjet_efakep_err, combinedSF_zjet,combinedSF_zjet_err\n")
sumlog.write("central:%s\n"%[sf_zjets_gamma,sferr_zjets_gamma,sf_zjets_efakep,sferr_zjets_efakep,k_zjets,kerr_zjets])
sys_zjets_gamma=CombineSys(sf_zjets_gamma)
sys_zjets_efakep=CombineSys(sf_zjets_efakep)
sys_combZjets=CombineSys(k_zjets)
for sys in ['BbtagWeightUp','BbtagWeightDown','BeleWeightUp','BeleWeightDown','BtopPtWeightDown','BtopPtWeightUp','BphoWeightUp','BphoWeightDown']:
    [sysf_zjets_gamma,sysferr_zjets_gamma,sysf_zjets_efakep,sysferr_zjets_efakep]=doZJets(k_ttbar,k_wjets,sys)
    [sysk_zjets,syskerr_zjets]=doCombZJets(sysf_zjets_gamma,sysferr_zjets_gamma,sysf_zjets_efakep,sysferr_zjets_efakep,sys)
    sumlog.write("%s:%s\n"%(sys,[sysf_zjets_gamma,sysferr_zjets_gamma,sysf_zjets_efakep,sysferr_zjets_efakep,sysk_zjets,syskerr_zjets]))
    sys_zjets_gamma.pushsys(sysf_zjets_gamma)
    sys_zjets_efakep.pushsys(sysf_zjets_efakep)
    sys_combZjets.pushsys(sysk_zjets)
sumlog.write("CombineSYS:--%s--%s--%s\n\n\n"%(sys_zjets_gamma.sys(),sys_zjets_efakep.sys(),sys_combZjets.sys()))


#In SR1, fit the sfs for prompt non-prompt photons for samples: TT, TTG
SigmaIEIEresult=doSigmaIEIEfit(k_wjets,k_ttbar,k_zjets)
ChHadIsoresult=doChHadIsofit(k_wjets,k_ttbar,k_zjets)

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

combTTresult=doCombTT(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma,"")
combTTGresult=doCombTTG(sf_promptgamma,sferr_promptgamma,sf_nonpromptgamma,sferr_nonpromptgamma,"")
doCombTTaTTG(sf_nonpromptgamma,sf_promptgamma,k_ttbar,"")
sumlog.write("\n\n####################################################################")
sumlog.write("\n photon purity template fit scale factor for promptphoton and nonpromptphoton and combinedsf for tt, ttg\n")
sumlog.write("\nSYSTEMATIC:SigIEIE sf_promptg, sf_promptg_err, sf_nong, sf_nong_err, combinedSF_tt,tt_err, combineSF_ttg, ttg_err \n")
sumlog.write("central:%s\n"%(SigmaIEIEresult+combTTresult+combTTGresult))
sysIEIE_ppurity_promptgamma=CombineSys(SigmaIEIEresult[0])
sysIEIE_ppurity_nongamma=CombineSys(SigmaIEIEresult[2])
sysIEIE_tt=CombineSys(combTTresult[0])
sysIEIE_ttg=CombineSys(combTTGresult[0])
for sys in ['BbtagWeightUp','BbtagWeightDown','BeleWeightUp','BeleWeightDown','BtopPtWeightDown','BtopPtWeightUp','BphoWeightUp','BphoWeightDown']:
    [sysa,sysb,sysc,sysd]=doSigmaIEIEfit(k_wjets,k_ttbar,k_zjets,sys)
    [systt,systterr]=doCombTT(sysa,sysb,sysc,sysd,sys)
    [systtg,systtgerr]=doCombTTG(sysa,sysb,sysc,sysd,sys)
    sumlog.write("%s:%s\n"%(sys,[sysa,sysb,sysc,sysd,systt,systterr,systtg,systtgerr]))
    sysIEIE_ppurity_promptgamma.pushsys(sysa)
    sysIEIE_ppurity_nongamma.pushsys(sysc)
    sysIEIE_tt.pushsys(systt)
    sysIEIE_ttg.pushsys(systtg)
sumlog.write("CombineSYS:--%s--%s--%s--%s\n\n\n"%(sysIEIE_ppurity_promptgamma.sys(),sysIEIE_ppurity_nongamma.sys(),sysIEIE_tt.sys(),sysIEIE_ttg.sys()))

sumlog.write("\n\n####################################################################")
sumlog.write("\n photon purity template fit scale factor for promptphoton and nonpromptphoton (chargedHardron Iso)\n")
sumlog.write("\nSYSTEMATIC: sf_promptg, sf_promptg_err, sf_nong, sf_nong_err, combinedSF_tt,tt_err, combineSF_ttg, ttg_err \n")
sumlog.write("central:%s\n"%(ChHadIsoresult))
sysCHIso_ppurity_promptgamma=CombineSys(ChHadIsoresult[0])
sysCHIso_ppurity_nongamma=CombineSys(ChHadIsoresult[2])

for sys in ['BbtagWeightUp','BbtagWeightDown','BeleWeightUp','BeleWeightDown','BtopPtWeightDown','BtopPtWeightUp']:
    [sysa,sysb,sysc,sysd]=doChHadIsofit(k_wjets,k_ttbar,k_zjets,sys)
    sumlog.write("%s:%s\n"%(sys,[sysa,sysb,sysc,sysd]))
    sysCHIso_ppurity_promptgamma.pushsys(sysa)
    sysCHIso_ppurity_nongamma.pushsys(sysc)
sumlog.write("CombineSYS:--%s--%s\n\n\n"%(sysCHIso_ppurity_promptgamma.sys(),sysCHIso_ppurity_nongamma.sys()))

sumlog.close()
log.close()
