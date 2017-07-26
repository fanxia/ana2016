# To calculate the acceptance for signal mc
import math,sys
import ROOT
import time
import datetime
from ROOT import *
from array import array
import os, string, math


##############################################################################################
#############cuts definition, make sure consistent with plots' cuts###########################
##############################################################################################

cut_pre_ebjj="Bnbjet>0 && BelePt>35 " # add it yourself                                                                         
cut_SR1_ebjj="(Bnbjet>0 && BnPho==1 && BelePt>35)*BphoWeight " # add it yourself                                               
cut_SR1_ebjj_4gamma="(BelePt>35 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1)*BphoWeight" # add it yourself                   
cut_SR2_ebjj="(BelePt>35 && Bnbjet>0 && BnPho>1)*BphoWeight" # add it yourself                                                  
cut_CR1_ebjj="BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1" # add it yourself                                                 
cut_CR1_ebjj_4fake="(BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake==1 && BCandPhoTag>>0&1==1)" # add it yourself                  
cut_CR2_ebjj="BelePt>35 && Bnbjet>0 && BnPho==0 && BnFake>1" # add it yourself                                                   

cut_pre_ejjj="BelePt>35 && Bnjet>2 && BelePt>35" # add it yourself                                                              
cut_SR1_ejjj="(BelePt>35 && BnPho==1)*BphoWeight" # add it yourself                                                             
cut_SR2_ejjj="(BelePt>35 && BnPho>1)*BphoWeight" # add it yourself                                                              
cut_CR1_ejjj="BelePt>35 && BnPho==0 && BnFake==1" # add it yourself                                                             
cut_CR2_ejjj="BelePt>35 && BnPho==0 && BnFake>1" # add it yourself                                                              

#******************************************************************************
cut_pre_mbjj="Bnbjet>0 && BmuPt>30 " # add it yourself
cut_SR1_mbjj="(Bnbjet>0 && BnPho==1 && BmuPt>30)*BphoWeight " # add it yourself
cut_SR1_mbjj_4gamma="(BmuPt>30 && Bnbjet>0 && BnPho==1 && BCandPhoTag>>3&1==1)*BphoWeight" # add it yourself
cut_SR2_mbjj="(BmuPt>30 && Bnbjet>0 && BnPho>1)*BphoWeight" # add it yourself
cut_CR1_mbjj="BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake==1" # add it yourself
cut_CR1_mbjj_4fake="(BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake==1 && BCandPhoTag>>0&1==1)" # add it yourself
cut_CR2_mbjj="BmuPt>30 && Bnbjet>0 && BnPho==0 && BnFake>1" # add it yourself

cut_pre_mjjj="BmuPt>30 && Bnjet>2 && BmuPt>30" # add it yourself
cut_SR1_mjjj="(BmuPt>30 && BnPho==1)*BphoWeight" # add it yourself
cut_SR2_mjjj="(BmuPt>30 && BnPho>1)*BphoWeight" # add it yourself
cut_CR1_mjjj="BmuPt>30 && BnPho==0 && BnFake==1" # add it yourself
cut_CR2_mjjj="BmuPt>30 && BnPho==0 && BnFake>1" # add it yourself

Ration_MuA=19.714/35.86
Ration_MuB=16.146/35.86
  
##############################################################################################
##############################################################################################

#****************Func get weighted entries from a tree**********
def Fun_passN(channel,tree,mst,mnlsp,cuts=""):
      if channel=="ELE":
            cutextra_ele="(BlheStopMass=={0} && BlheNLSPMass=={1})*BeleWeight*Bnlspdecayweight*BpileupWeight*BbtagWeight".format(mst,mnlsp)
            tree.Draw("BnVtx>>h0",cutextra_ele+"*("+cuts+")")
            result=h0.Integral()
      elif channel=="MU":
            cutextra_muA="(BlheStopMass=={0} && BlheNLSPMass=={1})*BmuWeight1*Bnlspdecayweight*BpileupWeight*BbtagWeight".format(mst,mnlsp) 
            cutextra_muB="(BlheStopMass=={0} && BlheNLSPMass=={1})*BmuWeight2*Bnlspdecayweight*BpileupWeight*BbtagWeight".format(mst,mnlsp) 
    
            tree.Draw("BnVtx>>h1",cutextra_muA+"*("+cuts+")")
            tree.Draw("Brho>>h2",cutextra_muB+"*("+cuts+")")
            result=Ration_MuA*h1.Integral()+Ration_MuB*h2.Integral()
      return result

