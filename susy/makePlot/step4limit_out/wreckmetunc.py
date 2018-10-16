#! /bin/env python
from ROOT import *
import os
#ELE
#inputfile='Oct16_ELE.root'
#def getname(cont,reg,mass,unc=''):return 'Oct16_ELE_{0}_SR{1}_ele_bjj_{3}_SMS_T6ttZg_{2}'.format(cont,reg,mass,unc)
#MU
inputfile='Oct16_Mu.root'
def getname(cont,reg,mass,unc=''):return 'Oct16_Mu_{0}_SR{1}_mu_bjj_{3}_SMS_T6ttZg_{2}'.format(cont,reg,mass,unc)


### output as xxx_output.root, comment out these 2 lines if you want to edit on original file #####
os.system('cp {0} {1}'.format(inputfile,inputfile.replace('.root','_sigmetupdate.root')))
inputfile=inputfile.replace('.root','_sigmetupdate.root')
###################################################################################################
f=TFile(inputfile,'update')

masslist=['Mst1500_Mnl1400', 'Mst1500_Mnl1350', 'Mst1500_Mnl1300', 'Mst1500_Mnl1200', 'Mst1500_Mnl1100', 'Mst1500_Mnl1000', 'Mst1500_Mnl900', 'Mst1500_Mnl800', 'Mst1500_Mnl700', 'Mst1500_Mnl600', 'Mst1500_Mnl500', 'Mst1500_Mnl400', 'Mst1500_Mnl300', 'Mst1500_Mnl200', 'Mst1500_Mnl100', 'Mst1500_Mnl75', 'Mst1500_Mnl50', 'Mst1500_Mnl25', 'Mst1500_Mnl10', 'Mst1450_Mnl1350', 'Mst1450_Mnl1300', 'Mst1450_Mnl1250', 'Mst1400_Mnl1300', 'Mst1400_Mnl1250', 'Mst1400_Mnl1200', 'Mst1400_Mnl1100', 'Mst1400_Mnl1000', 'Mst1400_Mnl900', 'Mst1400_Mnl800', 'Mst1400_Mnl700', 'Mst1400_Mnl600', 'Mst1400_Mnl500', 'Mst1400_Mnl400', 'Mst1400_Mnl300', 'Mst1400_Mnl200', 'Mst1400_Mnl100', 'Mst1400_Mnl75', 'Mst1400_Mnl50', 'Mst1400_Mnl25', 'Mst1400_Mnl10', 'Mst1350_Mnl1250', 'Mst1350_Mnl1200', 'Mst1350_Mnl1150', 'Mst1300_Mnl1200', 'Mst1300_Mnl1150', 'Mst1300_Mnl1100', 'Mst1300_Mnl1000', 'Mst1300_Mnl900', 'Mst1300_Mnl800', 'Mst1300_Mnl700', 'Mst1300_Mnl600', 'Mst1300_Mnl500', 'Mst1300_Mnl400', 'Mst1300_Mnl300', 'Mst1300_Mnl200', 'Mst1300_Mnl100', 'Mst1300_Mnl75', 'Mst1300_Mnl50', 'Mst1300_Mnl25', 'Mst1300_Mnl10', 'Mst1250_Mnl1150', 'Mst1250_Mnl1100', 'Mst1250_Mnl1050', 'Mst1200_Mnl1100', 'Mst1200_Mnl1050', 'Mst1200_Mnl1000', 'Mst1200_Mnl900', 'Mst1200_Mnl800', 'Mst1200_Mnl700', 'Mst1200_Mnl600', 'Mst1200_Mnl500', 'Mst1200_Mnl400', 'Mst1200_Mnl300', 'Mst1200_Mnl200', 'Mst1200_Mnl100', 'Mst1200_Mnl75', 'Mst1200_Mnl50', 'Mst1200_Mnl25', 'Mst1200_Mnl10', 'Mst1150_Mnl1050', 'Mst1150_Mnl1000', 'Mst1150_Mnl950', 'Mst1100_Mnl1000', 'Mst1100_Mnl950', 'Mst1100_Mnl900', 'Mst1100_Mnl800', 'Mst1100_Mnl700', 'Mst1100_Mnl600', 'Mst1100_Mnl500', 'Mst1100_Mnl400', 'Mst1100_Mnl300', 'Mst1100_Mnl200', 'Mst1100_Mnl100', 'Mst1100_Mnl75', 'Mst1100_Mnl50', 'Mst1100_Mnl25', 'Mst1100_Mnl10', 'Mst1050_Mnl950', 'Mst1050_Mnl900', 'Mst1050_Mnl850', 'Mst1000_Mnl900', 'Mst1000_Mnl850', 'Mst1000_Mnl800', 'Mst1000_Mnl700', 'Mst1000_Mnl600', 'Mst1000_Mnl500', 'Mst1000_Mnl400', 'Mst1000_Mnl300', 'Mst1000_Mnl200', 'Mst1000_Mnl100', 'Mst1000_Mnl75', 'Mst1000_Mnl50', 'Mst1000_Mnl25', 'Mst1000_Mnl10', 'Mst950_Mnl850', 'Mst950_Mnl800', 'Mst950_Mnl750', 'Mst900_Mnl800', 'Mst900_Mnl750', 'Mst900_Mnl700', 'Mst900_Mnl600', 'Mst900_Mnl500', 'Mst900_Mnl400', 'Mst900_Mnl300', 'Mst900_Mnl200', 'Mst900_Mnl100', 'Mst900_Mnl75', 'Mst900_Mnl50', 'Mst900_Mnl25', 'Mst900_Mnl10', 'Mst850_Mnl750', 'Mst850_Mnl700', 'Mst850_Mnl650', 'Mst800_Mnl700', 'Mst800_Mnl650', 'Mst800_Mnl600', 'Mst800_Mnl500', 'Mst800_Mnl400', 'Mst800_Mnl300', 'Mst800_Mnl200', 'Mst800_Mnl100', 'Mst800_Mnl75', 'Mst800_Mnl50', 'Mst800_Mnl25', 'Mst800_Mnl10', 'Mst750_Mnl650', 'Mst750_Mnl600', 'Mst750_Mnl550', 'Mst700_Mnl600', 'Mst700_Mnl550', 'Mst700_Mnl500', 'Mst700_Mnl400', 'Mst700_Mnl300', 'Mst700_Mnl200', 'Mst700_Mnl100', 'Mst700_Mnl10', 'Mst650_Mnl550', 'Mst650_Mnl500', 'Mst650_Mnl450', 'Mst600_Mnl500', 'Mst600_Mnl450', 'Mst600_Mnl400', 'Mst600_Mnl300', 'Mst600_Mnl200', 'Mst600_Mnl100', 'Mst600_Mnl10', 'Mst550_Mnl450', 'Mst550_Mnl400', 'Mst550_Mnl350', 'Mst500_Mnl400', 'Mst500_Mnl350', 'Mst500_Mnl300', 'Mst500_Mnl200', 'Mst500_Mnl100', 'Mst500_Mnl10', 'Mst450_Mnl350', 'Mst450_Mnl300', 'Mst450_Mnl250', 'Mst400_Mnl300', 'Mst400_Mnl250', 'Mst400_Mnl200', 'Mst400_Mnl100', 'Mst400_Mnl10', 'Mst350_Mnl250', 'Mst350_Mnl200', 'Mst350_Mnl150', 'Mst300_Mnl200', 'Mst300_Mnl150', 'Mst300_Mnl100', 'Mst300_Mnl10']
for mass in masslist:
    for reg in range(1,3):
        pfmet=f.Get(getname('pfMET',reg,mass))
        genmet=f.Get(getname('genMET',reg,mass))
        temp=pfmet-genmet
        metup=pfmet.Clone(getname('pfMET',reg,mass,'genMETUp_'))
        metdn=pfmet.Clone(getname('pfMET',reg,mass,'genMETDown_'))
        for i in range(pfmet.GetNbinsX()+2):
            metup.SetBinContent(i,pfmet.GetBinContent(i)+abs(temp.GetBinContent(i)))
            metdn.SetBinContent(i,max(0,pfmet.GetBinContent(i)-abs(temp.GetBinContent(i))))
        metup.Write(metup.GetName(),2,0)
        metdn.Write(metdn.GetName(),2,0)
print 'Done'


