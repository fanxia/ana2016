#!/bin/bash

#          inputpath, outputname, events/jobs
./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_DYJetsToLL_m50_aMCatNLO.root DYLL 1000000
./submitMC_step1.py root://eoscms//store/user/pbarria/ggntuples/mc/V08_00_24_00/output/job_spring16_WJetsToLNu_aMCatNLO_miniAOD.root WJetsToLNu 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_TT_powheg_ext3.root TT_powheg 2000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_Wg_MG.root Wg_MG 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_Zg_aMCatNLO.root Zg_aMCatNLO 1000000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_WW.root WW 200000

./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16_WZ.root WZ 200000

#./submitMC_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/MC/V08_00_11_01/job_spring16??.root ZZ

./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016D_PRv2.root SingleEleRun2016D 2000000

./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016B_PRv2.root SingleEleRun2016B 2000000

./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleEle_Run2016C_PRv2.root SingleEleRun2016C 2000000
#./submitData_step1.py root://eoscms//store/group/phys_smp/ggNtuples/13TeV/data/V08_00_11_01/job_SingleMu_Run2016D_PRv2.root SingleMuRun2016D 2000000