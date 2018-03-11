#! /usr/bin/env python
from ROOT import *
import ROOT
from array import array
import sys
import os



#fin=TFile("../script/lepgammaSF/MuonHLTEffi_RunB2F.root")
fin=TFile("../script/lepgammaSF/MuonHLTEffi_RunGH.root")

ratiohist=fin.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio")
ratiohist.Sumw2()

dthist=fin.Get("IsoMu24_OR_IsoTkMu24_PtEtaBins/efficienciesDATA/abseta_pt_DATA")
dthist.SetTitle("SingleMU HLT efficiency of 2016 RunGH data                      ;|#eta|;P_{T} (GeV/c)")
dthist.SetMinimum(0.7)
#dthist.GetYaxis().SetRangeUser(30,500)
#dthist.GetXaxis().SetRangeUser(-2.1,2.1)

ratiohist.SetTitle("SingleMU HLT scale factor of 2016 RunGH: Data/MC                       ;|#eta|;P_{T} (GeV/c)")
#ratiohist.GetYaxis().SetRangeUser(30,500)
#ratiohist.GetXaxis().SetRangeUser(-2.1,2.1)

#mchist.SetTitle("efficiency mc;|sc_#eta|;P_{T } (GeV/c)")
#dthist.Write()
#mchist.Write()
#ratiohist.Write()


###########################plot part#####################
os.system("mkdir cutAcountPlot")
c=ROOT.TCanvas("c","Plots",1100,1000)
gStyle.SetOptStat(0)
c.SetRightMargin(0.14)
gPad.SetLogy()
dthist.Draw("colz")
dthist.GetYaxis().SetMoreLogLabels()
dthist.GetYaxis().SetNoExponent()
dthist.Draw("colz")
dthist.GetYaxis().CenterTitle()
dthist.GetYaxis().SetTitleOffset(1.4)
dthist.GetZaxis().SetTitle("")
dthist.SetTitleSize(0.035,"XYZ")
dthist.SetTitleFont(42,"XYZ")
dthist.SetLabelFont(42,"XYZ")
dthist.SetLabelSize(0.035,"XYZ")
dthist.SetMarkerSize(1.5)
c.Update()
c.Print("cutAcountPlot/stackeffdata.pdf")

gStyle.SetPaintTextFormat("3.2f")
dthist.Draw("TEXT same")
c.Print("cutAcountPlot/stackeffdatatext.pdf")

#c.Clear()
#mchist.Draw("colz")
#mchist.GetYaxis().SetMoreLogLabels()
#mchist.GetYaxis().SetNoExponent()
#mchist.GetYaxis().CenterTitle()
#mchist.Draw("colz")
#mchist.GetYaxis().SetTitleOffset(1.2)
#c.Print("cutAcountPlot/stackeffmc.pdf")
#mchist.Draw("TEXT same")
#c.Print("cutAcountPlot/stackeffmctext.pdf")


c.Clear()
ratiohist.Draw("colz")
ratiohist.GetYaxis().SetMoreLogLabels()
ratiohist.GetYaxis().SetNoExponent()
ratiohist.GetYaxis().CenterTitle()
ratiohist.Draw("colz")
ratiohist.GetYaxis().SetTitleOffset(1.4)
ratiohist.GetZaxis().SetTitle("")
ratiohist.SetTitleSize(0.035,"XYZ")
ratiohist.SetTitleFont(42,"XYZ")
ratiohist.SetLabelFont(42,"XYZ")
ratiohist.SetLabelSize(0.035,"XYZ")
ratiohist.SetMarkerSize(1.5)
c.Update()
c.Print("cutAcountPlot/stacksf.pdf")

gStyle.SetPaintTextFormat("3.2f")
ratiohist.Draw("TEXT same")
c.Print("cutAcountPlot/stacksftext.pdf")

# colorid=[kRed,kBlue,kYellow,kGreen+3,kOrange,kGray,kRed+2,kBlue+2,kYellow+3,kGreen+1]
# titles=["SingleEle HLT eff for data","SingleEle HLT eff for mc","SingleEle HLT SF: Data/MC"]
# titleID=0
# gPad.SetLogy(0)
# for plothist in [dthist,mchist,ratiohist]:
#     hs=ROOT.THStack("hs","hs")
#     leg=ROOT.TLegend(0.6,0.45,0.86,0.65) 
#     c.Clear()
#     for xid in range(1,len(binx)):

#         legname="|sc#eta| "+str(binx[xid-1])+"~"+str(binx[xid])
#         histy=TH1F("histy","histy",len(biny)-1,array('d',biny))
#         for yid in range(1,len(biny)):
#             histy.SetBinContent(yid,plothist.GetBinContent(xid,yid))
#             histy.SetBinError(yid,plothist.GetBinError(xid,yid))
#         histy.SetLineColor(colorid[xid-1])
#         histy.SetLineWidth(2)
#         histy.SetStats(0)
        
#         hs.Add(histy)
#         leg.AddEntry(histy,legname,"l")

#     hs.Draw()
#     hs.GetXaxis().SetMoreLogLabels()
#     hs.GetXaxis().SetNoExponent()
#     hs.SetTitle(titles[titleID]+"; Pt/GeV")
# #hs.GetXaxis().SetRangeUser(20,100)
#     if titleID==2: hs.SetMaximum(1.2)
#     gPad.SetLogx()
#     hs.Draw("nostack,elp")
#     leg.Draw()
#     c.Print("cutAcountPlot/stackeff"+str(titleID)+".pdf")
#     titleID+=1










# fout.Close()


