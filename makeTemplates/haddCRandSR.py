import os,sys

masslist = [1100,1200,1300,1400,1500,1600,1700,1800]
brlist = [
#'bW0p0_tZ0p0_tH1p0_',
#'bW0p0_tZ0p2_tH0p8_',
#'bW0p0_tZ0p4_tH0p6_',
#'bW0p0_tZ0p5_tH0p5_',
#'bW0p0_tZ0p6_tH0p4_',
#'bW0p0_tZ0p8_tH0p2_',
#'bW0p0_tZ1p0_tH0p0_',
#'bW0p2_tZ0p0_tH0p8_',
#'bW0p2_tZ0p2_tH0p6_',
#'bW0p2_tZ0p4_tH0p4_',
#'bW0p2_tZ0p6_tH0p2_',
#'bW0p2_tZ0p8_tH0p0_',
#'bW0p4_tZ0p0_tH0p6_',
#'bW0p4_tZ0p2_tH0p4_',
#'bW0p4_tZ0p4_tH0p2_',
#'bW0p4_tZ0p6_tH0p0_',
'bW0p5_tZ0p25_tH0p25_',
#'bW0p6_tZ0p0_tH0p4_',
#'bW0p6_tZ0p2_tH0p2_',
#'bW0p6_tZ0p4_tH0p0_',
#'bW0p8_tZ0p0_tH0p2_',
#'bW0p8_tZ0p2_tH0p0_',
#'bW1p0_tZ0p0_tH0p0_',
]

pre = 'templates_DnnTprime_TTM'
pre3 = 'templates_HTNtag_TTM'
post = '59p69fb_BKGNORM_rebinned_stat0p3.root'

for mass in masslist:
    for br in brlist:
        brBB = br.replace('bW','tW').replace('tZ','bZ').replace('tH','bH')
        #os.system('hadd -f templatesCRhtSR_MVAfixBB/'+pre.replace('TTM','BBM')+str(mass)+'_'+brBB+post+' templatesCR_NtagMVABB/'+pre3.replace('TTM','BBM')+str(mass)+'_'+brBB+post+' templatesSR_MVAfixBB/'+pre.replace('TTM','BBM')+str(mass)+'_'+brBB+post)
        os.system('hadd -f templatesCRhtntag4SR_MVAfixTT/'+pre+str(mass)+'_'+br+post+' templatesCR_HTNtag4TT/'+pre3+str(mass)+'_'+br+post+' templatesSR_HTNtag4TT/'+pre+str(mass)+'_'+br+post)
        
