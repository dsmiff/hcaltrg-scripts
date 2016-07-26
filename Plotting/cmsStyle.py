'''
Official CMS styles.
CMS style distributions made via functions defined below.
'''

import ROOT as r

def cmsStyling(lumi, energy, title='', onLeft=True, sp=0, textScale=1.):
    
    energy = int(energy)
    lumi   = int(lumi)

    n1 = r.TLatex()
    n1.SetNDC();
    n1.SetTextFont(42);
    n1.SetTextSize(0.03);    
    n1.DrawLatex(0.68, 0.91,  "%.1f pb^{-1} (13 TeV)" % lumi);
    
    n2 = r.TLatex()
    n2.SetNDC();
    n2.SetLineWidth(2)
    n2.SetTextFont(61);
    n2.SetTextSize(0.06);
    n2.DrawLatex(0.15, 0.84, "CMS");    
    
    n3 = r.TLatex();
    n3.SetNDC();
    n3.SetTextFont(52);
    n3.SetTextSize(0.05);
    n3.DrawLatex(0.15, 0.78, title);

def setupStack(name, nJetBin=None, htBin=None, pSet=None):
    if nJetBin is None:
        if htBin is None:
            stack = r.THStack(name, name)
        else:
            stack = r.THStack(name+'_'+htBin, name+'_'+htBin)
    else:
        stack = r.THStack(name+'_'+nJetBin,name+'_'+nJetBin+'_'+htBin)      
        
    return stack

def setupCanvas(canvas_args):
    canvas = r.TCanvas(*canvas_args)
    canvas.SetBottomMargin(0.)

    return canvas

def setupLegend(legend_args):
    leg =  r.TLegend(*legend_args)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0)
    
    return leg

def setProcessName(process):
    names = process.split('_')
    pres = []
    for name in names:
        pres.append(name)
        if 'HT' in name: break
    pProcesses = pres[:-1]
    range = pres[-1:]
    if len(pProcesses) == 1:
        pProcess = pProcesses[0]
    elif len(pProcesses) == 2:
        pProcess = pProcesses[0] + pProcesses[1]

    return pProcess + '(' + range[0] + ')'


if __name__ == '__main__':

    import ROOT as r
    
    c1 = r.TCanvas('c1', 'c1')
    
    h = r.TH1F("h", "; p_{T}^{Bar} (TeV); Events / 2 TeV (10^{3})", 50, -50, 50)
    gaus1 = r.TF1('gaus1', 'gaus')
    gaus1.SetParameters(1, 0, 5)
    h.FillRandom("gaus1", 50000)
    h.Scale(0.001)
    h.Draw()

    legend_args = (0.645, 0.79, 0.985, 0.91, '', 'NDC')
    
    legend = r.TLegend(*legend_args)
    legend.SetFillStyle(0)
    legend.AddEntry(h, "h1", "l")
    legend.AddEntry(h, "h1 again", "l")
    legend.Draw()

    cmsStyling(25000., 13., title='test')

    r.gStyle.SetOptStat(0000)
    r.gPad.Update()
    r.gPad.SaveAs('tdrstyle.png')
