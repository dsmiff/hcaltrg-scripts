'''
Generic plot maker for HCal DPG studies
'''
import os
import sys
import PlotTools
from Plotting import CONST_PARAMS, log
from string import *
import ROOT as r

def make1Dplot(infile, outfile, plot):
    h = PlotTools.getHist(plot, infile)
    histo = PlotTools.setStyle(h, plot)
    cname = "%s"%(plot)
    draw1Dplot(h, outputdir, outfile, cname)

def draw1Dplot(h, outputdir, outfile, cname):
    canvas = r.TCanvas(cname, "")
    canvas.cd()
    if h.ClassName()=='TH1D':
        canvas.SetLogy()
        h.Draw("HIST")
    else:
        h.Draw("COLZ")

    t2 = r.TLatex();
    t2.SetNDC();
    t2.SetNDC();
    t2.SetLineWidth(2)
    t2.SetTextFont(61);
    t2.SetTextSize(0.06);
    t2.DrawLatex(0.13, 0.84, "CMS");
    
    t3 = r.TLatex();
    t3.SetNDC();
    t3.SetTextFont(52);
    t3.SetTextSize(0.05);
    t3.DrawLatex(0.13, 0.78, "Simulation Preliminary");
    
    canvas.SaveAs(outputdir+"/"+cname+".png")
    outfile.cd()
    canvas.Write()
    canvas.Close()

if __name__=='__main__':
    if len(sys.argv) < 3:
        print "Run as python %s <outputdir> <ROOT file>" % (sys.argv[0])
        sys.exit()
        
    outputdir = sys.argv[1]
    histfile  = sys.argv[2]

    if len(sys.argv) < 4:
        print "Will assume Background only 1D plots"
    else:
        datadir = sys.argv[3]

    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    outfile = r.TFile.Open(outputdir+"/generic_plots.root", "RECREATE")
    
    intLumi = CONST_PARAMS.get('intLumi')

    if os.path.isfile(histfile):
        hFile = r.TFile.Open(histfile)        
    else:        
        print "File does not exist"
        sys.exit(1)            

    r.gStyle.SetOptStat(0)
    r.gStyle.SetTextFont(42)

    samples = CONST_PARAMS.get('signal_samples')

    plots = ['photonEt']

    for plot in plots:
        try:        
            make1Dplot(hFile, outfile, plot)
        except RuntimeError, e:
            print >> sys.stderr, "Unable to run, check your hist dictionary"
            sys.exit(1)
    
    log.info("All histograms drawn")
