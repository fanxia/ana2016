#!/bin/bash                                                        


MClist="TT_powheg TTGJets TTZToQQ TTZToLLNuNu TTWJetsToLNu TTWJetsToQQ WJetsToLNu WW WZ ZZ ZGTo2LG WGToLNuG ST_s-channel_4f_leptonDecays ST_t-channel_antitop_4f_leptonDecays ST_t-channel_top_4f_leptonDecays ST_tW_antitop_5f_inclus ST_tW_top_5f_inclus"
EleDatalist="SingleEle_Run2016B_sepRereco0 SingleEle_Run2016B_sepRereco1 SingleEle_Run2016B_sepRereco2 SingleEle_Run2016C_SepRereco SingleEle_Run2016D_SepRereco"

for mc in $MClist
do
    echo "Now checking output jobs of $mc"

    for entry in MC_Out_step1/$mc/ana_rootJan26/log*txt
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

    for entry in Data_Out_step1/$data/ana_rootJan26/log*txt
    do
	if [ ! -s $entry ]
	then
            echo "${entry##*/} is empty!"
	fi
    done
    
    echo "*********************************"
done


exit
