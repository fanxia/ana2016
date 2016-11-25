#!/usr/bin/env python
import os, re
import commands
import sys
import math

MClist=['TT_powheg','WJetsToLNu','DYLL','WW','WZ','Wg_MG','Zg_aMCatNLO']
#MClist=['WZ','Wg_MG','Zg_aMCatNLO']

# hadd step1 mc outputs and mv it to ntupleStore/ 
for mc in MClist:
    os.system("hadd -k step1_{0}.root MC_Out_step1/{0}/ana_rootNov23/step1*.root".format(mc))
    os.system("mv step1_{0}.root ../../ntupleStore".format(mc))
