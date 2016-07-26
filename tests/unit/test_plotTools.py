import os
import unittest
import ROOT as r
from Plotting.scripts import PlotTools

##_____________________________________________________________________||
class TestPlotTools(unittest.TestCase):

    def test_setStyle(self):
        h = r.TH1D("h", "; p_{T}^{Bar} (TeV); Events / 2 TeV (10^{3})", 50, -50, 50)
        gaus1 = r.TF1('gaus1', 'gaus')
        gaus1.SetParameters(1, 0, 5)
        h.FillRandom("gaus1", 50000)
        h.Scale(0.001)
        histo = PlotTools.setStyle(h, 'photonEt')
        self.assertTrue(histo.ClassName(), 'TH1D')

    def test_getHist(self):
        fileName = 'test.root'
        file = r.TFile(fileName, "RECREATE")
        h = r.TH1D("h", "; p_{T}^{Bar} (TeV); Events / 2 TeV (10^{3})", 50, -50, 50)
        gaus1 = r.TF1('gaus1', 'gaus')
        gaus1.SetParameters(1, 0, 5)
        h.FillRandom("gaus1", 50000)
        h.Scale(0.001)
        h.Write()
        file.Write()
        histo = PlotTools.getHist('h', file)
        self.assertTrue(histo.ClassName(), 'TH1D')
        os.remove(fileName)

##_____________________________________________________________________||
if __name__=='__main__':
    unittest.main()
