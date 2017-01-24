#!/usr/bin/env python
from ROOT import *
import os, re
import commands
from commands import getoutput
import math, time
import sys

GetIn=sys.argv[1]

outputfile=sys.argv[2]
ScriptName = "../data_diLep-ana_step1.py" # script to be used
if '.root' in GetIn:
   # got nenties as the number of entries
   inputfile=TFile.Open(sys.argv[1])
   inputtree=inputfile.Get("ggNtuplizer/EventTree")
   totaleventnumber=inputtree.GetEntries()
########   customization  area #########
   interval = int(sys.argv[3]) # number files to be processed in a single job, take care to split your file so that you run on all files. The last job might be with smaller number of files (the ones that remain).
   totaljobs = int(totaleventnumber)/interval+1
   intervallist=[i*interval for i in range(totaljobs)]
   if intervallist[-1]!=totaleventnumber: intervallist.append(totaleventnumber)
   queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########
#os.system("rm -r log 2>/dev/null")
   os.system("mkdir -p "+sys.argv[2]+"_dilep-step1_log")
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
      with open(sys.argv[2]+'_dilepjob{0}.sh'.format(x), 'w') as fout:fout.write(jobscr.replace('LOWLIMIT',str(intervallist[x])).replace('UPLIMIT',str(intervallist[x+1])).replace('JOBID',str(x)).replace('INPUT',sys.argv[1]).replace('OUTNAME',sys.argv[2]))
      os.system("chmod 755 "+sys.argv[2]+"_dilepjob{0}.sh".format(x))
   ###### sends bjobs ######
      os.system("bsub -q "+queue+" -o "+sys.argv[2]+"_dilep-step1_log/log{0} ".format(x)+sys.argv[2]+"_dilepjob{0}.sh".format(x))
      print "job nr " + str(x) + " submitted"
      os.system("cp "+sys.argv[2]+"_dilepjob{0}.sh ".format(x)+sys.argv[2]+"_dilep-step1_log/")
   #os.chdir("../..")







# GetIn: /store/user/fxia/xxdir/   start and end with '/'


if not '.root' in GetIn:
   tmpinputfilelist=getoutput('eos ls '+GetIn+'*.root').split('\n')
   inputfilelist=[("root://eoscms/"+GetIn+lis) for lis in tmpinputfilelist ]
#   inputfilelist.extend(getoutput().split('\n'))
   totalfilenumber=len(inputfilelist)
########   customization  area #########
   interval = int(sys.argv[3]) # number files to be processed in a single job
   totaljobs = int(totalfilenumber)/interval+1
   intervallist=[i*interval for i in range(totaljobs)]
   if intervallist[-1]!=totalfilenumber: intervallist.append(totalfilenumber)
   queue = "8nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########
#os.system("rm -r log 2>/dev/null")
   os.system("mkdir -p "+sys.argv[2]+"_dilep-step1_log")
#os.chdir(sys.argv[3]+"_step1output/log")
   jobscr='''
#!/bin/sh
cd $LS_SUBCWD
eval `scramv1 runtime -sh`
python {0} INPUT OUTNAME JOBID
echo 'STOP---------------'
'''.format(ScriptName)
##### loop for creating and sending jobs #####
   for x in range(len(intervallist)-1):
   ##### creates directory and file list for job #######
   #os.system("mkdir tmp/"+str(x))
   #os.chdir("tmp/"+str(x))
   #os.system("cp ../{0} .".format(ScriptName))
   ##### creates jobs #######
      INPUTthis="'{}'".format(' '.join(inputfilelist[intervallist[x]:intervallist[x+1]])+"")
      with open(sys.argv[2]+'_dilepjob{0}.sh'.format(x), 'w') as fout:fout.write(jobscr.replace('JOBID',str(x)).replace('INPUT',INPUTthis).replace('OUTNAME',sys.argv[2]))
      os.system("chmod 755 "+sys.argv[2]+"_dilepjob{0}.sh".format(x))
   ###### sends bjobs ######
      os.system("bsub -q "+queue+" -o "+sys.argv[2]+"_dilep-step1_log/log{0} ".format(x)+sys.argv[2]+"_dilepjob{0}.sh".format(x))
      print "job nr " + str(x) + " submitted"
      os.system("cp "+sys.argv[2]+"_dilepjob{0}.sh ".format(x)+sys.argv[2]+"_dilep-step1_log/")
   #os.chdir("../..")



   
print "\nyour jobs:"
os.system("bjobs")
print '\nEND\n'


