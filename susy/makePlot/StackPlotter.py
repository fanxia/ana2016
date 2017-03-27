import ROOT
import math, os
from TreePlotter import TreePlotter

def convertToPoisson(h,blinding=False,blindingCut=100):
    graph = ROOT.TGraphAsymmErrors()
    q = (1-0.6827)/2.

    xAxisMin = h.GetXaxis().GetXmin()
    xAxisMax = h.GetXaxis().GetXmax()
    igrbin=0
    for i in range(1,h.GetNbinsX()+1):
        x=h.GetXaxis().GetBinCenter(i)
        xLow =h.GetXaxis().GetBinLowEdge(i) 
        xHigh =h.GetXaxis().GetBinUpEdge(i) 
        y=h.GetBinContent(i)
        yLow=0
        yHigh=0
        if y < 0.1: continue
        if blinding and x>blindingCut: continue
        if x<xAxisMin+0.001 or x>xAxisMax: continue
        yLow = y-ROOT.Math.chisquared_quantile_c(1-q,2*y)/2.
        yHigh = ROOT.Math.chisquared_quantile_c(q,2*(y+1))/2.-y
        graph.SetPoint(igrbin,x,y)
        graph.SetPointEYlow(igrbin,yLow)
        graph.SetPointEYhigh(igrbin,yHigh)
#        graph.SetPointEXlow(igrbin,0.0)
#        graph.SetPointEXhigh(igrbin,0.0)
        graph.SetPointEXlow(igrbin,x-xLow)
        graph.SetPointEXhigh(igrbin,xHigh-x)
        igrbin += 1



    graph.SetMarkerStyle(20)
    graph.SetLineWidth(2)
    graph.SetMarkerSize(1.)
    graph.SetMarkerColor(ROOT.kBlack)
    

    return graph    

def GetEffHist(h1):
    effhist = h1.Clone('eff_'+h1.GetName())
    nbinsX = h1.GetNbinsX()
    error1=ROOT.Double(0.0)
    error2=ROOT.Double(0.0)
    for ibin in range(1,nbinsX+1):
        n_pass = h1.IntegralAndError(ibin, nbinsX,error1)
        n_fail = h1.IntegralAndError(0, ibin-1,error2)
        eff = n_pass/(n_pass+n_fail)
        eff_err = math.sqrt((n_fail**2*error1**2+n_pass**2*error2**2)/(n_pass+n_fail)**4)
        effhist.SetBinContent(ibin, eff)
        effhist.SetBinError(ibin,eff_err)
    return effhist

def GetSignifHist(Hsig,Hbkg,Nsig,Nbkg):

    Hsignif = Hsig.Clone('signif_'+Hsig.GetName())
    Hsignif.SetTitle("Significance vs. cuts")

    for i in range(0,Hsignif.GetNbinsX()+1):
        i_nsig = Nsig*Hsig.GetBinContent(i)
        i_nbkg = Nbkg*Hbkg.GetBinContent(i)
        #print "i_nsig = "+str(i_nsig)+"; i_nbkg = "+str(i_nbkg)
        sb = i_nsig+i_nbkg
        #if i_nsig<=0 or i_nbkg<=0 : print "i_nsig = "+str(i_nsig)+"; i_nbkg = "+str(i_nbkg) 
        i_signif = i_nsig/math.sqrt(sb) if i_nsig>0.0 else 0.0
        Hsignif.SetBinContent(i, i_signif)

    return Hsignif


def GetROCGraph(Hsig,Hbkg):

    graph = ROOT.TGraph()
    ig=0
    for i in range(1,Hsig.GetNbinsX()+1):
        i_sig = Hsig.GetBinContent(i)
        i_bkg = Hbkg.GetBinContent(i)
        graph.SetPoint(ig,i_sig,1.0-i_bkg)
        ig += 1

    hist = ROOT.TH1F('roc_'+Hsig.GetName(),'roc_'+Hsig.GetName(),500,0,1)
    for i in range(1, 500):
        hist.SetBinContent(i, graph.Eval(hist.GetBinCenter(i)))

    graph.Delete()

    return hist



def GetRatioHist(h1, hstack,blinding=False,blindingCut=100):
    hratio = h1.Clone("hRatio")
    h2 = hstack.GetHistogram()
    h2.SetName('hstackmerge')
    for hist in hstack.GetHists():
        h2.Add(hist)

    for i in xrange(h1.GetXaxis().GetNbins()):
        N1 = h1.GetBinContent(i)
        N2 = h2.GetBinContent(i)
        E1 = h1.GetBinError(i)
        E2 = h2.GetBinError(i)
        RR = N1/N2 if N2>0 else 0
        EE = 0 if N2<=0 else math.sqrt(N2*N2*E1*E1+N1*N1*E2*E2)/N2/N2

        hratio.SetBinContent(i, RR)
        hratio.SetBinError(i, EE)
        if blinding and h1.GetBinCenter(i)>blindingCut: 
            hratio.SetBinContent(i, 0)
            hratio.SetBinError(i, 0)

    hratio.SetMarkerStyle(20)
    hratio.SetLineWidth(1)
    hratio.SetMarkerSize(1.)
    hratio.SetMarkerColor(ROOT.kBlack)
    hratio.GetXaxis().SetTitle('')
    hratio.GetYaxis().SetTitle('Data/MC')
    #hratio.GetYaxis().SetRangeUser(0.0,2.0)
    hratio.GetYaxis().SetRangeUser(0.5,1.5)
    hratio.GetXaxis().SetLabelFont(42)
    hratio.GetXaxis().SetLabelOffset(0.007)
    hratio.GetXaxis().SetLabelSize(0.1)
    hratio.GetXaxis().SetTitleSize(0.05)
    hratio.GetXaxis().SetTitleOffset(1.15)
    hratio.GetXaxis().SetTitleFont(42)
    hratio.GetYaxis().SetLabelFont(42)
    hratio.GetYaxis().SetLabelOffset(0.01)
    hratio.GetYaxis().SetLabelSize(0.06)
    hratio.GetYaxis().SetTitleSize(0.12)
    hratio.GetYaxis().SetTitleOffset(0.5)
    hratio.GetYaxis().SetTitleFont(42)
    hratio.GetZaxis().SetLabelFont(42)
    hratio.GetZaxis().SetLabelOffset(0.007)
    hratio.GetZaxis().SetLabelSize(0.045)
    hratio.GetZaxis().SetTitleSize(0.05)
    hratio.GetZaxis().SetTitleFont(42)

    return hratio

