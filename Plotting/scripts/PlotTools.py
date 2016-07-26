import os
import sys
import ROOT as r
from plotInfo_cfi import labelDict

##____________________________________________________________________________________________||
def setStyle(hist, plot):

    if hist.ClassName()=='TH1D':
        try: 
            var = labelDict[plot]
            hist.GetXaxis().SetTitle(var)
            hist.GetYaxis().SetTitle("Events /%.2f" %(hist.GetXaxis().GetBinWidth(2)))
        except IOError, e:
            print >> sys.stderr, "Plot not found"
    else: 
        vars = plot.split('_')
        varX = labelDict[vars[0]]
        varY = labelDict[vars[1]]
        hist.GetXaxis().SetTitle(varX)
        hist.GetYaxis().SetTitle(varY)

    hist.SetTitle("")
    hist.SetMaximum(hist.GetMaximum()*1.25)

    return hist

##____________________________________________________________________________________________||
def getTotalHist(name, samples, plot, analyzer, file):
    
    hTotal = getHist(name, samples[0], plot, analyzer, file)
    for sample in samples[1:]:
        hTotal.Add(getHist(name, sample, plot, analyzer, file))

    return hTotal

##____________________________________________________________________________________________||
def getSmCount(name,samples,plot,analyzer,file, binA=0):

    smCount = 0
    smCountErrSq = 0.0
    for sample in samples:
        h = getHist(name,sample,plot,analyzer,file)
        smCountErrTmp = r.Double(0.)
        smCount += h.IntegralAndError(binA, h.GetNbinsX()+1, smCountErrTmp)
        smCountErrSq += smCountErrTmp**2
    
    return smCount

##____________________________________________________________________________________________||
def getHist(plot, file):
    
    histDict = {}
    name = file.GetName().split('/')[-1][:-5]
    hDict = findObject(file, name, histDict)
    h = hDict[name+'__'+plot]
    
    return h

##____________________________________________________________________________________________||
def findObject(objects,name, dict):

    for key in objects.GetListOfKeys():
        obj = key.ReadObj()
        if not obj.IsA().InheritsFrom( r.TDirectory.Class() ):
            dict[name+'__'+obj.GetName()] = obj.Clone()
        else:
            findObject(obj, name+'__'+obj.GetName(), dict)           
            pass
        pass
    return dict

##____________________________________________________________________________________________||
def numplaces(num, uncert=False):
    if uncert:
        l, r = '{}'.format(num).split('+/-')
        a, b = l.split('.')
        c, d = r.split('.')
        return len(a), len(b), len(d)
    else:
        # TODO temporary hack
        a, b = '{:.1f}'.format(num).split('.')
        return len(a), len(b)

##____________________________________________________________________________________________||
def is_uncert(num):
    uncert = True
    try:
        num.nominal_value
        num.std_dev
    except:
        uncert = False
    return uncert

##____________________________________________________________________________________________||
def table(names, cols):
    result = []

    spec = ' '.join(map(genspec, cols))

    result.append(r'\begin{{tabular}}{{{}}}'.format(spec))
    result.append(r'\toprule')
    result.append(' & '.join(map(r'\multicolumn{{1}}{{c}}{{{}}}'.format, names)) + r'\\')
    result.append(r'\midrule')

    line = []
    maxlen = 0
    for c in cols:
        maxlen = max(len(c), maxlen)
    for i in range(maxlen):
        for c in cols:
            try:
                if is_uncert(c[i]):
                    line.append('{:L}'.format(c[i]))
                else:
                    line.append('{}'.format(c[i]))
            except:
                line.append('')
        result.append(' & '.join(line) + r' \\')
        line = []

    result.append(r'\bottomrule')
    result.append(r'\end{tabular}')

    return '\n'.join(result)

##____________________________________________________________________________________________||
def genspec(col):
    amax = 0
    bmax = 0
    cmax = 0
    for v in col:
        if is_uncert(v):
            a, b, c = numplaces(v, uncert=True)
            if a > amax:
                amax = a
            if b > bmax:
                bmax = b
            if c > cmax:
                cmax = c
        else:
            a, b = numplaces(v)
            if a > amax:
                amax = a
            if b > bmax:
                bmax = b
    if cmax:
        return 'S[table-format={}.{}({})]'.format(amax, bmax, cmax)
    else:
        return 'S[table-format={}.{}]'.format(amax, bmax)

##____________________________________________________________________________________________||
if __name__=='__main__':
    pass
