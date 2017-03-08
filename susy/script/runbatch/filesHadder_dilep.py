#!/usr/bin/env python
import os, re
import commands
import sys
import math


MClist=['TTGG','TTGJets']
#MClist=['WZ','Wg_MG','Zg_aMCatNLO']
EleDatalist=[]
#EleDatalist=['SingleEle_Run2016B_FebReminiAOD','SingleEle_Run2016C_FebReminiAOD','SingleEle_Run2016D_FebReminiAOD','SingleEle_Run2016E_FebReminiAOD','SingleEle_Run2016F_FebReminiAOD1','SingleEle_Run2016F_FebReminiAOD2','SingleEle_Run2016G_FebReminiAOD','SingleEle_Run2016H_FebReminiAODv2','SingleEle_Run2016H_FebReminiAODv3']
# hadd step1 mc outputs and mv it to ntupleStore/ 
for mc in MClist:
    os.system("hadd -k step1_{0}_dilep.root MC_dilepOut_step1/{0}/dilepana_rootMar07/step1*.root".format(mc))
    os.system("mv step1_{0}_dilep.root ../../ntupleStore".format(mc))


for Eledata in EleDatalist:
    os.system("hadd -k -f step1_{0}_dilep.root Data_dilepOut_step1/{0}/dilepana_rootMar06/step1*.root".format(Eledata))
    os.system("mv step1_{0}_dilep.root ../../ntupleStore".format(Eledata))
