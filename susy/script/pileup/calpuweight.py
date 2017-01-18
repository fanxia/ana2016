#!/bin/python
#this script to calculat the pileup weight
#data input is the data_true.root
#mc input is the pdf list

from ROOT import *
import ROOT
import sys

ddata=TFile.Open("pileup_2016data_final.root")
pileupdata=ddata.Get("pileup")
Ndata=pileupdata.Integral()
pileupdata.Scale(1.0/Ndata)

#this mc pu is for moriond17
mclist=[1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,0.000109362 ,0.000140973 ,0.000240998 ,0.00071209 ,0.00130121 ,0.00245255 ,0.00502589 ,0.00919534 ,0.0146697 ,0.0204126 ,0.0267586 ,0.0337697 ,0.0401478 ,0.0450159 ,0.0490577 ,0.0524855 ,0.0548159 ,0.0559937 ,0.0554468 ,0.0537687 ,0.0512055 ,0.0476713 ,0.0435312 ,0.0393107 ,0.0349812 ,0.0307413 ,0.0272425 ,0.0237115 ,0.0208329 ,0.0182459 ,0.0160712 ,0.0142498 ,0.012804 ,0.011571 ,0.010547 ,0.00959489 ,0.00891718 ,0.00829292 ,0.0076195 ,0.0069806 ,0.0062025 ,0.00546581 ,0.00484127 ,0.00407168 ,0.00337681 ,0.00269893 ,0.00212473 ,0.00160208 ,0.00117884 ,0.000859662 ,0.000569085 ,0.000365431 ,0.000243565 ,0.00015688 ,9.88128e-05 ,6.53783e-05 ,3.73924e-05 ,2.61382e-05 ,2.0307e-05 ,1.73032e-05 ,1.435e-05 ,1.36486e-05 ,1.35555e-05 ,1.37491e-05 ,1.34255e-05 ,1.33987e-05 ,1.34061e-05 ,1.34211e-05 ,1.34177e-05 ,1.32959e-05 ,1.33287e-05]


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
leg.AddEntry(pileupdata,"2016Data pu_true","l")
pileupmc.Draw("same")
pileupmc.SetLineColor(kBlue)
leg.AddEntry(pileupmc,"Moriond17MC pu_true","l")
leg.Draw()

c.Print("PUTrue-2016data_vs_Moriand17mc.pdf","pdf")

f.Close()
