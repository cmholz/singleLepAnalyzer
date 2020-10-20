#!/usr/bin/python

targetlumi = 35867. # 1/pb
targetlumi2017 = 41530.
targetlumi2018 = 59690.

genHTweight={}
genHTweight['WJetsMG100'] = 0.998056#https://github.com/jmhogan/GenHTweight/blob/master/WJetsToLNuSFs.txt
genHTweight['WJetsMG200'] = 0.978569
genHTweight['WJetsMG400'] = 0.928054
genHTweight['WJetsMG600'] = 0.856705
genHTweight['WJetsMG800'] = 0.757463
genHTweight['WJetsMG1200']= 0.608292
genHTweight['WJetsMG2500']= 0.454246

genHTweight['DYMG100'] = 1.007516#https://github.com/jmhogan/GenHTweight/blob/master/DYJetsToLLSFs.txt
genHTweight['DYMG200'] = 0.992853
genHTweight['DYMG400'] = 0.974071
genHTweight['DYMG600'] = 0.948367
genHTweight['DYMG800'] = 0.883340
genHTweight['DYMG1200']= 0.749894
genHTweight['DYMG2500']= 0.617254

BR={}
BR['BW'] = 0.5
BR['TZ'] = 0.25
BR['TH'] = 0.25
BR['TTBWBW'] = BR['BW']*BR['BW']
BR['TTTHBW'] = 2*BR['TH']*BR['BW']
BR['TTTZBW'] = 2*BR['TZ']*BR['BW']
BR['TTTZTZ'] = BR['TZ']*BR['TZ']
BR['TTTZTH'] = 2*BR['TZ']*BR['TH']
BR['TTTHTH'] = BR['TH']*BR['TH']

BR['TW'] = 0.5
BR['BZ'] = 0.25
BR['BH'] = 0.25
BR['BBTWTW'] = BR['TW']*BR['TW']
BR['BBBHTW'] = 2*BR['BH']*BR['TW']
BR['BBBZTW'] = 2*BR['BZ']*BR['TW']
BR['BBBZBZ'] = BR['BZ']*BR['BZ']
BR['BBBZBH'] = 2*BR['BZ']*BR['BH']
BR['BBBHBH'] = BR['BH']*BR['BH']

# Number of processed MC events (before selections)
nRun={}
# new counts for 2016.  updated May 3, 2020
#nRun['DYMG200'] = 11206441.0 # from integral 11225887.0, file DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_1_hadd.root 1-5
nRun['DYMG400'] = 9725661.0 # from integral 9725661.0, file DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root 1-2
nRun['DYMG600'] = 8259668.0 # from integral 8259668.0, file DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG800'] = 2673066.0 # from integral 2673066.0, file DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG1200'] = 596079.0 # from integral 596079.0, file DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG2500'] = 399492.0 # from integral 399492.0, file DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht1000'] = 15189124.0 # from integral 15189124.0, file QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root 1-2
nRun['QCDht1500'] = 11800132.0 # from integral 11800132.0, file QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['QCDht2000'] = 6019541.0 # from integral 6019541.0, file QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root
#nRun['QCDht200'] = 54251666.0 # from integral 54289442.0, file QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['QCDht300'] = 54233588.0 # from integral 54233588.0, file QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root 1-5
nRun['QCDht500'] = 62622029.0 # from integral 62622029.0, file QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root 1-2
nRun['QCDht700'] = 37213646.0 # from integral 37213646.0, file QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root 1-3


## 2L2Nu, Had, SemiLep --> sample1 sample2
# counts from dump counts

##variables are numbers from dumpcounts
#nRun['TTJets0'] = num for sample 1 * 0.8832
#nRun['TTJetsExt0'] = num for sample 2 * 0.8832
##Almost like you're removing 2L2Nu completely everywhere
##Replace "had" with "sample 1" and "semiLep" with sample2
##'''
nrunttJets2L2Nu = 67272494.0 # from integral 67820400.0, file TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nruntthad = 67944132.0 # from integral 68498800.0, file TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nrunttJetsSemiLep = 107604800.0 # from integral 107604800.0, file TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nrunttJets = 76294178.0 # from integral 76294178.0, file TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nrunttJetsPS = 77746400.0 # from integral 77746400.0, file TT_TuneCUETP8M2T4_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root 
nruntt1000 = 19253087.0 # from integral 19253087.0, file TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8_hadd.root
nruntt700 = 29545508.0 # from integral 29545508.0, file TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8_hadd.root

