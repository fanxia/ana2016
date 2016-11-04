#!/usr/bin/env python
from ROOT import *
import os, re
import commands
import math, time
import sys


# got nenties as the number of entries
inputfile=TFile.Open(sys.argv[1])
inputtree=inputfile.Get("ggNtuplizer/EventTree")
outputfile=sys.argv[2]
totaleventnumber=inputtree.GetEntries()
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
interval = int(sys.argv[3]) # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
totaljobs = int(totaleventnumber)/interval+1
intervallist=[i*interval for i in range(totaljobs)]
if intervallist[-1]!=totaleventnumber: intervallist.append(totaleventnumber)
ScriptName = "mc_ana_step1.py" # script to be used
queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########
#os.system("rm -r log 2>/dev/null")
os.system("mkdir -p "+sys.argv[2]+"_step1_log")
#os.chdir(sys.argv[3]+"_step1output/log")
jobscr='''
#!/bin/sh
cd $LS_SUBCWD
eval `scramv1 runtime -sh`
python {0} INPUT OUTNAME JOBID LOWLIMIT UPLIMIT
echo 'STOP---------------'
'''.format(ScriptName)
##### loop for creating and sending jobs #####
for x in range(len(intervallist)-1):
   ##### creates directory and file list for job #######
   #os.system("mkdir tmp/"+str(x))
   #os.chdir("tmp/"+str(x))
   #os.system("cp ../{0} .".format(ScriptName))
   ##### creates jobs #######
   with open('job{0}.sh'.format(x), 'w') as fout:fout.write(jobscr.replace('LOWLIMIT',str(intervallist[x])).replace('UPLIMIT',str(intervallist[x+1])).replace('JOBID',str(x)).replace('INPUT',sys.argv[1]).replace('OUTNAME',sys.argv[2]))
   os.system("chmod 755 job{0}.sh".format(x))
   ###### sends bjobs ######
   os.system("bsub -q "+queue+" -o "+sys.argv[2]+"_step1_log/log{0} job{0}.sh".format(x))
   print "job nr " + str(x) + " submitted"
   os.system("mv job{0}.sh ".format(x)+sys.argv[2]+"_step1_log/")
   #os.chdir("../..")
   
print "\nyour jobs:"
os.system("bjobs")
print '\nEND\n'

