from ROOT import *

class TemplateFitter(object):
    def __init__(self):
        self.mcsample={}
        self.mcorder={}
        self.data=TH1F()
    def pushdata(self,datan,datahist):
        self.data=datahist
        self.dataname=datan
    def adddata(self,datahist,scal=1):
        self.data.Add(datahist,scal*1)
    def subdata(self,subhist,scal=1):
        self.data.Add(subhist,-1*scal)
    def pushmc(self,mcname,mchist,scal=1,col=0):
        self.mcorder[mcname]=len(self.mcsample)
        self.mcsample[self.mcorder[mcname]]=mchist
        self.mcsample[self.mcorder[mcname]].Scale(scal)
        if col!=0:self.mcsample[self.mcorder[mcname]].SetFillColor(col)
    def addmc(self,mcname,mchist,scal=1):
#        mchist.Scale(scal)
#        print mchist.GetName()
#        self.mcsample[self.mcorder[mcname]]+=mchist
        self.mcsample[self.mcorder[mcname]].Add(mchist,scal*1)
    def tempfit(self):
        mc = TObjArray(len(self.mcsample))
        for i in self.mcsample:
            mc.Add(self.mcsample[i])
        fitself = TFractionFitter(self.data, mc)
        fitself.Fit()
        self.result={}
        for i in self.mcorder:
            self.result[i]=[Double(),Double(),Double(),Double()]
            fitself.GetResult(self.mcorder[i],self.result[i][0],self.result[i][1])
            self.result[i][2]=self.result[i][0]*self.data.Integral()/self.mcsample[self.mcorder[i]].Integral()
            self.result[i][3]=self.result[i][1]*self.data.Integral()/self.mcsample[self.mcorder[i]].Integral()

    def tempfitplot(self,foutname,plotname,xtitle,ytitle):
        self.fout=TFile.Open(foutname+".root", 'UPDATE')
        c1 = TCanvas("c1","c1", 800, 800)
        hdiff=self.data.Clone("hdiff")
        hdiffor=self.data.Clone("hdiffor")
        self.data.Draw()
#        self.data.SetAxisRange(20, 180, "X")
#        self.data.Draw()
        gStyle.SetOptStat(0)
        pad1=TPad("","",0,0.25,1,1)
        pad2=TPad("","",0,0.00,1,0.25)
        pad2.SetTopMargin(0.05)
        pad1.Draw()
        pad2.Draw()
        hs = THStack("hs"+plotname,"after applying template fit results")
        hsor = THStack("hsor"+plotname,"before template fit")
        leg= TLegend(0.62,0.65,0.90,0.90,"","brNDC")
#         for i in self.mcorder:
#             hsor.Add(self.mcsample[self.mcorder[i]],"hist")
#             newhist=self.mcsample[self.mcorder[i]].Clone("newhist")
#             newhist.Scale(self.result[i][2])
# #            hs.Add(self.mcsample[self.mcorder[i]],"hist")
#             hs.Add(newhist,"hist")
#             leg.AddEntry(self.mcsample[self.mcorder[i]],str(i),"f")

        for i in range(len(self.mcorder)):
            mcna=self.mcorder.keys()[self.mcorder.values().index(i)]
            hsor.Add(self.mcsample[i],"hist")
            newhist=self.mcsample[i].Clone("newhist")
            newhist.Scale(self.result[mcna][2])
            hs.Add(newhist,"hist")
            leg.AddEntry(self.mcsample[i],str(mcna),"f") 

        leg.AddEntry(self.data,self.dataname,"p")
        c1.cd()
        pad1.cd()
#        pad1.SetLogy()
        pad1.SetLogy(0)
        hs.SetMaximum(max(self.data.GetMaximum()*1.2,hs.GetMaximum()*1.3))
#        hs.SetMaximum(hs.GetMaximum()*10)
        hs.Draw()
        hs.GetXaxis().SetTitle(xtitle)
        hs.GetYaxis().SetTitle(ytitle)
        hs.GetYaxis().SetTitleOffset(1.2)
        self.data.Draw("Ep same")
        leg.Draw("same")
        pad2.cd()
        pad2.SetLogy(0)
        hssum=hs.GetStack().Last().Clone("hssum")
        hdiff.Divide(hssum)
        hdiff.SetTitle(";;Data/Bkgs")
        hdiff.GetYaxis().SetTitleOffset(0.5)
        hdiff.GetYaxis().SetTitleSize(0.07)
        hdiff.SetMaximum(2.)
        hdiff.SetMinimum(0.)
        hdiff.Draw("e same")
        line=TLine(0,1,hs.GetXaxis().GetXmax(),1)
        line.SetLineStyle(2)
        line.SetLineColor(kRed)
        line.Draw("same")
        c1.Print(foutname+"_tempfit"+plotname+".pdf(")


#        c1.Clear()
        pad1.cd()
        pad1.Clear()
        hsor.SetMaximum(max(self.data.GetMaximum()*1.2,hsor.GetMaximum()*1.3))
        hsor.Draw()
        hsor.GetXaxis().SetTitle(xtitle)
        hsor.GetYaxis().SetTitle(ytitle)
        hsor.GetYaxis().SetTitleOffset(1.2)
        self.data.Draw("Ep same")
        leg.Draw("same")
        pad2.cd()
#        pad2.Clear()


        pad2.SetLogy(0)
        hsorsum=hsor.GetStack().Last().Clone("hsorsum")
        hdiffor.Divide(hsorsum)
        hdiffor.SetMaximum(2.)
        hdiffor.SetMinimum(0.)
        hdiffor.Draw("e")
        hdiffor.SetTitle(";;Data/Bkgs  ")
        hdiffor.GetYaxis().SetTitleSize(0.07)
        hdiffor.GetYaxis().SetTitleOffset(0.5)
        line=TLine(0,1,hsor.GetXaxis().GetXmax(),1)
        line.SetLineStyle(2)
        line.SetLineColor(kRed)
        line.Draw("same")
        

        c1.Print(foutname+"_tempfit"+plotname+".pdf)")

        hs.Write()
        hsor.Write()
        self.data.Write()
        self.fout.Close()

