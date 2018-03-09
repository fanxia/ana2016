#! /bin/env python

########################### configuration section ####################################
import sys
if len(sys.argv)<2:
    print >> sys.stderr, "\nError:\tNo config file in the arguments\nUsage:\t{0} configfile\n".format(sys.argv[0])
    sys.exit()
execfile(sys.argv[1])

########################### main function ####################################
from ROOT import *
gStyle.SetOptStat(0)
gROOT.SetBatch()
inf=TFile(infilename)
def newth1(tag=''):
    newh=inf.Get('{0}_{1}'.format(tagname,mcbkg[0])).Clone(tag)
    newh.Reset()
#    newh.Sumw2()
    return newh

########################### MC ratio plot with systematics ####################################
# sum plot
errall,systall=Double(),0
summc=newth1("mcsum")
for bkg in mcbkg:summc.Add(inf.Get('{0}_{1}'.format(tagname,bkg)))
evtall=summc.IntegralAndError(1,summc.GetNbinsX(),errall)
for i in range(1,summc.GetNbinsX()):
    print i,summc.GetBinContent(i),summc.GetBinError(i)
print
# adding shapeunc
unccont=[newth1() for i in range(len(shapeunc))]
for i,sp in enumerate(shapeunc):
    for bkg in mcbkg:unccont[i].Add(inf.Get('{0}_{1}Up_{2}'.format(tagname,sp,bkg))-inf.Get('{0}_{1}Down_{2}'.format(tagname,sp,bkg)))
    systall+=unccont[i].Integral(1,unccont[i].GetNbinsX())**2/4
shperr=[newth1() for i in range(len(shapeunc))]
for i in range(len(shapeunc)):
    for j in range(1,unccont[i].GetNbinsX()):
        shperr[i].SetBinError(j,abs(unccont[i].GetBinContent(j))/2.)
# adding lnNunc
unccont=[newth1() for i in range(len(lnNunc))]
for i,ln in enumerate(lnNunc):
    if ln[1]=='All':unccont[i].Add(summc,ln[0])
    else:
        mcs=[x for x in ln[1].split() if x in mcbkg]
        for bkg in mcs:unccont[i].Add(inf.Get('{0}_{1}'.format(tagname,bkg)),ln[0])
    systall+=unccont[i].Integral(1,unccont[i].GetNbinsX())**2
lnNerr=[newth1() for i in range(len(lnNunc))]
for i in range(len(lnNunc)):
    for j in range(1,unccont[i].GetNbinsX()):
        lnNerr[i].SetBinError(j,unccont[i].GetBinContent(j))
systall**=0.5
# merging error
for i in shperr: summc.Add(i)
for i in lnNerr: summc.Add(i)
for i in range(1,summc.GetNbinsX()):
    print i,summc.GetBinContent(i),summc.GetBinError(i)
print
c=inf.Get(tagname+'_c1')
ratio=c.FindObject(tagname+"_pad2").GetPrimitive("hMCstats")
leg=c.FindObject(tagname+"_pad2").GetPrimitive(tagname+"_leg2")
leg.Clear()
leg.AddEntry(ratio,'uncertainty','f')
for i in range(1,ratio.GetNbinsX()):ratio.SetBinError(i,summc.GetBinError(i)/summc.GetBinContent(i))
ratio.SetFillColor(kGray)
ratio.SetFillStyle(1001)
c.Print("step6_out/"+tagname+".pdf")

########################### MC bkgs and their systematics  ####################################
err=Double()
print 'bkg\t N\t stat\t syst'
for bkg in mcbkg+mcsig:
    mchist=inf.Get('{0}_{1}'.format(tagname,bkg))
    evt=mchist.IntegralAndError(1,mchist.GetNbinsX(),err)
    syst=0
    for sp in shapeunc:
        syst+=(inf.Get('{0}_{1}Up_{2}'.format(tagname,sp,bkg)).Integral(1,mchist.GetNbinsX())-inf.Get('{0}_{1}Down_{2}'.format(tagname,sp,bkg)).Integral(1,mchist.GetNbinsX()))**2/4

    for ln in lnNunc:
        if ln[1]=='All' or bkg in ln[1].split():syst+=(ln[0]*evt)**2
    syst**=0.5
    print '{0}\t {1:.4f}\t {2:.4f}\t {3:.4f}'.format(bkg,evt,err,syst)
print '{0}\t {1:.4f}\t {2:.4f}\t {3:.4f}'.format('All',evtall,errall,systall)
