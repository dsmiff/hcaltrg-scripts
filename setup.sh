. /cvmfs/cms.cern.ch/cmsset_default.sh
cd ../CMSSW_8_1_0_pre8/src
eval `scramv1 runtime -sh`
cd - > /dev/null
export PYTHONPATH=$PWD/AlphaTwirl:$PYTHONPATH
export PYTHONPATH=$PWD/:$PYTHONPATH
python Core/splash.py