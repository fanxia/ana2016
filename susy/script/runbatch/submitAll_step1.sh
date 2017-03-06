#!/bin/bash

# First method to submit jobs for single huge input:  script   filepath(root://eoscms//store/../xx.root) OUTName events/jobs
# Second method to submit jobs for dir containing many inputfiles:  script   dirpath(/store/../)         OUTName files/jobs
# 


########################################################################
#################################  MC  #################################
########################################################################
 ./submitMC_step1.py /store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext3-v2/161211_211239/0000/ TT_powheg 10
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTGJets.root TTGJets 1000000

./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTWJetsToLNu.root TTWJetsToLNu 500000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTWJetsToQQ.root TTWJetsToQQ 500000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTZToLLNuNu.root TTZToLLNuNu 500000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTZToQQ.root TTZToQQ 500000


#V+jets
#./submitMC_step1.py root://eoscms//store/user/pbarria/ggntuples/mc/V08_00_24_00/output/job_spring16_WJetsToLNu_aMCatNLO_miniAOD.root WJetsToLNu 1000000

./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_24_00/job_spring16_W3JetsToLNu/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_job_spring16_W3JetsToLNu/170207_095808/0000/ W3JetsToLNu 2

./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_24_00/job_spring16_W4JetsToLNu/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_job_spring16_W4JetsToLNu/170202_160516/0000/ W4JetsToLNu 2


#*******ZJets
./submitMC_step1.py /store/user/fxia/ggntuples/mc/V08_00_24_00/job_spring16_DYJetsToLL_M-50_TuneCUETP8M1/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_job_spring16_DYJetsToLL_M-50_TuneCUETP8M1/170210_133830/0000/ DYJetsToLL 10


# diboson
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_WW.root WW 200000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_WZ.root WZ 200000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_ZZ.root ZZ 200000

#V+gamma
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_WGToLNuG.root WGToLNuG 1000000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_ZGTo2LG.root ZGTo2LG 1000000

#Single Top
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/job_spring16_ST_s-channel_4f_leptonDecays_miniAOD.root ST_s-channel_4f_leptonDecays 400000

#./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/job_spring16_ST_t-channel_antitop_4f_inclusiveDecays_miniAOD.root ST_t-channel_antitop_4f_inclus 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_t-channel_antitop_4f_leptonDecays_miniAOD.root ST_t-channel_antitop_4f_leptonDecays 400000
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_t-channel_top_4f_leptonDecays_miniAOD.root ST_t-channel_top_4f_leptonDecays 400000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_tW_antitop_5f_inclusiveDecays_miniAOD.root ST_tW_antitop_5f_inclus 400000
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_tW_top_5f_inclusiveDecays_miniAOD.root ST_tW_top_5f_inclus 400000





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
