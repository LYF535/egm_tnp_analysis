from libPython.tnpClassUtils import tnpSample

#github branches
#LegacyReReco2016: https://github.com/swagata87/egm_tnp_analysis/tree/Legacy2016_94XIDv2 
#ReReco2017: https://github.com/swagata87/egm_tnp_analysis/tree/tnp_2017datamc_IDV2_10_2_0
#PromptReco2018: https://github.com/swagata87/egm_tnp_analysis/tree/egm_tnp_Prompt2018_102X_10222018_MC102XECALnoiseFix200kRelVal
#UL2017: https://github.com/swagata87/egm_tnp_analysis/blob/UL2017Final/etc/inputs/tnpSampleDef.py

### eos repositories
eosLegacyReReco2016 = '/eos/cms/store/group/phys_egamma/swmukher/egmNtuple_V2ID_2016/'
eosReReco2017 = '/eos/cms/store/group/phys_egamma/swmukher/ntuple_2017_v2/'
eosReReco2018 = '/eos/cms/store/group/phys_egamma/swmukher/rereco2018/ECAL_NOISE/'

# UL Summer19
eosUL2016preVFP  = '/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016preVFP/merged/'
eosUL2016postVFP = '/eos/cms/store/group/phys_egamma/tnpTuples/rasharma/2021-02-10/UL2016postVFP/merged/'
eosUL2017 = '/eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2017/merged/'
eosUL2018 = '/eos/cms/store/group/phys_egamma/tnpTuples/tomc/2020-05-20/UL2018/merged/'

#Run3
eosRun3 = '/eos/cms/store/group/phys_egamma/ec/fmausolf/EGM_comm/'

eos_Run3_124X = '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-04-25/2022/'
eos_Run3_PromptReco = '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-04-25/2022/'
eos_Reco_Run3_PromptReco = '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-05-01/2022/data/'
eos_Reco_Run3_124X = '/eos/cms/store/group/phys_egamma/tnpTuples/bjoshi/2023-02-09/2022/mc/'

#---------------- Custom Photon ID selection efficiency measrement samples ----------------
eos2022 = '/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/TnP_samples/2022'
Run3_2022preEE = {
        'DY_MC_NLO_2022preEE'   : tnpSample('DY_MC_NLO_2022preEE', eos2022 + '/sim/DY_NLO/merged_Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2.root', isMC=True, nEvts = 7286732),
        'DY_MC_LO_2022preEE'    : tnpSample('DY_MC_LO_2022preEE', eos2022 + '/sim/DY_LO/merged_DYJetsToLL_M_50_Run3Summer22MiniAODv4-forPOG_130X_mcRun3_2022_realistic_v5-v2.root', isMC=True, nEvts = 3595138),
        'Data_2022preEE'        : tnpSample('Data_2022preEE', eos2022 + '/data/merged_Run2022_BCD_ReReco_updated.root', lumi = 7.98),
        }
Run3_2022postEE = {
        'DY_MC_NLO_2022postEE'  : tnpSample('DY_MC_NLO_2022postEE', eos2022 + '/sim/DY_NLO/merged_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2.root', isMC=True, nEvts = 27397320),
        'DY_MC_LO_2022postEE'   : tnpSample('DY_MC_LO_2022postEE', eos2022 + '/sim/DY_LO/merged_DYJetsToLL_M_50_Run3Summer22EEMiniAODv4-forPOG_130X_mcRun3_2022_realistic_postEE_v6-v2.root', isMC=True, nEvts = 12144692),
        'Data_2022postEE'       : tnpSample('Data_2022postEE', eos2022 + '/data/merged_Run2022_EReReco_FG_PromptReco_updated.root', lumi = 26.67),
        }

eos2023 = '/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023'
Run3_2023preBPix = {
        'DY_MC_NLO_2023preBPix' : tnpSample('DY_MC_NLO_2023preBPix', eos2023 + '/DY_NLO_2023preBPIX.root', isMC=True, nEvts = 21841873),
        'DY_MC_LO_2023preBPix'  : tnpSample('DY_MC_LO_2023preBPix', eos2023 + '/DY_LO_2023preBPIX.root', isMC=True, nEvts = 18539920),
        'Data_2023preBPix'      : tnpSample('Data_2023preBPix', eos2023 + '/data_2023C.root', lumi = 17.79),
        }
