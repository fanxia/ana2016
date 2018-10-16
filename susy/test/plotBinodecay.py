#!/bin/python
# 8.25.2017 by Fan Xia
# plot bino decay brs

import os
import sys
import ROOT
from ROOT import *
import math

#pdg2016
sw2=0.23129
cw2=1-sw2
mZ=91.1876


def fun1(x):
    mass=x[0]
    if mass<mZ: br=1.0
    else:br= cw2/(cw2+sw2*(1.-mZ**2/mass**2)**4)
    return br

def fun2(x):
    mass=x[0]
    if mass<mZ: br=0.0
    else: br= 1.-cw2/(cw2+sw2*(1.-mZ**2/mass**2)**4)
    return br


p1=ROOT.TF1("Bino Decays",fun1,0,1000)
p2=ROOT.TF1("p2",fun2,0,1000)
l1=ROOT.TLine(0,cw2,1000,cw2)
l2=ROOT.TLine(0,sw2,1000,sw2)
t1=ROOT.TPaveText(0.25,0.65,0.35,0.7,"NDC")
t2=ROOT.TPaveText(0.25,0.3,0.35,0.35,"NDC")
t3=ROOT.TPaveText(0.6,0.6,0.7,0.7,"NDC")
t4=ROOT.TPaveText(0.6,0.30,0.7,0.40,"NDC")
t1.SetFillColor(0)
t2.SetFillColor(0)
t3.SetFillColor(0)
t4.SetFillColor(0)
t1.AddText("Cos^{2}#theta_{w}")
t1.SetTextColor(kRed)
t2.AddText("Sin^{2}#theta_{w}")
t2.SetTextColor(kBlue)
t3.AddText("#gamma+#tilde{G}")
t3.SetTextColor(kRed)
t4.AddText("Z+#tilde{G}")
t4.SetTextColor(kBlue)

l1.SetLineStyle(2)
l1.SetLineColor(kRed)
l2.SetLineStyle(2)
l2.SetLineColor(kBlue)

c=ROOT.TCanvas("c","c",600,500)
#c.cd()
p1.SetTitle("Bino Decays;M_{#tilde{B}};B.R.")
p1.GetYaxis().CenterTitle(True)
p1.GetXaxis().CenterTitle(True)
p1.SetLineColor(kRed)
p1.GetXaxis().SetNdivisions(505)
p1.SetMaximum(1.02)
p1.SetMinimum(-0.02)
p2.SetMaximum(1.02)
p2.SetMinimum(-0.02)
p2.SetLineColor(kBlue)
p1.Draw()
p2.Draw("SAME")
l1.Draw("same")
l2.Draw("same")
t1.Draw("same")
t2.Draw("same")
t3.Draw("same")
t4.Draw("same")
c.Print("binobr.pdf")
