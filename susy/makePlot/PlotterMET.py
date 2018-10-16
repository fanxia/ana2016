from ROOT import *
import math

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

    def syserror(self,hista,histb,erra,errb):
        numa=hista.Integral()
        numb=histb.Integral()
        self.ratiosysErr= math.sqrt(erra*erra*numa*numa+errb*errb*numb*numb)/(numa+numb)
        

    def plotMETcompare(self,foutname,plotname,xtitle,ytitle,sys):
        self.fout=TFile.Open(foutname+".root", 'UPDATE')
        c1 = TCanvas("c1","c1", 800, 800)

        self.befhist.SetLineWidth(2)
        self.afthist.SetLineWidth(2)
        self.befhist.Draw()
#        self.befhist.GetXaxis().SetTitleOffset(0.9)
        self.befhist.SetTitle(";"+xtitle+";"+ytitle)
        self.befhist.SetMinimum(0.0)
        self.befhist.GetXaxis().SetTitleSize(0.8*self.befhist.GetXaxis().GetTitleSize())
        self.befhist.SetMaximum(max(self.befhist.GetMaximum(),self.afthist.GetMaximum())*1.2)

        gStyle.SetOptStat(0)
        pad1=TPad("","",0,0.25,1,1)
        pad2=TPad("","",0,0.0,1,0.25)
#        pad2.SetTopMargin(0.05)
        pad1.Draw()
        pad2.Draw()


        pad1.cd()
        leg= TLegend(0.62,0.7,0.90,0.90,"","brNDC")
        leg.AddEntry(self.befhist,self.befhistname,"l")
        leg.AddEntry(self.afthist,self.afthistname,"l")

        self.befhist.Draw("hist")
        self.afthist.Draw("hist same")
        leg.Draw("same")

        pad2.cd()
        leg2= TLegend(0.45,0.69,0.68,0.89,"","brNDC")
        leg2.SetFillColor(18)
        leg2.SetBorderSize(0)
        hratio=self.afthist.Clone("hratio")
        hratio.Divide(self.befhist)
        hratio.SetTitle(";;After/Before")
        hratio.GetXaxis().SetTitle("")
        hratio.GetYaxis().SetTitleOffset(0.3)
        hratio.GetXaxis().SetTitleOffset(2)
        hratio.GetYaxis().SetTitleSize(0.6)
        hratio.SetMaximum(1.5) #
        hratio.SetMinimum(0.5) #
        hratio.SetTitle(";;") #
        hratio.Draw("e")
        leg2.AddEntry(hratio,"After / Before","l")

        hratio.Fit("pol0")
#        leg2.Draw("same")
        c1.Print(foutname+"_"+sys+plotname+".pdf")
        self.ratio=hratio.GetFunction("pol0").GetParameter(0)
        self.ratioErr=hratio.GetFunction("pol0").GetParError(0)
