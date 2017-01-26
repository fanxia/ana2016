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

INPUTFileN=sys.argv[1]
OUTPUTName=sys.argv[2]
print "input: ",INPUTFileN
print "output: ",OUTPUTName


chain_in = ROOT.TChain("ggNtuplizer/EventTree")
for inputf in INPUTFileN.split():
    chain_in.Add(inputf)
chain_in.SetBranchStatus("AK8*",0)
#print"Total events for processing: ",chain_in.GetEntries()
event=chain_in

if len(sys.argv)>4:
    fileID=int(sys.argv[3])
    startEntryNumber=int(sys.argv[4])
    endEntryNumber=int(sys.argv[5])
elif len(sys.argv)==4:
    fileID=int(sys.argv[3])
    startEntryNumber=0
    endEntryNumber=chain_in.GetEntries()
else:
    fileID=-999
    startEntryNumber=0
    endEntryNumber=chain_in.GetEntries()

print "fileID: ",fileID
print "startEntryNumber: ",startEntryNumber
print "endEntryNumber: ",endEntryNumber
fileIDn=fileID


dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p MC_dilepOut_step1/'+OUTPUTName+'/dilepana_root'+dd)
os.chdir('MC_dilepOut_step1/'+OUTPUTName+'/dilepana_root'+dd)
log = open("logstep1-dilep_"+OUTPUTName+"_"+str(fileID)+".txt","w")
file_out = ROOT.TFile("step1-dilep_"+OUTPUTName+"_"+str(fileID)+".root","recreate")

processdnevent = 0
# the following list used to count event numbers in order: ele,eQCD,mu,muQCD trees
Pass_1lep = [0,0,0,0]
Pass_nHLT = [0,0,0,0]
Pass_npre = [0,0,0,0]

Pass_npre_btag = [0,0,0,0]


#-----define hists for counting
Binlabel= ["TotalEvent","Pass_1lep","Pass_nHLT","Pass_npre","Pass_npre_btag","0","0","0","0","0"]
H_ee=ROOT.TH1F("H_ee","H_ele",10,0,10)
for nbin in range(10): H_ee.GetXaxis().SetBinLabel(nbin+1,Binlabel[nbin])
H_eeQCD=H_ee.Clone("H_eeQCD")
H_mumu=H_ee.Clone("H_mumu")
H_mmQCD=H_ee.Clone("H_mmQCD")


#--------------define branches to record seleted obj------------

BmuPt=vector(float)(0)
BmuPt=vector(float)(0)
BmuEn=vector(float)(0)
BmuEta1=vector(float)(0)
BmuPhi=vector(float)(0)
BmuPFChIso=vector(float)(0)
BmuPFPhoIso=vector(float)(0)
BmuPFNeuIso=vector(float)(0)
BmuPFPUIso=vector(float)(0)
BmuPFMiniIso=vector(float)(0)
BmuPFRelCombIso=vector(float)(0)
BmumuInvMass=array('d',[-99.])

BelePt=vector(float)(0)
BeleEn=vector(float)(0)
BeleEta=vector(float)(0)
BeleSCEta=vector(float)(0)
BelePhi=vector(float)(0)
BelePFChIso=vector(float)(0)
BelePFPhoIso=vector(float)(0)
BeleNeuIso=vector(float)(0)
BelePFPUIso=vector(float)(0)
BeleConvVeto=vector(int)(0)
BelePFMiniIso=vector(float)(0)
BelePFRelCombIso=vector(float)(0)
BeeInvMass=array('d',[-99.])

BnVtx=array('i',[-99])
Brho=array('d',[-99.])
BrhoCentral=array('d',[-99.])
BpfMET=array('d',[-99.])
BpfMeTPhi=array('d',[-99.])
BPUTrue=array('d',[-99.])
BgenWeight=array('d',[-99.])
BMHT=array('d',[-99.])
BHT=array('d',[-99.])
Bnjet=array('i',[-99])
Bnbjet=array('i',[-99])

