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

INPUTFile=sys.argv[1]
OUTPUTName=sys.argv[2]
print "input: ",INPUTFile
print "output: ",OUTPUTName

DoTopPt=False
if "TT" in OUTPUTName: 
    DoTopPt=True
    print "Will find gen top pair pt for this bkg"

chain_in = ROOT.TChain("ggNtuplizer/EventTree")
for inputf in INPUTFile.split():
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



dd=datetime.datetime.now().strftime("%b%d")
os.system('mkdir -p MC_Out_step1/'+OUTPUTName+'/ana_root'+dd)
os.chdir('MC_Out_step1/'+OUTPUTName+'/ana_root'+dd)
log = open("logstep1_"+OUTPUTName+"_"+str(fileID)+".txt","w")
file_out = ROOT.TFile("step1_"+OUTPUTName+"_"+str(fileID)+".root","recreate")

processdnevent = 0
# the following list used to count event numbers in order: ele,eQCD,mu,muQCD trees
Pass_1lep = [0,0,0,0]
Pass_nHLT = [0,0,0,0]
Pass_npre = [0,0,0,0]
Pass_nSR1 = [0,0,0,0]
Pass_nSR2 = [0,0,0,0]
Pass_nCR1 = [0,0,0,0]
Pass_nCR2 = [0,0,0,0]

Pass_npre_btag = [0,0,0,0]
Pass_nSR1_btag = [0,0,0,0]
Pass_nSR2_btag = [0,0,0,0]
Pass_nCR1_btag = [0,0,0,0]
Pass_nCR2_btag = [0,0,0,0]

#-----define hists for counting
Binlabel= ["TotalEvent","Pass_1lep","Pass_nHLT","Pass_npre","Pass_nSR1","Pass_nSR2","Pass_nCR1","Pass_nCR2","Pass_npre_btag","Pass_nSR1_btag","Pass_nSR2_btag","Pass_nCR1_btag","Pass_nCR2_btag","0","0","0","0","0"]
H_ele=ROOT.TH1F("H_ele","H_ele",15,0,15)
for nbin in range(15): H_ele.GetXaxis().SetBinLabel(nbin+1,Binlabel[nbin])
H_eQCD=H_ele.Clone("H_eQCD")
H_mu=H_ele.Clone("H_mu")
H_mQCD=H_ele.Clone("H_mQCD")
#H_mu=ROOT.TH1F("H_mu","H_mu",15,0,15)
#H_mQCD=ROOT.TH1F("H_mQCD","H_mQCD",15,0,15)


#--------------define branches to record seleted obj------------

BmuPt=array('d',[-99.])
BmuPt=array('d',[-99.])
BmuEn=array('d',[-99.])
BmuEta1=array('d',[-99.])
BmuPhi=array('d',[-99.])
BmuPFChIso=array('d',[-99.])
BmuPFPhoIso=array('d',[-99.])
BmuPFNeuIso=array('d',[-99.])
BmuPFPUIso=array('d',[-99.])
BmuPFMiniIso=array('d',[-99.])
BmuPFRelCombIso=array('d',[-99.])

BelePt=array('d',[-99.])
BeleEn=array('d',[-99.])
BeleEta=array('d',[-99.])
BeleSCEta=array('d',[-99.])
BelePhi=array('d',[-99.])
BelePFChIso=array('d',[-99.])
BelePFPhoIso=array('d',[-99.])
BeleNeuIso=array('d',[-99.])
BelePFPUIso=array('d',[-99.])
BeleConvVeto=array('i',[-99])
BelePFMiniIso=array('d',[-99.])
BelePFRelCombIso=array('d',[-99.])

Bregion=array('i',[-99])
BnVtx=array('i',[-99])
Brho=array('d',[-99.])
BrhoCentral=array('d',[-99.])
BpfMET=array('d',[-99.])
BpfMeTPhi=array('d',[-99.])
BPUTrue=array('d',[-99.])
BgenWeight=array('d',[-99.])
BlepMt=array('d',[-99.])
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
BCandphoSigmaIEtaIEtaFull=vector(float)(0) #phoSigmaIEtaIEtaFull5x5
BCandphoSigmaIPhiIPhiFull=vector(float)(0) #phoSigmaIPhiIPhiFull5x5
BCandphoPFChIso=vector(float)(0)
BCandphoPFCorChIso=vector(float)(0)  #corrected chiso
BCandphoGenmatch=vector(int)(0)
BCandphoLepInvMass=vector(float)(0)

