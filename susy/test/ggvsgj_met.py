from ROOT import *  
f1=TFile("../ntupleStore/step1p5_TTGJets.root")
f2=TFile("../ntupleStore/step1p5_TTGG.root")
t1=f1.Get("EventTree_ele")
t2=f2.Get("EventTree_ele")
c1=TCanvas()
c1.SetLogy()
gStyle.SetOptStat(000000)
t1.Draw("BpfMET>>h1(100,0,1000)","Bnbjet>0&&BelePt>35")
t2.Draw("BpfMET>>h2(100,0,1000)","Bnbjet>0&&BelePt>35")
h1.Scale(1/h1.Integral())
h2.Scale(1/h2.Integral())
h1.SetLineColor(2)
t1.Draw("BpfMET>>h1s(100,0,1000)","(Bnbjet>0&&BelePt>35&&BnPho==1)*BphoWeight")
t2.Draw("BpfMET>>h2s(100,0,1000)","(Bnbjet>0&&BelePt>35&&BnPho==1)*BphoWeight")
h1s.Scale(1/h1s.Integral())
h2s.Scale(1/h2s.Integral())
h1s.SetLineColor(2)
t2.Draw("BpfMET>>h2s2(100,0,1000)","(Bnbjet>0&&BelePt>35&&BnPho>1)*BphoWeight")
t1.Draw("BpfMET>>h1s2(100,0,1000)","(Bnbjet>0&&BelePt>35&&BnPho>1)*BphoWeight")
h1s2.SetLineColor(2)
h1s2.Scale(1/h1s2.Integral())
h2s2.Scale(1/h2s2.Integral())

lg=TLegend(.7,.7,.9,.9)
lg.AddEntry(h1s2,"TTGJets")
lg.AddEntry(h2s2,"TTGG")
h1s2.SetTitle("MET in SR2;MET [GeV]")
h1s2.Draw()
h2s2.Draw('same')
lg.Draw("same")
c1.Print("sr2_ggvsgj.png")
h1s.SetTitle("MET in SR;MET [GeV]")
h1s.Draw()
h2s.Draw('same')
lg.Draw("same")
c1.Print("sr_ggvsgj.png")
h1.SetTitle("MET in pre-region;MET [GeV]")
h1.Draw()
h2.Draw('same')
lg.Draw("same")
c1.Print("pr_ggvsgj.png")