class StackPlotter(object):
    def __init__(self,defaultCut="1",outDir='.', outTag="stack_plotter"):
        self.plotters = []
        self.types    = []
        self.labels   = []
        self.names    = []
        self.log=False
        self.defaultCut=defaultCut
        self.outTag=outTag
        self.outDir=outDir
        self.outFileName=outDir+'/'+outTag
        self.doRatioPlot=False

        self.fout = ROOT.TFile.Open(self.outFileName+'.root', 'recreate')
        c1 = ROOT.TCanvas(self.outTag, self.outTag, 800, 1040);
        c1.Print(self.outFileName+'.ps[')
        c1.Print(self.outFileName+'.pdf[')

    def setPaveText(self, paveText):
        self.paveText = paveText

    def setAlias(self, alias, definition):
        for plotter in self.plotters:
            plotter.setAlias(alias, definition)

    def closePSFile(self):
        c1 = ROOT.TCanvas(self.outTag, self.outTag);
        c1.Print(self.outFileName+'.ps]')
        c1.Print(self.outFileName+'.pdf]')
        #ROOT.gROOT.ProcessLine('.! ps2pdf '+self.outFileName+'.ps '+self.outFileName+'.pdf')
       
    def closeROOTFile(self):
        self.fout.Close()

 
    def setLog(self,doLog):
        self.log=doLog
    def addPlotter(self,plotter,name="",label = "label",typeP = "background"):
        self.plotters.append(plotter)
        self.types.append(typeP)
        self.labels.append(label)
        self.names.append(name)

    def rmPlotter(self, plotter, name="",label = "label", typeP = "background"):
        self.plotters.remove(plotter)
        self.types.remove(typeP)
        self.labels.remove(label)
        self.names.remove(name)

    def doRatio(self,doRatio):
        self.doRatioPlot = doRatio

    def drawStack(self,var,cut,lumi,bins=-1,mini=-1,maxi=-1,channel="",titlex = "", units = "", output = 'out', outDir='.', separateSignal=False, blinding=False, blindingCut=100.0, fakeData=False):

        #fout = ROOT.TFile.Open(outDir+'/'+outputTag+'_'+output+'.root', 'recreate')
        print"start drawing plot: ",output
        self.fout.cd()

        c1 = ROOT.TCanvas(output+'_'+"c1", "c1", 800, 1040); c1.Draw()
        #c1.SetWindowSize(700 + (700 - c1.GetWw()), (910 + (910 - c1.GetWh())))
        p1 = ROOT.TPad(output+'_'+"pad1","pad1",0,0.25,1,0.99)
        p1.SetBottomMargin(0.15)
        p1.SetLeftMargin(0.15)
        p1.Draw()
        p2 = ROOT.TPad(output+'_'+"pad2","pad2",0,0,1,0.25)
        p2.SetTopMargin(0.03)
        p2.SetBottomMargin(0.3)
        p2.SetLeftMargin(0.15)
        p2.SetFillStyle(0)
        p2.Draw()

        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        
        p1.cd()
            
        hists=[]
        stack = ROOT.THStack(output+'_'+"stack","")
        
        signal=0
        background=0
        backgroundErr=0
        
        signals = []       
        signalHs = [] 
        signalLabels = []

        dataH=None
        dataG=None
        error=ROOT.Double(0.0)

        cutL="("+self.defaultCut+")*("+cut+")"

        for (plotter,typeP,label,name) in zip(self.plotters,self.types,self.labels,self.names):
            if (typeP =="background") or (not separateSignal and typeP == "signal"):
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                #hist.SetName(output+'_'+name)
                hist.SetLineWidth(1)
                stack.Add(hist)
                hists.append(hist)
                print label+" : %f\n" % hist.Integral()
 
                if typeP == "signal" :
                    signal+=hist.Integral()
                if typeP == "background" :
                    background+=hist.IntegralAndError(1,hist.GetNbinsX(),error)
                    backgroundErr+=error*error

            if separateSignal and typeP == "signal":
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                #hist.SetName(output+'_'+name)
                hists.append(hist)
                signalHs.append(hist)
                signals.append(hist.Integral())
                signalLabels.append(label)
                print label+" : %f\n" % hist.Integral()

            if typeP =="data":
                hist = plotter.drawTH1(output+'_'+typeP,var,cutL,"1",bins,mini,maxi,titlex,units)
                #hist.SetName(output+'_'+typeP)
                hist.SetMarkerStyle(20)
                hist.SetLineWidth(1)
                hist.SetMarkerSize(1.)
                hist.SetMarkerColor(ROOT.kBlack)
                hist.SetBinErrorOption(1)
                hists.append(hist)
                dataH=hist
                dataH.SetLineWidth(1)
                dataG=convertToPoisson(hist,blinding,blindingCut)
                dataG.SetName(output+'_'+'dataG')
                dataG.SetLineWidth(1)
                print label+" : %f\n" % hist.Integral()
                
 
        #if data not found plot stack only

        if dataH != None:                  
            datamax = ROOT.Math.chisquared_quantile_c((1-0.6827)/2.,2*(dataH.GetMaximum()+1))/2.
        else: 
            datamax = stack.GetMaximum()

        if not self.log:
            frame = p1.DrawFrame(mini,0.0,maxi,max(stack.GetMaximum(),datamax)*1.20)
        else:    
            frame = p1.DrawFrame(mini,0.1,maxi,max(stack.GetMaximum(),datamax)*100)

        frame.SetName(output+'_'+'frame')
        frame.GetXaxis().SetLabelFont(42)
        frame.GetXaxis().SetLabelOffset(0.007)
        frame.GetXaxis().SetLabelSize(0.03)
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetTitleFont(42)
        frame.GetYaxis().SetLabelFont(42)
        frame.GetYaxis().SetLabelOffset(0.007)
        frame.GetYaxis().SetLabelSize(0.045)
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.4)
        frame.GetYaxis().SetTitleFont(42)
        frame.GetZaxis().SetLabelFont(42)
        frame.GetZaxis().SetLabelOffset(0.007)
        frame.GetZaxis().SetLabelSize(0.045)
        frame.GetZaxis().SetTitleSize(0.05)
        frame.GetZaxis().SetTitleFont(42)


        if type(bins)==list:
            frame.GetXaxis().SetTitle(titlex + " (" +units+")")
            frame.GetYaxis().SetTitle("Events /  "+units)
        else:    
            frame.GetXaxis().SetTitle(titlex)
            frame.GetYaxis().SetTitle("Events / Bin")


        frame.Draw()


        channelComment=ROOT.TPaveText(0.25,0.8,0.55,0.88,"NDC")
        channelComment.SetFillColor(ROOT.kGray)
