# Using the resulting hists from step1, to calculate some scale factors: QCD factor, wjets,ttbar sfs....
#!/usr/bin/env python
import math,sys
import ROOT
from ROOT import *
import os, string, math, pickle
from TemplateFitter import TemplateFitter


tag=sys.argv[1]

elefin=TFile.Open("step1_out/"+tag+"_ELE.root")  #input of ele channel
eefin=TFile.Open("step1_out/"+tag+"_EE.root")    #input of ee channel
foutname="step2_out/fitfactor_ELE_"+tag
frootout=TFile.Open(foutname+".root","recreate")
frootout.Close()
log=open(foutname+".log","w")


####################################################################
# __                       __       __                             #
#|  \                     |  \     /  \                            #
# \$$ _______   __     __ | $$\   /  $$          ______    ______  #
#|  \|       \ |  \   /  \| $$$\ /  $$$         /      \  /      \ #
#| $$| $$$$$$$\ \$$\ /  $$| $$$$\  $$$$        |  $$$$$$\|  $$$$$$\#
#| $$| $$  | $$  \$$\  $$ | $$\$$ $$ $$        | $$    $$| $$    $$#
#| $$| $$  | $$   \$$ $$  | $$ \$$$| $$        | $$$$$$$$| $$$$$$$$#
#| $$| $$  | $$    \$$$   | $$  \$ | $$ ______  \$$     \ \$$     \#
# \$$ \$$   \$$     \$     \$$      \$$|      \  \$$$$$$$  \$$$$$$$#
#                                       \$$$$$$                    #
####################################################################
######Invmass(ee) fit for DY/Zg  ###################################
print "Invmass(ee) templit fit for DY and Zgamma Bkgs"
InvEEFitter=TemplateFitter()
InvEEhistname=tag+"_EE_Mass_ee_ee_bjj_"
InvEEFitter.pushdata("SingleEle 2016 Data",eefin.Get(InvEEhistname+"data"))

InvEEFitter.pushmc("Bkgs",eefin.Get(InvEEhistname+"VV"))
InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"TTG"))
InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"Wgamma"))
InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"WJets"))

InvEEFitter.pushmc("DY/Z#gamma",eefin.Get(InvEEhistname+"Zgamma"))

# InvEEFitter.pushmc("Bkgs",eefin.Get(InvEEhistname+"TTV"))
# InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"TTG"))
# InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"TT"))
# #InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"TT"),scal=k_ttbar)
# #InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"WJets"),scal=k_wjets)
# InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"WJets"))
# InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"VV"))
# InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"ST"))
# InvEEFitter.addmc("Bkgs",eefin.Get(InvEEhistname+"WG"))


# InvEEFitter.pushmc("DY/Z#gamma",eefin.Get(InvEEhistname+"ZJets"))
# InvEEFitter.addmc("DY/Z#gamma",eefin.Get(InvEEhistname+"ZG"))

InvEEFitter.tempfit()
InvEEFitter_result=InvEEFitter.result
k_bkgs=InvEEFitter_result['Bkgs'][2]
k_ee=InvEEFitter_result['DY/Z#gamma'][2]

log.write("\n\n####################################################################")
log.write("\n####################InvmassEE Fitter##################################")
log.write("\n####################InvmassEE Fitter##################################")
log.write("\n%s\n"%InvEEFitter_result)
log.write("\n In Ele channel, the scale factor for DY&Vgamma is %s"%k_ee)
log.write("\n In Ele channel, the scale factor for Bkgs is %s"%k_bkgs)
log.write("\n#################################################################")
log.write("\n#################################################################\n\n\n")
InvEEFitter.tempfitplot(foutname,"invmass(ee)","Invmass(ee)(GeV)","Events/bin")

print "The scale factor for DY&Zgamma  is",k_ee
print "The scale factor for bkgs is",k_bkgs
print "*******************************************************\n\n\n"


#################### QCD scale factor ######################
###,--.             ,-----.     ,-----. ,------.        ####
###|  |,-.         '  .-.  '   '  .--./ |  .-.  \       ####
###|     /         |  | |  |   |  |     |  |  \  :      ####
###|  \  \  ,----. '  '-'  '-. '  '--'\ |  '--'  /      ####
###`--'`--' '----'  `-----'--'  `-----' `-------'       ####
#################### QCD scale factor ######################                                                    

print "*****************Calculate QCD sf********************"
hdata=elefin.Get(tag+"_ELE_pfMET_pre_ele_bjj_4qcd_data")
ndata=hdata.Integral()

summc=0.
#mcnamelist=['TTV','TTG','VV','Vgamma','ST','ZJets','WJets','TT']
mcnamelist=['TTG','VV','Zgamma','Wgamma','WJets']
for mcname in mcnamelist:
    hmc=elefin.Get(tag+"_ELE_pfMET_pre_ele_bjj_4qcd_"+mcname)
    nmc=hmc.Integral()
    summc+=nmc

hqcd=elefin.Get(tag+"_ELE_pfMET_pre_ele_bjj_4qcd_QCD")
nqcd=hqcd.Integral()

k_qcd=(ndata-summc)/nqcd
print "k_QCD = ",k_qcd
print "*******************************************************\n\n\n"

log.write("\n###############################################################")
log.write("\n############Get QCD scale factor###############################")
log.write("\n###############################################################")
log.write("\nNdata=%s;NsummedMC=%s;NQCD=%s"%(ndata,summc,nqcd))
log.write("\nk_qcd = %s"%k_qcd)
log.write("\n###############################################################")
log.write("\n###############################################################\n")