#****************Func plot 2d tgraph****************************
def Fun_plot2DGraph(graph,name,title,zmax,zmin,xtitle,ytitle,logz=0, text=""):
      c=ROOT.TCanvas("c","c",1000,800);
      c.SetRightMargin(0.12)
      gStyle.SetPalette(1)
      virtualLineA = ROOT.TLine(300, 300, 1400, 1400);
      virtualLineA.SetLineStyle(2);
      virtualLineA.SetLineWidth(2);
      nlspCommentA = ROOT.TLatex(650, 670, "m_{ #tilde{t}} < m_{ Bino}");
      nlspCommentA.SetTextAngle(40);
      nlspCommentA.SetTextSize(0.025);
      # top mass=172
      virtualLineB = ROOT.TLine(300, 128, 1500, 1328);
      virtualLineB.SetLineStyle(2);
      virtualLineB.SetLineWidth(2);
      nlspCommentB = ROOT.TLatex(650, 500, "m_{ #tilde{t}} < m_{ Bino}+m_{ t}");
      nlspCommentB.SetTextAngle(35);
      nlspCommentB.SetTextSize(0.025);

      comment = ROOT.TLatex(400, 1000, text);
#      comment.SetTextAngle(40);
      comment.SetTextSize(0.05);



      graph.SetTitle(title)
      graph.SetMaximum(zmax)
      graph.SetMinimum(zmin)
      graph.GetXaxis().SetTitle(xtitle)
      graph.GetXaxis().SetLabelSize(0.025)
      graph.GetYaxis().SetLabelSize(0.025)
      graph.GetZaxis().SetLabelSize(0.03)
      graph.GetYaxis().SetTitle(ytitle)
      graph.GetYaxis().SetTitleOffset(1.3)
      graph.Draw("colz")
      graph.Write(name)
      gPad.SetLogz(logz)

      virtualLineA.Draw("same")
      virtualLineB.Draw("same")
      nlspCommentA.Draw("same")
      nlspCommentB.Draw("same")
      comment.Draw("same")
      c.Print("sigAcc/"+name+".pdf")
#***************************************************************

###------------find stop xsec from .dat file-------------------
stopxsfile="sigxsec/stop_pair_13TeVxs.dat"
stopxslist=[[float(element) for element in line.strip().split()] for line in open(stopxsfile).read().strip().split('\n')]
stopxsdic={i[0]:i[1:] for i in stopxslist}



#H_sigscan=ROOT.TH2D("H_sigscan","H_sigscan",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp  


INPUTFile=sys.argv[1]
file_in=TFile.Open(INPUTFile)
os.system('mkdir sigAcc')
file_out=TFile("sigAcc/Acceptance_"+sys.argv[2]+".root","recreate")

Gr2D_sigscan=ROOT.TGraph2D()
Gr2D_sigxsec=ROOT.TGraph2D()
Gr2D_ELE_pre_bjj_Acc=ROOT.TGraph2D()   #ele
Gr2D_ELE_SR1_bjj_Acc=ROOT.TGraph2D()   #ele
Gr2D_ELE_SR2_bjj_Acc=ROOT.TGraph2D()   #ele

Gr2D_MU_pre_bjj_Acc=ROOT.TGraph2D()    #muon
Gr2D_MU_SR1_bjj_Acc=ROOT.TGraph2D()    #muon
Gr2D_MU_SR2_bjj_Acc=ROOT.TGraph2D()    #muon

Gr2D_pre_bjj_Acc=ROOT.TGraph2D()    #ele+muon
Gr2D_SR1_bjj_Acc=ROOT.TGraph2D()    #ele+muon
Gr2D_SR2_bjj_Acc=ROOT.TGraph2D()    #ele+muon



