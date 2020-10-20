#!/bin/bash

hostname 

outDir=$1
iPlot=$2
region=$3
isCategorized=$4
isEM=$5
tag=$6
algo=$7

source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 project CMSSW CMSSW_10_2_10
cd CMSSW_10_2_10
eval `scramv1 runtime -sh`
cd -

python -u doHists.py $outDir $iPlot $region $isCategorized $isEM $tag $algo
