import math, sys
import ROOT
from ROOT import *
from PlotterMET import PlotterMET

tag=sys.argv[1]
fin=TFile.Open("step1_out/"+tag+"_ELE.root")
foutname="step2_out/plotMET_ELE_"+tag
frootout=TFile.Open(foutname+".root","recreate")
frootout.Close()

DoZjets=True
sf_zjets_efakep=1.9
sf_zjets_gamma=1.1


if DoZjets==True:
    print "plot MET comparison before/after Zjets sfs"
    PlotMETZjets=PlotterMET()
    PlotMETZjets.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchnonele_ZJets"),col=kBlue)
    PlotMETZjets.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchele_ZJets"))
    PlotMETZjets.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchnonele_ZJets"),col=kRed,scal=sf_zjets_gamma)
    PlotMETZjets.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammamatchele_ZJets"),scal=sf_zjets_efakep)

    PlotMETZjets.plotMETcompare(foutname,"Zjets","pfMET(GeV)","")
    print "In Zjets samples, SF for non-ele-faked photon events is ",sf_zjets_gamma," and for ele faked gamma is ",sf_zjets_efakep
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETZjets.ratio
    print "And the ratio Error is ",PlotMETZjets.ratioErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"


    print "plot nJet comparison before/after Zjets sfs"
    PlotnJetsZjets=PlotterMET()
    PlotnJetsZjets.pushbef("before",fin.Get(tag+"_ELE_Bnjet_SR1_ele_bjj_gammamatchnonele_ZJets"),col=kBlue)
    PlotnJetsZjets.addbef(fin.Get(tag+"_ELE_Bnjet_SR1_ele_bjj_gammamatchele_ZJets"))
    PlotnJetsZjets.pushaft("after",fin.Get(tag+"_ELE_Bnjet_SR1_ele_bjj_gammamatchnonele_ZJets"),col=kRed,scal=sf_zjets_gamma)
    PlotnJetsZjets.addaft(fin.Get(tag+"_ELE_Bnjet_SR1_ele_bjj_gammamatchele_ZJets"),scal=sf_zjets_efakep)

    PlotnJetsZjets.plotMETcompare(foutname,"Zjets","N_{jets}","")
    print "In Zjets samples, SF for non-ele-faked photon events is ",sf_zjets_gamma," and for ele faked gamma is ",sf_zjets_efakep
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotnJetsZjets.ratio
    print "And the ratio Error is ",PlotnJetsZjets.ratioErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"


if DoTT==True:
    print "plot MET comparison before/after TT sfs"
    PlotMETTT=PlotterMET()
    PlotMETTT.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),col=kBlue)
    PlotMETTT.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"))
    PlotMETTT.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),col=kRed,scal=sf_promptgamma)
    PlotMETTT.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma)

    PlotMETTT.plotMETcompare(foutname,"TT","pfMET(GeV)","")
    print "In TT samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTT.ratio
    print "And the ratio Error is ",PlotMETTT.ratioErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"

if DoTTG==True:
    print "plot MET comparison before/after TTG sfs"
    PlotMETTTG=PlotterMET()
    PlotMETTTG.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kBlue)
    PlotMETTTG.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"))
    PlotMETTTG.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kRed,scal=sf_promptgamma)
    PlotMETTTG.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"),scal=sf_nonpromptgamma)

    PlotMETTTG.plotMETcompare(foutname,"TTG","pfMET(GeV)","")
    print "In TTG samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTTG.ratio
    print "And the ratio Error is ",PlotMETTTG.ratioErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"

if DoTTcom==True:
    print "plot MET comparison before/after TT&TTG sfs, use only plot, don't use the following sf"
    PlotMETTTcom=PlotterMET()
    PlotMETTTcom.pushbef("before",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kBlue)
    PlotMETTTcom.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"))
    PlotMETTTcom.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"))
    PlotMETTTcom.addbef(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"))
    PlotMETTTcom.pushaft("after",fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TTG"),col=kRed,scal=sf_promptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TTG"),scal=sf_nonpromptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagenjet_TT"),scal=sf_nonpromptgamma)
    PlotMETTTcom.addaft(fin.Get(tag+"_ELE_pfMET_SR1_ele_bjj_gammagennojet_TT"),scal=sf_promptgamma)

    PlotMETTTcom.plotMETcompare(foutname,"TTaTTG","pfMET(GeV)","")
    print "In TT/TTG samples, SF for non-prompt photon(jet) events is ",sf_nonpromptgamma," and for prompt gamma is ",sf_promptgamma
    print "Before/After applying the above sfs, the total ratio for the whole sample is ",PlotMETTTcom.ratio
    print "And the ratio Error is ",PlotMETTTcom.ratioErr
    print "You need to carefully check the before/after ratio hists to make sure the seperate sfs won't affect the MET shape"