BnPho=array('i',[-99])
BnFake=array('i',[-99])

BGenTopAPt=array('d',[-99.])
BGenTopBPt=array('d',[-99.])


#-----------------Define tree------------------------------
tree1_out=TTree("EventTree_ele","EventTree_ele")
tree1_out.Branch("Bregion",Bregion,"Bregion/I")
tree1_out.Branch("BnVtx",BnVtx,"BnVtx/I")
tree1_out.Branch("Brho",Brho,"Brho/D")
tree1_out.Branch("BrhoCentral",BrhoCentral,"BrhoCentral/D")
tree1_out.Branch("BPUTrue",BPUTrue,"BPUTrue/D")
tree1_out.Branch("BgenWeight",BgenWeight,"BgenWeight/D")
tree1_out.Branch("BpfMET",BpfMET,"BpfMET/D")
tree1_out.Branch("BpfMeTPhi",BpfMeTPhi,"BpfMeTPhi/D")
tree1_out.Branch("BlepMt",BlepMt,"BlepMt/D")
tree1_out.Branch("BMHT",BMHT,"BMHT/D")
tree1_out.Branch("BHT",BHT,"BHT/D")

tree1_out.Branch("BelePt",BelePt,"BelePt/D")
tree1_out.Branch("BeleEn",BeleEn,"BeleEn/D")
tree1_out.Branch("BeleEta",BeleEta,"BeleEta/D")
tree1_out.Branch("BeleSCEta",BeleSCEta,"BeleSCEta/D")
tree1_out.Branch("BelePhi",BelePhi,"BelePhi/D")
tree1_out.Branch("BelePFMiniIso",BelePFMiniIso,"BelePFMiniIso/D")
tree1_out.Branch("BelePFRelCombIso",BelePFRelCombIso,"BelePFRelCombIso/D")

tree1_out.Branch("BmuPt",BmuPt,"BmuPt/D")
tree1_out.Branch("BmuEn",BmuEn,"BmuEn/D")
tree1_out.Branch("BmuEta",BmuEta1,"BmuEta/D")
tree1_out.Branch("BmuPhi",BmuPhi,"BmuPhi/D")
tree1_out.Branch("BmuPFMiniIso",BmuPFMiniIso,"BmuPFMiniIso/D")
tree1_out.Branch("BmuPFRelCombIso",BmuPFRelCombIso,"BmuPFRelCombIso/D")

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
tree1_out.Branch("BCandphoSigmaIEtaIEtaFull",BCandphoSigmaIEtaIEtaFull)
tree1_out.Branch("BCandphoSigmaIPhiIPhiFull",BCandphoSigmaIPhiIPhiFull)
tree1_out.Branch("BCandphoPFChIso",BCandphoPFChIso)
tree1_out.Branch("BCandphoPFCorChIso",BCandphoPFCorChIso)
tree1_out.Branch("BCandphoGenmatch",BCandphoGenmatch)
tree1_out.Branch("BCandphoLepInvMass",BCandphoLepInvMass)


tree1_out.Branch("BnPho",BnPho,"BnPho/I")
tree1_out.Branch("BnFake",BnFake,"BnFake/I")

tree1_out.Branch("BGenTopAPt",BGenTopAPt,"BGenTopAPt/D")
tree1_out.Branch("BGenTopBPt",BGenTopBPt,"BGenTopBPt/D")




