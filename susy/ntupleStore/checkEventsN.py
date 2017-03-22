#!/usr/bin/env python
#check the total events numbers, especially for data

import os
import sys
from ROOT import *
from commands import getoutput


filelist=getoutput('ls step1_*.root').split('\n')
#print filelist

for f in filelist:
    fl=TFile.Open(f)
    if "dilep" in f:
        h=fl.Get("H_ee")
    else: h=fl.Get("H_ele")
    ev=h.GetBinContent(1)
    print "*********************************************"
    print f
    print "The total processed events number in this file is ", ev
