#!/bin/bash

# First method to submit jobs for single huge input:  script   filepath(root://eoscms//store/../xx.root) OUTName events/jobs
# Second method to submit jobs for dir containing many inputfiles:  script   dirpath(/store/../)         OUTName files/jobs
# 

######################################################################
######################## Signal MC ###################################
######################################################################
./submitSig_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_SMS-T6ttZg/ SMS-T6ttZg 1

exit


########################################################################
#################################  MC  #################################
########################################################################

#./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTJets_DiLept/ TTJets_DiLept 2 
#./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_TTJets_SingleLeptFromTbar/ TTJets_SingleLeptFromTbar 2
#./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_TTJets_SingleLeptFromT/ TTJets_SingleLeptFromT 2

#exit
#TT
./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TT/ TT 2

./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTGJets/ TTGJets 2
./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTGG_0Jets/ TTGG 1

#TTV
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTWJetsToLNu/ TTWJetsToLNu 1
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTWJetsToQQ/ TTWJetsToQQ 1
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTZToLLNuNu/ TTZToLLNuNu 2
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTZToQQ/ TTZToQQ 1

#W+jets

./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_W4JetsToLNu/ W4JetsToLNu 2
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_W3JetsToLNu/ W3JetsToLNu 2
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_W2JetsToLNu/ W2JetsToLNu 2


#*******ZJets
./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_DYJetsToLL/ DYJetsToLL 2

# diboson
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_WZ/ WZ 2
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_ZZ/ ZZ 2
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_WW/ WW 2



#V+gamma
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_WGToLNuG/ WGToLNuG 2
./submitMC_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_ZGTo2LG/ ZGTo2LG 2


#Single Top
./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_ST_s-channel_4f_leptonDecays/ ST_s-channel_4f_leptonDecays 1

./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_t-channel_top_4f_inclusiveDecays/ ST_t-channel_top_4f_inclusiveDecays 5
./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_t-channel_antitop_4f_inclusiveDecays/ ST_t-channel_antitop_4f_inclusiveDecays 4

#./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_antitop_5f_NoFullyHadronicDecays/ ST_tW_antitop_5f_NoFullyHadronicDecays 2
#./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_top_5f_NoFullyHadronicDecays/ ST_tW_top_5f_NoFullyHadronicDecays 2

./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_antitop_5f_inclusiveDecays/ ST_tW_antitop_5f_inclusiveDecays 1
./submitMC_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_top_5f_inclusiveDecays/ ST_tW_top_5f_inclusiveDecays 1





#exit
########################################################################
#################################  DATA  ###############################
########################################################################
########### * Electron*  ###############

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016B_FebReminiAOD/ SingleEle_Run2016B_FebReminiAOD 20

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016C_FebReminiAOD/ SingleEle_Run2016C_FebReminiAOD 20

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016D_FebReminiAOD/ SingleEle_Run2016D_FebReminiAOD 20

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016E_FebReminiAOD/ SingleEle_Run2016E_FebReminiAOD 20

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016F_FebReminiAOD1/ SingleEle_Run2016F_FebReminiAOD1 20
./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016F_FebReminiAOD2/ SingleEle_Run2016F_FebReminiAOD2 20

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016G_FebReminiAOD/ SingleEle_Run2016G_FebReminiAOD 20

./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016H_FebReminiAODv2/ SingleEle_Run2016H_FebReminiAODv2 20
./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016H_FebReminiAODv3/ SingleEle_Run2016H_FebReminiAODv3 20

########### * Muon*    #################
 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016B_FebReminiAOD/ SingleMu_Run2016B_FebReminiAOD 20

 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016C_FebReminiAOD/ SingleMu_Run2016C_FebReminiAOD 20

 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016D_FebReminiAOD/ SingleMu_Run2016D_FebReminiAOD 20

 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016E_FebReminiAOD/ SingleMu_Run2016E_FebReminiAOD 20

 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016F_FebReminiAOD1/ SingleMu_Run2016F_FebReminiAOD1 20
 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016F_FebReminiAOD2/ SingleMu_Run2016F_FebReminiAOD2 20

 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016G_FebReminiAOD/ SingleMu_Run2016G_FebReminiAOD 20

 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016H_FebReminiAODv2/ SingleMu_Run2016H_FebReminiAODv2 20
 ./submitData_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016H_FebReminiAODv3/ SingleMu_Run2016H_FebReminiAODv3 20
