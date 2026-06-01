#!/usr/bin/env bash
# FORCE_REGEN_HOME=1 to update the homepage but the rest of link need to be updated
# FORCE_REGEN_SUB=1 to update the homepage but the rest of link need to be updated
# FORCE_REGEN_FIT=1 to update the homepage but the rest of link need to be updated

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ./publish.sh [electron|muon]

Modes:
  electron   Keep existing photon/electron publishing behavior (default).
  muon       Publish muon Run2024 pages using the same publish_subpage.sh code path.

Muon mode environment overrides:
  MUON_TNP_ROOT      default: /eos/home-p/pelai/HZa/root_mTnP
  MUON_WEB_ROOT      default: /eos/user/p/pelai/www/HZa/sfs_muon
  MUON_HOME_URL      default: /HZa/sfs_muon/
  MUON_DEST_PREFIX   default: run2024
  MUON_FITS_ROOT     default: /eos/home-p/pelai/HZa/root_mTnP/fits_data/muon/generalTracks/Z/Run2024
  MUON_SUMMARY_ROOT  default: /eos/home-p/pelai/HZa/root_mTnP/plots/muon/generalTracks/Z/Run2024
EOF
}

publish_electron() {
  # Electron Trigger SFs
  # Double Trigger Lower Leg 12
  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_dielleg12trigger_gap_2024/htoza_dielleg12trigger_gap_2024_sf \
    --hometitle "Custom Electron Double Lower Leg Trigger12 Gap 2024" \
    --title "Efficiency / Scale Factor Measurements — htoza_dielleg12trigger_gap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg12trigger_gap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg12trigger_gap_2024_sf \
    --section-url "#Resolve_Electron_Double_Lower_Trigger12_gap_2024"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_dielleg12trigger_nongap_2024/htoza_dielleg12trigger_nongap_2024_sf \
    --hometitle "Custom Electron Double Lower Leg Trigger12 Nongap 2024" \
    --title "Efficiency / Scale Factor Measurements — htoza_dielleg12trigger_nongap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg12trigger_nongap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg12trigger_nongap_2024_sf \
    --section-url "#Resolve_Electron_Double_Lower_Trigger12_nongap_2024"

  # Double Trigger Upper Leg 23
  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_dielleg23trigger_gap_2024/htoza_dielleg23trigger_gap_2024_sf \
    --hometitle "Custom Electron Double Upper Leg Trigger23 Gap 2024" \
    --title "Efficiency / Scale Factor Measurements — htoza_dielleg23trigger_gap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg23trigger_gap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg23trigger_gap_2024_sf \
    --section-url "#Resolve_Electron_Double_Upper_Trigger23_gap_2024"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_dielleg23trigger_nongap_2024/htoza_dielleg23trigger_nongap_2024_sf \
    --hometitle "Custom Electron Double Upper Leg Trigger23 Nongap 2024" \
    --title "Efficiency / Scale Factor Measurements — htoza_dielleg23trigger_nongap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg23trigger_nongap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/htoza_dielleg23trigger_nongap_2024_sf \
    --section-url "#Resolve_Electron_Double_Upper_Trigger23_nongap_2024"

  # Single Trigger 30
  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_sielleg30trigger_gap_2024/htoza_sielleg30trigger_gap_2024_sf \
    --hometitle "Custom Electron Single Trigger30 Gap 2024" \
    --title "Efficiency / Scale Factor Measurements — htoza_sielleg30trigger_gap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/htoza_sielleg30trigger_gap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/htoza_sielleg30trigger_gap_2024_sf \
    --section-url "#Resolve_Electron_Single_Trigger30_gap_2024"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_sielleg30trigger_nongap_2024/htoza_sielleg30trigger_nongap_2024_sf \
    --hometitle "Custom Electron Single Trigger30 Nongap 2024" \
    --title "Efficiency / Scale Factor Measurements — htoza_sielleg30trigger_nongap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/htoza_sielleg30trigger_nongap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/htoza_sielleg30trigger_nongap_2024_sf \
    --section-url "#Resolve_Electron_Single_Trigger30_nongap_2024"

  # Electron ID
  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_elid_gap_2024/hza_elid_gap_2024_sf \
    --hometitle "Custom Electron ID Gap 2024" \
    --title "Efficiency / Scale Factor Measurements — hza_elid_gap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_elid_nongap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_elid_gap_2024_sf \
    --section-url "#Resolve_Electron_ID_gap_2024"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_elid_nongap_2024/hza_elid_nongap_2024_sf \
    --hometitle "Custom Electron ID Nongap 2024" \
    --title "Efficiency / Scale Factor Measurements — hza_elid_nongap_2024_sf" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_elid_nongap_2024_sf/plots/Data_2024 \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_elid_nongap_2024_sf \
    --section-url "#Resolve_Electron_ID_nongap_2024"

  # Low pT
  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_lowpt_2023postBPix/hza_resolve_phid_lowpt_2024 \
    --hometitle "Resolve Custom Photon ID Low pT 2024"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_lowpt_2024" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2024_sf/plots/Data_2024C \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2024_sf \
    --section-url "#Resolve_Custom_Photon_ID_lowpt_2024"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_lowpt_2023postBPixHole/hza_resolve_phid_lowpt_2023postBPixHole \
    --hometitle "Resolve Custom Photon ID Low pT 2023postBPixHole"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_lowpt_2023postBPixHole" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2023postBPixHole_sf/plots/Data_2023postBPix \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2023postBPixHole_sf \
    --section-url "#Resolve_Custom_Photon_ID_lowpt_2023postBPixHole"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_lowpt_2023postBPix/hza_resolve_phid_lowpt_2023postBPix \
    --hometitle "Resolve Custom Photon ID Low pT 2023postBPix"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_lowpt_2023postBPix" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2023postBPix_sf/plots/Data_2023postBPix \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2023postBPix_sf \
    --section-url "#Resolve_Custom_Photon_ID_lowpt_2023postBPix"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_lowpt_2023preBPix/hza_resolve_phid_lowpt_2023preBPix \
    --hometitle "Resolve Custom Photon ID Low pT 2023preBPix"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_lowpt_2023preBPix" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2023preBPix_sf/plots/Data_2023preBPix \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2023preBPix_sf \
    --section-url "#Resolve_Custom_Photon_ID_lowpt_2023preBPix"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_lowpt_2022postEE/hza_resolve_phid_lowpt_2022postEE \
    --hometitle "Resolve Custom Photon ID Low pT 2022postEE"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_lowpt_2022postEE" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2022postEE_sf/plots/Data_2022postEE \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2022postEE_sf \
    --section-url "#Resolve_Custom_Photon_ID_lowpt_2022postEE"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_lowpt_2022preEE/hza_resolve_phid_lowpt_2022preEE \
    --hometitle "Resolve Custom Photon ID Low pT 2022preEE"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_lowpt_2022preEE" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2022preEE_sf/plots/Data_2022preEE \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_lowpt_2022preEE_sf \
    --section-url "#Resolve_Custom_Photon_ID_lowpt_2022preEE"

  # High pT
  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_2023postBPix/hza_resolve_phid_2024 \
    --hometitle "Resolve Custom Photon ID 2024"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_2024" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2024_sf/plots/Data_2024C \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2024_sf \
    --section-url "#Resolve_Custom_Photon_ID_2024"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_2023postBPixHole/hza_resolve_phid_2023postBPixHole \
    --hometitle "Resolve Custom Photon ID 2023postBPixHole"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_2023postBPixHole" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2023postBPixHole_sf/plots/Data_2023postBPix \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2023postBPixHole_sf \
    --section-url "#Resolve_Custom_Photon_ID_2023postBPixHole"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_2023postBPix/hza_resolve_phid_2023postBPix \
    --hometitle "Resolve Custom Photon ID 2023postBPix"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_2023postBPix" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2023postBPix_sf/plots/Data_2023postBPix \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2023postBPix_sf \
    --section-url "#Resolve_Custom_Photon_ID_2023postBPix"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_2023preBPix/hza_resolve_phid_2023preBPix \
    --hometitle "Resolve Custom Photon ID 2023preBPix"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_2023preBPix" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2023preBPix_sf/plots/Data_2023preBPix \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2023preBPix_sf \
    --section-url "#Resolve_Custom_Photon_ID_2023preBPix"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_2022postEE/hza_resolve_phid_2022postEE \
    --hometitle "Resolve Custom Photon ID 2022postEE"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_2022postEE" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2022postEE_sf/plots/Data_2022postEE \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2022postEE_sf \
    --section-url "#Resolve_Custom_Photon_ID_2022postEE"

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --dest resolve_ph_2022preEE/hza_resolve_phid_2022preEE \
    --hometitle "Resolve Custom Photon ID 2022preEE"\
    --title "Efficiency / Scale Factor Measurements — hza_resolve_phid_2022preEE" \
    --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2022preEE_sf/plots/Data_2022preEE \
    --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2022preEE_sf \
    --section-url "#Resolve_Custom_Photon_ID_2022preEE"
}

