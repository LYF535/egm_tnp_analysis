#!/bin/bash

# $1 config: etc/config/settings_pho_run2022FG.py
# $2 id
# python tnpEGM_fitter.py $1 --flag $2 --checkBins
# python tnpEGM_fitter.py $1 --flag $2 --createBins
# python tnpEGM_fitter.py $1 --flag $2 --createHists
# python tnpEGM_fitter.py $1 --flag $2 --doFit
# python tnpEGM_fitter.py $1 --flag $2 --sumUp

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
baseDir="$script_dir"
# baseDir="/afs/cern.ch/work/p/pelai/learning/TnP/CMSSW_11_2_0/src/exercise/Short_exercise/Photon_ID_SF/egm_tnp_analysis"

# Custom Photon ID
# -------- High pT --------
sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_2022preEE hza_resolve_phid_2022preEE_sf
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_2022postEE hza_resolve_phid_2022postEE_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_2023preBPix hza_resolve_phid_2023preBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_2023postBPix hza_resolve_phid_2023postBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_2023postBPixHole hza_resolve_phid_2023postBPixHole_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_2024 hza_resolve_phid_2024_sf &

# -------- Low pT --------
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_lowpt_2022preEE hza_resolve_phid_lowpt_2022preEE_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_lowpt_2022postEE hza_resolve_phid_lowpt_2022postEE_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_lowpt_2023preBPix hza_resolve_phid_lowpt_2023preBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_lowpt_2023postBPix hza_resolve_phid_lowpt_2023postBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settings_resolve_phid_lowpt_2023postBPixHole hza_resolve_phid_lowpt_2023postBPixHole_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph.settingsResolve_phid_lowpt_2024 hzaResolve_phid_lowpt_2024_sf &


# Photon CSEV SFs
### -------- High R9 --------
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_hr9_2022preEE hza_resolve_phcsev_hr9_2022preEE_sf
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_hr9_2022postEE hza_resolve_phcsev_hr9_2022postEE_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_hr9_2023preBPix hza_resolve_phcsev_hr9_2023preBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_hr9_2023postBPix hza_resolve_phcsev_hr9_2023postBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_hr9_2023postBPixHole hza_resolve_phcsev_hr9_2023postBPixHole_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_hr9_2024 hza_resolve_phcsev_hr9_2024_sf &

# ### -------- Low R9 --------
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_lr9_2022preEE hza_resolve_phcsev_lr9_2022preEE_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_lr9_2022postEE hza_resolve_phcsev_lr9_2022postEE_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_lr9_2023preBPix hza_resolve_phcsev_lr9_2023preBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_lr9_2023postBPix hza_resolve_phcsev_lr9_2023postBPix_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_lr9_2023postBPixHole hza_resolve_phcsev_lr9_2023postBPixHole_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ph_csev.settings_resolve_phcsev_lr9_2024 hza_resolve_phcsev_lr9_2024_sf &
#------------------------------------------------------------------------------------------------------------

# Electron ID and Trigger SFs
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_elid_nongap_2024 hza_elid_nongap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_elid_gap_2024 hza_elid_gap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_dielleg12trigger_nongap_2024 htoza_dielleg12trigger_nongap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_dielleg12trigger_gap_2024 htoza_dielleg12trigger_gap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_dielleg23trigger_nongap_2024 htoza_dielleg23trigger_nongap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_dielleg23trigger_gap_2024 htoza_dielleg23trigger_gap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_sielleg30trigger_nongap_2024 htoza_sielleg30trigger_nongap_2024_sf &
# sh $baseDir/run.sh egm_tnp_analysis.etc.config.hza_ele.settings_htoza_sielleg30trigger_gap_2024 htoza_sielleg30trigger_gap_2024_sf &
# #------------------------------------------------------------------------------------------------------------

# BUILD_CPP=1 sh $baseDir/run.sh egm_tnp_analysis.etc.config.settings_resolve_pho_2022preEE hza_phid_2022preEE_sf