tree2_out=tree1_out.CloneTree(0)
tree3_out=tree1_out.CloneTree(0)
tree4_out=tree1_out.CloneTree(0)
tree2_out.SetObject("EventTree_eQCD","EventTree_eQCD")
tree3_out.SetObject("EventTree_mu","EventTree_mu")
tree4_out.SetObject("EventTree_mQCD","EventTree_mQCD")
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
    if len(elelist)==1 and elelist[0][1]==1 and len(mulist)==0: 
            Scanmode="eleTree"
            lep_ind=elelist[0][0]
            lep_Mt=(2*event.elePt[lep_ind]*event.pfMET*(1-TMath.Cos(event.elePhi[lep_ind]-event.pfMETPhi)))**0.5
    elif len(elelist)==1 and elelist[0][1]==3 and len(mulist)==0:
            Scanmode="eQCDTree"
            lep_ind=elelist[0][0]
            lep_Mt=(2*event.elePt[lep_ind]*event.pfMET*(1-TMath.Cos(event.elePhi[lep_ind]-event.pfMETPhi)))**0.5
        
        
    elif len(elelist)==0  and len(mulist)==1 and mulist[0][1]==1: 
            Scanmode="muTree"
            lep_ind=mulist[0][0]
            lep_Mt=(2*event.muPt[lep_ind]*event.pfMET*(1-TMath.Cos(event.muPhi[lep_ind]-event.pfMETPhi)))**0.5
    elif len(elelist)==0  and len(mulist)==1 and mulist[0][1]==3:
            Scanmode="mQCDTree"
            lep_ind=mulist[0][0]
            lep_Mt=(2*event.muPt[lep_ind]*event.pfMET*(1-TMath.Cos(event.muPhi[lep_ind]-event.pfMETPhi)))**0.5
    else : continue

    Scanmode_ind=["eleTree","eQCDTree","muTree","mQCDTree"].index(Scanmode)
    Pass_1lep[Scanmode_ind]+=1
#--------------1.HLT cut-------------

    CheckHLT=True
    if CheckHLT:
        if Scanmode=="eleTree": 
            hlt=event.HLTEleMuX>>3&1
        elif Scanmode=="eQCDTree": 
            hlt=1
        elif Scanmode=="muTree": 
            hlt=(event.HLTEleMuX>>19&1 and event.HLTEleMuX>>20&1)
        elif Scanmode=="mQCDTree": 
            hlt=(event.HLTEleMuX>>19&1 and event.HLTEleMuX>>20&1)

        if hlt==1: Pass_nHLT[Scanmode_ind] +=1
        else: continue

    else:   Pass_nHLT[Scanmode_ind] +=1






#-------------2.5 find photon before jets-------------
    #Candpholist: [[index,phoTag,dr_lep,corChIso,genmatch(only4mc)],[],,,]
    Candpholist=Fun_findCandpho(Scanmode,mulist,elelist,event)
    BnCandPho[0]=len(Candpholist)
    BnPho[0]=len([p for p in Candpholist if p[1]>>3&1==1])
    BnFake[0]=len([p for p in Candpholist if p[1]>>0&1==1])


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
    Bregion[0]=0  # To this step: pass the pre selection
    Pass_npre[Scanmode_ind]+=1
    if CheckBtag: Pass_npre_btag[Scanmode_ind]+=1

#-------------------------define signal region1 &2

    if BnPho[0]==1:
        Bregion[0]=1
        Pass_nSR1[Scanmode_ind]+=1
        if CheckBtag: Pass_nSR1_btag[Scanmode_ind]+=1
    elif BnPho[0]>=2:    
        Bregion[0]=2
        Pass_nSR2[Scanmode_ind]+=1
        if CheckBtag: Pass_nSR2_btag[Scanmode_ind]+=1
#------------------------------define control region 1&2 depends on fake numbers
    if BnFake[0]==1 and BnPho[0]==0:
        Bregion[0]=3
        Pass_nCR1[Scanmode_ind]+=1
        if CheckBtag: Pass_nCR1_btag[Scanmode_ind]+=1
    elif BnFake[0]>=2 and BnPho[0]==0:
        Bregion[0]=4
        Pass_nCR2[Scanmode_ind]+=1
        if CheckBtag: Pass_nCR2_btag[Scanmode_ind]+=1