#        channelComment.SetFillStyle(0)
        channelComment.SetLineColor(0)
        channelComment.SetBorderSize(0)
        channelComment.AddText(channel)
        channelComment.Draw("SAME")


        stack.Draw("A,HIST,SAME")
        ROOT.gStyle.SetErrorX(0.5)
        if dataH !=None:

#            dataH.Draw("E1 same")
            dataG.Draw("Psame")              
        if separateSignal and len(signalHs)>0:
            for sigH in signalHs:
                sigH.Draw("HIST,SAME")

        legend = ROOT.TLegend(0.62,0.65,0.92,0.90,"","brNDC")
        legend.SetName(output+'_'+'legend')
	legend.SetBorderSize(0)
	legend.SetLineColor(1)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)

        legend.SetFillColor(ROOT.kWhite)
        legend.SetNColumns(2)   #testpoint
        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
            if typeP != "data" and typeP !='signal':
                legend.AddEntry(histo,label,"f")
            elif typeP == 'data':
                legend.AddEntry(histo,label,"p")

        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
            if typeP == "signal":
                legend.AddEntry(histo,label,"f")


 #       ROOT.SetOwnership(legend,False)

        legend.Draw()
        if self.log:
            p1.SetLogy()
        #p1.SetLeftMargin(p1.GetLeftMargin()*1.15)
        p1.Update()
        p2.Update()
        c1.Update()




        print"---------------------------"
        if not separateSignal:
            print "Signal = %f" %(signal)
        elif len(signalHs)>0:
            for (sig,sigLab) in reversed(zip(signals,signalLabels)):
                print "Signal "+sigLab+" = "+str(sig)
        print "Bkg    = %f" %(background)
        if dataH is not None:
            print "Observed = %f"%(dataH.Integral())
            integral = dataH.IntegralAndError(1,dataH.GetNbinsX(),error)
            if background>0.0:
                print "Data/Bkg= {ratio} +- {err}".format(ratio=integral/background,err=math.sqrt(error*error/(background*background)+integral*integral*backgroundErr/(background*background*background*background)))
        print"################################################"

	pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
        pt.SetName(output+'_'+'pavetext')
	pt.SetBorderSize(0)
	pt.SetTextAlign(12)
	pt.SetFillStyle(0)
	pt.SetTextFont(42)
	pt.SetTextSize(0.03)
	#text = pt.AddText(0.15,0.3,"CMS Preliminary")
	text = pt.AddText(0.15,0.3,"CMS Work in progress")
#	text = pt.AddText(0.25,0.3,"#sqrt{s} = 7 TeV, L = 5.1 fb^{-1}  #sqrt{s} = 8 TeV, L = 19.7 fb^{-1}")
	#text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV 2015 L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	#text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	text = pt.AddText(0.55,0.3,self.paveText) 
	pt.Draw()   
        

        if self.doRatioPlot:
            hratio = GetRatioHist(dataH,stack,blinding, blindingCut)
            hratio.SetName(output+'_'+'hratio')
            hline = hratio.Clone(output+'_'+"hline")
            for ii in range(hline.GetNbinsX()+1): 
                hline.SetBinContent(ii,1.0)
                hline.SetBinError(ii,0.0)
            hline.SetLineColor(ROOT.kRed)
            hline.SetFillStyle(0)
            p2.cd()
            hratio.Draw('AXIS')
            hline.Draw('HIST,SAME')
            hratio.Draw('E1,P,SAME')
                

        # blinding mask 
        if blinding : 
            hmask_data = dataH.Clone(output+'_'+"hmask_data")
            for ibb in range(hmask_data.GetNbinsX()+1): 
                if hmask_data.GetBinCenter(ibb)<=blindingCut: 
                    hmask_data.SetBinContent(ibb,-100)
                    hmask_data.SetBinError(ibb,0)
                else:
                    hmask_data.SetBinContent(ibb,1e100)
                    hmask_data.SetBinError(ibb,0)
            hmask_data.SetFillStyle(3003)
            hmask_data.SetFillColor(36)
            hmask_data.SetLineStyle(6)
            hmask_data.SetLineColor(16)
            p1.cd()
            hmask_data.Draw("HIST,SAME")

            if self.doRatioPlot:
                hmask_ratio = hratio.Clone(output+'_'+"hmask_ratio")
                for ibb in range(hmask_ratio.GetNbinsX()+1):
                    if hmask_ratio.GetBinCenter(ibb)<=blindingCut:
                        hmask_ratio.SetBinContent(ibb,-100)
                        hmask_ratio.SetBinError(ibb,0)
                    else:
                        hmask_ratio.SetBinContent(ibb,1e100)
                        hmask_ratio.SetBinError(ibb,0)
                hmask_ratio.SetFillStyle(3003)
                hmask_ratio.SetFillColor(36)
                hmask_ratio.SetLineStyle(6)
                hmask_ratio.SetLineColor(16)
                p2.cd()
                hmask_ratio.Draw("HIST,SAME")

        plot={'canvas':c1,'stack':stack,'legend':legend,'data':dataH,'dataG':dataG,'latex1':pt}
        if separateSignal and len(signalHs)>0:
            for (sigH,sigLab) in reversed(zip(signalHs,signalLabels)):
                plot['signal_'+sigLab] = sigH

        p1.RedrawAxis()
        p1.Update()
        c1.Update()

        #c1.Print(outDir+'/'+self.outputTag+'_'+output+'.eps')
        #os.system('epstopdf '+outDir+'/'+output+'.eps')
        c1.Print(self.outFileName+'.ps')
        c1.Print(self.outFileName+'.pdf')

        self.fout.cd()
        c1.Write() 
        stack.Write()
        #if dataH: dataH.Write()
        if dataG: dataG.Write()
        pt.Write()
        legend.Write()
        p1.Write()
        p2.Write()
        if self.doRatioPlot:   hratio.Write()
        frame.Write()
        for hist in hists: hist.Write()  
        #fout.Close()

        #c1.Delete()
        #p1.Delete()
        #p2.Delete()

        return plot