nRun['TTJets0'] = nrunttJets*0.8832 + nrunttJetsPS*0.8832   # hadronic*BR(0-700)
nRun['TTJets700'] = nrunttJets*0.0921 + nrunttJetsPS*0.0921 + nruntt700   #hadronic*BR(700-1000) + mass700*BR(hadronic)
nRun['TTJets1000'] = nrunttJets*0.02474 + nrunttJetsPS*0.02474 + nruntt1000  #hadronic*BR(1000+) + mass1000*BR(hadronic
nRun['TTJetsPS0'] = nrunttJetsPS*0.8832 + nrunttJets*0.8832  # semilept*BR(0-700)
nRun['TTJetsPS700'] = nrunttJetsPS*0.0921 + nrunttJets*0.0921 + nruntt700   #semilept*BR(700-1000) + mass700*BR(semilept)
nRun['TTJetsPS1000'] = nrunttJetsPS*0.02474 + nrunttJets*0.02474 + nruntt1000   #semilept*BR(1000+) + mass1000*BR(semilept)
nRun['TTJets2L2nu0'] = nrunttJets2L2Nu*0.8832  #dilepton*BR(0-700)
nRun['TTJets2L2nu700'] = nrunttJets2L2Nu*0.0921 + nruntt700*0.105 #dilepton*BR(700-1000) + mass700*BR(dilepton)
nRun['TTJets2L2nu1000'] = nrunttJets2L2Nu*0.02474 + nruntt1000*0.105 #dilepton*BR(1000+) + mass1000*BR(dilepton)
nRun['TTJetsHad0'] = nruntthad*0.8832   # hadronic*BR(0-700)
nRun['TTJetsHad700'] = nruntthad*0.0921 + nruntt700*0.457 #hadronic*BR(700-1000) + mass700*BR(hadronic)
nRun['TTJetsHad1000'] = nruntthad*0.02474 + nruntt1000*0.457 #hadronic*BR(1000+) + mass1000*BR(hadronic
nRun['TTJetsSemiLep0'] = nrunttJetsSemiLep*0.8832  # semilept*BR(0-700)
nRun['TTJetsSemiLep700'] = nrunttJetsSemiLep*0.0921 + nruntt700*0.438 #semilept*BR(700-1000) + mass700*BR(semilept)
nRun['TTJetsSemiLep1000'] = nrunttJetsSemiLep*0.02474 + nruntt1000*0.438 #semilept*BR(1000+) + mass1000*BR(semilept)
nRun['TTJetsPH700mtt'] = nruntt700 + nruntthad*0.0921 + nrunttJetsSemiLep*0.0921 + nrunttJets2L2Nu*0.0921 #mass700 + inclusive*BR(700)
nRun['TTJetsPH1000mtt'] = nruntt1000 + nruntthad*0.02474 + nrunttJetsSemiLep*0.02474 + nrunttJets2L2Nu*0.02474 #mass1000 + inclusive*BR(1000)


nRun['Ts'] = 6105500.0 # from integral 9811800.0, file ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_hadd.root 
nRun['Tbt'] = 39635800.0 # from integral 39635800.0, file ST_t-channel_antitop_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin_1_hadd.root
nRun['Tt']= 67981000.0 # from integral 67981000.0, file ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin_1_hadd.root
nRun['TtW'] = 992024.0 # from integral 992024.0, file ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_hadd.root
nRun['TbtW'] = 998276.0 # from integral 998276.0, file ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_hadd.root


#nRun['WJetsMG200'] = 25423155.0 # from integral 25468933.0, file WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root 1-7
nRun['WJetsMG400'] = 7673923.0 # from integral 7673923.0, file WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root 
nRun['WJetsMG600'] = 18687480.0 # from integral 18687480.0, file WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG800'] = 7729615.0 # from integral 7729615.0, file WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG1200'] = 6828327.0 # from integral 6828327.0, file WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG2500'] = 2617018.0 # from integral 2617018.0, file WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root

