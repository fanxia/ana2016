#!/bin/python
#this script to calculat the pileup weight
#data input is the data_true.root
#mc input is the pdf list

from ROOT import *
import ROOT
import sys

ddata=TFile.Open("SingleEle_Run2016BCD_pileup.root")
pileupdata=ddata.Get("pileup")
Ndata=pileupdata.Integral()
pileupdata.Scale(1.0/Ndata)

mclist=[0.000829312873542,
        0.00124276120498,
        0.00339329181587,
        0.00408224735376,
        0.00383036590008,
        0.00659159288946,
        0.00816022734493,
        0.00943640833116,
        0.0137777376066,
        0.017059392038,
        0.0213193035468,
        0.0247343174676,
        0.0280848773878,
        0.0323308476564,
        0.0370394341409,
        0.0456917721191,
        0.0558762890594,
        0.0576956187107,
        0.0625325287017,
        0.0591603758776,
        0.0656650815128,
        0.0678329011676,
        0.0625142146389,
        0.0548068448797,
        0.0503893295063,
        0.040209818868,
        0.0374446988111,
        0.0299661572042,
        0.0272024759921,
        0.0219328403791,
        0.0179586571619,
        0.0142926728247,
        0.00839941654725,
        0.00522366397213,
        0.00224457976761,
        0.000779274977993,
        0.000197066585944,
        7.16031761328e-05,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0]

log=open("puweight.txt","w")
f=TFile("pileup.root","recreate")
puweight=ROOT.TH1F("puweight","puweight",80,0,80)
pileupmc=ROOT.TH1F("pileupmc","pileupmc",80,0,80)
#pileupdata=ROOT.TH1F("pileupdata","pileupdata",50,0,50)
#pileupmc=ROOT.TH1F("pileupmc","pileupmc",50,0,50)

c=ROOT.TCanvas("c","Plots",1000,1000)
c.cd()
#gStyle.SetOptStat(0)
leg=ROOT.TLegend(0.6,0.8,0.9,0.9)


datalist=[]
#pileupdata.Draw()

for m in range(1,pileupdata.GetXaxis().GetNbins()+1):
    datalist.append(pileupdata.GetBinContent(m))

pileupdata.SetTitle("pileupdata")
pileupdata.Write()
log.write("INPUT data true pu %s\n"%datalist)


for i in range(1,pileupdata.GetXaxis().GetNbins()+1):
    if i>len(mclist): pileupmc.SetBinContent(i,0.)
    else:    pileupmc.SetBinContent(i,mclist[i-1])

pileupmc.Write()

puweight=pileupdata.Clone("weight")
puweight.Divide(pileupmc)

puweightlist=[]
for j in range(0,puweight.GetNbinsX()):
#    if mclist[j]!=0. and j+1>len(mclist): puweightlist.append(datalist[j]/mclist[j])
#    else: puweightlist.append(0.)
    puweightlist.append(puweight.GetBinContent(j+1))
puweight.Write()

log.write("pileweightlist: %s\n"%puweightlist)
log.close()

gStyle.SetOptStat(0)
pileupdata.Draw("hist")
pileupdata.SetTitle("pileupTrue")
pileupdata.SetLineColor(kBlack)
leg.AddEntry(pileupdata,"Data pu_true","l")
pileupmc.Draw("same")
pileupmc.SetLineColor(kBlue)
leg.AddEntry(pileupmc,"MC pu_true","l")
leg.Draw()

c.Print("PUTrue-dataBCD_vs_mc.pdf","pdf")

f.Close()
