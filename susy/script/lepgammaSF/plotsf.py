#! /usr/bin/env python
from ROOT import *
import ROOT
from array import array
import sys
import os


def Fun_thisSF(eta,pt,sfhist):
    if pt>=sfhist.GetYaxis().GetXmax(): #above pt range            
        result=[sfhist.GetBinContent(sfhist.GetXaxis().FindBin(eta),sfhist.GetYaxis().GetLast()),2.*sfhist.GetBinError(sfhist.GetXaxis().FindBin(eta),sfhist.GetYaxis().GetLast())]
    else: result=[sfhist.GetBinContent(sfhist.FindBin(eta,pt)),sfhist.GetBinError(sfhist.FindBin(eta,pt))]
    return result[0]

def Fun_thisSFTGraph(par,sfhist):
    result=[sfhist.Eval(par)] 
    return result[0]


file_eleSF_reco = TFile.Open("eleEffi-reco.root")
eleRecosfHist=file_eleSF_reco.Get("EGamma_SF2D")
file_eleSF_id = TFile.Open("eleEffi-tightID.root")
eleIDsfHist=file_eleSF_id.Get("EGamma_SF2D")

file_mu1SF_id=TFile.Open("MuonIDEffi_RunB2F.root")
file_muSF2_id=TFile.Open("MuonIDEffi_RunGH.root")
muIDsf1Hist=file_mu1SF_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")
muIDsf2Hist=file_muSF2_id.Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio")

file_muSF1_iso=TFile.Open("MuonIsoEffi_RunB2F.root")
file_muSF2_iso=TFile.Open("MuonIsoEffi_RunGH.root")
muIsosf1Hist=file_muSF1_iso.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")
muIsosf2Hist=file_muSF2_iso.Get("TightISO_TightID_pt_eta/abseta_pt_ratio")

file_muSF1_Trk = TFile.Open("MuonTrkEffi_RunB2H.root")
file_muSF2_Trk = TFile.Open("MuonTrkEffi_RunB2H.root")
muTrksf1Hist=file_muSF1_Trk.Get("ratio_eff_aeta_dr030e030_corr")
muTrksf2Hist=file_muSF2_Trk.Get("ratio_eff_aeta_dr030e030_corr")

file_phoSF=TFile.Open("gammaIDsf.root")
file_phoPixSF=TFile.Open("gammaPixelvetosf.root")
phosfHist=file_phoSF.Get("EGamma_SF2D")
phoPixsfHist=file_phoPixSF.Get("Scaling_Factors_HasPix_R9 Inclusive")

fout=TFile("SFplots.root","recreate")



binye=[35,50,100,200,500]
binxe=[-2.1,-1.566,-1.44,-0.8,0,0.8,1.44,1.566,2.1]
sfehist=TH2F("sfe","sfe",len(binxe)-1,array('d',binxe),len(binye)-1,array('d',binye))
sfehist.Sumw2()


binym=[30,40,50,60,120,200,500]
binxm=[0,0.9,1.2,2.1,2.4]
sfm1hist=TH2F("sfm1","sfm1",len(binxm)-1,array('d',binxm),len(binym)-1,array('d',binym))
sfm1hist.Sumw2()
sfm2hist=TH2F("sfm2","sfm2",len(binxm)-1,array('d',binxm),len(binym)-1,array('d',binym))
sfm2hist.Sumw2()


binyp=[20,35,50,100,200,500]
binxp=[-1.44,-0.8,0,0.8,1.44]
sfphist=TH2F("sfp","sfp",len(binxp)-1,array('d',binxp),len(binyp)-1,array('d',binyp))
sfphist.Sumw2()