Run3_2023postBPix = {
        'DY_MC_NLO_2023postBPix': tnpSample('DY_MC_NLO_2023postBPix', eos2023 + '/photonIDpostBPIXntuples/DY_NLO_2023postBPIX.root', isMC=True, nEvts = 13142450),
        'DY_MC_LO_2023postBPix' : tnpSample('DY_MC_LO_2023postBPix', eos2023 + '/photonIDpostBPIXntuples/DY_LO_2023postBPIX.root', isMC=True, nEvts = 9750346),
        'Data_2023postBPix'     : tnpSample('Data_2023postBPix', eos2023 + '/photonIDpostBPIXntuples/data_2023D.root', lumi = 9.45),
        }


eos2024 = '/eos/cms/store/group/phys_egamma/ScaleFactors/Data2024/PhoID/tnp_ntuples/merged_era'
Run3_2024 = {
        'DY_MC_NLO_2024' : tnpSample('DY_MC_NLO_2024', eos2024 + '/TnPTree_mc_amcatnlo.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2024'  : tnpSample('DY_MC_LO_2024', eos2024 + '/TnPTree_mc_madgraph.root', isMC=True, nEvts = 202883601),
        'Data_2024C'     : tnpSample('Data_2024C', eos2024 + '/TnPTree_data_C.root', lumi = 7.24),
        'Data_2024D'     : tnpSample('Data_2024D', eos2024 + '/TnPTree_data_D.root', lumi = 7.96),
        'Data_2024E'     : tnpSample('Data_2024E', eos2024 + '/TnPTree_data_E.root', lumi = 11.32),
        'Data_2024F'     : tnpSample('Data_2024F', eos2024 + '/TnPTree_data_F.root', lumi = 27.76),
        'Data_2024G'     : tnpSample('Data_2024G', eos2024 + '/TnPTree_data_G.root', lumi = 37.77),
        'Data_2024H'     : tnpSample('Data_2024H', eos2024 + '/TnPTree_data_H.root', lumi = 5.44),
        'Data_2024I'     : tnpSample('Data_2024I', eos2024 + '/TnPTree_data_I.root', lumi = 11.47),
        }

#---------------- electron offline selection, single-/double-trigger efficiency measrement samples ----------------
eos2024ele = '/eos/project/h/htozg-dy-privatemc/pelai/root_make_TnP_ntuple'
Run3_2024_ele = {
        'DY_MC_NLO_2024' : tnpSample('DY_MC_NLO_2024', eos2024ele + '/mc/DY_NLO_2024/DY_NLO_2024.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2024'  : tnpSample('DY_MC_LO_2024',  eos2024ele + '/mc/DY_LO_2024/DY_LO_2024.root', isMC=True, nEvts = 202883601),
        'Data_2024'      : tnpSample('Data_2024',      eos2024ele + '/data/Data_2024.root', lumi = 108.95),
        }

#---------------- photon CSEV efficiency measrement samples ----------------
eoszmmg = '/eos/home-p/pelai/HZa/root_P2Root/run3_tnp_zmmg'
Run3_2022preEE_zmmg = {
        'DY_MC_NLO_2022preEE'    : tnpSample('DY_MC_NLO_2022preEE',    eoszmmg + '/mc/DYJetsToLL/2022preEE.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2022preEE'     : tnpSample('DY_MC_LO_2022preEE',     eoszmmg + '/mc/DYJetsToLL_MLM/2022preEE.root', isMC=True, nEvts = 202883601),
        'Data_2022preEE'         : tnpSample('Data_2022preEE',         eoszmmg + '/Data_tnp_zmmg/2022preEE.root', lumi = 108.95),
        }
Run3_2022postEE_zmmg = {
        'DY_MC_NLO_2022postEE'   : tnpSample('DY_MC_NLO_2022postEE',   eoszmmg + '/mc/DYJetsToLL/2022postEE.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2022postEE'    : tnpSample('DY_MC_LO_2022postEE',    eoszmmg + '/mc/DYJetsToLL_MLM/2022postEE.root', isMC=True, nEvts = 202883601),
        'Data_2022postEE'        : tnpSample('Data_2022postEE',        eoszmmg + '/Data_tnp_zmmg/2022postEE.root', lumi = 108.95),
        }
Run3_2023preBPix_zmmg = {
        'DY_MC_NLO_2023preBPix'  : tnpSample('DY_MC_NLO_2023preBPix',  eoszmmg + '/mc/DYJetsToLL/2023preBPix.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2023preBPix'   : tnpSample('DY_MC_LO_2023preBPix',   eoszmmg + '/mc/DYJetsToLL_MLM/2023preBPix.root', isMC=True, nEvts = 202883601),
        'Data_2023preBPix'       : tnpSample('Data_2023preBPix',       eoszmmg + '/Data_tnp_zmmg/2023preBPix.root', lumi = 108.95),
        }
Run3_2023postBPix_zmmg = {
        'DY_MC_NLO_2023postBPix' : tnpSample('DY_MC_NLO_2023postBPix', eoszmmg + '/mc/DYJetsToLL/2023postBPix.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2023postBPix'  : tnpSample('DY_MC_LO_2023postBPix',  eoszmmg + '/mc/DYJetsToLL_MLM/2023postBPix.root', isMC=True, nEvts = 202883601),
        'Data_2023postBPix'      : tnpSample('Data_2023postBPix',      eoszmmg + '/Data_tnp_zmmg/2023postBPix.root', lumi = 108.95),
        }
Run3_2024_zmmg = {
        'DY_MC_NLO_2024'         : tnpSample('DY_MC_NLO_2024',         eoszmmg + '/mc/DYJetsTo2Mu/2024.root', isMC=True, nEvts = 203271136),
        'DY_MC_LO_2024'          : tnpSample('DY_MC_LO_2024',          eoszmmg + '/mc/DYJetsToLL_MLM/2024.root', isMC=True, nEvts = 202883601),
        'Data_2024'              : tnpSample('Data_2024',              eoszmmg + '/Data_tnp_zmmg/2024.root', lumi = 108.95),
        }
#--------------------------------------------------------------------------------

ReReco2017 = {

    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosReReco2017 + 'DYJetsToLL.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_1j_madgraph'              : tnpSample('DY_1j_madgraph',
                                       eosReReco2017 + 'DY1JetsToLLM50madgraphMLM.root',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       eosMoriond18 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
                                       eosReReco2017 + 'DYJetsToLLM50amcatnloFXFXext.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2017B' : tnpSample('data_Run2017B' , eosReReco2017 + 'RunB.root' , lumi = 4.793 ),
    'data_Run2017C' : tnpSample('data_Run2017C' , eosReReco2017 + 'RunC.root' , lumi = 9.753),
    'data_Run2017D' : tnpSample('data_Run2017D' , eosReReco2017 + 'RunD.root' , lumi = 4.320 ),
    'data_Run2017E' : tnpSample('data_Run2017E' , eosReReco2017 + 'RunE.root' , lumi = 8.802),
    'data_Run2017F' : tnpSample('data_Run2017F' , eosReReco2017 + 'RunF.root' , lumi = 13.567),
}

LegacyReReco2016 = {

    'DY_madgraph' : tnpSample('DY_madgraph', 
                                        eosLegacyReReco2016 + 'TnPTree_DY_M50_madgraphMLM.root',
                                        isMC = True, nEvts =  -1 ),
    'DY_amcatnlo' : tnpSample('DY_amcatnlo', 
                                        eosLegacyReReco2016 + 'TnPTree_DY_M50_amcatnloFXFX.root',
                                        isMC = True, nEvts =  -1 ),

    'data_Run2016Bv2' : tnpSample('data_Run2017Bv2' , eosLegacyReReco2016 + 'TnPTree_2016B_2.root' , lumi = 5.785 ),
    'data_Run2016C' : tnpSample('data_Run2017C' , eosLegacyReReco2016 + 'TnPTree_2016C.root' , lumi = 2.573 ),
    'data_Run2016D' : tnpSample('data_Run2017D' , eosLegacyReReco2016 + 'TnPTree_2016D.root' , lumi = 4.248 ),
    'data_Run2016E' : tnpSample('data_Run2017E' , eosLegacyReReco2016 + 'TnPTree_2016E.root' , lumi = 3.947 ),
    'data_Run2016F' : tnpSample('data_Run2017F' , eosLegacyReReco2016 + 'TnPTree_2016F.root' , lumi = 3.102 ),
    'data_Run2016G' : tnpSample('data_Run2017G' , eosLegacyReReco2016 + 'TnPTree_2016G.root' , lumi = 7.540 ),
    'data_Run2016H' : tnpSample('data_Run2017H' , eosLegacyReReco2016 + 'TnPTree_2016H.root' , lumi = 7.813 ),
}


ReReco2018 = {
    ### MiniAOD TnP for IDs scale 

    'DY_madgraph'              : tnpSample('DY_madgraph',
                                            eosReReco2018 + 'DYJetsToLLmadgraphMLM.root',
                                            isMC = True, nEvts =  -1 ),

    'DY_powheg'              : tnpSample('DY_powheg',
                                            eosReReco2018 + 'DYToEEpowheg.root',
                                            isMC = True, nEvts =  -1 ),
    

    'data_Run2018A' : tnpSample('data_Run2018A' , eosReReco2018 + 'RunA.root' , lumi = 10.723),  
    'data_Run2018B' : tnpSample('data_Run2018B' , eosReReco2018 + 'RunB.root' , lumi = 5.964),
    'data_Run2018C' : tnpSample('data_Run2018C' , eosReReco2018 + 'RunC.root' , lumi = 6.382),
    'data_Run2018D' : tnpSample('data_Run2018D' , eosReReco2018 + 'RunD.root' , lumi = 29.181), 
}

UL2016_preVFP = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2016preVFP + 'DY_LO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2016preVFP + 'DY_NLO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2016B' : tnpSample('data_Run2016B' , eosUL2016preVFP + 'Run2016B_L1matched.root' , lumi = 5.9098246),
    'data_Run2016C' : tnpSample('data_Run2016C' , eosUL2016preVFP + 'Run2016C_L1matched.root' , lumi = 2.64992914),
    'data_Run2016D' : tnpSample('data_Run2016D' , eosUL2016preVFP + 'Run2016D_L1matched.root' , lumi = 4.292865604),
    'data_Run2016E' : tnpSample('data_Run2016E' , eosUL2016preVFP + 'Run2016E_L1matched.root' , lumi = 4.185165152),
    'data_Run2016F' : tnpSample('data_Run2016F' , eosUL2016preVFP + 'Run2016F_L1matched.root' , lumi = 2.725508364)
}

UL2016_postVFP = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2016postVFP + 'DY_LO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2016postVFP + 'DY_NLO_L1matched.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2016F' : tnpSample('data_Run2016F' , eosUL2016postVFP + 'Run2016F_L1merged.root' , lumi = 0.414987426),
    'data_Run2016G' : tnpSample('data_Run2016G' , eosUL2016postVFP + 'Run2016G_L1matched.root' , lumi = 7.634508755),
    'data_Run2016H' : tnpSample('data_Run2016H' , eosUL2016postVFP + 'Run2016H_L1matched.root' , lumi = 8.802242522)
    }

UL2017 = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2017 + 'DY_LO.root ',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2017 + 'DY_NLO.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2017B' : tnpSample('data_Run2017B' , eosUL2017 + 'Run2017B.root' , lumi = 4.793961427),
    'data_Run2017C' : tnpSample('data_Run2017C' , eosUL2017 + 'Run2017C.root' , lumi = 9.631214821),
    'data_Run2017D' : tnpSample('data_Run2017D' , eosUL2017 + 'Run2017D.root' , lumi = 4.247682053),
    'data_Run2017E' : tnpSample('data_Run2017E' , eosUL2017 + 'Run2017E.root' , lumi = 9.313642402),
    'data_Run2017F' : tnpSample('data_Run2017F' , eosUL2017 + 'Run2017F.root' , lumi = 13.510934811),
}

UL2018 = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosUL2018 + 'DY_LO.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnloext'           : tnpSample('DY_amcatnloext',
                                       eosUL2018 + 'DY_NLO.root',
                                       isMC = True, nEvts =  -1 ),


    'data_Run2018A' : tnpSample('data_Run2018A' , eosUL2018 + 'Run2018A.root' , lumi = 14.02672485),
    'data_Run2018B' : tnpSample('data_Run2018B' , eosUL2018 + 'Run2018B.root' , lumi = 7.060617355),
    'data_Run2018C' : tnpSample('data_Run2018C' , eosUL2018 + 'Run2018C.root' , lumi = 6.894770971),
    'data_Run2018D' : tnpSample('data_Run2018D' , eosUL2018 + 'Run2018D.root' , lumi = 31.74220577),
}

Run3 = {
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                       eosRun3 + 'DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8_EleID_PhoID/DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8/DYToEE_M-50_NNPDF31_TuneCP5_13p6TeV-powheg-pythia8_EleID_PhoID/221018_080249/0000/merged.root',
                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
#                                       eosUL2017 + 'DYJetsToLLM50amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),
#    'DY_amcatnloext'                 : tnpSample('DY_amcatnloext',
#                                       eosUL2017 + 'DYJetsToLL_amcatnloFXFX.root',
#                                       isMC = True, nEvts =  -1 ),


    'data_Run3B' : tnpSample('data_Run3B' , eosRun3 + 'ntuple_Run3_data_2022B_EleID_PhoID/data/EGamma/crab_Egamma2022B_EleID_PhoID/221012_155735/0000/merged.root' , lumi = 0.086),
    'data_Run3C' : tnpSample('data_Run3C' , eosRun3 + 'ntuple_Run3_data_2022C_EleID_PhoID/data/EGamma/crab_Egamma2022C_EleID_PhoID/221014_145533/0000/merged.root' , lumi = 4.45),
    'data_Run3D' : tnpSample('data_Run3D' , eosRun3 + 'ntuple_Run3_data_2022D_EleID_PhoID/data/EGamma/crab_Egamma2022D_EleID_PhoID/221014_145636/0000/merged.root' , lumi = 0.912),
    'data_Run3E' : tnpSample('data_Run3E' , eosRun3 + 'ntuple_Run3_data_2022E_EleID_PhoID/data/EGamma/crab_Egamma2022E_EleID_PhoID/221018_073725/0000/merged.root' , lumi = 2.08),
    'data_Run3F' : tnpSample('data_Run3F' , eosRun3 + 'ntuple_Run3_data_2022F_EleID_PhoID/data/EGamma/crab_Egamma2022F_EleID_PhoID/221114_171125/0000/merged.root' , lumi = 4.99),
    'data_Run3G' : tnpSample('data_Run3G' , eosRun3 + 'ntuple_Run3_data_2022G_EleID_PhoID/data/EGamma/crab_Egamma2022G_EleID_PhoID/221211_201213/0000/merged.root' , lumi = 2.43),
}



Run3_124X_PromptReco2022F = {
        'DY_1j_madgraph_postEE'    : tnpSample('DY_1j_madgraph_postEE', eos_Run3_124X + '/mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_2022_DY_LO_postEE.root', isMC=True, nEvts = 96505000),
        'data_Run2022F': tnpSample('data_Run2022F', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022F.root', lumi = 18.0064)}

Run3_124X_PromptReco2022G = {
        'DY_1j_madgraph_postEE'    : tnpSample('DY_1j_madgraph_postEE', eos_Run3_124X + '/mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_2022_DY_LO_postEE.root', isMC=True, nEvts = 96505000),
        'data_Run2022G': tnpSample('data_Run2022G', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022G.root', lumi = 3.1219)}

Run3_124X_PromptReco_preEE = {
        'DY_1j_madgraph'    : tnpSample('DY_1j_madgraph', eos_Run3_PromptReco + '/mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_2022_DY_LO.root', isMC=True, nEvts = 27310302),
        'data_Run2022B': tnpSample('data_Run2022B', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022B.root', lumi = 0.0975),
        'data_Run2022C': tnpSample('data_Run2022C', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022C.root', lumi = 5.0702),
        'data_Run2022D': tnpSample('data_Run2022D', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022D.root', lumi = 1.8260),
        }

Run3_124X_PromptReco_postEE = {
        'DY_1j_madgraph_postEE'    : tnpSample('DY_1j_madgraph_postEE', eos_Run3_124X + '/mc/TnPTree_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_2022_DY_LO_postEE.root', isMC=True, nEvts = 96505000),
        'data_Run2022E': tnpSample('data_Run2022E', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022E.root', lumi = 5.8784),
        'data_Run2022F': tnpSample('data_Run2022F', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022F.root', lumi = 18.0064),
        'data_Run2022G': tnpSample('data_Run2022G', eos_Run3_PromptReco + '/data/TnPTree_EGamma_2022_Run2022G.root', lumi = 3.1219)
        }

Run3_Reco_124X_PromptReco_postEE = {
        'DY_1j_madgraph_postEE'    : tnpSample('DY_1j_madgraph_postEE', eos_Reco_Run3_124X + 'TnPTree_DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8_2022_DY_LO_postEE.root', isMC=True, nEvts = 96505000),
        'data_Run2022E': tnpSample('data_Run2022E', eos_Reco_Run3_PromptReco + '/TnPTree_EGamma_2022_Run2022E.root', lumi = 5.8784),
        'data_Run2022F': tnpSample('data_Run2022F', eos_Reco_Run3_PromptReco + '/TnPTree_EGamma_2022_Run2022F.root', lumi = 18.0064),
        'data_Run2022G': tnpSample('data_Run2022G', eos_Reco_Run3_PromptReco + '/TnPTree_EGamma_2022_Run2022G.root', lumi = 3.1219)
        }
