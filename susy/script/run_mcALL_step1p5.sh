#!/bin/bash
# ./run_mcALL_step1p5.sh 
# ./run_mcALL_step1p5.sh dilep

# python mc_ana_step1p5.py ../ntupleStore/step1_TT_powheg.root TT_powheg

#python mc_ana_step1p5.py ../ntupleStore/step1_TTGJets.root TTGJets
#python mc_ana_step1p5.py ../ntupleStore/step1_TTGG.root TTGG

# python mc_ana_step1p5.py ../ntupleStore/step1_TTZToQQ.root TTZToQQ
# python mc_ana_step1p5.py ../ntupleStore/step1_TTZToLLNuNu.root TTZToLLNuNu

# python mc_ana_step1p5.py ../ntupleStore/step1_TTWJetsToLNu.root TTWJetsToLNu
# python mc_ana_step1p5.py ../ntupleStore/step1_TTWJetsToQQ.root TTWJetsToQQ



#python mc_ana_step1p5.py ../ntupleStore/step1_W4JetsToLNu.root W4JetsToLNu
# python mc_ana_step1p5.py ../ntupleStore/step1_DYLL.root DYLL

#python mc_ana_step1p5.py ../ntupleStore/step1_WGToLNuG.root WGToLNuG
#python mc_ana_step1p5.py ../ntupleStore/step1_ZGTo2LG.root ZGTo2LG

#python mc_ana_step1p5.py ../ntupleStore/step1_WZ.root WZ
#python mc_ana_step1p5.py ../ntupleStore/step1_ZZ.root ZZ
#python mc_ana_step1p5.py ../ntupleStore/step1_WW.root WW




if [ $1 == "dilep" ]
then
    script=mc_diLep-ana_step1p5.py
    aa="_"$1
else
    script=mc_ana_step1p5.py
fi


#MClist="TTJets_DiLept TTJets_SingleLeptFromT TTJets_SingleLeptFromTbar"
#MClist="TT TTGJets TTGG TTWJetsToLNu TTWJetsToQQ TTZToLLNuNu TTZToQQ"
MClist="TT TTGJets TTGG TTWJetsToLNu TTWJetsToQQ TTZToLLNuNu TTZToQQ W4JetsToLNu DYJetsToLL WGToLNuG WW WZ ZGTo2LG ZZ ST_s-channel_4f_leptonDecays ST_tW_antitop_5f_inclusiveDecays ST_tW_top_5f_inclusiveDecays ST_t-channel_antitop_4f_inclusiveDecays ST_t-channel_top_4f_inclusiveDecays W3JetsToLNu W2JetsToLNu"
#MClist="ST_t-channel_top_4f_inclusiveDecays W3JetsToLNu W2JetsToLNu"

for mc in $MClist
do
    echo "########################################################"
    echo "----Begin $1 Step1p5 for $mc-----"
    python $script ../ntupleStore/step1_$mc$aa.root $mc
    echo "########################################################"
done


