# Tai Sakuma <sakuma@cern.ch>

##__________________________________________________________________||
class EventAuxiliary(object):
    # https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/DataFormats/Provenance/interface/EventAuxiliary.h

    def begin(self, event):
        self.run = [ ]
        self.lumi = [ ]
        self.eventId = [ ]
        self._attach_to_event(event)

    def _attach_to_event(self, event):
        event.run = self.run
        event.lumi = self.lumi
        event.eventId = self.eventId

    def event(self, event):
        self._attach_to_event(event)

        eventAuxiliary = event.edm_event.eventAuxiliary()
        self.run[:] = [eventAuxiliary.run()]
        self.lumi[:] = [eventAuxiliary.luminosityBlock()]
        self.eventId[:] = [eventAuxiliary.event()]

##__________________________________________________________________||
class MET(object):
    def begin(self, event):
        self.pfMet = [ ]
        self._attach_to_event(event)

        self.handlePFMETs = Handle("std::vector<reco::PFMET>")

    def _attach_to_event(self, event):
        event.pfMet = self.pfMet

    def event(self, event):
        self._attach_to_event(event)

        edm_event = event.edm_event

        edm_event.getByLabel("pfMet", self.handlePFMETs)
        met = self.handlePFMETs.product().front()
        self.pfMet[:] = [met.pt()]

    def end(self):
        self.handlePFMETs = None

##__________________________________________________________________||
class Scratch(object):
    def begin(self, event):
        self._attach_to_event(event)

        self.handleHFPreRecHit = Handle("edm::SortedCollection<HFPreRecHit,edm::StrictWeakOrdering<HFPreRecHit> >")
        # SortedCollection: https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/DataFormats/Common/interface/SortedCollection.h
        # HFPreRecHit: https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/DataFormats/HcalRecHit/interface/HFPreRecHit.h

    def _attach_to_event(self, event):
        pass

    def event(self, event):
        self._attach_to_event(event)

        edm_event = event.edm_event

        edm_event.getByLabel('hfprereco', self.handleHFPreRecHit)
        hfPreRecoHits = self.handleHFPreRecHit.product()

        # for i in range(hfPreRecoHits.size()):
        #     rechit =  hfPreRecoHits[i]
        #     print rechit.id()

        for rechit in hfPreRecoHits:
            print rechit.id().ieta(),
            print rechit.id().iphi(),
            print rechit.getHFQIE10Info(0).charge(),
            print rechit.getHFQIE10Info(0).energy(),
            print rechit.getHFQIE10Info(0).timeRising(),
            print rechit.getHFQIE10Info(0).timeFalling(),
            print rechit.getHFQIE10Info(0).nRaw(),
            print rechit.getHFQIE10Info(0).soi(),
            print

        # print hfPreRecoHit.getHFQIE10Info(0)
        # print hfPreRecoHit.getHFQIE10Info(1)

    def end(self):
        self.handleHFPreRecHit = None

##__________________________________________________________________||
from DataFormats.FWLite import Handle
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_1_X/DataFormats/FWLite/python/__init__.py

##__________________________________________________________________||