################### M3 templit fit for wjets and tt bkgs ####################
####     ,--.           ,--.          ,--.   ,--. ,----.                ##### 
####     |  |  ,---.  ,-'  '-.        |   `.'   | '.-.  |               #####
####,--. |  | | .-. : '-.  .-'        |  |'.'|  |   .' <                #####
####|  '-'  / \   --.   |  |   ,----. |  |   |  | /'-'  |               #####
#### `-----'   `----'   `--'   '----' `--'   `--' `----'                #####
################### M3 templit fit for wjets and tt bkgs ####################

print "M3 templit fit for wjets and tt bkgs"
JetM3Fitter=TemplateFitter()
JetM3histname=tag+"_ELE_BjetM3_pre_ele_bjj_"
JetM3Fitter.pushdata("SingleEle 2016 Data",elefin.Get(JetM3histname+"data"))
JetM3Fitter.subdata(elefin.Get(JetM3histname+"VV"))
#JetM3Fitter.subdata(elefin.Get(JetM3histname+"ZJets"))
JetM3Fitter.subdata(elefin.Get(JetM3histname+"TTG"))
JetM3Fitter.subdata(elefin.Get(JetM3histname+"QCD"),scal=k_qcd)

JetM3Fitter.pushmc("wjets",elefin.Get(JetM3histname+"WJets"))
JetM3Fitter.pushmc("ttbar",elefin.Get(JetM3histname+"TTG"))
#JetM3Fitter.pushmc("ttbar",elefin.Get(JetM3histname+"TT"))
#JetM3Fitter.addmc("ttbar",elefin.Get(JetM3histname+"TTG"))

JetM3Fitter.tempfit()
JetM3Fitter_result=JetM3Fitter.result
k_wjets=JetM3Fitter_result['wjets'][2]
k_ttbar=JetM3Fitter_result['ttbar'][2]
log.write("\n\n###############################################################")
log.write("\n####################JetM3Fitter##################################")
log.write("\n####################JetM3Fitter##################################")
log.write("\n%s\n"%JetM3Fitter_result)
log.write("\n The scale factor for wjets is %s"%k_wjets)
log.write("\n The scale factor for ttbar is %s"%k_ttbar)
log.write("\n#################################################################")
log.write("\n#################################################################\n\n\n")
JetM3Fitter.tempfitplot(foutname,"JetM3","Jet_M3(GeV)","Events/bin")


print "The scale factor for wjets is",k_wjets
print "The scale factor for ttbar is",k_ttbar
print "*******************************************************\n\n\n"


sys.exit()


########################################################################################################
##,--.                     ,--.   ,--.                                                                ##
##`--' ,--,--,  ,--.  ,--. |   `.'   |         ,---.   ,---.   ,--,--. ,--,--,--. ,--,--,--.  ,--,--. ##
##,--. |      \  \  `'  /  |  |'.'|  |        | .-. : | .-. | ' ,-.  | |        | |        | ' ,-.  | ##
##|  | |  ||  |   \    /   |  |   |  | ,----. \   --. ' '-' ' \ '-'  | |  |  |  | |  |  |  | \ '-'  | ##
##`--' `--''--'    `--'    `--'   `--' '----'  `----' .`-  /   `--`--' `--`--`--' `--`--`--'  `--`--' ##
##                                                    `---'                                           ##
########################################################################################################      ##Only need in elechannel, in SR1, template fit invmass(egamma) to get sfs for DY,Vgamma bkgs                 
print "Invmass(ele_gamma) templit fit for DY and Vgamma Bkgs"
InvEGFitter=TemplateFitter()
InvEGhistname=tag+"_ELE_Invlepgamma_SR1_ele_bjj_"
InvEGFitter.pushdata("SingleEle 2016 Data",elefin.Get(InvEGhistname+"data"))

InvEGFitter.pushmc("Bkgs",elefin.Get(InvEGhistname+"TTV"))
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"TTG"))
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"TT"),scal=k_ttbar)
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"WJets"),scal=k_wjets)
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"VV"))
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"ST"))
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"gammamatchnonele_ZJets"))
InvEGFitter.addmc("Bkgs",elefin.Get(InvEGhistname+"gammamatchnonele_Vgamma"))


InvEGFitter.pushmc("DY/V#gamma",elefin.Get(InvEGhistname+"gammamatchele_ZJets"))
InvEGFitter.addmc("DY/V#gamma",elefin.Get(InvEGhistname+"gammamatchele_Vgamma"))

InvEGFitter.tempfit()
InvEGFitter_result=InvEGFitter.result
k_bkgs=InvEGFitter_result['Bkgs'][2]
k_egamma=InvEGFitter_result['DY/V#gamma'][2]

log.write("\n\n####################################################################")
log.write("\n####################InvmassEG Fitter##################################")
log.write("\n####################InvmassEF Fitter##################################")
log.write("\n%s\n"%InvEGFitter_result)
log.write("\n Only in Ele channel, the scale factor for DY&Vgamma is %s"%k_egamma)
log.write("\n Only in Ele channel, the scale factor for Bkgs is %s"%k_bkgs)
log.write("\n#################################################################")
log.write("\n#################################################################\n\n\n")
InvEGFitter.tempfitplot(foutname,"SR1invEleG","Invmass(ele-gamma)(GeV)","Events/bin")

print "The scale factor for DY&Vgamma  is",k_egamma
print "The scale factor for bkgs is",k_bkgs
print "*******************************************************\n\n\n"





log.close()