#---------------Fill the pretree-----------------------------------




    BpfMET[0]=event.pfMET
    BpfMeTPhi[0]=event.pfMETPhi
    BnVtx[0]=event.nVtx
    Brho[0]=event.rho
    BrhoCentral[0]=event.rhoCentral
    BPUTrue[0]=event.puTrue[12] # puBX=12,intime pu
    BgenWeight[0]=event.genWeight
    BlepMt[0]=lep_Mt
    BMHT[0]=Fun_mht(mulist,elelist,Candpholist,jetlist,event)
    BHT[0]=Fun_ht(jetlist,event)


    if Scanmode in ["eleTree","eQCDTree"]:
        BelePt[0]=(event.elePt[lep_ind])
        BeleEn[0]=(event.eleEn[lep_ind])
        BeleEta[0]=(event.eleEta[lep_ind])
        BeleSCEta[0]=(event.eleSCEta[lep_ind])
        BelePhi[0]=(event.elePhi[lep_ind])
        BelePFMiniIso[0]=(event.elePFMiniIso[lep_ind])
        BelePFRelCombIso[0]=(elelist[0][2])

        
    if Scanmode in ["muTree","mQCDTree"]:
        BmuPt[0]=(event.muPt[lep_ind])
        BmuEn[0]=(event.muEn[lep_ind])
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
        BjetEn.push_back(event.jetEn[jet[0]])
        BjetEta.push_back(event.jetEta[jet[0]])
        BjetPhi.push_back(event.jetPhi[jet[0]])
        BjetHadFlvr.push_back(event.jetHadFlvr[0])
        Bbtagged.push_back(jet[1])
    BjetM3[0]=Fun_JetM3(jetlist,event)    

#---------------Fill gen top pair pt for sm ttbar bkgs-------------
    if DoTopPt:
        GenTopPairpt=Fun_FindGenTopPair(event)
        BGenTopAPt[0]=GenTopPairpt[0]
        BGenTopBPt[0]=GenTopPairpt[1]


#-----------------Fill the photons/fakes----------------


#    if len(Candpholist)>0: print Candpholist
    for pho in Candpholist:
        BCandPhoTag.push_back(pho[1]) 
        BCandphoEt.push_back(event.phoEt[pho[0]])
        BCandphoEta.push_back(event.phoEta[pho[0]])
        BCandphoSCEta.push_back(event.phoSCEta[pho[0]])
        BCandphoPhi.push_back(event.phoPhi[pho[0]])
        BCandphoR9.push_back(event.phoR9[pho[0]])
        BCandphoHoverE.push_back(event.phoHoverE[pho[0]])
        BCandphoSigmaIEtaIEtaFull.push_back(event.phoSigmaIEtaIEtaFull5x5[pho[0]])
        BCandphoSigmaIPhiIPhiFull.push_back(event.phoSigmaIPhiIPhiFull5x5[pho[0]])
        BCandphoPFChIso.push_back(event.phoPFChIso[pho[0]])
        BCandphoPFCorChIso.push_back(pho[3])
        BCandphoGenmatch.push_back(pho[4])
        BCandphoLepInvMass.push_back(Fun_invmass_pholep(Scanmode,lep_ind,pho[0],event))

    
    if Scanmode=="eleTree": tree1_out.Fill()
    if Scanmode=="eQCDTree": tree2_out.Fill()
    if Scanmode=="muTree": tree3_out.Fill()
    if Scanmode=="mQCDTree": tree4_out.Fill()

#----------------------clean branches for next event
    BmuPt[0]=-99.
    BmuPt[0]=-99.
    BmuEn[0]=-99.
    BmuEta1[0]=-99.
    BmuPhi[0]=-99.
    BmuPFChIso[0]=-99.
    BmuPFPhoIso[0]=-99.
    BmuPFNeuIso[0]=-99.
    BmuPFPUIso[0]=-99.
    BmuPFMiniIso[0]=-99.
    BmuPFRelCombIso[0]=-99.

    BelePt[0]=-99.
    BeleEn[0]=-99.
    BeleEta[0]=-99.
    BeleSCEta[0]=-99.
    BelePhi[0]=-99.
    BelePFChIso[0]=-99.
    BelePFPhoIso[0]=-99.
    BeleNeuIso[0]=-99.
    BelePFPUIso[0]=-99.
    BeleConvVeto[0]=-99
    BelePFMiniIso[0]=-99.
    BelePFRelCombIso[0]=-99.

    Bregion[0]=-99
    BnVtx[0]=-99
    Brho[0]=-99.
    BrhoCentral[0]=-99.
    BpfMET[0]=-99.
    BpfMeTPhi[0]=-99.
    BgenWeight[0]=-99.
    BPUTrue[0]=-99.
    BlepMt[0]=-99.
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
    BCandphoSigmaIEtaIEtaFull.clear()
    BCandphoSigmaIPhiIPhiFull.clear()
    BCandphoPFChIso.clear()
    BCandphoPFCorChIso.clear()
    BCandphoGenmatch.clear()
    BCandphoLepInvMass.clear()

    BnPho[0]=-99
    BnFake[0]=-99

    BGenTopAPt[0]=-99.    
    BGenTopBPt[0]=-99.    

