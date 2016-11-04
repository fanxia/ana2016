#!/bin/bash

#          inputpath, outputname, events/jobs
#./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_DYJetsToLL_m50_aMCatNLO.root DYLL 1000000
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_WJetsToLNu_aMCatNLO.root WJetsToLNu 1000000

 ./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_TT_powheg_ext3.root TT_powheg 2000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_Wg_MG.root Wg_MG 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_Zg_aMCatNLO.root Zg_aMCatNLO 1000000



./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016D_PRv2.root SingleEleRun2016D 2000000