import os,sys

filelist = {
'BprimeBprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':7,
'BprimeBprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':3,
'BprimeBprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
#'BprimeBprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':3,
#'BprimeBprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'BprimeBprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_BHBH_1_hadd.root':4,
'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
#'DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8_1_hadd.root':5,
'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':2,
'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':2,
'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
#'QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root':5,
'QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':5,
'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':2,
'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':3,
'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_hadd.root':0,
'ST_t-channel_antitop_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin_1_hadd.root':4,
'ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin_1_hadd.root':7,
'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_hadd.root':0,
'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4_hadd.root':0,

###### Don't need for 2016 ####
'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root':6,
'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000_1_hadd.root':6,
'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf_1_hadd.root':6,
'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root':6,
'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000_1_hadd.root':6,
'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf_1_hadd.root':6,
'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root':12,
'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt700to1000_1_hadd.root':12,
'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt1000toInf_1_hadd.root':12,
######

'TTWJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root':0,
'TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8_1_hadd.root':2,
#'TT_TuneCUETP8M2T4_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root':2,
#'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Mtt0to700_hadd.root':0,
'TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1100_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1200_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1300_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1400_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':3,
'TprimeTprime_M-1500_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1600_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1700_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-1800_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
#'TprimeTprime_M-700_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
#'TprimeTprime_M-800_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'TprimeTprime_M-900_TuneCUETP8M1_13TeV-madgraph-pythia8_BWBW_1_hadd.root':4,
'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':2,
'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_hadd.root':0,
'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':2,
'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_1_hadd.root':2,
#'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root':8,
'WW_TuneCUETP8M1_13TeV-pythia8_hadd.root':0,
'WZ_TuneCUETP8M1_13TeV-pythia8_hadd.root':0,
'ZZ_TuneCUETP8M1_13TeV-pythia8_hadd.root':0,
'ttHToNonbb_M125_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8_hadd.root':0,
'ttHTobb_M125_13TeV_powheg_pythia8_hadd.root':0,
'TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8_hadd.root':0,
'TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8_hadd.root':0,

}

from ROOT import TFile, TH1
eosdir = 'root://cmseos.fnal.gov//store/user/cholz/FWLJMET102X_1lep2016Dnn_06092020_step1hadds/'
for filekey in sorted(filelist.keys()):
    print('-------------------------------------------------------')
    rfile = TFile.Open(eosdir+filekey)
    hist = rfile.Get("weightHist")

    if filelist[filekey] > 1:
        print 'Opening ',filelist[filekey],'files:'
        for ifile in range(2,filelist[filekey]+1):
            #print 'file #',ifile
            tempfile = TFile.Open(eosdir+filekey.replace('_1_','_'+str(ifile)+'_'))
            temphist = tempfile.Get("weightHist")
	    #print "temphist: ",temphist
            temphist.SetDirectory(0)
            hist.Add(temphist)
            tempfile.Close()                                  

    adjusted = hist.GetBinContent(1)
    integral = hist.GetBinContent(5) + hist.GetBinContent(7)
    newpdf = hist.GetBinContent(2)

    if 'prime' not in filekey:
        print(str(adjusted)+'. # from integral '+str(integral)+', file '+filekey)
    else:
        print(str(newpdf)+'. # from integral '+str(integral)+', file '+filekey)

print 'done'





