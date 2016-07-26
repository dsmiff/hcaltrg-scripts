import os

CONST_PARAMS = {
    'intLumi': 21790.9,
    'signal_samples': ['samplesSignal'],
    'signal_modles': ['signalModels'],
    }

numcores = os.sysconf('SC_NPROCESSORS_ONLN')
if numcores is None:
    numcores = 1

import ROOT
ROOT.kTRUE
import logging
try: 
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

log = logging.getLogger(__name__)
log.addHandler(NullHandler())
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
streamer = logging.StreamHandler()
log.setLevel(logging.INFO)
streamer.setFormatter(formatter)
log.addHandler(streamer)

# Speed up
ROOT.SetSignalPolicy(ROOT.kSignalFast)
ROOT.gROOT.SetBatch(True)
log.info("ROOT is in batch mode")
