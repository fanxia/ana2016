#!/bin/bash

# First method to submit jobs for single huge input:  script   filepath(root://eoscms//store/../xx.root) OUTName events/jobs
# Second method to submit jobs for dir containing many inputfiles:  script   dirpath(/store/../)         OUTName files/jobs
# 


########################################################################
#################################  MC  #################################
########################################################################


./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTGJets/ TTGJets 2
./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTGG_0Jets/ TTGG 1

#TTV


#V+jets
#./submitMC-dilep_step1.py root://eoscms//store/user/pbarria/ggntuples/mc/V08_00_24_00/output/job_spring16_WJetsToLNu_aMCatNLO_miniAOD.root WJetsToLNu 1000000

#./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_24_00/job_spring16_W3JetsToLNu/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_job_spring16_W3JetsToLNu/170207_095808/0000/ W3JetsToLNu 2

#./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_24_00/job_spring16_W4JetsToLNu/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_job_spring16_W4JetsToLNu/170202_160516/0000/ W4JetsToLNu 2


#*******ZJets


# diboson


#V+gamma

#Single Top



########################################################################
#################################  DATA  ###############################
########################################################################
########### * Electron*  ###############

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016B_FebReminiAOD/ SingleEle_Run2016B_FebReminiAOD 20

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016C_FebReminiAOD/ SingleEle_Run2016C_FebReminiAOD 20

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016D_FebReminiAOD/ SingleEle_Run2016D_FebReminiAOD 20

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016E_FebReminiAOD/ SingleEle_Run2016E_FebReminiAOD 20

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016F_FebReminiAOD1/ SingleEle_Run2016F_FebReminiAOD1 20
./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016F_FebReminiAOD2/ SingleEle_Run2016F_FebReminiAOD2 20

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016G_FebReminiAOD/ SingleEle_Run2016G_FebReminiAOD 20

./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016H_FebReminiAODv2/ SingleEle_Run2016H_FebReminiAODv2 20
./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016H_FebReminiAODv3/ SingleEle_Run2016H_FebReminiAODv3 20

########### * Muon*    #################
 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016B_FebReminiAOD/ SingleMu_Run2016B_FebReminiAOD 20

 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016C_FebReminiAOD/ SingleMu_Run2016C_FebReminiAOD 20

 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016D_FebReminiAOD/ SingleMu_Run2016D_FebReminiAOD 20

 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016E_FebReminiAOD/ SingleMu_Run2016E_FebReminiAOD 20

 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016F_FebReminiAOD1/ SingleMu_Run2016F_FebReminiAOD1 20
 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016F_FebReminiAOD2/ SingleMu_Run2016F_FebReminiAOD2 20

 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016G_FebReminiAOD/ SingleMu_Run2016G_FebReminiAOD 20

 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016H_FebReminiAODv2/ SingleMu_Run2016H_FebReminiAODv2 20
 ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016H_FebReminiAODv3/ SingleMu_Run2016H_FebReminiAODv3 20
