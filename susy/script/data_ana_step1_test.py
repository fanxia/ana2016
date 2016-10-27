#!/bin/python

import os
import sys
import time
import datetime
import ROOT
from ROOT import *
from array import array
from ana2016.susy import *
from ana2016.susy.ana_muon import *
from ana2016.susy.ana_ele import *
from ana2016.susy.ana_jet import *
from ana2016.susy.ana_photon import *
from ana2016.susy.Utilfunc import *


sw = ROOT.TStopwatch()
sw.Start()
print "------------Start--------------"
print "input: "+sys.argv[1]
print "output: "+sys.argv[2]

if sys.argv[2]=='dataEle': Channel=111
if sys.argv[2]=='dataMu': Channel=222


chain_in = ROOT.TChain("ggNtuplizer/EventTree")
#chain_in.Add("../preselected/reduced_Muchannel_dataSingleMu.root")
chain_in.Add(sys.argv[1])
chain_in.SetBranchStatus("AK8*",0)
print"Total events for processing: ",chain_in.GetEntries()

dd=datetime.datetime.now().strftime("%b%d")
log = open("anaLog_step1.txt","a")
os.system('mkdir -p Out_step1/ana_root'+dd)
os.chdir('Out_step1/ana_root'+dd)
file_out = ROOT.TFile("step1_"+sys.argv[2]+".root","recreate")

processdnevent = 0
Pass_1lep = 0
Pass_nHLT = 0
Pass_npre = 0
Pass_nSR1 = 0
Pass_nSR2 = 0
Pass_nCR1 = 0
Pass_nCR2 = 0




#--------------define branches to record seleted obj------------

BmuPt=array('d',[-1.])
BmuEta1=array('d',[-1.])
BmuPhi=array('d',[-1.])
BmuPFChIso=array('d',[-1.])
BmuPFPhoIso=array('d',[-1.])
BmuPFNeuIso=array('d',[-1.])
BmuPFPUIso=array('d',[-1.])
BmuPFMiniIso=array('d',[-1.])
BmuPFRelCombIso=array('d',[-1.])

BelePt=array('d',[-1.])
BeleEta=array('d',[-1.])
BelePhi=array('d',[-1.])
BelePFChIso=array('d',[-1.])
BelePFPhoIso=array('d',[-1.])
BeleNeuIso=array('d',[-1.])
BelePFPUIso=array('d',[-1.])
BeleConvVeto=array('i',[-1])
BelePFMiniIso=array('d',[-1.])
BelePFRelCombIso=array('d',[-1.])

Bregion=array('i',[-1])
BnVtx=array('i',[-1])
Brho=array('d',[-1.])
BpfMET=array('d',[-1.])
BMt=array('d',[-1.])
Bnjet=array('i',[-1])
Bnbjet=array('i',[-1])

BjetPt=vector(float)(0)
BjetEta=vector(float)(0)
BjetPhi=vector(float)(0)
Bbtagged=vector(int)(0)


BnCandPho=array('i',[-1])
BCandPhoTag=vector(int)(0)  # (0,1) for (fake,photon)
BCandphoEt=vector(float)(0)
BCandphoEta=vector(float)(0)
BCandphoPhi=vector(float)(0)
BCandphoR9=vector(float)(0)
BCandphoHoverE=vector(float)(0)
BCandphoSigmaIEtaIEta=vector(float)(0)
BCandphoSigmaIPhiIPhi=vector(float)(0)
BCandphoPFChIso=vector(float)(0)

BnPho=array('i',[-1])
BnFake=array('i',[-1])



#-----------------Define tree------------------------------
if Channel==111:
    tree_out=TTree("EventTree_ele","EventTree_ele")
if Channel==222:
    tree_out=TTree("EventTree_mu","EventTree_mu")
tree_out.Branch("Bregion",Bregion,"Bregion/I")
tree_out.Branch("BnVtx",BnVtx,"BnVtx/I")
tree_out.Branch("Brho",Brho,"Brho/D")
tree_out.Branch("BpfMET",BpfMET,"BpfMET/D")
tree_out.Branch("BMt",BMt,"BMt/D")

if Channel==111:
    tree_out.Branch("BelePt",BelePt,"BelePt/D")
    tree_out.Branch("BeleEta",BeleEta,"BeleEta/D")
    tree_out.Branch("BelePhi",BelePhi,"BelePhi/D")
    tree_out.Branch("BelePFMiniIso",BelePFMiniIso,"BelePFMiniIso/D")
    tree_out.Branch("BelePFRelCombIso",BelePFRelCombIso,"BelePFRelCombIso/D")