#'''ASK about these too'''
#nRun['WJetsPt100'] = 120124110.*(1.-2.*0.32) #Full =120124110, neg frac 0.32
#nRun['WJetsPt250'] = 12022587.*(1.-2.*0.31555) #Full = 12022587, neg frac 0.31555 
#nRun['WJetsPt400'] = 1939947.*(1.-2.*0.30952) #Full = 1939947, neg frac 0.30952
#nRun['WJetsPt600'] = 1974619.*(1.-2.*0.29876) #Full = 1974619, neg frac 0.29876
#''''''

nRun['WW'] = 7982180.0 # from integral 7982180.0, file WW_TuneCUETP8M1_13TeV-pythia8_hadd.root
nRun['WZ'] = 3997571.0 # from integral 3997571.0, file WZ_TuneCUETP8M1_13TeV-pythia8_hadd.root 
nRun['ZZ'] = 1988098.0 # from integral 1988098.0, file ZZ_TuneCUETP8M1_13TeV-pythia8_hadd.root

#'''
#ASK ABOUT THESE
#nRun['TTW'] = 
#9384328. # from integral 9425384.0, file ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
#nRun['TTZ'] = 
#8519074. # from integral 8536618.0, file ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
#nRun['TTH'] = 
#9580578. # from integral 9783674.0, file ttH_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
#nRun['TTWq'] = 
#430310. #from 833298
#nRun['TTZq'] = 
#351164. #from 749400
#'''

nRun['TTWl'] = 2716249.0 # from integral 5280565.0, file TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root 
nRun['TTZl'] = 6403526.0 # from integral 13727464.0, file TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_1_hadd.root
nRun['TTHnoB'] = 3877940.0 # from integral 3952850.0, file ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8_hadd.root
nRun['TTHB'] = 3936004.0 # from integral 3936004.0, file ttHTobb_M125_13TeV_powheg_pythia8_hadd.root



TT700 = 762800.0 # from integral 762800.0, file TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT800 = 785000.0 # from integral 785000.0, file TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT900 = 831200.0 # from integral 831200.0, file TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1000 = 828800.0 # from integral 828800.0, file TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1100 = 832800.0 # from integral 832800.0, file TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1200 = 799800.0 # from integral 799800.0, file TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1300 = 804200.0 # from integral 804200.0, file TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1400 = 682200.0 # from integral 682200.0, file TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1500 = 830400.0 # from integral 830400.0, file TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1600 = 811000.0 # from integral 811000.0, file TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1700 = 751800.0 # from integral 751800.0, file TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root
TT1800 = 833000.0 # from integral 833000.0, file TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root