##################################

    def drawStackSketch(self,var,cut,lumi,bins=-1,mini=-1,maxi=-1,channel="",titlex = "", units = "", output = 'out', outDir='.', separateSignal=False, blinding=False, blindingCut=100.0, fakeData=False):

        #fout = ROOT.TFile.Open(outDir+'/'+outputTag+'_'+output+'.root', 'recreate')
        print"start drawing sketch plot: ",output
        output=output+"_sketch"
        self.fout.cd()

        c1 = ROOT.TCanvas(output+'_'+"c1", "c1", 800, 1040); c1.Draw()
        #c1.SetWindowSize(700 + (700 - c1.GetWw()), (910 + (910 - c1.GetWh())))
        p1 = ROOT.TPad(output+'_'+"pad1","pad1",0,0.25,1,0.99)
        p1.SetBottomMargin(0.15)
        p1.SetLeftMargin(0.15)
        p1.Draw()
        p2 = ROOT.TPad(output+'_'+"pad2","pad2",0,0,1,0.25)
        p2.SetTopMargin(0.03)
        p2.SetBottomMargin(0.3)
        p2.SetLeftMargin(0.15)
        p2.SetFillStyle(0)
        p2.Draw()

        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        
        p1.cd()
            
        hists=[]
        stack = ROOT.THStack(output+'_'+"stack","")
        
        signal=0
        background=0
        backgroundErr=0
        
        signals = []       
        signalHs = [] 
        signalLabels = []

        dataH=None
        dataG=None
        error=ROOT.Double(0.0)

        cutL="("+self.defaultCut+")*("+cut+")"

        for (plotter,typeP,label,name) in zip(self.plotters,self.types,self.labels,self.names):
            if (typeP =="background") or (not separateSignal and typeP == "signal"):
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                #hist.SetName(output+'_'+name)
                hist.SetLineWidth(1)
                stack.Add(hist)
                hists.append(hist)
                print label+" : %f\n" % hist.Integral()
 
                if typeP == "signal" :
                    signal+=hist.Integral()
                if typeP == "background" :
                    background+=hist.IntegralAndError(1,hist.GetNbinsX(),error)
                    backgroundErr+=error*error

            if separateSignal and typeP == "signal":
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                #hist.SetName(output+'_'+name)
                hists.append(hist)
                signalHs.append(hist)
                signals.append(hist.Integral())
                signalLabels.append(label)
                print label+" : %f\n" % hist.Integral()

            if typeP =="data":
                hist = plotter.drawTH1(output+'_'+typeP,var,cutL,"1",bins,mini,maxi,titlex,units)
                #hist.SetName(output+'_'+typeP)
                hist.SetMarkerStyle(20)
                hist.SetLineWidth(1)
                hist.SetMarkerSize(1.)
                hist.SetMarkerColor(ROOT.kBlack)
                hist.SetBinErrorOption(1)
                hists.append(hist)
                dataH=hist
                dataH.SetLineWidth(1)
                dataG=convertToPoisson(hist,blinding,blindingCut)
                dataG.SetName(output+'_'+'dataG')
                dataG.SetLineWidth(1)
                print label+" : %f\n" % hist.Integral()
                

 
        #if data not found plot stack only

        if dataH != None:                  
            datamax = ROOT.Math.chisquared_quantile_c((1-0.6827)/2.,2*(dataH.GetMaximum()+1))/2.
        else: 
            datamax = stack.GetMaximum()

        if not self.log:
            frame = p1.DrawFrame(mini,0.0,maxi,max(stack.GetMaximum(),datamax)*1.20)
        else:    
            frame = p1.DrawFrame(mini,0.1,maxi,max(stack.GetMaximum(),datamax)*100)

        frame.SetName(output+'_'+'frame')
        frame.GetXaxis().SetLabelFont(42)
        frame.GetXaxis().SetLabelOffset(0.007)
        frame.GetXaxis().SetLabelSize(0.03)
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetTitleFont(42)
        frame.GetYaxis().SetLabelFont(42)
        frame.GetYaxis().SetLabelOffset(0.007)
        frame.GetYaxis().SetLabelSize(0.045)
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.4)
        frame.GetYaxis().SetTitleFont(42)
        frame.GetZaxis().SetLabelFont(42)
        frame.GetZaxis().SetLabelOffset(0.007)
        frame.GetZaxis().SetLabelSize(0.045)
        frame.GetZaxis().SetTitleSize(0.05)
        frame.GetZaxis().SetTitleFont(42)


        if type(bins)==list:
            frame.GetXaxis().SetTitle(titlex + " (" +units+")")
            frame.GetYaxis().SetTitle("Events /  "+units)
        else:    
            frame.GetXaxis().SetTitle(titlex)
            frame.GetYaxis().SetTitle("Events / Bin")



        frame.Draw()


        channelComment=ROOT.TPaveText(0.25,0.8,0.55,0.88,"NDC")
        channelComment.SetFillColor(ROOT.kGray)
#        channelComment.SetFillStyle(0)
        channelComment.SetLineColor(0)
        channelComment.SetBorderSize(0)
        channelComment.AddText(channel)
        channelComment.Draw("SAME")


#        copystack=stack
        sumstack=stack.GetStack().Last().Clone()
        sumstack.SetName("summedbkg")
#        stack.Draw("A,HIST,SAME")
        sumstack.SetLineColor(ROOT.kBlue)
        sumstack.SetLineWidth(2)
        sumstack.SetFillColor(0)
        sumstack.Draw("HIST,SAME")
        ROOT.gStyle.SetErrorX(0.5)
        if dataH !=None:

#            dataH.Draw("E1 same")
            dataG.Draw("Psame")              
        if separateSignal and len(signalHs)>0:
            for sigH in signalHs:
                sigH.Draw("HIST,SAME")

        legend = ROOT.TLegend(0.62,0.80,0.92,0.90,"","brNDC")
        legend.SetName(output+'_'+'legend')
	legend.SetBorderSize(0)
	legend.SetLineColor(1)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)

        legend.SetFillColor(ROOT.kWhite)
        legend.AddEntry(sumstack,"Bkgs Sum","p")
        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
