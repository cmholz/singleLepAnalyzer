#Arguements: iPlot, region, isCategorized, directory, blind, yLog, rebinning

#plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets iNBDeepJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_May2020TT_May9 False False 
#    python plotTemplates.py $iPlot PS False kinematicsPS_May2020TT_May9 False True  
    #python plotTemplates.py $iPlot CR False kinematicsCR_May2020TT_May9 False False
    #python plotTemplates.py $iPlot CR False kinematicsCR_May2020TT_May9 False True
#done

#plotList='tmass HT'

#plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnBprime DnnWJetsBB DnnTTbarBB tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NBDeepJets NBJetsNoSF NBDeepJetNoSF NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEta JetEtaAK8 NTrue minMlb minDPhiMetJet lepPhi'
#plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NBDeepJets NBJetsNoSF NBDeepJetNoSF NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEta JetEtaAK8 NTrue minMlb minDPhiMetJet lepPhi'
plotList='lepPhi NBDeepJet'
#plotList2='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR'
#plotList2='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR'
#plotList3='ST HT DnnTprime DnnWJets DnnTTbar'
#plotList3='ST HT DnnBprime DnnWJetsBB DnnTTbarBB'
#plotList4='ST Tp2Mass Tp2MDnn Tp2MST DnnTprime HT'
#plotList4='ST Bp2Mass Bp2MDnn Bp2MST DnnBprime HT'
#plotList5='DnnTprime'
#plotList6='DnnBrime'
#plotList7='HTNtag'
#plotList='DnnTprime DnnWJets DnnTTbar HT Tp2Mass probSumDecay probSumFoprobb probh probj probt probw probz probb probh probj probt probw probz'
#plotListb='DnnBprime DnnWJetsBB DnnTTbarBB HT Bp2Mass probSumDecay probSumFoprobb probh probj probt probw probz probb probh probj probt probw probz'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False False
    python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False True
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False True
done

#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False True
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True False
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True True
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False False
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False False
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False True
#done

#for iPlot in $plotListb; do
#    echo $iPlot
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020BB False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020BB False True
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020BB True False
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020BB True True
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020BB False False
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020BB False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020BB False False
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020BB False True
#done

#
#for iPlot in $plotList2; do
#    echo $iPlot
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False True
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False False
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False False
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False True
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True True
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True False
#done
##
#for iPlot in $plotList3; do
#    echo $iPlot
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False False
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False False
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False True
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True False
#    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True True
#done

#for iPlot in $plotList5; do
#    echo $iPlot
#    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True True 0p3
#done
#
#for iPlot in $plotList6; do
#    echo $iPlot
#    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True True 0p3
#done
#
#for iPlot in $plotList7; do
#    echo $iPlot
#    python plotTemplates.py $iPlot CR True templatesCR_June2020TT False False 0p3
#    python plotTemplates.py $iPlot CR True templatesCR_June2020TT False True 0p3
#    python plotTemplates.py $iPlot SR True templatesCR_June2020TT True False 0p3
#    python plotTemplates.py $iPlot SR True templatesCR_June2020TT True True 0p3
#done


#for iPlot in $plotList5; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT  True False 0p3
#    python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT True True 0p3
#done







#for iPlot in $plotList; do
#    echo $iPlot
    #python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False False
    #python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False True
    #python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False False
    #python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False True
    #python plotTemplates.py $iPlot CR False kinematicsCR_June2020 False False
    #python plotTemplates.py $iPlot CR False kinematicsCR_June2020 False True
    #python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False False
    #python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False True
    #python plotTemplates.py $iPlot SR False kinematicsSR_May2020TT_May9 True False
    #python plotTemplates.py $iPlot SR False kinematicsSR_May2020TT_May9 True True
#done

#plotList='ST HT DnnTprime DnnWJets DnnTTbar'
#for iPlot in $plotList; do
#    echo $iPlot
#    #python plotTemplates.py $iPlot TTCR False kinematicsTTCR_May2020TT_May9 False False 
#    #python plotTemplates.py $iPlot TTCR False kinematicsTTCR_May2020TT_May9 False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_May2020TT_May9 False False 
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_May2020TT_May9 False True
#    #python plotTemplates.py $iPlot SR False kinematicsSR_May2020TT_May9 True False
#    #python plotTemplates.py $iPlot SR False kinematicsSR_May2020TT_May9 True True
#done

#plotList='DnnTprime'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot SR True templatesSR_May2020TT_May9 True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_May2020TT_May9 True True 0p3
#done



# SPECIAL PS PLOTS
#plotList='DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False False
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False True
#done