BjetPt=vector(float)(0)
BjetEn=vector(float)(0)
BjetEta=vector(float)(0)
BjetPhi=vector(float)(0)
BjetHadFlvr=vector(int)(0)
Bbtagged=vector(int)(0)
BjetM3=array('d',[-99])

BnCandPho=array('i',[-99])
BCandPhoTag=vector(int)(0)  # tag>>(3,0,1,2)&1 for (photon,fake,wo..,wo..)
BCandphoEt=vector(float)(0)
BCandphoEta=vector(float)(0)
BCandphoSCEta=vector(float)(0)
BCandphoPhi=vector(float)(0)
BCandphoR9=vector(float)(0)
BCandphoHoverE=vector(float)(0)
BCandphoSigmaIEtaIEta=vector(float)(0)
BCandphoSigmaIPhiIPhi=vector(float)(0)
BCandphoPFChIso=vector(float)(0)
BCandphoGenmatch=vector(int)(0)
#BCandphoLepInvMass=vector(float)(0)




#-----------------Define tree------------------------------
tree1_out=TTree("EventTree_ee","EventTree_ee")
tree1_out.Branch("BnVtx",BnVtx,"BnVtx/I")
tree1_out.Branch("Brho",Brho,"Brho/D")
tree1_out.Branch("BrhoCentral",BrhoCentral,"BrhoCentral/D")
tree1_out.Branch("BPUTrue",BPUTrue,"BPUTrue/D")
tree1_out.Branch("BgenWeight",BgenWeight,"BgenWeight/D")
tree1_out.Branch("BpfMET",BpfMET,"BpfMET/D")
tree1_out.Branch("BpfMeTPhi",BpfMeTPhi,"BpfMeTPhi/D")
tree1_out.Branch("BMHT",BMHT,"BMHT/D")
tree1_out.Branch("BHT",BHT,"BHT/D")

tree1_out.Branch("BelePt",BelePt)
tree1_out.Branch("BeleEn",BeleEn)
tree1_out.Branch("BeleEta",BeleEta)
tree1_out.Branch("BeleSCEta",BeleSCEta)
tree1_out.Branch("BelePhi",BelePhi)
tree1_out.Branch("BelePFMiniIso",BelePFMiniIso)
tree1_out.Branch("BelePFRelCombIso",BelePFRelCombIso)
tree1_out.Branch("BeeInvMass",BeeInvMass,"BeeInvMass/D")

tree1_out.Branch("BmuPt",BmuPt)
tree1_out.Branch("BmuEn",BmuEn)
tree1_out.Branch("BmuEta",BmuEta1)
tree1_out.Branch("BmuPhi",BmuPhi)
tree1_out.Branch("BmuPFMiniIso",BmuPFMiniIso)
tree1_out.Branch("BmuPFRelCombIso",BmuPFRelCombIso)
tree1_out.Branch("BmumuInvMass",BmumuInvMass,"BmumuInvMass/D")

tree1_out.Branch("Bnjet",Bnjet,"Bnjet/I")
tree1_out.Branch("Bnbjet",Bnbjet,"Bnbjet/I")
tree1_out.Branch("BjetPt",BjetPt)
tree1_out.Branch("BjetEn",BjetEn)
tree1_out.Branch("BjetEta",BjetEta)
tree1_out.Branch("BjetPhi",BjetPhi)
tree1_out.Branch("BjetHadFlvr",BjetHadFlvr)
tree1_out.Branch("Bbtagged",Bbtagged)
tree1_out.Branch("BjetM3",BjetM3,"BjetM3/D")

tree1_out.Branch("BnCandPho",BnCandPho,"BnCandPho/I")
tree1_out.Branch("BCandPhoTag",BCandPhoTag)
tree1_out.Branch("BCandphoEt",BCandphoEt)
tree1_out.Branch("BCandphoEta",BCandphoEta)
tree1_out.Branch("BCandphoSCEta",BCandphoSCEta)
tree1_out.Branch("BCandphoPhi",BCandphoPhi)
tree1_out.Branch("BCandphoR9",BCandphoR9)
tree1_out.Branch("BCandphoHoverE",BCandphoHoverE)
tree1_out.Branch("BCandphoSigmaIEtaIEta",BCandphoSigmaIEtaIEta)
tree1_out.Branch("BCandphoSigmaIPhiIPhi",BCandphoSigmaIPhiIPhi)
tree1_out.Branch("BCandphoPFChIso",BCandphoPFChIso)
tree1_out.Branch("BCandphoGenmatch",BCandphoGenmatch)
#tree1_out.Branch("BCandphoLepInvMass",BCandphoLepInvMass)