if Channel==222:
    tree_out.Branch("BmuPt",BmuPt,"BmuPt/D")
    tree_out.Branch("BmuEta",BmuEta1,"BmuEta/D")
    tree_out.Branch("BmuPhi",BmuPhi,"BmuPhi/D")
#    tree_out.Branch("BmuPFChIso",BmuPFChIso,"BmuPFChIso/D")
    tree_out.Branch("BmuPFMiniIso",BmuPFMiniIso,"BmuPFMiniIso/D")
    tree_out.Branch("BmuPFRelCombIso",BmuPFRelCombIso,"BmuPFRelCombIso/D")

    

tree_out.Branch("Bnjet",Bnjet,"Bnjet/I")
tree_out.Branch("Bnbjet",Bnbjet,"Bnbjet/I")
tree_out.Branch("BjetPt",BjetPt)
tree_out.Branch("BjetEta",BjetEta)
tree_out.Branch("Bbtagged",Bbtagged)

tree_out.Branch("BnCandPho",BnCandPho,"BnCandPho/I")
tree_out.Branch("BCandPhoTag",BCandPhoTag)
tree_out.Branch("BCandphoEt",BCandphoEt)
tree_out.Branch("BCandphoEta",BCandphoEta)
tree_out.Branch("BCandphoPhi",BCandphoPhi)
tree_out.Branch("BCandphoR9",BCandphoR9)
tree_out.Branch("BCandphoHoverE",BCandphoHoverE)
tree_out.Branch("BCandphoSigmaIEtaIEta",BCandphoSigmaIEtaIEta)
tree_out.Branch("BCandphoSigmaIPhiIPhi",BCandphoSigmaIPhiIPhi)
tree_out.Branch("BCandphoPFChIso",BCandphoPFChIso)

tree_out.Branch("BnPho",BnPho,"BnPho/I")
tree_out.Branch("BnFake",BnFake,"BnFake/I")



treeQCD_out=tree_out.CloneTree(0)
if Channel==111:
    treeQCD_out.SetName("EventTree_eQCD")
if Channel==222:
    treeQCD_out.SetName("EventTree_mQCD")
#--------


PassQCD_1lep = 0
PassQCD_nHLT = 0
PassQCD_npre = 0
PassQCD_nSR1 = 0
PassQCD_nSR2 = 0
PassQCD_nCR1 = 0
PassQCD_nCR2 = 0


for event in chain_in :

    (processdnevent)+=1
    if (processdnevent)%10000 ==0:
        print "Processing entry ", processdnevent


#----------0.event clean and modesetting----------

    QCDmode=False
    Sigmode=False
    if not event.hasGoodVtx: continue


   # elelist:[[index,ID,iso],[]...]
   # mulist: [[index,ID,iso],[]...]
    mulist=Fun_findmu(event)
    elelist=Fun_findele(event)




#-------------1. Only one tight lepton(OR one tight QCDlep)-------
    if Channel==111:
        if len(elelist)==1 and elelist[0][1]==1 and len(mulist)==0: 
            Sigmode=True
            lep_ind=elelist[0][0]
            lep_Mt=(2*event.elePt[lep_ind]*event.pfMET*(1-TMath.Cos(event.elePhi[lep_ind]-event.pfMETPhi)))**0.5
        elif len(elelist)==1 and elelist[0][1]==3 and len(mulist)==0:
            QCDmode=True
            lep_ind=elelist[0][0]
            lep_Mt=(2*event.elePt[lep_ind]*event.pfMET*(1-TMath.Cos(event.elePhi[lep_ind]-event.pfMETPhi)))**0.5
        
        
    if Channel==222:  
        if len(elelist)==0  and len(mulist)==1 and mulist[0][1]==1: 
            Sigmode=True
            lep_ind=mulist[0][0]
            lep_Mt=(2*event.muPt[lep_ind]*event.pfMET*(1-TMath.Cos(event.muPhi[lep_ind]-event.pfMETPhi)))**0.5
        elif len(elelist)==0  and len(mulist)==1 and mulist[0][1]==3:
            QCDmode=True
            lep_ind=mulist[0][0]
            lep_Mt=(2*event.muPt[lep_ind]*event.pfMET*(1-TMath.Cos(event.muPhi[lep_ind]-event.pfMETPhi)))**0.5
    if not (Sigmode or QCDmode) : continue
    if Sigmode:    Pass_1lep+=1
    if QCDmode:    PassQCD_1lep+=1


