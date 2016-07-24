#!/usr/bin/env python
# Tai Sakuma <sakuma@cern.ch>
import os, sys
import argparse

import ROOT

import AlphaTwirl

ROOT.gROOT.SetBatch(1)

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help = "the path to the input file")
parser.add_argument("-p", "--processes", default = 1, type = int, help = "number of processes to run in parallel")
parser.add_argument('-o', '--outdir', default = os.path.join('tbl', 'out'))
parser.add_argument('--force', action = 'store_true', default = False, help = 'recreate all output files')
args = parser.parse_args()

##__________________________________________________________________||
def main():

    progressMonitor = AlphaTwirl.ProgressBar.NullProgressMonitor()
    communicationChannel = AlphaTwirl.Concurrently.CommunicationChannel(args.processes, progressMonitor)
    progressMonitor.begin()
    communicationChannel.begin()

    reader_collector_pairs = [(Reader(), AlphaTwirl.EventReader.NullCollector())]

    tableConfigCompleter = AlphaTwirl.Configure.TableConfigCompleter(
        defaultCountsClass = AlphaTwirl.Counter.Counts,
        defaultOutDir = args.outdir
    )

    echo = AlphaTwirl.Binning.Echo(nextFunc = None)
    tblcfg = [
        dict(branchNames = ('run', ), binnings = (echo, )),
        dict(branchNames = ('lumi', ), binnings = (echo, )),
        dict(branchNames = ('eventId', ), binnings = (echo, )),
    ]

    tblcfg = [tableConfigCompleter.complete(c) for c in tblcfg]
    if not args.force:
        tblcfg = [c for c in tblcfg if c['outFile'] and not os.path.exists(c['outFilePath'])]

    reader_collector_pairs.extend([AlphaTwirl.Configure.build_counter_collector_pair(c) for c in tblcfg])

    reader_top = AlphaTwirl.EventReader.ReaderComposite()
    collector_top = AlphaTwirl.EventReader.CollectorComposite(progressMonitor.createReporter())
    for r, c in reader_collector_pairs:
        reader_top.add(r)
        collector_top.add(c)


    eventLoopRunner = AlphaTwirl.EventReader.MPEventLoopRunner(communicationChannel)
    eventBuilder = EventBuilder()
    eventReader = AlphaTwirl.EventReader.EventReader(eventBuilder, eventLoopRunner, reader_top, collector_top)

    eventReader.begin()

    dataset = Dataset('root3', [args.input])
    eventReader.read(dataset)

    eventReader.end()


    communicationChannel.end()
    progressMonitor.end()

##__________________________________________________________________||
class Reader(object):
    def begin(self, event):
        self.run = [ ]
        self.lumi = [ ]
        self.eventId = [ ]
        self._attach_to_event(event)

        self.handleHFPreRecHit = Handle("edm::SortedCollection<HFPreRecHit,edm::StrictWeakOrdering<HFPreRecHit> >")
        self.handlePFMETs = Handle("std::vector<reco::PFMET>")

    def _attach_to_event(self, event):
        event.run = self.run
        event.lumi = self.lumi
        event.eventId = self.eventId

    def event(self, event):
        self._attach_to_event(event)

        self.run[:] = [event.eventAuxiliary().run()]
        self.lumi[:] = [event.eventAuxiliary().luminosityBlock()]
        self.eventId[:] = [event.eventAuxiliary().event()]
        print '%6d'    % self.run[0],
        print '%10d'   % self.lumi[0],
        print '%9d'    % self.eventId[0],
        print

        event.getByLabel("pfMet", self.handlePFMETs)
        print self.handlePFMETs.product().front()

        event.getByLabel('hfprereco', self.handleHFPreRecHit)
        print self.handleHFPreRecHit.product()

    def end(self):
        self.handleHFPreRecHit = None
        self.handlePFMETs = None

##__________________________________________________________________||
def loadLibraries():
    argv_org = list(sys.argv)
    sys.argv = [e for e in sys.argv if e != '-h']
    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.AutoLibraryLoader.enable()
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.gSystem.Load("libDataFormatsPatCandidates")
    sys.argv = argv_org

##__________________________________________________________________||
loadLibraries()
from DataFormats.FWLite import Events, Handle

##__________________________________________________________________||
class Dataset(object):
    def __init__(self, name, files):
        self.name = name
        self.files = files

##__________________________________________________________________||
class EventBuilder(object):
    def __init__(self):
        pass

    def build(self, dataset, start = 0, nEvents = -1):
        return Events(dataset.files)

##__________________________________________________________________||
if __name__ == '__main__':
    main()