tree2_out=tree1_out.CloneTree(0)
tree3_out=tree1_out.CloneTree(0)
tree4_out=tree1_out.CloneTree(0)
tree2_out.SetObject("EventTree_eeQCD","EventTree_eeQCD")
tree3_out.SetObject("EventTree_mumu","EventTree_mumu")
tree4_out.SetObject("EventTree_mmQCD","EventTree_mmQCD")
#--------


#for event in chain_in :
for entrynumber in range(startEntryNumber,endEntryNumber):
    event.GetEntry(entrynumber)
#    print "entry:",entrynumber

    (processdnevent)+=1
    if (processdnevent)%10000 ==0:
        print "Processing entry ", processdnevent
#    print "Processing entry ", processdnevent

#----------0.event clean and modesetting----------



    Scanmode="None"
    if not event.isPVGood: continue

   # elelist:[[index,ID,iso],[]...]
   # mulist: [[index,ID,iso],[]...]
   # ID: 0 for loose, 1 for tight, 3 for QCDmode
    mulist=Fun_findmu(event)
    elelist=Fun_findele(event)



#-------------1. Only one tight lepton(OR one tight QCDlep)-------
    if len(elelist)==2 and elelist[0][1]==1 and elelist[1][1]==1 and len(mulist)==0: 
            Scanmode="eeTree"
    elif len(elelist)==2 and elelist[0][1]==3 and elelist[1][1]==3 and len(mulist)==0:
            Scanmode="eeQCDTree"
        
        
    elif len(elelist)==0  and len(mulist)==2 and mulist[0][1]==1 and mulist[1][1]==1: 
            Scanmode="mumuTree"
    elif len(elelist)==0  and len(mulist)==2 and mulist[0][1]==3 and mulist[1][1]==3:
            Scanmode="mmQCDTree"
    else : continue

    Scanmode_ind=["eeTree","eeQCDTree","mumuTree","mmQCDTree"].index(Scanmode)
    Pass_1lep[Scanmode_ind]+=1
#--------------1.HLT cut-------------

    CheckHLT=False
    if CheckHLT:
        if Scanmode=="eeTree": 
            hlt=event.HLTEleMuX>>55&1
        elif Scanmode=="eeQCDTree": 
            hlt=1
        elif Scanmode=="mumuTree": 
            hlt=(event.HLTEleMuX>>31&1 and event.HLTEleMuX>>32&1)
        elif Scanmode=="mmQCDTree": 
            hlt=(event.HLTEleMuX>>31&1 and event.HLTEleMuX>>32&1)

        if hlt==1: Pass_nHLT[Scanmode_ind] +=1
        else: continue

    else:   Pass_nHLT[Scanmode_ind] +=1






#-------------2.5 find photon before jets-------------
    #original Candpholist: [[index,phoTag,dr_lep,genmatch(only4mc)],[],[],,,]
    #for the dilepton event selection, only save the loose photon(no fake...)
    Candpholist1=Fun_findCandpho(Scanmode,mulist,elelist,event)
    Candpholist=[p for p in Candpholist1 if p[1]>>3&1==1]
    BnCandPho[0]=len(Candpholist)


#---------------3. more than 3 jets and at least 1 btagged----
    # jetlist:[[index,btagged],[],[],...]

    CheckBtag=False
    GoodJets=False
    jetlist=Fun_findjet(Scanmode,mulist,elelist,Candpholist,event)
    nbtagged=sum(jet[1] for jet in jetlist)
    if len(jetlist)>=3: 
        GoodJets=True
        if nbtagged>=1: CheckBtag=True

    if not GoodJets: continue

    Pass_npre[Scanmode_ind]+=1
    if CheckBtag: Pass_npre_btag[Scanmode_ind]+=1

