#!/bin/bash

# First method to submit jobs for single huge input:  script   filepath(root://eoscms//store/../xx.root) OUTName events/jobs
# Second method to submit jobs for dir containing many inputfiles:  script   dirpath(/store/../)         OUTName files/jobs
# 
runMC=false
runSig=false
runDataEle=false
runDataMu=true

########################################################################
#################################  MC  #################################
########################################################################
if [ "$runMC" = true ]; then
#./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTJets_DiLept/ TTJets_DiLept 2 
#./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_TTJets_SingleLeptFromTbar/ TTJets_SingleLeptFromTbar 2
#./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_TTJets_SingleLeptFromT/ TTJets_SingleLeptFromT 2

#exit

    ./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TT/ TT 2
    ./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTGJets/ TTGJets 2
    ./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTGG_0Jets/ TTGG 1


#TTV
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTWJetsToLNu/ TTWJetsToLNu 1
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTWJetsToQQ/ TTWJetsToQQ 1
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTZToLLNuNu/ TTZToLLNuNu 2
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_TTZToQQ/ TTZToQQ 1

#W+jets

    ./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_W4JetsToLNu/ W4JetsToLNu 2
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_W3JetsToLNu/ W3JetsToLNu 2
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_W2JetsToLNu/ W2JetsToLNu 2
#*******ZJets
    ./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_DYJetsToLL/ DYJetsToLL 2

# diboson
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_WZ/ WZ 2
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_ZZ/ ZZ 2
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_WW/ WW 2

#V+gamma
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_WGToLNuG/ WGToLNuG 2
    ./submitMC-dilep_step1.py /store/caf/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_ZGTo2LG/ ZGTo2LG 2
#Single Top
    ./submitMC-dilep_step1.py /store/user/fxia/ggntuples/mc/V08_00_26_01/job_summer16_ST_s-channel_4f_leptonDecays/ ST_s-channel_4f_leptonDecays 1

    ./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_t-channel_top_4f_inclusiveDecays/ ST_t-channel_top_4f_inclusiveDecays 5
    ./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_t-channel_antitop_4f_inclusiveDecays/ ST_t-channel_antitop_4f_inclusiveDecays 4

#./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_antitop_5f_NoFullyHadronicDecays/ ST_tW_antitop_5f_NoFullyHadronicDecays 2
#./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_top_5f_NoFullyHadronicDecays/ ST_tW_top_5f_NoFullyHadronicDecays 2

    ./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_antitop_5f_inclusiveDecays/ ST_tW_antitop_5f_inclusiveDecays 1
    ./submitMC-dilep_step1.py /store/user/yanchu/ggntuples/mc/V08_00_26_01/job_summer16_ST_tW_top_5f_inclusiveDecays/ ST_tW_top_5f_inclusiveDecays 1

fi

########################################################################
#################################  DATA  ###############################
########################################################################
########### * Electron*  ###############
if [ "$runDataEle" = true ]; then
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016B_FebReminiAOD/ SingleEle_Run2016B_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016C_FebReminiAOD/ SingleEle_Run2016C_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016D_FebReminiAOD/ SingleEle_Run2016D_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016E_FebReminiAOD/ SingleEle_Run2016E_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016F_FebReminiAOD1/ SingleEle_Run2016F_FebReminiAOD1 20
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016F_FebReminiAOD2/ SingleEle_Run2016F_FebReminiAOD2 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016G_FebReminiAOD/ SingleEle_Run2016G_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016H_FebReminiAODv2/ SingleEle_Run2016H_FebReminiAODv2 20
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleEle_Run2016H_FebReminiAODv3/ SingleEle_Run2016H_FebReminiAODv3 20
fi


########### * Muon*    #################
if [ "$runDataMu" = true ]; then
    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016B_FebReminiAOD/ SingleMu_Run2016B_FebReminiAOD 20

    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016C_FebReminiAOD/ SingleMu_Run2016C_FebReminiAOD 20

    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016D_FebReminiAOD/ SingleMu_Run2016D_FebReminiAOD 20

    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016E_FebReminiAOD/ SingleMu_Run2016E_FebReminiAOD 20

    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016F_FebReminiAOD1/ SingleMu_Run2016F_FebReminiAOD1 20
    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016F_FebReminiAOD2/ SingleMu_Run2016F_FebReminiAOD2 20

    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016G_FebReminiAOD/ SingleMu_Run2016G_FebReminiAOD 20

    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016H_FebReminiAODv2/ SingleMu_Run2016H_FebReminiAODv2 20
    # ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_01/job_SingleMu_Run2016H_FebReminiAODv3/ SingleMu_Run2016H_FebReminiAODv3 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016B_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016B_FebReminiAOD/170504_031253/0000/ SingleMu_Run2016B_FebReminiAOD00 20
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016B_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016B_FebReminiAOD/170504_031253/0001/ SingleMu_Run2016B_FebReminiAOD01 20
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016B_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016B_FebReminiAOD/170504_031253/0002/ SingleMu_Run2016B_FebReminiAOD02 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016C_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016C_FebReminiAOD/170504_031315/0000/ SingleMu_Run2016C_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016D_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016D_FebReminiAOD/170504_031338/0000/ SingleMu_Run2016D_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016E_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016E_FebReminiAOD/170504_031500/0000/ SingleMu_Run2016E_FebReminiAOD 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016F_FebReminiAOD1/SingleMuon/crab_job_SingleMu_Run2016F_FebReminiAOD1/170504_032109/0000/ SingleMu_Run2016F_FebReminiAOD1 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016F_FebReminiAOD2/SingleMuon/crab_job_SingleMu_Run2016F_FebReminiAOD2/170504_032129/0000/ SingleMu_Run2016F_FebReminiAOD2 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016G_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016G_SepRereco/170504_032204/0000/ SingleMu_Run2016G_FebReminiAOD00 20
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016G_FebReminiAOD/SingleMuon/crab_job_SingleMu_Run2016G_SepRereco/170504_032204/0001/ SingleMu_Run2016G_FebReminiAOD01 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016H_PRv2/SingleMuon/crab_job_SingleMu_Run2016H_PRv2/170504_032250/0000/ SingleMu_Run2016H_FebReminiAODv200 20
    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016H_PRv2/SingleMuon/crab_job_SingleMu_Run2016H_PRv2/170504_032250/0001/ SingleMu_Run2016H_FebReminiAODv201 20

    ./submitData-dilep_step1.py /store/group/phys_smp/ggNtuples/13TeV/data/V08_00_26_02/job_SingleMu_Run2016H_PRv3/SingleMuon/crab_job_SingleMu_Run2016H_PRv3/170504_032312/0000/ SingleMu_Run2016H_FebReminiAODv3 20

fi