publish_muon_one() {
  local home_title="$1"
  local wp="$2"
  local dest_slug="$3"
  local fit_variants=(Nominal AltBkg AltSig massBinDown massBinUp massRangeDown massRangeUp)
  local fit_args=()
  local var
  for var in "${fit_variants[@]}"; do
    fit_args+=(--src-fits-prefixed "${var}:${MUON_FITS_ROOT}/${var}/${wp}")
  done

  bash "${SCRIPT_DIR}/publish_subpage.sh" \
    --web-root "${MUON_WEB_ROOT}" \
    --home-url "${MUON_HOME_URL}" \
    --dest "${MUON_DEST_PREFIX}/${dest_slug}" \
    --hometitle "${home_title}" \
    --title "Efficiency / Scale Factor Measurements — ${wp}" \
    "${fit_args[@]}" \
    --src-summary "${MUON_SUMMARY_ROOT}/${wp}/efficiency" \
    --copy-pdf \
    --hide-pdf-in-html \
    --section-url "#${dest_slug}" \
    --summary-include "${wp}_abseta_pt_efficiencyData.png" \
    --summary-include "${wp}_abseta_pt_efficiencyMC.png" \
    --summary-include "${wp}_abseta_pt.png" \
    --summary-include "${wp}_abseta_pt_combined_syst.png" \
    --summary-include "${wp}_abseta_All_vs_pt.png" \
    --summary-include "${wp}_pt_All_vs_abseta.png" \
    --summary-include "SF_abseta_All_vs_pt.png" \
    --summary-include "SF_pt_All_vs_abseta.png" \
    --summary-order "SF_pt_All_vs_abseta.png" \
    --summary-order "SF_abseta_All_vs_pt.png" \
    --summary-order "${wp}_pt_All_vs_abseta.png" \
    --summary-order "${wp}_abseta_All_vs_pt.png" \
    --summary-order "${wp}_abseta_pt_efficiencyData.png" \
    --summary-order "${wp}_abseta_pt_efficiencyMC.png" \
    --summary-order "${wp}_abseta_pt.png" \
    --summary-order "${wp}_abseta_pt_combined_syst.png"
}

