# -*- coding: utf-8 -*-
import os, sys
if '_mod_path' not in globals() or not _mod_path:
    _mod_path = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    if _mod_path not in sys.path:
        sys.path.insert(0, _mod_path)

#############################################################
########## General settings
#############################################################
# EA reference: https://indico.cern.ch/event/1204277/contributions/5064356/attachments/2538496/4369369/CutBasedPhotonID_20221031.pdf
# flag to be Tested

# BPix：-1.566 < ph_sc_eta < 0 且 -1.2 < ph_sc_phi < -0.8
_include_region = ' ((ph_sc_eta > -1.566 && ph_sc_eta < 0) && (ph_sc_phi > -1.2 && ph_sc_phi < -0.8)) '

flags = {
    # Run3 custom ID aligned to ZaTaggerRun3.select_photons
    'hza_resolve_phid_lowpt_2023postBPixHole_sf': (
        # pT + acceptance
        '(ph_et > 10) && ((abs(ph_sc_eta) < 1.4442) || (abs(ph_sc_eta) > 1.566 && abs(ph_sc_eta) < 2.5))'
        ' && ('
        # ================= EB block =================
        # ================= H/E =================
        '  (abs(ph_sc_eta) < 1.4442'
        '   && (('
        '         (abs(ph_sc_eta) > 0.0 && abs(ph_sc_eta) < 1.0)'
        '         && (ph_hoe - event_rho*0.00198598 - (event_rho*event_rho)*(-0.0000115014)'
        '             < 0.0417588)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 1.0 && abs(ph_sc_eta) < 1.4442)'
        '         && (ph_hoe - event_rho*0.208571 - (event_rho*event_rho)*(-0.0000115014)'
        '             < 0.0417588)'
        '       ))'
        # ================= Ch ISO =================
        '   && (('
        '         (abs(ph_sc_eta) > 0.0 && abs(ph_sc_eta) < 1.0)'
        '         && (ph_chIso - event_rho*0.0342898 - (event_rho*event_rho)*(-0.000103508)'
        '             < 0.316306)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 1.0 && abs(ph_sc_eta) < 1.4442)'
        '         && (ph_chIso - event_rho*0.0281424 - (event_rho*event_rho)*(-0.000031494)'
        '             < 0.316306)'
        '       ))'
        # ================= H ISO =================
        '   && (('
        '         (abs(ph_sc_eta) > 0.0 && abs(ph_sc_eta) < 1.0)'
        '         && (ph_neuIso - event_rho*0.17005 - (event_rho*event_rho)*(-0.000835)'
        '             < (0.39057 + 0.0100547*ph_et + 0.0000578332*ph_et*ph_et))'
        '       ) || ('
        '         (abs(ph_sc_eta) > 1.0 && abs(ph_sc_eta) < 1.4442)'
        '         && (ph_neuIso - event_rho*0.208571 - (event_rho*event_rho)*(-0.000905)'
        '             < (0.39057 + 0.0100547*ph_et + 0.0000578332*ph_et*ph_et))'
        '       ))'
        '  )'
        '  ||'
        # ================= EE block =================
        # ================= H/E =================
        '  (abs(ph_sc_eta) > 1.566 && abs(ph_sc_eta) < 2.5'
        '   && (('
        '         (abs(ph_sc_eta) > 1.566 && abs(ph_sc_eta) < 2.0)'
        '         && (ph_hoe - event_rho*0.00302416 - (event_rho*event_rho)*(-0.0000151973)'
        '             < 0.00254267)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.0 && abs(ph_sc_eta) < 2.2)'
        '         && (ph_hoe - event_rho*0.306529 - (event_rho*event_rho)*(-0.0000149651)'
        '             < 0.00254267)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.2 && abs(ph_sc_eta) < 2.3)'
        '         && (ph_hoe - event_rho*0.322673 - (event_rho*event_rho)*(-0.0000147232)'
        '             < 0.00254267)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.3 && abs(ph_sc_eta) < 2.4)'
        '         && (ph_hoe - event_rho*0.315793 - (event_rho*event_rho)*(-0.0000213958)'
        '             < 0.00254267)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.4 && abs(ph_sc_eta) < 2.5)'
        '         && (ph_hoe - event_rho*0.36531 - (event_rho*event_rho)*(-0.0000280795)'
        '             < 0.00254267)'
        '       ))'
        # ================= Ch ISO =================
        '   && (('
        '         (abs(ph_sc_eta) > 1.566 && abs(ph_sc_eta) < 2.0)'
        '         && (ph_chIso - event_rho*0.0288533 - (event_rho*event_rho)*(-0.0000666148)'
        '             < 0.292664)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.0 && abs(ph_sc_eta) < 2.2)'
        '         && (ph_chIso - event_rho*0.028789 - (event_rho*event_rho)*(-0.0000684993)'
        '             < 0.292664)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.2 && abs(ph_sc_eta) < 2.3)'
        '         && (ph_chIso - event_rho*0.0264064 - (event_rho*event_rho)*(-0.0000889189)'
        '             < 0.292664)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.3 && abs(ph_sc_eta) < 2.4)'
        '         && (ph_chIso - event_rho*0.025587 - (event_rho*event_rho)*(-0.0000590178)'
        '             < 0.292664)'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.4 && abs(ph_sc_eta) < 2.5)'
        '         && (ph_chIso - event_rho*0.0224817 - (event_rho*event_rho)*(-0.0000422712)'
        '             < 0.292664)'
        '       ))'
        # ================= H ISO =================
        '   && (('
        '         (abs(ph_sc_eta) > 1.566 && abs(ph_sc_eta) < 2.0)'
        '         && (ph_neuIso - event_rho*0.246494 - (event_rho*event_rho)*(-0.000722)'
        '             < (0.0292617 + 0.0116989*ph_et + 0.0000747603*ph_et*ph_et))'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.0 && abs(ph_sc_eta) < 2.2)'
        '         && (ph_neuIso - event_rho*0.306529 - (event_rho*event_rho)*(-0.000608)'
        '             < (0.0292617 + 0.0116989*ph_et + 0.0000747603*ph_et*ph_et))'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.2 && abs(ph_sc_eta) < 2.3)'
        '         && (ph_neuIso - event_rho*0.322673 - (event_rho*event_rho)*(-0.000750)'
        '             < (0.0292617 + 0.0116989*ph_et + 0.0000747603*ph_et*ph_et))'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.3 && abs(ph_sc_eta) < 2.4)'
        '         && (ph_neuIso - event_rho*0.315793 - (event_rho*event_rho)*(-0.000795)'
        '             < (0.0292617 + 0.0116989*ph_et + 0.0000747603*ph_et*ph_et))'
        '       ) || ('
        '         (abs(ph_sc_eta) > 2.4 && abs(ph_sc_eta) < 2.5)'
        '         && (ph_neuIso - event_rho*0.36531 - (event_rho*event_rho)*(-0.000439)'
        '             < (0.0292617 + 0.0116989*ph_et + 0.0000747603*ph_et*ph_et))'
        '       ))'
        '  )'
        ' )'
    ),
}