def Fillplot(binx,biny,sfhist,hists):
    for i in range(len(binx)-1):
        for j in range(len(biny)-1):
            xc=(binx[i]+binx[i+1])/2.
            yc=(biny[j]+biny[j+1])/2.
            sf=1.
            for h in hists:
                if h==muTrksf1Hist or h==muTrksf2Hist:
                    sf*=Fun_thisSFTGraph(xc,h)
                elif h==phoPixsfHist:
                    sf*=Fun_thisSF(abs(xc),yc,h)
                else:
                    sf*=Fun_thisSF(xc,yc,h)

            sfhist.SetBinContent(sfhist.FindBin(xc,yc),sf)
    sfhist.Write()


Fillplot(binxe,binye,sfehist,[eleRecosfHist,eleIDsfHist])
Fillplot(binxm,binym,sfm1hist,[muTrksf1Hist,muIDsf1Hist,muIsosf1Hist])
Fillplot(binxm,binym,sfm2hist,[muTrksf2Hist,muIDsf2Hist,muIsosf2Hist])
Fillplot(binxp,binyp,sfphist,[phosfHist,phoPixsfHist])





###########################plot part#####################
os.system("mkdir SFPlot")
c=ROOT.TCanvas("c","Plots",1000,1200)
c.SetRightMargin(0.13)
gStyle.SetOptStat(0)

gPad.SetLogy()
sfehist.SetTitle("Electron Scale Factor in 2016 Run;#eta; P_{T}")
sfehist.Draw("colz")
sfehist.GetYaxis().SetMoreLogLabels()
sfehist.GetYaxis().SetNoExponent()
sfehist.Draw("colz")
sfehist.GetYaxis().CenterTitle()
sfehist.GetYaxis().SetTitleOffset(1.4)
c.Print("SFPlot/elesf.pdf")

sfehist.SetMarkerSize(1.5)
gStyle.SetPaintTextFormat("3.2f")
sfehist.Draw("TEXT same")
c.Print("SFPlot/elesftext.pdf")

c.Clear()
sfm1hist.SetTitle("Muon Scale Factor in 2016 RunB2F;|#eta|; P_{T}")
sfm1hist.Draw("colz")
sfm1hist.GetYaxis().SetMoreLogLabels()
sfm1hist.GetYaxis().SetNoExponent()
sfm1hist.Draw("colz")
sfm1hist.GetYaxis().CenterTitle()
sfm1hist.GetYaxis().SetTitleOffset(1.4)
c.Print("SFPlot/muonsf1.pdf")

sfm1hist.SetMarkerSize(1.5)
gStyle.SetPaintTextFormat("3.2f")
sfm1hist.Draw("TEXT same")
c.Print("SFPlot/muonsf1text.pdf")

c.Clear()
sfm2hist.SetTitle("Muon Scale Factor in 2016 RunGH;|#eta|; P_{T}")
sfm2hist.Draw("colz")
sfm2hist.GetYaxis().SetMoreLogLabels()
sfm2hist.GetYaxis().SetNoExponent()
sfm2hist.Draw("colz")
sfm2hist.GetYaxis().CenterTitle()
sfm2hist.GetYaxis().SetTitleOffset(1.4)
c.Print("SFPlot/muonsf2.pdf")

sfm2hist.SetMarkerSize(1.5)
gStyle.SetPaintTextFormat("3.2f")
sfm2hist.Draw("TEXT same")
c.Print("SFPlot/muonsf2text.pdf")

c.Clear()
sfphist.SetTitle("Photon Scale Factor in 2016 Run;#eta; P_{T}")
sfphist.Draw("colz")
sfphist.GetYaxis().SetMoreLogLabels()
sfphist.GetYaxis().SetNoExponent()
sfphist.Draw("colz")
sfphist.GetYaxis().CenterTitle()
sfphist.GetYaxis().SetTitleOffset(1.4)
c.Print("SFPlot/photonsf.pdf")

sfphist.SetMarkerSize(1.5)
gStyle.SetPaintTextFormat("3.2f")
sfphist.Draw("TEXT same")
c.Print("SFPlot/photonsftext.pdf")





fout.Close()
