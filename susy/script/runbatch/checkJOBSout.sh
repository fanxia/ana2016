#!/bin/bash                                                        

#  eg check ana output:   ./checkJOBSout.sh Mar06
#  eg check dilep-ana output:   ./checkJOBSout.sh Mar06 dilep

#MClist="TT_powheg TTGJets TTZToQQ TTZToLLNuNu TTWJetsToLNu TTWJetsToQQ WJetsToLNu WW WZ ZZ ZGTo2LG WGToLNuG ST_s-channel_4f_leptonDecays ST_t-channel_antitop_4f_leptonDecays ST_t-channel_top_4f_leptonDecays ST_tW_antitop_5f_inclus ST_tW_top_5f_inclus"
#EleDatalist="SingleEle_Run2016B_SepRereco0 SingleEle_Run2016B_SepRereco1 SingleEle_Run2016B_SepRereco2 SingleEle_Run2016C_SepRereco SingleEle_Run2016D_SepRereco SingleEle_Run2016E_SepRereco SingleEle_Run2016F_SepRereco1 SingleEle_Run2016F_SepRereco2 SingleEle_Run2016G_sepRereco0  SingleEle_Run2016G_sepRereco1 SingleEle_Run2016G_sepRereco2 SingleEle_Run2016H_PRv3"
#MuDatalist="SingleMu_Run2016B_SepRereco0 SingleMu_Run2016B_SepRereco1 SingleMu_Run2016B_SepRereco2 SingleMu_Run2016C_SepRereco SingleMu_Run2016D_SepRereco SingleMu_Run2016E_SepRereco"
#MClist="TTGJets TTGG"
MClist=""
EleDatalist="SingleEle_Run2016B_FebReminiAOD SingleEle_Run2016C_FebReminiAOD SingleEle_Run2016D_FebReminiAOD SingleEle_Run2016E_FebReminiAOD SingleEle_Run2016F_FebReminiAOD1 SingleEle_Run2016F_FebReminiAOD2 SingleEle_Run2016G_FebReminiAOD SingleEle_Run2016H_FebReminiAODv2 SingleEle_Run2016H_FebReminiAODv3"
MuDatalist=""
for mc in $MClist
do
    echo "Now checking output jobs of $mc"

    for entry in MC_$2Out_step1/$mc/$2ana_root$1/log*txt
    do
	if [ ! -s $entry ]
	then
            echo "${entry##*/} is empty!"
	fi
    done
    
    echo "*********************************"
done

for data in $EleDatalist
do
    echo "Now checking output jobs of $data"

    for entry in Data_$2Out_step1/$data/$2ana_root$1/log*txt
    do
	if [ ! -s $entry ]
	then
            echo "${entry##*/} is empty!"
	fi
    done
    
    echo "*********************************"
done

for data in $MuDatalist
do
    echo "Now checking output jobs of $data"

    for entry in Data_$2Out_step1/$data/$2ana_root$1/log*txt
    do
	if [ ! -s $entry ]
	then
            echo "${entry##*/} is empty!"
	fi
    done
    
    echo "*********************************"
done


exit