nRun['TTM700BWBW'] = TT700*0.333*0.333
nRun['TTM800BWBW'] = TT800*0.333*0.333
nRun['TTM900BWBW'] = TT900*0.333*0.333
nRun['TTM1000BWBW'] = TT1000*0.333*0.333
nRun['TTM1100BWBW'] = TT1100*0.333*0.333
nRun['TTM1200BWBW'] = TT1200*0.333*0.333
nRun['TTM1300BWBW'] = TT1300*0.333*0.333
nRun['TTM1400BWBW'] = TT1400*0.333*0.333 
nRun['TTM1500BWBW'] = TT1500*0.333*0.333 
nRun['TTM1600BWBW'] = TT1600*0.333*0.333 
nRun['TTM1700BWBW'] = TT1700*0.333*0.333 
nRun['TTM1800BWBW'] = TT1800*0.333*0.333
nRun['TTM700THBW'] = TT700*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM800THBW'] = TT800*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM900THBW'] = TT900*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1000THBW'] = TT1000*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1100THBW'] = TT1100*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1200THBW'] = TT1200*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1300THBW'] = TT1300*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1400THBW'] = TT1400*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1500THBW'] = TT1500*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1600THBW'] = TT1600*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1700THBW'] = TT1700*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM1800THBW'] = TT1800*0.333*0.333*2 #THBW Scaled by 2
nRun['TTM700TZBW'] = TT700*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM800TZBW'] = TT800*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM900TZBW'] = TT900*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM900TZBW'] = TT900*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1000TZBW'] = TT1000*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1100TZBW'] = TT1100*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1200TZBW'] = TT1200*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1300TZBW'] = TT1300*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1400TZBW'] = TT1400*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1500TZBW'] = TT1500*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1600TZBW'] = TT1600*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1700TZBW'] = TT1700*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM1800TZBW'] = TT1800*0.333*0.333*2 #TZBW Scaled by 2
nRun['TTM700TZTZ'] = TT700*0.333*0.333
nRun['TTM800TZTZ'] = TT800*0.333*0.333
nRun['TTM900TZTZ'] = TT900*0.333*0.333
nRun['TTM1000TZTZ'] = TT1000*0.333*0.333
nRun['TTM1100TZTZ'] = TT1100*0.333*0.333
nRun['TTM1200TZTZ'] = TT1200*0.333*0.333
nRun['TTM1300TZTZ'] = TT1300*0.333*0.333
nRun['TTM1400TZTZ'] = TT1400*0.333*0.333 
nRun['TTM1500TZTZ'] = TT1500*0.333*0.333 
nRun['TTM1600TZTZ'] = TT1600*0.333*0.333 
nRun['TTM1700TZTZ'] = TT1700*0.333*0.333 
nRun['TTM1800TZTZ'] = TT1800*0.333*0.333 
nRun['TTM700TZTH'] = TT700*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM800TZTH'] = TT800*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM900TZTH'] = TT900*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1000TZTH'] = TT1000*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1100TZTH'] = TT1100*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1200TZTH'] = TT1200*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1300TZTH'] = TT1300*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1400TZTH'] = TT1400*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1500TZTH'] = TT1500*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1600TZTH'] = TT1600*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1700TZTH'] = TT1700*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM1800TZTH'] = TT1800*0.333*0.333*2 #TZTH Scaled by 2
nRun['TTM700THTH'] = TT700*0.333*0.333
nRun['TTM800THTH'] = TT800*0.333*0.333
nRun['TTM900THTH'] = TT900*0.333*0.333
nRun['TTM1000THTH'] = TT1000*0.333*0.333
nRun['TTM1100THTH'] = TT1100*0.333*0.333
nRun['TTM1200THTH'] = TT1200*0.333*0.333
nRun['TTM1300THTH'] = TT1300*0.333*0.333
nRun['TTM1400THTH'] = TT1400*0.333*0.333 
nRun['TTM1500THTH'] = TT1500*0.333*0.333 
nRun['TTM1600THTH'] = TT1600*0.333*0.333 
nRun['TTM1700THTH'] = TT1700*0.333*0.333 
nRun['TTM1800THTH'] = TT1800*0.333*0.333



BB700 = 682400.0 # from integral 682400.0, file BprimeBprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB800 = 761200.0 # from integral 761200.0, file BprimeBprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB900 = 799800.0 # from integral 799800.0, file BprimeBprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1000 = 831400.0 # from integral 831400.0, file BprimeBprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1100 = 774800.0 # from integral 774800.0, file BprimeBprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1200 = 825400.0 # from integral 825400.0, file BprimeBprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1300 = 805200.0 # from integral 805200.0, file BprimeBprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1400 = 826200.0 # from integral 826200.0, file BprimeBprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1500 = 784000.0 # from integral 784000.0, file BprimeBprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1600 = 684000.0 # from integral 684000.0, file BprimeBprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1700 = 751800.0 # from integral 751800.0, file BprimeBprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root
BB1800 = 833000.0 # from integral 833000.0, file BprimeBprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root

