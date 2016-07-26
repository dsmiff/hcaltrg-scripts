import ROOT as r

class HistClass(object):
    def __init__(self, dimension, variable, bins, store_to_file=False):
        self.dimension = dimension
        self.variable  = variable
        self.bins      = bins
        self.hists     = {}
        self.storeHist = store_to_file
        
    def __len__(self):
        return len(self.bins)

    def register(self):
        if self.storeHist:
            self.file = r.TFile('twirl_outputs.root', 'RECREATE')
        else: pass

        self.histType = 'TH' + str(self.dimension)
        histo = getattr(r, self.histType)
        if self.__len__()==3:
            nBins, xMin, xMax = self.getHistDetails(self.bins)
            self.histo = histo(self.variable, self.variable, nBins, xMin, xMax)
        elif self.__len__()==6:
            nXBins, xMin, xMax, nYBins, yMin, yMax = self.getHistDetails(self.bins)
            self.histo = histo(self.variable, self.variable, nXBins, xMin, xMax, nYBins, yMin, yMax)
        else:
            print("ERROR: Please add more/less bin information")

        self.hists['h_{0}'.format(self.variable)] = self.histo
        
    def fill(self, value, weight=None):
        if value is not None:
            if len(self.hists)==1: histName = self.hists.keys()[0]
            else: print("More than one histogram %s is declared " % (self.hists.keys()))
            hist     = self.hists[histName]

            if weight is None: weight = 1
            hist.Fill(value, weight)
            
    def write(self):
        if self.storeHist:
            self.file.Write()
            
    def getHistDetails(self, bins):
        if self.__len__()==3:
            return bins[0], bins[1], bins[2]
        else:
            return bins[0], bins[1], bins[2], bins[3], bins[4], bins[5]
