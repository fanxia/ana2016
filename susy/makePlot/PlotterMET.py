from ROOT import *

class PlotterMET(object):
    def __init__(self):
        self.befhist=TH1D()
        self.afthist=TH1D()
    def pushbef(self,hname,hist,scal=1,col=0):
        self.befhist=hist.Clone()
        self.befhist.Scale(scal)
        self.befhistname=hname
        self.befhist.SetLineColor(col)
        self.befhist.SetFillColor(0)
    def addbef(self,hist,scal=1):
        self.befhist.Add(hist,scal*1)

    def pushaft(self,hname,hist,scal=1,col=0):
        self.afthist=hist.Clone()
        self.afthist.Scale(scal)
        self.afthistname=hname
        self.afthist.SetLineColor(col)
        self.afthist.SetFillColor(0)
    def addaft(self,hist,scal=1):
        self.afthist.Add(hist,scal)

    def plotMETcompare(self,foutname,plotname,xtitle,ytitle):
        self.fout=TFile.Open(foutname+".root", 'UPDATE')
        c1 = TCanvas("c1","c1", 800, 800)

        self.befhist.Draw()
        self.befhist.GetXaxis().SetTitleOffset(0.8)
        self.befhist.SetTitle(";"+xtitle+";"+ytitle)
        self.befhist.SetMinimum(0.0)
        self.befhist.SetMaximum(max(self.befhist.GetMaximum(),self.afthist.GetMaximum())*1.2)

        gStyle.SetOptStat(0)
        pad1=TPad("","",0,0.25,1,1)
        pad2=TPad("","",0,0.0,1,0.25)
#        pad2.SetTopMargin(0.05)
        pad1.Draw()
        pad2.Draw()


        pad1.cd()
        leg= TLegend(0.62,0.65,0.90,0.90,"","brNDC")
        leg.AddEntry(self.befhist,self.befhistname,"l")
        leg.AddEntry(self.afthist,self.afthistname,"l")

        self.befhist.Draw("hist")
        self.afthist.Draw("hist same")
        leg.Draw("same")

        pad2.cd()
        hratio=self.afthist.Clone("hratio")
        hratio.Divide(self.befhist)
        hratio.SetTitle(";;after/before    ")
        hratio.GetXaxis().SetTitle("")
        hratio.GetYaxis().SetTitleOffset(0.5)
        hratio.GetXaxis().SetTitleOffset(2)
        hratio.Draw("e")

        hratio.Fit("pol0")
        c1.Print(foutname+"_"+plotname+".pdf")
        self.ratio=hratio.GetFunction("pol0").GetParameter(0)
        self.ratioErr=hratio.GetFunction("pol0").GetParError(0)
