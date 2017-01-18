#!/bin/bash

# First method to submit jobs for single huge input:  script   filepath(root://eoscms//store/../xx.root) OUTName events/jobs
# Second method to submit jobs for dir containing many inputfiles:  script   dirpath(/store/../)         OUTName files/jobs
# 


########################################################################
#################################  MC  #################################
########################################################################
./submitMC_step1.py /store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/TT_TuneCUETP8M1_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext3-v2/161211_211239/0000/ TT_powheg 10
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTGJets.root TTGJets 1000000

./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTWJetsToLNu.root TTWJetsToLNu 1000000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTWJetsToQQ.root TTWJetsToQQ 1000000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTZToLLNuNu.root TTZToLLNuNu 1000000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_TTZToQQ.root TTZToQQ 1000000


#V+jets
./submitMC_step1.py root://eoscms//store/user/pbarria/ggntuples/mc/V08_00_24_00/output/job_spring16_WJetsToLNu_aMCatNLO_miniAOD.root WJetsToLNu 1000000
#*******ZJets

# diboson
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_WW.root WW 200000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_WZ.root WZ 200000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_ZZ.root ZZ 200000

#V+gamma
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_WGToLNuG.root WGToLNuG 1000000
./submitMC_step1.py root://eoscms//store/user/fxia/ggntuples/mc/V08_00_24_00/output/job_spring16_ZGTo2LG.root ZGTo2LG 1000000

#Single Top
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/job_spring16_ST_s-channel_4f_leptonDecays_miniAOD.root ST_s-channel_4f_leptonDecays 1000000

#./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/job_spring16_ST_t-channel_antitop_4f_inclusiveDecays_miniAOD.root ST_t-channel_antitop_4f_inclus 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_t-channel_antitop_4f_leptonDecays_miniAOD.root ST_t-channel_antitop_4f_leptonDecays 1000000
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_t-channel_top_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_t-channel_top_4f_leptonDecays_miniAOD.root ST_t-channel_top_4f_leptonDecays 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_tW_antitop_5f_inclusiveDecays_miniAOD.root ST_tW_antitop_5f_inclus 1000000
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_24_00/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/job_spring16_ST_tW_top_5f_inclusiveDecays_miniAOD.root ST_tW_top_5f_inclus 1000000






########################################################################
#################################  DATA  ###############################
########################################################################
########### * Electron*  ###############
/eos/cms/store/user/cmkuo/job_SingleEle_Run2016B_SepRereco/SingleElectron/crab_job_SingleEle_Run2016B_SepRereco/161218_023412/

./submitData_step1.py /eos/cms/store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_SingleEle_Run2016C_SepRereco/ SingleEle_Run2016C_SepRereco 20

./submitData_step1.py /eos/cms/store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_SingleEle_Run2016D_SepRereco/ SingleEle_Run2016D_SepRereco 20

./submitData_step1.py /eos/cms/store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_SingleEle_Run2016E_SepRereco/ SingleEle_Run2016E_SepRereco 20

./submitData_step1.py root://eoscms//store/user/fxia/ggntuples/data/V08_00_24_00/job_SingleEle_Run2016H_PRv3.root SingleEle_Run2016H_PRv3 2000000



#./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016D_PRv2.root SingleEleRun2016D 2000000

#./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016B_PRv2.root SingleEleRun2016B 2000000

#./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016C_PRv2.root SingleEleRun2016C 2000000
#./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleMu_Run2016D_PRv2.root SingleMuRun2016D 2000000


########### * Muon*    #################

./submitData_step1.py /eos/cms/store/group/phys_smp/ggNtuples/13TeV/data/V08_00_24_00/job_SingleMu_Run2016C_SepRereco/ SingleMu_Run2016C_SepRereco 20