#            if typeP != "data" and typeP !='signal':
#                legend.AddEntry(histo,label,"f")

            if typeP == 'data':
                legend.AddEntry(histo,label,"p")

        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
            if typeP == "signal":
                legend.AddEntry(histo,label,"f")


 #       ROOT.SetOwnership(legend,False)

        legend.Draw()
        if self.log:
            p1.SetLogy()
        #p1.SetLeftMargin(p1.GetLeftMargin()*1.15)
        p1.Update()
        p2.Update()
        c1.Update()




        print"---------------------------"
        if not separateSignal:
            print "Signal = %f" %(signal)
        elif len(signalHs)>0:
            for (sig,sigLab) in reversed(zip(signals,signalLabels)):
                print "Signal "+sigLab+" = "+str(sig)
        print "Bkg    = %f" %(background)
        if dataH is not None:
            print "Observed = %f"%(dataH.Integral())
            integral = dataH.IntegralAndError(1,dataH.GetNbinsX(),error)
            if background>0.0:
                print "Data/Bkg= {ratio} +- {err}".format(ratio=integral/background,err=math.sqrt(error*error/(background*background)+integral*integral*backgroundErr/(background*background*background*background)))
        print"################################################"



	pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
        pt.SetName(output+'_'+'pavetext')
	pt.SetBorderSize(0)
	pt.SetTextAlign(12)
	pt.SetFillStyle(0)
	pt.SetTextFont(42)
	pt.SetTextSize(0.03)
	#text = pt.AddText(0.15,0.3,"CMS Preliminary")
	text = pt.AddText(0.15,0.3,"CMS Work in progress")
#	text = pt.AddText(0.25,0.3,"#sqrt{s} = 7 TeV, L = 5.1 fb^{-1}  #sqrt{s} = 8 TeV, L = 19.7 fb^{-1}")
	#text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV 2015 L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	#text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV 2016 L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	text = pt.AddText(0.55,0.3,self.paveText) 
	pt.Draw()   
        
        


        if self.doRatioPlot:
            p2.cd()
            stack.Draw()
            hratio = GetRatioHist(dataH,stack,blinding, blindingCut)
            hratio.SetName(output+'_'+'hratio')
            hline = hratio.Clone(output+'_'+"hline")
            for ii in range(hline.GetNbinsX()+1): 
                hline.SetBinContent(ii,1.0)
                hline.SetBinError(ii,0.0)
            hline.SetLineColor(ROOT.kRed)
            hline.SetFillStyle(0)