publish_muon() {
  MUON_TNP_ROOT="${MUON_TNP_ROOT:-/eos/home-p/pelai/HZa/root_mTnP}"
  MUON_WEB_ROOT="${MUON_WEB_ROOT:-/eos/user/p/pelai/www/HZa/sfs_muon}"
  MUON_HOME_URL="${MUON_HOME_URL:-/HZa/sfs_muon/}"
  MUON_DEST_PREFIX="${MUON_DEST_PREFIX:-run2024}"
  MUON_FITS_ROOT="${MUON_FITS_ROOT:-${MUON_TNP_ROOT}/fits_data/muon/generalTracks/Z/Run2024}"
  MUON_SUMMARY_ROOT="${MUON_SUMMARY_ROOT:-${MUON_TNP_ROOT}/plots/muon/generalTracks/Z/Run2024}"

  publish_muon_one \
    "Muon Double Trigger Lower Leg 2024" \
    "NUM_Mu8leg_DEN_HToZa_SignalMuons" \
    "muon_double_trigger_lower_leg_2024"
  publish_muon_one \
    "Muon Double Trigger Upper Leg 2024" \
    "NUM_Mu17leg_DEN_HToZa_SignalMuons" \
    "muon_double_trigger_upper_leg_2024"
  publish_muon_one \
    "Muon Single Trigger 2024" \
    "NUM_Mu24leg_DEN_HToZa_SignalMuons" \
    "muon_single_trigger_2024"
  publish_muon_one \
    "Muon Offline Selection 2024" \
    "NUM_HToZa_SignalMuons_DEN_TrackerMuons" \
    "muon_offline_selection_2024"
}

MODE="${1:-electron}"
case "${MODE}" in
  electron)
    publish_electron
    ;;
  muon)
    publish_muon
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown mode: ${MODE}"
    usage
    exit 1
    ;;
esac
