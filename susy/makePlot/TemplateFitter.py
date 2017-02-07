from ROOT import *

class TemplateFitter(object):
    def __init__(self):
        self.mcsample={}
        self.mcorder={}
        self.data=TH1F()
    def pushdata(self,datan,datahist):
        self.data=datahist
        self.dataname=datan
    def adddata(self,datahist):
        self.data+=datahist
    def subdata(self,subhist):
        self.data.Add(subhist,-1)
    def pushmc(self,mcname,mchist):
        self.mcorder[mcname]=len(self.mcsample)
        self.mcsample[self.mcorder[mcname]]=mchist
    def addmc(self,mcname,mchist):
        self.mcsample[self.mcorder[mcname]]+=mchist
    def tempfit(self):
        mc = TObjArray(len(self.mcsample))
        for i in self.mcsample:
            mc.Add(self.mcsample[i])
        fitself = TFractionFitter(self.data, mc)
        fitself.Fit()
        self.result={}
        for i in self.mcorder:
            self.result[i]=[Double(),Double(),Double()]
            fitself.GetResult(self.mcorder[i],self.result[i][0],self.result[i][1])
            self.result[i][2]=self.result[i][0]*self.data.Integral()/self.mcsample[self.mcorder[i]].Integral()

    def tempfitplot(self,foutname,plotname,xtitle,ytitle):
        self.fout=TFile.Open(foutname+".root", 'UPDATE')
        c1 = TCanvas("c1","c1", 800, 800)
        hs = THStack("hs"+plotname,"")
        hsor = THStack("hsor"+plotname,"")
        leg= TLegend(0.62,0.65,0.92,0.90,"","brNDC")
        for i in self.mcorder:
            hsor.Add(self.mcsample[self.mcorder[i]],"hist")
            self.mcsample[self.mcorder[i]].Scale(self.result[i][2])
            hs.Add(self.mcsample[self.mcorder[i]],"hist")
            leg.AddEntry(self.mcsample[self.mcorder[i]],str(i),"f")
        
        leg.AddEntry(self.data,self.dataname,"p")
        c1.cd()
        hs.Draw()
        hs.GetXaxis().SetTitle(xtitle)
        hs.GetYaxis().SetTitle(ytitle)
        hs.GetYaxis().SetTitleOffset(1.2)

        gPad.SetLogy()
        self.data.Draw("Ep same")
        leg.Draw("same")
        c1.Print("Templatefitplots/tempfit"+plotname+".pdf(")
        c1.Clear()
        hsor.Draw()
        hsor.GetXaxis().SetTitle(xtitle)
        hsor.GetYaxis().SetTitle(ytitle)
        hsor.GetYaxis().SetTitleOffset(1.2)

        self.data.Draw("Ep same")
        leg.Draw("same")
        c1.Print("Templatefitplots/tempfit"+plotname+".pdf)")

        hs.Write()
        hsor.Write()
        self.data.Write()
        self.fout.Close()