#---fill the hist----
Binlist=[Pass_1lep,Pass_nHLT,Pass_npre,Pass_nSR1,Pass_nSR2,Pass_nCR1,Pass_nCR2,Pass_npre_btag,Pass_nSR1_btag,Pass_nSR2_btag,Pass_nCR1_btag,Pass_nCR2_btag]
Histlist=[H_ele,H_eQCD,H_mu,H_mQCD]
for hist in range(len(Histlist)):
    Histlist[hist].SetBinContent(1,processdnevent)
    for bin in range(len(Binlist)):
        Histlist[hist].SetBinContent(bin+2,Binlist[bin][hist])


#--------------------------------------

file_out.Write()
file_out.Close()

print "----------------------"
print "TotalEventNumber = ", processdnevent
print "Scanmode:-eleTree-|-eQCDTree-|-muTree-|-mQCDTree"
print "n_1lep pass = ", Pass_1lep
print "n_HLT pass  = ", Pass_nHLT
print "n_pre select= ", Pass_npre
print "      n_SR1 = ", Pass_nSR1
print "      n_SR2 = ", Pass_nSR2
print "      n_CR1 = ", Pass_nCR1
print "      n_CR2 = ", Pass_nCR2

print "Scanmode(with >=1 Btagget):-eleTree-|-eQCDTree-|-muTree-|-mQCDTree"
print "n_pre select= ",Pass_npre_btag
print "      n_SR1 = ", Pass_nSR1_btag
print "      n_SR2 = ", Pass_nSR2_btag
print "      n_CR1 = ", Pass_nCR1_btag
print "      n_CR2 = ", Pass_nCR2_btag



print "----------------------"


#### to write in logpre.txt
log.write("############################################################\n")
log.write("INPUT %s"%INPUTFile)
log.write("\nOutPUT %s %s"%(OUTPUTName,fileID))
log.write("\nTotalEventNumber = %s"%(event.GetEntries()))
log.write("\n%s"%datetime.datetime.now())
log.write("\nstartEntry: %s endEntry %s"%(startEntryNumber,endEntryNumber))
log.write("\nProcessedEventNumber = %s"%processdnevent)
log.write("\nScanmode:-eleTree-|-eQCDTree-|-muTree-|-mQCDTree")
log.write( "\nn_1lep pass =%s "%Pass_1lep)
log.write( "\nn_HLT pass =%s "%Pass_nHLT)
log.write("\nNoBtag requirement")
log.write("\nn_pre selection = %s"%Pass_npre)
log.write("\nn_SR1 =%s "%Pass_nSR1)
log.write("\nn_SR2 =%s "%Pass_nSR2)
log.write("\nn_CR1 =%s "%Pass_nCR1)
log.write("\nn_CR2 =%s "%Pass_nCR2)
log.write("\nWith Btag requirement nBtagged>=1")
log.write("\nn_pre selection(bjj) = %s"%Pass_npre_btag)
log.write("\nn_SR1_bjj =%s "%Pass_nSR1_btag)
log.write("\nn_SR2_bjj =%s "%Pass_nSR2_btag)
log.write("\nn_CR1_bjj =%s "%Pass_nCR1_btag)
log.write("\nn_CR2_bjj =%s "%Pass_nCR2_btag)

log.write( "\n----------------------\n\n")
log.close()


sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"

