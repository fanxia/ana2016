#!/usr/bin/env python
#./filesHadder.py Mar08
import os, re
import commands
import sys
import math

date=sys.argv[1]
#MClist=['TTJets_DiLept','TTJets_SingleLeptFromT','TTJets_SingleLeptFromTbar']
#MClist=['TT','TTGJets','TTWJetsToLNu','TTWJetsToQQ','TTZToLLNuNu','TTZToQQ','W4JetsToLNu','DYJetsToLL','WGToLNuG','WW','WZ','ZGTo2LG','ZZ','ST_s-channel_4f_leptonDecays','ST_tW_antitop_5f_inclusiveDecays','ST_tW_top_5f_inclusiveDecays','ST_t-channel_antitop_4f_inclusiveDecays','ST_t-channel_top_4f_inclusiveDecays','W3JetsToLNu','W2JetsToLNu']
MClist=[]

#EleDatalist=['SingleEle_Run2016B_FebReminiAOD','SingleEle_Run2016C_FebReminiAOD','SingleEle_Run2016D_FebReminiAOD','SingleEle_Run2016E_FebReminiAOD','SingleEle_Run2016F_FebReminiAOD1','SingleEle_Run2016F_FebReminiAOD2','SingleEle_Run2016G_FebReminiAOD','SingleEle_Run2016H_FebReminiAODv2','SingleEle_Run2016H_FebReminiAODv3']
EleDatalist=[]

#MuDatalist=['SingleMu_Run2016B_FebReminiAOD','SingleMu_Run2016C_FebReminiAOD','SingleMu_Run2016D_FebReminiAOD','SingleMu_Run2016E_FebReminiAOD','SingleMu_Run2016F_FebReminiAOD1','SingleMu_Run2016F_FebReminiAOD2','SingleMu_Run2016G_FebReminiAOD','SingleMu_Run2016H_FebReminiAODv2','SingleMu_Run2016H_FebReminiAODv3']
#MuDatalist=['SingleMu_Run2016B_FebReminiAOD']

MuDatalist=['SingleMu_Run2016B_FebReminiAOD00','SingleMu_Run2016B_FebReminiAOD01','SingleMu_Run2016B_FebReminiAOD02','SingleMu_Run2016C_FebReminiAOD','SingleMu_Run2016D_FebReminiAOD','SingleMu_Run2016E_FebReminiAOD','SingleMu_Run2016F_FebReminiAOD1','SingleMu_Run2016F_FebReminiAOD2','SingleMu_Run2016G_FebReminiAOD00','SingleMu_Run2016G_FebReminiAOD01','SingleMu_Run2016H_FebReminiAODv200','SingleMu_Run2016H_FebReminiAODv201','SingleMu_Run2016H_FebReminiAODv3']

#MuDatalist=[]

# hadd step1 mc outputs and mv it to ntupleStore/ 
for mc in MClist:
    os.system("hadd -k step1_{0}.root MC_Out_step1/{0}/ana_root{1}/step1*.root".format(mc,date))
    os.system("mv step1_{0}.root ../../ntupleStore".format(mc))

#sys.exit()

for Eledata in EleDatalist:
    os.system("hadd -k -f step1_{0}.root Data_Out_step1/{0}/ana_root{1}/step1*.root".format(Eledata,date))
    os.system("mv step1_{0}.root ../../ntupleStore".format(Eledata))

#sys.exit()

for Mudata in MuDatalist:
    os.system("hadd -k -f step1_{0}.root Data_Out_step1/{0}*/ana_root{1}/step1*.root".format(Mudata,date))
    os.system("mv step1_{0}.root ../../ntupleStore".format(Mudata))
