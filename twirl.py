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
args = parser.parse_args()

##__________________________________________________________________||
def main():

    inputPath = args.input

    eventLoop = AlphaTwirl.EventReader.EventLoop(
        eventBuilder = EventBuilder(),
        dataset = [inputPath],
        reader = Reader()
    )

    eventLoop()

##__________________________________________________________________||
class Reader(object):
    def begin(self, event): pass

    def event(self, event):
        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()
        print '%6d'    % run,
        print '%10d'   % lumi,
        print '%9d'    % eventId,
        print

    def end(self): pass

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
class EventBuilder(object):
    def __init__(self):
        pass

    def build(self, files, start = 0, nEvents = -1):
        return Events(files)

##__________________________________________________________________||
if __name__ == '__main__':
    main()