#---------------Fill the pretree-----------------------------------


    BpfMET[0]=event.pfMET
    BpfMeTPhi[0]=event.pfMETPhi
    BnVtx[0]=event.nVtx
    Brho[0]=event.rho
    BrhoCentral[0]=event.rhoCentral
    BPUTrue[0]=event.puTrue[12] # puBX=12,intime pu
    BgenWeight[0]=event.genWeight
    BMHT[0]=Fun_mht(mulist,elelist,Candpholist,jetlist,event)
    BHT[0]=Fun_ht(jetlist,event)
    if Scanmode in ["eeTree","eeQCDTree"]:
        BeeInvMass[0]=Fun_invmass_dilep(Scanmode,elelist,event)
        for ele in elelist:
            BelePt.push_back(event.elePt[ele[0]])
            BeleEn.push_back(event.eleEn[ele[0]])
            BeleEta.push_back(event.eleEta[ele[0]])
            BeleSCEta.push_back(event.eleSCEta[ele[0]])
            BelePhi.push_back(event.elePhi[ele[0]])
            BelePFMiniIso.push_back(event.elePFMiniIso[ele[0]])
            BelePFRelCombIso.push_back(elelist[0][2])

        
    if Scanmode in ["muTree","mQCDTree"]:
        BmumuInvMass[0]=Fun_invmass_dilep(Scanmode,mulist,event)
        for mu in mulist:
            BmuPt.push_back(event.muPt[mu[0]])
            BmuEn.push_back(event.muEn[mu[0]])
            BmuEta1.push_back(event.muEta[mu[0]])
            BmuPhi.push_back(event.muPhi[mu[0]])
            #        BmuPFChIso.push_back(event.muPFChIso[mu[0]])
            #        BmuPFPhoIso.push_back(event.muPFPhoIso[mu[0]])
            #        BmuPFNeuIso.push_back(event.muPFNeuIso[mu[0]])
            #        BmuPFPUIso.push_back(event.muPFPUIso[mu[0]])
            BmuPFMiniIso.push_back(event.muPFMiniIso[mu[0]])
            BmuPFRelCombIso.push_back(mulist[0][2])

    Bnjet[0]=len(jetlist)
    Bnbjet[0]=nbtagged
    for jet in jetlist:
        BjetPt.push_back(event.jetPt[jet[0]])
        BjetEn.push_back(event.jetEn[jet[0]])
        BjetEta.push_back(event.jetEta[jet[0]])
        BjetPhi.push_back(event.jetPhi[jet[0]])
        BjetHadFlvr.push_back(event.jetHadFlvr[0])
        Bbtagged.push_back(jet[1])
    BjetM3[0]=Fun_JetM3(jetlist,event)    
#-----------------Fill the photons----------------

    for pho in Candpholist:
        BCandPhoTag.push_back(pho[1]) 
        BCandphoEt.push_back(event.phoEt[pho[0]])
        BCandphoEta.push_back(event.phoEta[pho[0]])
        BCandphoSCEta.push_back(event.phoSCEta[pho[0]])
        BCandphoPhi.push_back(event.phoPhi[pho[0]])
        BCandphoR9.push_back(event.phoR9[pho[0]])
        BCandphoHoverE.push_back(event.phoHoverE[pho[0]])
        BCandphoSigmaIEtaIEta.push_back(event.phoSigmaIEtaIEta[pho[0]])
        BCandphoSigmaIPhiIPhi.push_back(event.phoSigmaIPhiIPhi[pho[0]])
        BCandphoPFChIso.push_back(event.phoPFChIso[pho[0]])
        BCandphoGenmatch.push_back(pho[3])
#        BCandphoLepInvMass.push_back(Fun_invmass_pholep(Scanmode,lep_ind,pho[0],event))

    
    if Scanmode=="eeTree": tree1_out.Fill()
    if Scanmode=="eeQCDTree": tree2_out.Fill()
    if Scanmode=="mumuTree": tree3_out.Fill()
    if Scanmode=="mmQCDTree": tree4_out.Fill()