H2D_ELE_pre_bjj_passN=ROOT.TH2D("H2D_ELE_pre_bjj_passN","H2D_ELE_pre_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 
H2D_ELE_SR1_bjj_passN=ROOT.TH2D("H2D_ELE_SR1_bjj_passN","H2D_ELE_SR1_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 
H2D_ELE_SR2_bjj_passN=ROOT.TH2D("H2D_ELE_SR2_bjj_passN","H2D_ELE_SR2_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 

H2D_MU_pre_bjj_passN=ROOT.TH2D("H2D_MU_pre_bjj_passN","H2D_MU_pre_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 
H2D_MU_SR1_bjj_passN=ROOT.TH2D("H2D_MU_SR1_bjj_passN","H2D_MU_SR1_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 
H2D_MU_SR2_bjj_passN=ROOT.TH2D("H2D_MU_SR2_bjj_passN","H2D_MU_SR2_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 

H2D_pre_bjj_passN=ROOT.TH2D("H2D_pre_bjj_passN","H2D_pre_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 
H2D_SR1_bjj_passN=ROOT.TH2D("H2D_SR1_bjj_passN","H2D_SR1_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 
H2D_SR2_bjj_passN=ROOT.TH2D("H2D_SR2_bjj_passN","H2D_SR2_bjj_passN",1240,280.5,1520.5,1420,0.5,1420.5) #x:stop, y:nlsp 


print "input: ",INPUTFile
print "output: ","Acceptance_"+sys.argv[2]+".root"

H_sigscan=file_in.Get("H_sigscan").Clone()
EleTree=file_in.Get("EventTree_ele")
MuTree=file_in.Get("EventTree_mu")


scanpoints=[]
for x in range(300,1501):
    for y in range(10,1401):
        scanNumber=H_sigscan.GetBinContent(H_sigscan.FindBin(x,y))
        if scanNumber>0:
            xsec=stopxsdic[x]
            scanpoints.append([x,y,scanNumber,xsec[0]])

Ind=0
for point in scanpoints:
    Mst=point[0]
    Mnlsp=point[1]
    Gr2D_sigscan.SetPoint(ind,Mst,Mnlsp,point[2])
    Gr2D_sigxsec.SetPoint(ind,Mst,Mnlsp,point[3])

#    cutextra_ele="(BlheStopMass=={0} && BlheNLSPMass=={1})*BeleWeight*Bnlspdecayweight*BpileupWeight*BbtagWeight".format(Mst,Mnlsp)
#    cutextra_muA="(BlheStopMass=={0} && BlheNLSPMass=={1})*BmuWeight1*Bnlspdecayweight*BpileupWeight*BbtagWeight".format(Mst,Mnlsp) 
#    cutextra_muB="(BlheStopMass=={0} && BlheNLSPMass=={1})*BmuWeight2*Bnlspdecayweight*BpileupWeight*BbtagWeight".format(Mst,Mnlsp) 
    
    ELE_pre_bjj_passN=Fun_passN("ELE",EleTree,Mst,Mnlsp,cut_pre_ebjj)
    ELE_SR1_bjj_passN=Fun_passN("ELE",EleTree,Mst,Mnlsp,cut_SR1_ebjj)
    ELE_SR2_bjj_passN=Fun_passN("ELE",EleTree,Mst,Mnlsp,cut_SR2_ebjj)

    MU_pre_bjj_passN=Fun_passN("MU",MuTree,Mst,Mnlsp,cut_pre_mbjj)
    MU_SR1_bjj_passN=Fun_passN("MU",MuTree,Mst,Mnlsp,cut_SR1_mbjj)
    MU_SR2_bjj_passN=Fun_passN("MU",MuTree,Mst,Mnlsp,cut_SR2_mbjj)

    pre_bjj_passN=ELE_pre_bjj_passN+MU_pre_bjj_passN
    SR1_bjj_passN=ELE_SR1_bjj_passN+MU_SR1_bjj_passN
    SR2_bjj_passN=ELE_SR2_bjj_passN+MU_SR2_bjj_passN


    H2D_ELE_pre_bjj_passN.SetBinContent(H2D_ELE_pre_bjj_passN.FindBin(Mst,Mnlsp),ELE_pre_bjj_passN)
    H2D_ELE_SR1_bjj_passN.SetBinContent(H2D_ELE_SR1_bjj_passN.FindBin(Mst,Mnlsp),ELE_SR1_bjj_passN)
    H2D_ELE_SR2_bjj_passN.SetBinContent(H2D_ELE_SR2_bjj_passN.FindBin(Mst,Mnlsp),ELE_SR2_bjj_passN)

    H2D_MU_pre_bjj_passN.SetBinContent(H2D_MU_pre_bjj_passN.FindBin(Mst,Mnlsp),MU_pre_bjj_passN)
    H2D_MU_SR1_bjj_passN.SetBinContent(H2D_MU_SR1_bjj_passN.FindBin(Mst,Mnlsp),MU_SR1_bjj_passN)
    H2D_MU_SR2_bjj_passN.SetBinContent(H2D_MU_SR2_bjj_passN.FindBin(Mst,Mnlsp),MU_SR2_bjj_passN)

    H2D_pre_bjj_passN.SetBinContent(H2D_pre_bjj_passN.FindBin(Mst,Mnlsp),pre_bjj_passN)
    H2D_SR1_bjj_passN.SetBinContent(H2D_SR1_bjj_passN.FindBin(Mst,Mnlsp),SR1_bjj_passN)
    H2D_SR2_bjj_passN.SetBinContent(H2D_SR2_bjj_passN.FindBin(Mst,Mnlsp),SR2_bjj_passN)

    Gr2D_ELE_pre_bjj_Acc.SetPoint(ind,Mst,Mnlsp,ELE_pre_bjj_passN/point[2])    
    Gr2D_ELE_SR1_bjj_Acc.SetPoint(ind,Mst,Mnlsp,ELE_SR1_bjj_passN/point[2])   
    Gr2D_ELE_SR2_bjj_Acc.SetPoint(ind,Mst,Mnlsp,ELE_SR2_bjj_passN/point[2])

    Gr2D_MU_pre_bjj_Acc.SetPoint(ind,Mst,Mnlsp,MU_pre_bjj_passN/point[2])    
    Gr2D_MU_SR1_bjj_Acc.SetPoint(ind,Mst,Mnlsp,MU_SR1_bjj_passN/point[2])   
    Gr2D_MU_SR2_bjj_Acc.SetPoint(ind,Mst,Mnlsp,MU_SR2_bjj_passN/point[2])

    Gr2D_pre_bjj_Acc.SetPoint(ind,Mst,Mnlsp,pre_bjj_passN/point[2])    
    Gr2D_SR1_bjj_Acc.SetPoint(ind,Mst,Mnlsp,SR1_bjj_passN/point[2])   
    Gr2D_SR2_bjj_Acc.SetPoint(ind,Mst,Mnlsp,SR2_bjj_passN/point[2])

    
    ind+=1


Fun_plot2DGraph(graph=Gr2D_sigscan,name="Gr2D_sigscan",title="SMS-T6ttZg scan",zmax=60000,zmin=0,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0)
Fun_plot2DGraph(graph=Gr2D_sigxsec,name="Gr2D_sigxsec",title="Xsec[pb]",zmax=10,zmin=0.00008,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=1)

Fun_plot2DGraph(graph=Gr2D_ELE_pre_bjj_Acc,name="Gr2D_ELE_pre_bjj_Acc",title="SMS-T6ttZg",zmax=0.05,zmin=0.02,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{#it{e}_bjj pre-selection}{ Acceptance*#varepsilon}")
Fun_plot2DGraph(graph=Gr2D_ELE_SR1_bjj_Acc,name="Gr2D_ELE_SR1_bjj_Acc",title="SMS-T6ttZg",zmax=0.023,zmin=0.01,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{    #it{e}_bjj SR1}{Acceptance*#varepsilon}")
Fun_plot2DGraph(graph=Gr2D_ELE_SR2_bjj_Acc,name="Gr2D_ELE_SR2_bjj_Acc",title="SMS-T6ttZg",zmax=0.017,zmin=0.002,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{    #it{e}_bjj SR2}{Acceptance*#varepsilon}")

Fun_plot2DGraph(graph=Gr2D_MU_pre_bjj_Acc,name="Gr2D_MU_pre_bjj_Acc",title="SMS-T6ttZg",zmax=0.05,zmin=0.02,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{#mu_bjj pre-selection}{ Acceptance*#varepsilon}")
Fun_plot2DGraph(graph=Gr2D_MU_SR1_bjj_Acc,name="Gr2D_MU_SR1_bjj_Acc",title="SMS-T6ttZg",zmax=0.025,zmin=0.01,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{    #mu_bjj SR1}{Acceptance*#varepsilon}")
Fun_plot2DGraph(graph=Gr2D_MU_SR2_bjj_Acc,name="Gr2D_MU_SR2_bjj_Acc",title="SMS-T6ttZg",zmax=0.018,zmin=0.003,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{    #mu_bjj SR2}{Acceptance*#varepsilon}")

Fun_plot2DGraph(graph=Gr2D_pre_bjj_Acc,name="Gr2D_pre_bjj_Acc",title="SMS-T6ttZg",zmax=0.095,zmin=0.045,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{(#it{e}+#mu)_bjj pre-selection}{ Acceptance*#varepsilon}")
Fun_plot2DGraph(graph=Gr2D_SR1_bjj_Acc,name="Gr2D_SR1_bjj_Acc",title="SMS-T6ttZg",zmax=0.05,zmin=0.02,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{    (#it{e}+#mu)_bjj SR1}{Acceptance*#varepsilon}")
Fun_plot2DGraph(graph=Gr2D_SR2_bjj_Acc,name="Gr2D_SR2_bjj_Acc",title="SMS-T6ttZg",zmax=0.033,zmin=0.006,xtitle="m_{ #tilde{t}} (GeV/c^{2})",ytitle="m_{ #tilde{#chi_{1}^{0}}} (GeV/c^{2})",logz=0,text="#splitline{    (#it{e}+#mu)_bjj SR2}{Acceptance*#varepsilon}")

file_out.Write()
file_out.Close()

