#!/usr/bin/python

"""The uncertainties of the group will be applied to individual background processes 
   of each group (this is just for the yield tables)"""
modelingSys={}
#X53X53, Inclusive WJets sample, NOT REWEIGHTED, 8OCT16--SS ==> UPDATE FOR X53!!!!!!!
modelingSys['top_nT0_nW0_nB0']  =0.#nB0 is not used in X5/3
modelingSys['top_nT0_nW0_nB1']  =0.11
modelingSys['top_nT0_nW0_nB2p'] =0.15
modelingSys['top_nT0_nW1p_nB0'] =0.
modelingSys['top_nT0_nW1p_nB1'] =0.11
modelingSys['top_nT0_nW1p_nB2p']=0.15

modelingSys['top_nT1p_nW0_nB0']  =0.#nB0 is not used in X5/3
modelingSys['top_nT1p_nW0_nB1']  =0.11
modelingSys['top_nT1p_nW0_nB2p'] =0.15
modelingSys['top_nT1p_nW1p_nB0'] =0.
modelingSys['top_nT1p_nW1p_nB1'] =0.11
modelingSys['top_nT1p_nW1p_nB2p']=0.15

modelingSys['ewk_nT0_nW0_nB0']  =0.
modelingSys['ewk_nT0_nW0_nB1']  =0.10
modelingSys['ewk_nT0_nW0_nB2p'] =0.10
modelingSys['ewk_nT0_nW1p_nB0'] =0.
modelingSys['ewk_nT0_nW1p_nB1'] =0.13
modelingSys['ewk_nT0_nW1p_nB2p']=0.13

modelingSys['ewk_nT1p_nW0_nB0']  =0.
modelingSys['ewk_nT1p_nW0_nB1']  =0.10
modelingSys['ewk_nT1p_nW0_nB2p'] =0.10
modelingSys['ewk_nT1p_nW1p_nB0'] =0.
modelingSys['ewk_nT1p_nW1p_nB1'] =0.13
modelingSys['ewk_nT1p_nW1p_nB2p']=0.13

modelingSys['topE']=0.12
modelingSys['topM']=0.13
modelingSys['topL']=0.13
modelingSys['topAll']=0.13
modelingSys['ewkE']=0.14
modelingSys['ewkM']=0.09
modelingSys['ewkL']=0.11
modelingSys['ewkAll']=0.11

#dummies:
modelingSys['top_nW0p_nB1p']=0.
modelingSys['ewk_nW0p_nB1p']=0.

##### NEW STUFF MAYBE???
modelingSys['ewk']=0
modelingSys['top']=0
modelingSys['qcd']=0
modelingSys['totBkg']=0
modelingSys['data']=0
modelingSys['dataOverBkg']=0
