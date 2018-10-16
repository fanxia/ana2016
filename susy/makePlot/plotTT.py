import math, sys
import ROOT
from ROOT import *

fin=TFile.Open("../ntupleStore/step1p5_TT.root")
foutname="plotTT_out/"

Ele_cut_pre_bjj="(Bnbjet>0 && BelePt>35 )"
Ele_cut_SR1_bjj="(Bnbjet>0 && BnPho==1 && BelePt>35)"
Ele_cut_SR2_bjj="(Bnbjet>0 && BnPho>1 && BelePt>35)"
Ele_cut_CR1_bjj="(BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1)"
Ele_cut_CR2_bjj="(BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake>1)"


Mu_cut_pre_bjj="(Bnbjet>0 && BmuPt>30)"
Mu_cut_SR1_bjj="(Bnbjet>0 && BnPho==1 && BmuPt>30)"
Mu_cut_SR2_bjj="(Bnbjet>0 && BnPho>1 && BmuPt>30)"
Mu_cut_CR1_bjj="(BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake==1)"
Mu_cut_CR2_bjj="(BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake>1)"

def plotcomp(h1,h2,xtitle,ytitle,com,plotname):
    c1 = TCanvas("c1","c1", 800, 800)
    gPad.SetLogy(1)
    h1.Draw()
    h1.GetXaxis().SetTitleOffset(0.8)
#    h1.GetXaxis().SetRangeUser(0,xmax)
    h1.SetTitle(";"+xtitle+";"+ytitle)
    h1.SetMinimum(0.0)
    h1.SetMaximum(max(h1.GetMaximum(),h2.GetMaximum())*1.2)
        
    gStyle.SetOptStat(0)
    pad1=TPad("","",0,0.25,1,1)
    pad2=TPad("","",0,0.0,1,0.25)
#        pad2.SetTopMargin(0.05)
    pad1.Draw()
    pad2.Draw()


    regionComment=ROOT.TPaveText(0.55,0.55,0.85,0.65,"NDC")
    regionComment.SetFillColor(0)
    regionComment.SetFillStyle(0)
    regionComment.SetLineColor(0)
    regionComment.SetBorderSize(0)
    regionComment.AddText(com)

    pad1.cd()
    leg= TLegend(0.62,0.65,0.90,0.90,"","brNDC")
    leg.AddEntry(h1,"tt_powheg before Top pt reweighting","l")
    leg.AddEntry(h2,"tt_powheg after Top pt reweighting","l")

    h2.SetLineColor(kRed)
    h1.Draw("hist")
    h2.Draw("hist same")
    regionComment.Draw("same")
    leg.Draw("same")

    pad2.cd()
    gStyle.SetOptStat(0)
    hratio=h2.Clone("hratio")
    hratio.Divide(h1)
    hratio.SetTitle(";;after/before    ")
    hratio.GetXaxis().SetTitle("")
    hratio.GetYaxis().SetTitleOffset(0.5)
    hratio.GetXaxis().SetTitleOffset(2)
    hratio.SetMaximum(1.5)
    hratio.SetMinimum(0.5)

    hline=hratio.Clone("hline")
    for ii in range(hline.GetNbinsX()+1): 
                hline.SetBinContent(ii,1.0)
                hline.SetBinError(ii,0.0)
    hline.SetLineColor(kBlack)
    pad2.Clear()
    hline.SetStats(0)
    hline.Draw()
    hratio.SetStats(0)
    hratio.Draw("e,same")

#    hratio.Fit("pol0")
    c1.Print(foutname+plotname+".pdf")
    c1.Clear()
#    ratio=hratio.GetFunction("pol0").GetParameter(0)
#    ratioErr=hratio.GetFunction("pol0").GetParError(0)


# plot ttbar Njets before and after top pt reweighting
tr=fin.Get("EventTree_ele")
tr.Draw("Bnjet>>hbef(12,3,15)",Ele_cut_pre_bjj,"")
tr.Draw("Bnjet>>haft(12,3,15)",Ele_cut_pre_bjj+"*BtopPtWeight","")
plotcomp(hbef,haft,"Njets","","ELE pre","Pre_ELE_Njets_TT")

# tr.Draw("BHT>>hbefht(150,0,1500)",Ele_cut_pre_bjj,"")
# tr.Draw("BHT>>haftht(150,0,1500)",Ele_cut_pre_bjj+"*BtopPtWeight","")

# plotcomp(hbefht,haftht,"HT","","ELE pre","Pre_ELE_HT_TT")


# mtr=fin.Get("EventTree_mu")
# mtr.Draw("Bnjet>>mhbef(12,3,15)",Mu_cut_pre_bjj,"")
# mtr.Draw("Bnjet>>mhaft(12,3,15)",Mu_cut_pre_bjj+"*BtopPtWeight","")
# plotcomp(mhbef,mhaft,"Njets","","MU pre","Pre_MU_Njets_TT")

# mtr.Draw("BHT>>mhbefht(150,0,1500)",Mu_cut_pre_bjj,"")
# mtr.Draw("BHT>>mhaftht(150,0,1500)",Mu_cut_pre_bjj+"*BtopPtWeight","")
# plotcomp(mhbefht,mhaftht,"HT","","MU pre","Pre_MU_HT_TT")



# plot ttbar HT before and after top pt reweighting   