nRun['BBM700TWTW'] = BB700*0.333*0.333
nRun['BBM800TWTW'] = BB800*0.333*0.333
nRun['BBM900TWTW'] = BB900*0.333*0.333
nRun['BBM1000TWTW'] = BB1000*0.333*0.333
nRun['BBM1100TWTW'] = BB1100*0.333*0.333
nRun['BBM1200TWTW'] = BB1200*0.333*0.333
nRun['BBM1300TWTW'] = BB1300*0.333*0.333
nRun['BBM1400TWTW'] = BB1400*0.333*0.333
nRun['BBM1500TWTW'] = BB1500*0.333*0.333
nRun['BBM1600TWTW'] = BB1600*0.333*0.333
nRun['BBM1700TWTW'] = BB1700*0.333*0.333
nRun['BBM1800TWTW'] = BB1800*0.333*0.333
nRun['BBM700BHTW'] = BB700*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM800BHTW'] = BB800*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM900BHTW'] = BB900*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1000BHTW'] = BB1000*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1100BHTW'] = BB1100*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1200BHTW'] = BB1200*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1300BHTW'] = BB1300*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1400BHTW'] = BB1400*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1500BHTW'] = BB1500*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1600BHTW'] = BB1600*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1700BHTW'] = BB1700*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM1800BHTW'] = BB1800*0.333*0.333*2 #BHTW Scaled by 2
nRun['BBM700BZTW'] = BB700*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM800BZTW'] = BB800*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM900BZTW'] = BB900*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1000BZTW'] = BB1000*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1100BZTW'] = BB1100*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1200BZTW'] = BB1200*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1300BZTW'] = BB1300*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1400BZTW'] = BB1400*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1500BZTW'] = BB1500*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1600BZTW'] = BB1600*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1700BZTW'] = BB1700*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM1800BZTW'] = BB1800*0.333*0.333*2 #BZTW Scaled by 2
nRun['BBM700BZBZ'] = BB700*0.333*0.333
nRun['BBM800BZBZ'] = BB800*0.333*0.333
nRun['BBM900BZBZ'] = BB900*0.333*0.333
nRun['BBM1000BZBZ'] = BB1000*0.333*0.333
nRun['BBM1100BZBZ'] = BB1100*0.333*0.333
nRun['BBM1200BZBZ'] = BB1200*0.333*0.333
nRun['BBM1300BZBZ'] = BB1300*0.333*0.333
nRun['BBM1400BZBZ'] = BB1400*0.333*0.333
nRun['BBM1500BZBZ'] = BB1500*0.333*0.333
nRun['BBM1600BZBZ'] = BB1600*0.333*0.333
nRun['BBM1700BZBZ'] = BB1700*0.333*0.333
nRun['BBM1800BZBZ'] = BB1800*0.333*0.333
nRun['BBM700BZBH'] = BB700*0.333*0.333*2
nRun['BBM800BZBH'] = BB800*0.333*0.333*2
nRun['BBM900BZBH'] = BB900*0.333*0.333*2
nRun['BBM1000BZBH'] = BB1000*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1100BZBH'] = BB1100*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1200BZBH'] = BB1200*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1300BZBH'] = BB1300*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1400BZBH'] = BB1400*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1500BZBH'] = BB1500*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1600BZBH'] = BB1600*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1700BZBH'] = BB1700*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM1800BZBH'] = BB1800*0.333*0.333*2 #BZBH Scaled by 2
nRun['BBM700BHBH'] = BB700*0.333*0.333
nRun['BBM800BHBH'] = BB800*0.333*0.333
nRun['BBM900BHBH'] = BB900*0.333*0.333
nRun['BBM1000BHBH'] = BB1000*0.333*0.333
nRun['BBM1100BHBH'] = BB1100*0.333*0.333
nRun['BBM1200BHBH'] = BB1200*0.333*0.333
nRun['BBM1300BHBH'] = BB1300*0.333*0.333
nRun['BBM1400BHBH'] = BB1400*0.333*0.333
nRun['BBM1500BHBH'] = BB1500*0.333*0.333
nRun['BBM1600BHBH'] = BB1600*0.333*0.333
nRun['BBM1700BHBH'] = BB1700*0.333*0.333
nRun['BBM1800BHBH'] = BB1800*0.333*0.333

# Cross sections for MC samples (in pb) -- most unchanged for 2017
xsec={}
xsec['DY'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG100'] = 147.4*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG200'] = 40.99*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG400'] = 5.678*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG600'] = 1.367*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG800'] = 0.6304*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG1200'] = 0.1514*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG2500'] = 0.003565*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['TTJets'] = 831.76
xsec['WJets'] = 61526.7
xsec['WJetsMG'] = 61526.7
xsec['TTJetsPH'] = 831.76 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
#xsec['TTJetsPH0to700inc'] = 831.76
#xsec['TTJetsPH700to1000inc'] = 831.76*0.0921 #(xsec*filtering coeff.)
#xsec['TTJetsPH1000toINFinc'] = 831.76*0.02474 #(xsec*filtering coeff.)

#Cross section -- physics-based interaction probability
#"Hadronic" = 45.7%
#"semileptonic" = 43.8%
#"2L2Nu" = 10.5%
#Sample1, Sample2 are the same -- just 831.76