#----------------------clean branches for next event
    BmuPt.clear()
    BmuPt.clear()
    BmuEn.clear()
    BmuEta1.clear()
    BmuPhi.clear()
    BmuPFChIso.clear()
    BmuPFPhoIso.clear()
    BmuPFNeuIso.clear()
    BmuPFPUIso.clear()
    BmuPFMiniIso.clear()
    BmuPFRelCombIso.clear()

    BelePt.clear()
    BeleEn.clear()
    BeleEta.clear()
    BeleSCEta.clear()
    BelePhi.clear()
    BelePFChIso.clear()
    BelePFPhoIso.clear()
    BeleNeuIso.clear()
    BelePFPUIso.clear()
#    BeleConvVeto.clear()
    BelePFMiniIso.clear()
    BelePFRelCombIso.clear()

    BnVtx[0]=-99
    Brho[0]=-99.
    BrhoCentral[0]=-99.
    BpfMET[0]=-99.
    BpfMeTPhi[0]=-99.
    BgenWeight[0]=-99.
    BPUTrue[0]=-99.
    Bnjet[0]=-99
    Bnbjet[0]=-99
    
    BjetPt.clear()
    BjetEn.clear()
    BjetEta.clear()
    BjetPhi.clear()
    BjetHadFlvr.clear()
    Bbtagged.clear()
    BjetM3[0]=-99.

    BnCandPho[0]=-99
    BCandPhoTag.clear()
    BCandphoEt.clear()
    BCandphoEta.clear()
    BCandphoSCEta.clear()
    BCandphoPhi.clear()
    BCandphoR9.clear()
    BCandphoHoverE.clear()
    BCandphoSigmaIEtaIEta.clear()
    BCandphoSigmaIPhiIPhi.clear()
    BCandphoPFChIso.clear()
    BCandphoGenmatch.clear()
#    BCandphoLepInvMass.clear()



#---fill the hist----
Binlist=[Pass_1lep,Pass_nHLT,Pass_npre,Pass_npre_btag]
Histlist=[H_ee,H_eeQCD,H_mumu,H_mmQCD]
for hist in range(len(Histlist)):
    Histlist[hist].SetBinContent(1,processdnevent)
    for bin in range(len(Binlist)):
        Histlist[hist].SetBinContent(bin+2,Binlist[bin][hist])


#--------------------------------------

file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", processdnevent
print "Scanmode:-eeTree-|-eeQCDTree-|-mumuTree-|-mmQCDTree"
print "n_1lep pass = ", Pass_1lep
print "n_HLT pass  = ", Pass_nHLT
print "n_pre select= ", Pass_npre

print "Scanmode(with >=1 Btagged):-eeTree-|-eeQCDTree-|-mumuTree-|-mmQCDTree"
print "n_pre select= ",Pass_npre_btag
print "----------------------"


#### to write in logpre.txt
log.write("############################################################\n")
log.write("INPUT %s"%INPUTFileN)
log.write("\nOutPUT %s %s"%(OUTPUTName,fileIDn))
log.write("\nTotalEventNumber = %s"%(event.GetEntries()))
log.write("\n%s"%datetime.datetime.now())
log.write("\nstartEntry: %s endEntry %s"%(startEntryNumber,endEntryNumber))
log.write("\nProcessedEventNumber = %s"%processdnevent)
log.write("\nScanmode:-eeTree-|-eeQCDTree-|-mumuTree-|-mumuQCDTree")
log.write( "\nn_1lep pass =%s "%Pass_1lep)
log.write( "\nn_HLT pass =%s "%Pass_nHLT)
log.write("\nNoBtag requirement")
log.write("\nn_pre selection = %s"%Pass_npre)
log.write("\nWith Btag requirement nBtagged>=1")
log.write("\nn_pre selection(bjj) = %s"%Pass_npre_btag)
log.write( "\n----------------------\n\n")
log.close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"