#--------------1.HLT cut-------------

    if Channel==111 and Sigmode: hlt=event.HLTEleMuX>>55&1
    if Channel==111 and QCDmode: hlt=1
    if Channel==222 and (Sigmode or QCDmode): hlt=(event.HLTEleMuX>>31&1 and event.HLTEleMuX>>32&1)

    if not hlt: continue
    if Sigmode:    Pass_nHLT+=1
    if QCDmode:    PassQCD_nHLT+=1




#-------------2.5 find photon before jets-------------
    #Candpholist: [[index,dr_lep,phoTag],[],[],,,]
    Candpholist=Fun_findCandpho(Channel,lep_ind,event)
    BnCandPho[0]=len(Candpholist)
    BnPho[0]=len([p for p in Candpholist if p[1]==1])
    BnFake[0]=len([p for p in Candpholist if p[1]==0])


#---------------3. more than 3 jets and at least 1 btagged----
    # jetlist:[[index,btagged],[],[],...]

    CheckBtag=True
    GoodJets=False
    jetlist=Fun_findjet(Candpholist,event)
    nbtagged=sum(jet[1] for jet in jetlist)
    if CheckBtag==False and len(jetlist)>=3: GoodJets=True
    if CheckBtag and len(jetlist)>=3 and nbtagged>=1: GoodJets=True

    if not GoodJets: continue



#-------------------------define signal region1 &2
    Bregion[0]=0
    if BnPho[0]==1:
        Bregion[0]=1
        if Sigmode:(Pass_nSR1)+=1
        if QCDmode:(PassQCD_nSR1)+=1

    elif BnPho[0]>=2:    
        Bregion[0]=2
        if Sigmode:(Pass_nSR2)+=1
        if QCDmode:(PassQCD_nSR2)+=1

#------------------------------define control region 1&2 depends on fake numbers
    if BnFake[0]==1 and BnPho[0]==0:
        Bregion[0]=3
        if Sigmode:(Pass_nCR1)+=1
        if QCDmode:(PassQCD_nCR1)+=1

    elif BnFake[0]>=2 and BnPho[0]==0:
        Bregion[0]=4
        if Sigmode:(Pass_nCR2)+=1
        if QCDmode:(PassQCD_nCR2)+=1

#---------------Fill the pretree-----------------------------------
    if Sigmode:(Pass_npre)+=1
    if QCDmode:(PassQCD_npre)+=1



    BpfMET[0]=event.pfMET
    BnVtx[0]=event.nVtx
    Brho[0]=event.rho
    BMt[0]=lep_Mt
    if Channel==111:
        BelePt[0]=(event.elePt[lep_ind])
        BeleEta[0]=(event.eleEta[lep_ind])
        BelePhi[0]=(event.elePhi[lep_ind])
        BelePFMiniIso[0]=(event.elePFMiniIso[lep_ind])
        BelePFRelCombIso[0]=(elelist[0][2])

        

    if Channel==222:
        BmuPt[0]=(event.muPt[lep_ind])
        BmuEta1[0]=(event.muEta[lep_ind])
        BmuPhi[0]=(event.muPhi[lep_ind])
#        BmuPFChIso[0]=(event.muPFChIso[lep_ind])
#        BmuPFPhoIso[0]=(event.muPFPhoIso[lep_ind])
#        BmuPFNeuIso[0]=(event.muPFNeuIso[lep_ind])
#        BmuPFPUIso[0]=(event.muPFPUIso[lep_ind])
        BmuPFMiniIso[0]=(event.muPFMiniIso[lep_ind])
        BmuPFRelCombIso[0]=(mulist[0][2])

    Bnjet[0]=len(jetlist)
    Bnbjet[0]=nbtagged
    for jet in jetlist:
        BjetPt.push_back(event.jetPt[jet[0]])
        BjetEta.push_back(event.jetEta[jet[0]])
        Bbtagged.push_back(jet[1])

#-----------------Fill the photons/fakes----------------