# don't need final multiplier
xsec['TTJets0'] = 831.76*0.8832 ## THESE WERE REMOVED: BRs from PDG Top Review 2018: 45.7%/43.8%/10.5% 0/1/2 leptons
xsec['TTJets700'] = 831.76*0.0921
xsec['TTJets1000'] = 831.76*0.02474
xsec['TTJetsPS0'] = 831.76*0.8832
xsec['TTJetsPS700'] = 831.76*0.0921
xsec['TTJetsPS1000'] = 831.76*0.02474
xsec['TTJetsHad0'] = 831.76*0.8832*0.457  ## BRs from PDG Top Review 2018: 45.7%/43.8%/10.5% 0/1/2 leptons
xsec['TTJetsHad700'] = 831.76*0.0921*0.457
xsec['TTJetsHad1000'] = 831.76*0.02474*0.457
xsec['TTJetsSemiLep0'] = 831.76*0.8832*0.438
xsec['TTJetsSemiLep700'] = 831.76*0.0921*0.438
xsec['TTJetsSemiLep1000'] = 831.76*0.02474*0.438
xsec['TTJets2L2nu0'] = 831.76*0.8832*0.105
xsec['TTJets2L2nu700'] = 831.76*0.0921*0.105
xsec['TTJets2L2nu1000'] = 831.76*0.02474*0.105
xsec['TTJetsPH700mtt'] = 831.76*0.0921 #(xsec*filtering coeff.)
xsec['TTJetsPH1000mtt'] = 831.76*0.02474 #(xsec*filtering coeff.)

xsec['TTJetsPH700mtt'] = 831.76*0.0921 #(xsec*filtering coeff.)
xsec['TTJetsPH1000mtt'] = 831.76*0.02474 #(xsec*filtering coeff.)

xsec['TTHnoB'] = 0.2151
xsec['TTHB'] = 0.2934

xsec['WJetsMG100'] = 1345.*1.21 # (1.21 = k-factor )# https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG200'] = 359.7*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG400'] = 48.91*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG600'] = 12.05*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG800'] = 5.501*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG1200'] = 1.329*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG2500'] = 0.03216*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns 
xsec['WJetsPt100'] = 676.3 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt250'] = 23.94 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt400'] = 3.031 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt600'] = 0.4524 #B2G-17-010 / AN2016_480_v5
xsec['WW'] = 118.7 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeVInclusive
xsec['WZ'] = 47.13 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['ZZ'] = 16.523 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['TTH'] = 0.5269 # from XsecDB, NLO
xsec['TTW'] = 0.4611 # from XsecDB, LO
xsec['TTZ'] = 0.5407 # from XsecDB, LO
xsec['TTZl'] = 0.2529 # from McM
xsec['TTZq'] = 0.5297 # from McM
xsec['TTWl'] = 0.2043 # from McM
xsec['TTWq'] = 0.4062 # from McM
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Ts'] = 10.32*0.333 #(leptonic, t+tbar) https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbs'] = 3.97*0.333 #(leptonic)# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TbtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec

xsec['TTM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo

xsec['BBM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo

xsec['X53X53M700left']   = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M700right']  = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M800left']   = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M800right']  = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M900left']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M900right']  = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1000left']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1000right'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1100left']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1100right'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1200left']  = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1200right'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1300left']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1300right'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1400left']  = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1400right'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1500left']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1500right'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1600left']  = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1600right'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top

xsec['QCDht100'] = 27990000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht200'] = 1712000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht300'] = 347700. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht500'] = 32100. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht700'] = 6831. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht1000'] = 1207. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht1500'] = 119.9 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht2000'] = 25.24 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()):
       # print 'sample: ',sample 
	if 'BBM' not in sample and 'TTM' not in sample: 
		#print sample, (xsec[sample]) , (nRun[sample])
		weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
	else: weight[sample] = (targetlumi*BR[sample[:2]+sample[-4:]]*xsec[sample[:-4]]) / (nRun[sample])
# Samples for Jet reweighting (to be able to run w/ and w/o JSF together!):
for sample in sorted(nRun.keys()):
	if 'QCDht' in sample or 'WJetsMG' in sample: weight[sample+'JSF'] = weight[sample]

#  LocalWords:  nRun
