#!/bin/python
# to run this script: python calBtagEff_step2.py inputdirname/ outputname

import os
import sys
import ROOT
from ROOT import *

INPUTDIR=sys.argv[1]
OutName=sys.argv[2]

os.system("hadd -fk "+OutName+"_BtagEff.root "+INPUTDIR+"*root")

#file_in=TFile.Open(OutName+"_BtagEff_step1.root")
#os.system("mv "+OutName+"_BtagEff_step1.root "+OutName+"_BtagEff.root")
file_out=TFile.Open(OutName+"_BtagEff.root","UPDATE")


lEff=file_out.Get("ltags").Clone("lEff")
lEff.Divide(file_out.Get("ljets"))

cEff=file_out.Get("ctags").Clone("cEff")
cEff.Divide(file_out.Get("cjets"))

bEff=file_out.Get("btags").Clone("bEff")
bEff.Divide(file_out.Get("bjets"))




file_out.Write()
file_out.Close()