#    if len(Candpholist)>0: print Candpholist
    for pho in Candpholist:
        BCandPhoTag.push_back(pho[1]) 
        BCandphoEt.push_back(event.phoEt[pho[0]])
        BCandphoEta.push_back(event.phoEta[pho[0]])
        BCandphoPhi.push_back(event.phoPhi[pho[0]])
        BCandphoR9.push_back(event.phoR9[pho[0]])
        BCandphoHoverE.push_back(event.phoHoverE[pho[0]])
        BCandphoSigmaIEtaIEta.push_back(event.phoSigmaIEtaIEta[pho[0]])
        BCandphoSigmaIPhiIPhi.push_back(event.phoSigmaIPhiIPhi[pho[0]])
        BCandphoPFChIso.push_back(event.phoPFChIso[pho[0]])


#    for fake in fakelist: 
#        BfakeEt.push_back(event.phoEt[fake[0]])
#        BfakeEta.push_back(event.phoEta[fake[0]])
#        BfakePhi.push_back(event.phoPhi[fake[0]])
#        BfakeR9.push_back(event.phoR9[fake[0]])
#        BfakeSigmaIEtaIEta.push_back(event.phoSigmaIEtaIEta[fake[0]])
#        BfakeSigmaIPhiIPhi.push_back(event.phoSigmaIPhiIPhi[fake[0]])
#        BfakePFChIso.push_back(event.phoPFChIso[fake[0]])




    
    if Sigmode: tree_out.Fill()
    if QCDmode: treeQCD_out.Fill()
#----------------------clean branches for next event
    BjetPt.clear()
    BjetEta.clear()
    BjetPhi.clear()
    Bbtagged.clear()

    BCandPhoTag.clear()
    BCandphoEt.clear()
    BCandphoEta.clear()
    BCandphoPhi.clear()
    BCandphoR9.clear()
    BCandphoHoverE.clear()
    BCandphoSigmaIEtaIEta.clear()
    BCandphoSigmaIPhiIPhi.clear()
    BCandphoPFChIso.clear()

#    BfakeEt.clear()
#    BfakeEta.clear()
#    BfakePhi.clear()
#    BfakeR9.clear()
#    BfakeSigmaIEtaIEta.clear()
#    BfakeSigmaIPhiIPhi.clear()
#    BfakePFChIso.clear()
        
        


file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", processdnevent
print "n_1lep pass = ", Pass_1lep
print "n_HLT pass = ", Pass_nHLT
print "n_pre selection = ",Pass_npre
print "n_SR1 = ", Pass_nSR1
print "n_SR2 = ", Pass_nSR2
print "n_CR1 = ", Pass_nCR1
print "n_CR2 = ", Pass_nCR2

print "QCDn_1lep pass = ", PassQCD_1lep
print "QCDn_HLT pass = ", PassQCD_nHLT
print "QCDn_pre selection = ",PassQCD_npre
print "QCDn_SR1 = ", PassQCD_nSR1
print "QCDn_SR2 = ", PassQCD_nSR2
print "QCDn_CR1 = ", PassQCD_nCR1
print "QCDn_CR2 = ", PassQCD_nCR2
print "----------------------"


#### to write in logpre.txt
log.write("############################################################\n")
log.write("INPUT %s"%sys.argv[1])
log.write("\nOutPUT %s\n"%sys.argv[2])
log.write("%s"%datetime.datetime.now())
log.write("\nTotalEventNumber = %s"%processdnevent)
log.write( "\nn_1lep pass =%s "%Pass_1lep)
log.write( "\nn_HLT pass =%s "%Pass_nHLT)
log.write("\nn_pre selection = %s"%Pass_npre)
log.write("\nn_SR1 =%s "%Pass_nSR1)
log.write("\nn_SR2 =%s "%Pass_nSR2)
log.write("\nn_CR1 =%s "%Pass_nCR1)
log.write("\nn_CR2 =%s "%Pass_nCR2)
log.write( "\nnQCD_1lep pass =%s "%PassQCD_1lep)
log.write( "\nnQCD_HLT pass =%s "%PassQCD_nHLT)
log.write("\nnQCD_pre selection = %s"%PassQCD_npre)
log.write("\nnQCD_SR1 =%s "%PassQCD_nSR1)
log.write("\nnQCD_SR2 =%s "%PassQCD_nSR2)
log.write("\nnQCD_CR1 =%s "%PassQCD_nCR1)
log.write("\nnQCD_CR2 =%s "%PassQCD_nCR2)

log.write( "\n----------------------\n\n")
log.close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"

