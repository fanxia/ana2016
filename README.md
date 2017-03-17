# analysis topology
# updata 2016/11/23

 dir python:
 to store all the function modules

 dir plot:
 the script to make plots

#IMPORTANT: dir script
 For data:
 step1 select the signal the QCD events for electron/mu


 For MC:
 step1 select the signal the QCD events for electron/mu
 step1p5 adding the reweight, scalefactor...



1 How to run btag eff:
  
1.1 ./submitMC_btag_step1.sh    This will produce multiple jobs to run through all MC datasets, save in to dir (MC_BtagEff_step1)
1.2 go check the dir (MC_BtagEff_step1), make sure every mc has got all the outputs
1.3 python calBtagEff_step2.py inputdirname/ outputname       
    for eg. python calBtagEff_step2.py MC_BtagEff_step1/WW/Nov17/ WW    Will finally give WW_BtagEff.root
1.4 repeat step1.3 for all the bkgs


#MakePlots
 Electron channel

 prepare the hists:
   python step1_ELE_plothists.py Tag
   python step1_EE_plothists.py Tag

 calculate all the factors:
   python step2_ELE_fitfactor.py Tag

 finally, stack the plots while applying all the factors:
   python step3_ELE_finalstack.py Tag