# baseOutDir = '/eos/home-p/pelai/HZa/root_TnP'
baseOutDir = '<Your base output directory>'  # set your output directory here

#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef as tnpSamples
tnpTreeDir = 'tnpPhoIDs'

samplesDef = {
        'data'  : tnpSamples.Run3_2023postBPix['Data_2023postBPix'].clone(),
        'mcNom' : tnpSamples.Run3_2023postBPix['DY_MC_LO_2023postBPix'].clone(),
        'tagSel': tnpSamples.Run3_2023postBPix['DY_MC_LO_2023postBPix'].clone(),
        'mcAlt': tnpSamples.Run3_2023postBPix['DY_MC_NLO_2023postBPix'].clone(),
    }


## can add data sample easily
# samplesDef['data'].add_sample(tnpSamples.Run3_124X_PromptReco2022G['data_Run2022G'].clone()) 
## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_MC_LO_2023postBPix')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 50 && abs(tag_sc_eta) < 2.17 && ph_mva122XV1 > 0.99 && ph_r9 > 0.99')

## set MC weight, simple way (use tree weight) 
# weightName = 'totWeight'
# if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
# if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
# if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking 
mcNom_puFile = '/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023/pileupReweightingFiles/postBPIX/DY_madgraph_pho.pu.puTree.root'
mcAlt_puFile = '/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023/pileupReweightingFiles/postBPIX/DY_amcatnloext_pho.pu.puTree.root'
weightName = 'weights_data_Run2023D.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree(mcNom_puFile)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree(mcAlt_puFile)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree(mcNom_puFile)

#############################################################
########## bining definition  [can be nD bining]
#############################################################
biningDef = [
   { 'var' : 'ph_sc_eta' , 'type': 'float', 'bins': [-1.566,-1.4442, 0.0] },
   { 'var' : 'ph_et' , 'type': 'float', 'bins': [10,20] }
]

#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17'

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
# additionalCuts = { 
#    0 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    1 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    2 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    3 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    4 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    5 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    6 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    7 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    8 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
#    9 : 'sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45',
# }

#### or remove any additional cut (default)
_nbins = (len(biningDef[0]['bins']) - 1) * (len(biningDef[1]['bins']) - 1)
additionalCuts = {ib: _include_region for ib in range(_nbins)}

