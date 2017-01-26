#!/usr/bin/env python
import os, re
import commands
import sys
import math

#MClist=['TT_powheg','WJetsToLNu','DYLL','WW','WZ','Wg_MG','Zg_aMCatNLO']
MClist=['TT_powheg','TTGJets','TTZToQQ','TTZToLLNuNu','TTWJetsToLNu','TTWJetsToQQ','WJetsToLNu','WW','WZ','ZZ','ZGTo2LG','WGToLNuG','ST_s-channel_4f_leptonDecays','ST_t-channel_antitop_4f_leptonDecays','ST_t-channel_top_4f_leptonDecays','ST_tW_antitop_5f_inclus','ST_tW_top_5f_inclus']
#MClist=[]
#MClist=['WZ','Wg_MG','Zg_aMCatNLO']
#EleDatalist=['SingleEle_Run2016C_SepRereco','SingleEle_Run2016D_SepRereco','SingleEle_Run2016E_SepRereco','SingleEle_Run2016H_PRv3']
EleDatalist=['SingleEle_Run2016B_sepRereco0','SingleEle_Run2016B_sepRereco1','SingleEle_Run2016B_sepRereco2','SingleEle_Run2016C_SepRereco','SingleEle_Run2016D_SepRereco']
#EleDatalist=[]

# hadd step1 mc outputs and mv it to ntupleStore/ 
for mc in MClist:
    os.system("hadd -k step1_{0}_miniIso.root MC_Out_step1/{0}/ana_rootJan26/step1*.root".format(mc))
    os.system("mv step1_{0}_miniIso.root ../../ntupleStore".format(mc))


for Eledata in EleDatalist:
    os.system("hadd -k -f step1_{0}_miniIso.root Data_Out_step1/{0}/ana_rootJan26/step1*.root".format(Eledata))
    os.system("mv step1_{0}_miniIso.root ../../ntupleStore".format(Eledata))
