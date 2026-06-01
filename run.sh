#!/bin/bash
set -euo pipefail

echo "PWD: $PWD"
echo "Setting environment..."

workdir="$(pwd)"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

detect_cmssw_src_from_path() {
  local start="$1"
  local cur="$start"
  while [[ "$cur" != "/" ]]; do
    if [[ "$(basename "$cur")" == "src" && -d "$cur/../.SCRAM" ]]; then
      echo "$cur"
      return 0
    fi
    cur="$(dirname "$cur")"
  done
  return 1
}

cmssw_src=""
if [[ -n "${CMSSW_BASE:-}" && -d "$CMSSW_BASE/src" ]]; then
  cmssw_src="$CMSSW_BASE/src"
else
  cmssw_src="$(detect_cmssw_src_from_path "$script_dir" || true)"
  if [[ -z "$cmssw_src" ]]; then
    cmssw_src="$(detect_cmssw_src_from_path "$workdir" || true)"
  fi
  if [[ -z "$cmssw_src" ]]; then
    echo "ERROR: Cannot locate CMSSW src directory."
    echo "       Please run 'cmsenv' in a valid CMSSW area, or run this script from inside CMSSW_*/src."
    exit 1
  fi
  export CMSSW_BASE="$(cd "$cmssw_src/.." && pwd)"
fi

pushd "$cmssw_src" >/dev/null
eval "$(scram runtime -sh)"
popd >/dev/null


pkg_parent="$(dirname "$script_dir")"

# Add the package parent directory so `python -m egm_tnp_analysis...` can be resolved.
export PYTHONPATH="$pkg_parent:${PYTHONPATH:-}"
export PYTHONIOENCODING="${PYTHONIOENCODING:-UTF-8}"
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"


# If your need it：BUILD_CPP=1 ./run.sh <settings_mod> <WP>
BUILD_CPP="${BUILD_CPP:-0}"
if [[ "$BUILD_CPP" == "1" ]]; then
  if command -v root-config >/dev/null 2>&1; then
    echo "[build] Trying building C++ extension (histUtils) ..."
    set +e
    bash "$script_dir/tools/build_histutils.sh"
    rc=$?
    set -e
    if [[ $rc -ne 0 ]]; then
      echo "[build][WARN] Failed to build C++ extension, will use existing .so or fallback."
    fi
  else
    echo "[build][WARN] root-config not found, skipping C++ extension build, using pure Python fallback."
  fi
else
  echo "[build] Skipping C++ extension build (set environment variable BUILD_CPP=1 to enable)."
fi


SETTINGS_MOD=$1
WP=$2   


# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --checkBins
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --createBins
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --createHists --sample mcNom
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --createHists --sample mcAlt
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --createHists --sample data
# # #----------- Fitting Procedure --------------
# # #----------- 1 MC Nominal Fit -----------------------
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --fitSample mcNom
# # #----------- 2 Data Fit -----------------------
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --fitSample data
# # # ----------- 3 MC Fit altsig -----------------------
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altSig
# # # ----------- 4 MC Fit altbkg -----------------------
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altBkg
# # # ----------- 5 MC Fit altSigBkg -----------------------
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altSigBkg
# # ----------- Get Results -----------------------
python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --sumUp --exportJson



# ----------- Tuning a bin --------------
# For Region
# High pT
# ----------- 2022preEE --------------
# for i in 00 15 20; do
#   python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --iBin ${i}
# done
# ----------- 2022postEE --------------
# for i in 00 15 20; do
#   python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --iBin ${i}
# done
# ----------- 2023postBPix --------------
# for i in 08; do
#   python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --iBin ${i}
# done
# Low pT
# ----------- 2022preEE --------------
# for i in 04 05; do
#   python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altBkg --iBin ${i}
# done


# Single Bin Tuning Example
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --iBin 7
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altBkg --iBin 6
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altSig --iBin 1
# python3 -m egm_tnp_analysis.tnpEGM_fitter "$SETTINGS_MOD" --flag "$WP" --doFit --altSigBkg --iBin 6

# sh publish.sh