#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2.0,0.5,5.0]",
    "acmsP[60.,45.,70.]","betaP[0.05,0.01,0.08]","gammaP[0.04, 0.02, 2]","peakP[87.0,82.0,90.0]",
    "acmsF[60.,35.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.04, 0.02, 2]","peakF[87.0,82.0,90.0]",
    ]

# # 3
# tnpParNomFit = [
#     "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
#     "meanF[-0.0,-5.0,5.0]","sigmaF[2.0,0.5,5.0]",
#     "acmsP[60.,45.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0.047, 2]","peakP[87.0,82.0,90.0]",
#     "acmsF[60.,35.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0.02, 2]","peakF[87.0,82.0,90.0]",
#     ]

# # 7
# tnpParNomFit = [
#     "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
#     "meanF[-0.0,-5.0,5.0]","sigmaF[2.0,0.5,5.0]",
#     "acmsP[60.,45.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, 0.02, 2]","peakP[87.0,82.0,90.0]",
#     "acmsF[60.,45.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, 0.02, 2]","peakF[87.0,82.0,90.0]",
#     ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]",
    "sigmaP[4.0, 3.0, 8.0]",
    "sigmaP_2[0.5, 0.5, 6.0]",
    "alphaP[2.0,1.2,3.5]" ,
    "nP[3,-5,5]",
    "sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]",
    "sigmaF[4.5, 3.0, 8.0]",
    "sigmaF_2[0.5, 0.5, 6.0]",
    "alphaF[2.0,1.2,3.5]",
    "nF[3,0,5]",
    "sosF[1,0.5,5.0]",
    "acmsP[40.,35.,48.]","betaP[0.04,0.005,0.06]","gammaP[0.04, 0.02, 1]","peakP[89.0,82.0,90.0]",
    "acmsF[50.,40.,70.]","betaF[0.04,0.01,0.06]","gammaF[0.04, 0.02, 1]","peakF[89.0,82.0,90.0]",
    ]

## 01
# tnpParAltSigFit = [
#     "meanP[-0.0,-5.0,5.0]",
#     "sigmaP[4.0, 3.0, 8.0]",
#     "sigmaP_2[0.5, 0.5, 6.0]",
#     "alphaP[2.0,1.2,3.5]" ,
#     "nP[3,-5,5]",
#     "sosP[1,0.5,5.0]",
#     "meanF[-0.0,-5.0,5.0]",
#     "sigmaF[4.5, 3.0, 8.0]",
#     "sigmaF_2[0.6, 0.6, 6.0]",
#     "alphaF[2.0,1.2,3.5]",
#     "nF[3,0,5]",
#     "sosF[1,0.5,5.0]",
#     "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[89.0,82.0,90.0]",
#     "acmsF[60.,40.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.04, 1]","peakF[89.0,82.0,90.0]",
#     ]

tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]

tnpParAltSigBkgFit = [
  'meanP[-0.0, -5.0, 5.0]',
  'sigmaP[0.5, 0.1, 2.0]',
  'sigmaP_2[0.5, 0.1, 2.0]',
  'sosP[0.10, 0.0, 1.0]',
  'meanF[-1.0, -5.0, 4.3]',
  'sigmaF[0.5, 0.1, 2.0]',
  'sigmaF_2[0.5, 0.1, 3.0]',
  'sosF[0.12, 0.0, 1.0]',
  'alphaP[2.0, 1.4, 3.5]', 'nP[0.4, 0.0, 1.5]',
  'alphaP_2[-0.012, -1, 0]',
  'alphaF[2.0, 1.4, 3.5]', 'nF[0.4, 0.0, 1.5]',
  'alphaF_2[-0.04, -1, -0.029]',
]

# # 01
# tnpParAltSigBkgFit = [
#   'meanP[-0.0, -5.0, 5.0]',
#   'sigmaP[0.5, 0.1, 2.0]',
#   'sigmaP_2[0.5, 0.1, 2.0]',
#   'sosP[0.10, 0.0, 1.0]',
#   'meanF[-0.0, -5.0, 5.0]',
#   'sigmaF[0.5, 0.1, 2.0]',
#   'sigmaF_2[0.5, 0.1, 3.0]',
#   'sosF[0.12, 0.0, 1.0]',
#   'alphaP[2.0, 1.4, 3.5]', 'nP[0.4, 0.0, 1.5]',
#   'alphaP_2[-0.012, -1, 0]',
#   'alphaF[2.0, 1.4, 3.5]', 'nF[0.4, 0.0, 1.5]',
#   'alphaF_2[-0.023, -1, -0.023]',
# ]