#            p2.cd()
            hratio.Draw('AXIS')
            hline.Draw('HIST,SAME')
            hratio.Draw('E1,P,SAME')
                

        # blinding mask 
        if blinding : 
            hmask_data = dataH.Clone(output+'_'+"hmask_data")
            for ibb in range(hmask_data.GetNbinsX()+1): 
                if hmask_data.GetBinCenter(ibb)<=blindingCut: 
                    hmask_data.SetBinContent(ibb,-100)
                    hmask_data.SetBinError(ibb,0)
                else:
                    hmask_data.SetBinContent(ibb,1e100)
                    hmask_data.SetBinError(ibb,0)
            hmask_data.SetFillStyle(3003)
            hmask_data.SetFillColor(36)
            hmask_data.SetLineStyle(6)
            hmask_data.SetLineColor(16)
            p1.cd()
            hmask_data.Draw("HIST,SAME")

            if self.doRatioPlot:
                hmask_ratio = hratio.Clone(output+'_'+"hmask_ratio")
                for ibb in range(hmask_ratio.GetNbinsX()+1):
                    if hmask_ratio.GetBinCenter(ibb)<=blindingCut:
                        hmask_ratio.SetBinContent(ibb,-100)
                        hmask_ratio.SetBinError(ibb,0)
                    else:
                        hmask_ratio.SetBinContent(ibb,1e100)
                        hmask_ratio.SetBinError(ibb,0)
                hmask_ratio.SetFillStyle(3003)
                hmask_ratio.SetFillColor(36)
                hmask_ratio.SetLineStyle(6)
                hmask_ratio.SetLineColor(16)
                p2.cd()
                hmask_ratio.Draw("HIST,SAME")

        plot={'canvas':c1,'stack':stack,'legend':legend,'data':dataH,'dataG':dataG,'latex1':pt}
        if separateSignal and len(signalHs)>0:
            for (sigH,sigLab) in reversed(zip(signalHs,signalLabels)):
                plot['signal_'+sigLab] = sigH

        p1.RedrawAxis()
        p1.Update()
        c1.Update()

        #c1.Print(outDir+'/'+self.outputTag+'_'+output+'.eps')
        #os.system('epstopdf '+outDir+'/'+output+'.eps')
        c1.Print(self.outFileName+'.ps')
        c1.Print(self.outFileName+'.pdf')

        self.fout.cd()
        c1.Write() 
        sumstack.Write()
        #if dataH: dataH.Write()
        #fout.Close()

        #c1.Delete()
        #p1.Delete()
        #p2.Delete()

        return plot











    def drawComp(self,var,cut,bins,mini,maxi,titlex = "", units = "", output='out.eps'):
        canvas = ROOT.TCanvas("canvas","")
        ROOT.SetOwnership(canvas,False)
        canvas.cd()
        hists=[]
        stack = ROOT.THStack("stack","")
        ROOT.SetOwnership(stack,False)

        canvas.Range(-68.75,-7.5,856.25,42.5)
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetBorderSize(2)
        canvas.SetTickx(1)
        canvas.SetTicky(1)
        canvas.SetLeftMargin(0.15)
        canvas.SetRightMargin(0.05)
        canvas.SetTopMargin(0.05)
        canvas.SetBottomMargin(0.15)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)


        for (plotter,typeP,label) in zip(self.plotters,self.types,self.labels):
                hist = plotter.drawTH1(hist.GetName()+label,var,cut,"1",bins,mini,maxi,titlex,units)
                #hist.SetFillStyle(0)
                #hist.SetName(hist.GetName()+label)
                hist.Scale(1./hist.Integral())
                stack.Add(hist)
                hists.append(hist)


        stack.Draw("HIST,NOSTACK")
        canvas.SetLeftMargin(canvas.GetLeftMargin()*1.15)

        if len(units):
            stack.GetXaxis().SetTitle(titlex + " [" +units+"]")
        else:
            stack.GetXaxis().SetTitle(titlex)
    
        stack.GetYaxis().SetTitle("a.u")
        stack.GetYaxis().SetTitleOffset(1.2)


        legend = ROOT.TLegend(0.6,0.6,0.9,0.9)
        legend.SetFillColor(ROOT.kWhite)
        for (histo,label,typeP) in zip(hists,self.labels,self.types):
                legend.AddEntry(histo,label,"lf")
        ROOT.SetOwnership(legend,False)
        legend.Draw()


	pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
	pt.SetBorderSize(0)
	pt.SetTextAlign(12)
	pt.SetFillStyle(0)
	pt.SetTextFont(42)
	pt.SetTextSize(0.03)
	text = pt.AddText(0.01,0.5,"CMS simulation")
	pt.Draw()   


        canvas.Update()

        #canvas.Print(output)
        #os.system('epstopdf '+output)
        canvas.Print(self.outFileName+'.ps')
        canvas.Print(self.outFileName+'.pdf')
        return canvas

        
        
    def drawCutEff(self,var,cut,lumi,bins,mini,maxi,titlex = "", units = "", output = 'out', outDir='.'):

        #fout = ROOT.TFile.Open(outDir+'/'+output+'.root', 'recreate')
        self.fout.cd()

        c1 = ROOT.TCanvas(output+'_'+"c1", "c1", 600, 600); c1.Draw()
        c1.SetWindowSize(600 + (600 - c1.GetWw()), (600 + (600 - c1.GetWh())))
        c1.SetBottomMargin(0.15)
        c1.SetLeftMargin(0.15)
        c1.SetFillStyle(0)

        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        
        hists=[]
        stack = ROOT.THStack(output+'_'+"stack","")
        
        signal=0
        background=0
        backgroundErr=0
        
        signals = []       
        signalHs = [] 
        signalLabels = []

        backgroundHs = []

        dataH=None
        error=ROOT.Double(0.0)

        cutL="("+self.defaultCut+")*("+cut+")"

        # fill histgrams 
        for (plotter,typeP,label,name) in zip(self.plotters,self.types,self.labels,self.names):
            if typeP == "background" :
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                stack.Add(hist)
                hists.append(hist)
                backgroundHs.append(hist)
                print label+" : %f\n" % hist.Integral()
                background+=hist.IntegralAndError(1,hist.GetNbinsX(),error)
                backgroundErr+=error*error

            if typeP == "signal" :
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                hists.append(hist)
                signalHs.append(hist)
                signals.append(hist.Integral())
                signalLabels.append(label)
                print label+" : %f\n" % hist.Integral()

            if typeP == "data":
                hist = plotter.drawTH1(output+'_'+typeP,var,cutL,"1",bins,mini,maxi,titlex,units)
                hists.append(hist)
                hist.SetMarkerStyle(20)
                hist.SetLineWidth(1)
                hist.SetLineColor(1)
                hist.SetMarkerSize(1.)
                hist.SetMarkerColor(ROOT.kBlack)
                hist.SetBinErrorOption(1)
                dataH=hist
                print label+" : %f\n" % hist.Integral()
                
        # sum background hist
        backgroundH = 0
        for idx,bkg in enumerate(backgroundHs):
            if idx==0: 
                backgroundH = backgroundHs[0].Clone(output+'_AllBkg')
            else:
                backgroundH.Add(backgroundHs[idx])
 
        # get efficiency hists
        SigEffHists = []
        BkgEffHists = []
        # loop over all hists
        # signal hists
        for hist in signalHs:
            effhist = GetEffHist(hist)
            SigEffHists.append(effhist)
            
        # sum of all background
        BkgEffHistAll = GetEffHist(backgroundH)
        BkgEffHistAll.SetLineColor(1)
        BkgEffHistAll.SetLineWidth(2)
        BkgEffHistAll.SetLineStyle(2)
        BkgEffHistAll.SetFillStyle(0)
        BkgEffHists.append(BkgEffHistAll)

        # background hists
        for hist in backgroundHs:
            effhist = GetEffHist(hist)
            effhist.SetLineColor(effhist.GetFillColor())
            effhist.SetFillStyle(0)
            BkgEffHists.append(effhist)

        # data hist
        DataEffHist = GetEffHist(dataH)
        DataEffHist.SetLineColor(1)
        DataEffHist.SetMarkerColor(1)
        DataEffHist.SetMarkerStyle(20)
        DataEffHist.SetFillStyle(0)
        DataEffHist.SetFillColor(0)

        frame = c1.DrawFrame(mini,0.0,maxi,1.3)

        if not self.log:
            frame = c1.DrawFrame(mini,0.0,maxi,1.3)
        else:
            frame = c1.DrawFrame(mini,0.0001,maxi,30)

        frame.SetName(output+'_'+'frame')
        frame.GetXaxis().SetLabelFont(42)
        frame.GetXaxis().SetLabelOffset(0.007)
        frame.GetXaxis().SetLabelSize(0.03)
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetTitleFont(42)
        frame.GetYaxis().SetLabelFont(42)
        frame.GetYaxis().SetLabelOffset(0.007)
        frame.GetYaxis().SetLabelSize(0.045)
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.4)
        frame.GetYaxis().SetTitleFont(42)
        frame.GetZaxis().SetLabelFont(42)
        frame.GetZaxis().SetLabelOffset(0.007)
        frame.GetZaxis().SetLabelSize(0.045)
        frame.GetZaxis().SetTitleSize(0.05)
        frame.GetZaxis().SetTitleFont(42)


        if len(units)>0:
            frame.GetXaxis().SetTitle(titlex + " (" +units+")")
            frame.GetYaxis().SetTitle("Efficiency")
        else:    
            frame.GetXaxis().SetTitle(titlex)
            frame.GetYaxis().SetTitle("Efficiency")


        frame.Draw()
        for hist in reversed(SigEffHists):
            hist.Draw("A,HIST,SAME")
        for hist in reversed(BkgEffHists):
            hist.Draw("A,HIST,SAME")
        DataEffHist.Draw("A,SAME")

        legend = ROOT.TLegend(0.62,0.6,0.92,0.90,"","brNDC")
        legend.SetName(output+'_'+'legend')
	legend.SetBorderSize(0)
	legend.SetLineColor(1)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)

        legend.SetFillColor(ROOT.kWhite)
        legend.AddEntry(BkgEffHistAll, "All Background", "l")

        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
            if typeP != "data" and typeP !='signal':
                legend.AddEntry(histo,label,"f")
            elif typeP == 'data':
                legend.AddEntry(histo,label,"pl")

        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
            if typeP == "signal":
                legend.AddEntry(histo,label,"f")



        legend.Draw()
        if self.log:
            c1.SetLogy()
        c1.Update()

	pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
        pt.SetName(output+'_'+'pavetext')
	pt.SetBorderSize(0)
	pt.SetTextAlign(12)
	pt.SetFillStyle(0)
	pt.SetTextFont(42)
	pt.SetTextSize(0.03)
	text = pt.AddText(0.15,0.3,"CMS Work in progress")
	text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV, L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	pt.Draw()   

        plot={'canvas':c1,'SigEffHists':SigEffHists,'BkgEffHists':BkgEffHists,'DataEffHist':DataEffHist,'legend':legend,'data':dataH, 'latex1':pt}

        c1.Update()
        #c1.Print(outDir+'/'+output+'.eps')
        #os.system('epstopdf '+outDir+'/'+output+'.eps')
        c1.Print(self.outFileName+'.ps')
        c1.Print(self.outFileName+'.pdf')
       
        self.fout.cd()
        c1.Write()
        pt.Write()
        legend.Write()
        frame.Write()
        for hist in hists: hist.Write() 
        for hist in SigEffHists: hist.Write() 
        for hist in BkgEffHists: hist.Write() 
        DataEffHist.Write()
        #fout.Close()

        return plot


    def drawCutSignif(self,var,cut,lumi,bins,mini,maxi,titlex = "", units = "", output = 'out', outDir='.'):

        #fout = ROOT.TFile.Open(outDir+'/'+output+'.root', 'recreate')
        self.fout.cd()

        c1 = ROOT.TCanvas(output+'_'+"c1", "c1", 600, 600); c1.Draw()
        c1.SetWindowSize(600 + (600 - c1.GetWw()), (600 + (600 - c1.GetWh())))
        c1.SetBottomMargin(0.15)
        c1.SetLeftMargin(0.15)
        c1.SetFillStyle(0)

        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        
        hists=[]
        stack = ROOT.THStack(output+'_'+"stack","")
        
        signal=0
        background=0
        backgroundErr=0
        
        signals = []       
        signalHs = [] 
        signalLabels = []

        backgroundHs = []

        dataH=None
        error=ROOT.Double(0.0)

        cutL="("+self.defaultCut+")*("+cut+")"

        # fill histgrams 
        for (plotter,typeP,label,name) in zip(self.plotters,self.types,self.labels,self.names):
            if typeP == "background" :
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                # remove negative bin
                for ibin in range(1, hist.GetNbinsX()+1):
                    if hist.GetBinContent(ibin)<=0.0 : hist.SetBinContent(ibin, 0.0)
                stack.Add(hist)
                hists.append(hist)
                backgroundHs.append(hist)
                print label+" : %f\n" % hist.Integral()
                background+=hist.IntegralAndError(1,hist.GetNbinsX(),error)
                backgroundErr+=error*error

            if typeP == "signal" :
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                # remove negative bin
                for ibin in range(1, hist.GetNbinsX()+1):
                    if hist.GetBinContent(ibin)<=0.0 : hist.SetBinContent(ibin, 0.0)
                hists.append(hist)
                signalHs.append(hist)
                signals.append(hist.Integral())
                signalLabels.append(label)
                print label+" : %f\n" % hist.Integral()
                
        # sum background hist
        backgroundH = 0
        for idx,bkg in enumerate(backgroundHs):
            if idx==0: 
                backgroundH = backgroundHs[0].Clone(output+'_AllBkg')
            else:
                backgroundH.Add(backgroundHs[idx])
 
        # get efficiency hists
        SigEffHists = []
        # loop over all hists
        # signal hists
        for hist in signalHs:
            effhist = GetEffHist(hist)
            SigEffHists.append(effhist)
            
        # sum of all background
        BkgEffHistAll = GetEffHist(backgroundH)
        BkgEffHistAll.SetLineColor(1)
        BkgEffHistAll.SetLineWidth(2)
        BkgEffHistAll.SetLineStyle(2)
        BkgEffHistAll.SetFillStyle(0)


        # get signal significance hists
        SigSignifHists = []
        nbkgAll = backgroundH.Integral()
        for idx,hist in enumerate(SigEffHists):
            nsig = signalHs[idx].Integral()
            sighist = GetSignifHist(hist,BkgEffHistAll,nsig, nbkgAll) 
            sighist.SetLineStyle(1)
            SigSignifHists.append(sighist)

        if not self.log:
            frame = c1.DrawFrame(mini,0.0,maxi,max( hist.GetMaximum() for hist in SigSignifHists )*1.3)
        else: 
            frame = c1.DrawFrame(mini,min( hist.GetMaximum() for hist in SigSignifHists )*0.01,maxi,max( hist.GetMaximum() for hist in SigSignifHists )*100)

        frame.SetName(output+'_'+'frame')
        frame.GetXaxis().SetLabelFont(42)
        frame.GetXaxis().SetLabelOffset(0.007)
        frame.GetXaxis().SetLabelSize(0.03)
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetTitleFont(42)
        frame.GetYaxis().SetLabelFont(42)
        frame.GetYaxis().SetLabelOffset(0.007)
        frame.GetYaxis().SetLabelSize(0.045)
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.4)
        frame.GetYaxis().SetTitleFont(42)
        frame.GetZaxis().SetLabelFont(42)
        frame.GetZaxis().SetLabelOffset(0.007)
        frame.GetZaxis().SetLabelSize(0.045)
        frame.GetZaxis().SetTitleSize(0.05)
        frame.GetZaxis().SetTitleFont(42)


        if len(units)>0:
            frame.GetXaxis().SetTitle(titlex + " (" +units+")")
            frame.GetYaxis().SetTitle("S/#sqrt{S+B}")
        else:    
            frame.GetXaxis().SetTitle(titlex)
            frame.GetYaxis().SetTitle("S/#sqrt{S+B}")


        frame.Draw()
        for hist in reversed(SigSignifHists):
            hist.Draw("A,HIST,SAME")

        legend = ROOT.TLegend(0.62,0.6,0.92,0.90,"","brNDC")
        legend.SetName(output+'_'+'legend')
	legend.SetBorderSize(0)
	legend.SetLineColor(1)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)

        legend.SetFillColor(ROOT.kWhite)
        for (histo,label) in reversed(zip(signalHs,signalLabels)):
            legend.AddEntry(histo,label,"f")

        legend.Draw()
        if self.log:
            c1.SetLogy()
        c1.Update()

	pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
        pt.SetName(output+'_'+'pavetext')
	pt.SetBorderSize(0)
	pt.SetTextAlign(12)
	pt.SetFillStyle(0)
	pt.SetTextFont(42)
	pt.SetTextSize(0.03)
	text = pt.AddText(0.15,0.3,"CMS Work in progress")
	text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV, L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	pt.Draw()   

        plot={'canvas':c1,'SigEffHists':SigEffHists,'BkgEffHistAll':BkgEffHistAll,'SigSignifHists':SigSignifHists,'legend':legend,'data':dataH, 'latex1':pt}

        c1.Update()
        #c1.Print(outDir+'/'+output+'.eps')
        #os.system('epstopdf '+outDir+'/'+output+'.eps')
        c1.Print(self.outFileName+'.ps')
        c1.Print(self.outFileName+'.pdf')
       
        self.fout.cd()
        c1.Write()
        pt.Write()
        legend.Write()
        frame.Write()
        for hist in hists: hist.Write() 
        for hist in SigEffHists: hist.Write() 
        for hist in SigSignifHists: hist.Write() 
        #fout.Close()

        return plot

    def drawCutROC(self,var,cut,lumi,bins,mini,maxi, titlex="", units="", output = 'out', outDir='.'):

        #fout = ROOT.TFile.Open(outDir+'/'+output+'.root', 'recreate')
        self.fout.cd()

        c1 = ROOT.TCanvas(output+'_'+"c1", "c1", 600, 600); c1.Draw()
        c1.SetWindowSize(600 + (600 - c1.GetWw()), (600 + (600 - c1.GetWh())))
        c1.SetBottomMargin(0.15)
        c1.SetLeftMargin(0.15)
        c1.SetFillStyle(0)

        ROOT.gStyle.SetOptStat(0)
        ROOT.gStyle.SetOptTitle(0)
        
        hists=[]
        stack = ROOT.THStack(output+'_'+"stack","")
        
        signal=0
        background=0
        backgroundErr=0
        
        signals = []       
        signalHs = [] 
        signalLabels = []

        backgroundHs = []

        dataH=None
        error=ROOT.Double(0.0)

        cutL="("+self.defaultCut+")*("+cut+")"

        # fill histgrams 
        for (plotter,typeP,label,name) in zip(self.plotters,self.types,self.labels,self.names):
            if typeP == "background" :
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                stack.Add(hist)
                hists.append(hist)
                backgroundHs.append(hist)
                print label+" : %f\n" % hist.Integral()
                background+=hist.IntegralAndError(1,hist.GetNbinsX(),error)
                backgroundErr+=error*error

            if typeP == "signal" :
                hist = plotter.drawTH1(output+'_'+name,var,cutL,lumi,bins,mini,maxi,titlex,units)
                hists.append(hist)
                signalHs.append(hist)
                signals.append(hist.Integral())
                signalLabels.append(label)
                print label+" : %f\n" % hist.Integral()
                
        # sum background hist
        backgroundH = 0
        for idx,bkg in enumerate(backgroundHs):
            if idx==0: 
                backgroundH = backgroundHs[0].Clone(output+'_AllBkg')
            else:
                backgroundH.Add(backgroundHs[idx])
 
        # get efficiency hists
        SigEffHists = []
        # loop over all hists
        # signal hists
        for hist in signalHs:
            effhist = GetEffHist(hist)
            SigEffHists.append(effhist)
            
        # sum of all background
        BkgEffHistAll = GetEffHist(backgroundH)
        BkgEffHistAll.SetLineColor(1)
        BkgEffHistAll.SetLineWidth(2)
        BkgEffHistAll.SetLineStyle(2)
        BkgEffHistAll.SetFillStyle(0)


        # get signal significance hists
        ROCGraphs = []
        for hist in SigEffHists:
            roc = GetROCGraph(hist,BkgEffHistAll) 
            roc.SetLineStyle(1)
            roc.SetLineWidth(2)
            roc.SetLineColor(hist.GetLineColor())
            roc.SetMarkerColor(hist.GetLineColor())
            ROCGraphs.append(roc)

        frame = c1.DrawFrame(0.95,0.95,1.01,1.01)

        frame.SetName(output+'_'+'frame')
        frame.GetXaxis().SetLabelFont(42)
        frame.GetXaxis().SetLabelOffset(0.007)
        frame.GetXaxis().SetLabelSize(0.03)
        frame.GetXaxis().SetTitleSize(0.05)
        frame.GetXaxis().SetTitleOffset(1.15)
        frame.GetXaxis().SetTitleFont(42)
        frame.GetYaxis().SetLabelFont(42)
        frame.GetYaxis().SetLabelOffset(0.007)
        frame.GetYaxis().SetLabelSize(0.045)
        frame.GetYaxis().SetTitleSize(0.05)
        frame.GetYaxis().SetTitleOffset(1.4)
        frame.GetYaxis().SetTitleFont(42)
        frame.GetZaxis().SetLabelFont(42)
        frame.GetZaxis().SetLabelOffset(0.007)
        frame.GetZaxis().SetLabelSize(0.045)
        frame.GetZaxis().SetTitleSize(0.05)
        frame.GetZaxis().SetTitleFont(42)


        frame.GetXaxis().SetTitle(var+" Sig. Eff.")
        frame.GetYaxis().SetTitle(var+" Bkg. Rej.")

        frame.Draw()
        for roc in reversed(ROCGraphs):
            roc.Draw("A,HIST,SAME")

        legend = ROOT.TLegend(0.62,0.6,0.92,0.90,"","brNDC")
        legend.SetName(output+'_'+'legend')
	legend.SetBorderSize(0)
	legend.SetLineColor(1)
	legend.SetLineStyle(1)
	legend.SetLineWidth(1)
	legend.SetFillColor(0)
	legend.SetFillStyle(0)
	legend.SetTextFont(42)

        legend.SetFillColor(ROOT.kWhite)
        for (histo,label,typeP) in reversed(zip(hists,self.labels,self.types)):
            if typeP == "signal":
                legend.AddEntry(histo,label,"f")

        legend.Draw()
        c1.Update()

	pt =ROOT.TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
        pt.SetName(output+'_'+'pavetext')
	pt.SetBorderSize(0)
	pt.SetTextAlign(12)
	pt.SetFillStyle(0)
	pt.SetTextFont(42)
	pt.SetTextSize(0.03)
	text = pt.AddText(0.15,0.3,"CMS Work in progress")
	text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV, L = "+"{:.3}".format(float(lumi)/1000)+" fb^{-1}")
	pt.Draw()   

        plot={'canvas':c1,'SigEffHists':SigEffHists,'BkgEffHistAll':BkgEffHistAll,'ROCGraphs':ROCGraphs,'legend':legend,'data':dataH, 'latex1':pt}

        c1.Update()
        #c1.Print(outDir+'/'+output+'.eps')
        #os.system('epstopdf '+outDir+'/'+output+'.eps')
        c1.Print(self.outFileName+'.ps')
        c1.Print(self.outFileName+'.pdf')
       
        self.fout.cd()
        c1.Write()
        pt.Write()
        legend.Write()
        frame.Write()
        for hist in hists: hist.Write() 
        for hist in SigEffHists: hist.Write() 
        for roc in ROCGraphs: roc.Write() 
        #fout.Close()

        return plot
