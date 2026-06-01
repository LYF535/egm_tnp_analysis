#!/usr/bin/env bash
set -euo pipefail

# 定位封包根目錄與 lib 目錄
TOOLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_DIR="$(cd "${TOOLS_DIR}/.." && pwd)"
LIB_DIR="${PKG_DIR}/libPython"

# 環境健檢
if ! command -v root-config >/dev/null 2>&1; then
  echo "[build_histutils] ERROR: root-config not found. Did you run 'cmsenv'?"
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "[build_histutils] ERROR: python3 not found in PATH."
  exit 1
fi

# 由 Python sysconfig 取得 EXT_SUFFIX 與 include 目錄
read -r EXT_SUFFIX PY_INC1 PY_INC2 <<<"$(python3 - <<'PY'
import sysconfig, sys
sfx = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
inc = sysconfig.get_paths().get("include") or ""
pinc = sysconfig.get_paths().get("platinclude") or ""
print(sfx, inc, pinc)
PY
)"
PY_INC_FLAGS=""
[[ -n "${PY_INC1}" && -d "${PY_INC1}" ]] && PY_INC_FLAGS+=" -I${PY_INC1}"
[[ -n "${PY_INC2}" && -d "${PY_INC2}" && "${PY_INC2}" != "${PY_INC1}" ]] && PY_INC_FLAGS+=" -I${PY_INC2}"

# 檢查 Python.h
if [[ -z "${PY_INC_FLAGS}" || ! -f "${PY_INC1}/Python.h" ]] && [[ ! -f "${PY_INC2}/Python.h" ]]; then
  echo "[build_histutils] ERROR: Python.h not found under:"
  echo "  - ${PY_INC1}"
  echo "  - ${PY_INC2}"
  echo "請確認已執行 'cmsenv' 並使用 CMSSW 提供的 python3。"
  exit 1
fi

ROOT_CFLAGS="$(root-config --cflags)"
ROOT_LIBS="$(root-config --libs)"

# 偵測來源檔位置
SRC_CAND1="${LIB_DIR}/histUtils.cpp"
SRC_CAND2="${PKG_DIR}/histUtils.cpp"
if [[ -f "${SRC_CAND1}" ]]; then
  SRC="${SRC_CAND1}"
elif [[ -f "${SRC_CAND2}" ]]; then
  SRC="${SRC_CAND2}"
else
  echo "[build_histutils] ERROR: cannot find histUtils.cpp under:"
  echo "  - ${SRC_CAND1}"
  echo "  - ${SRC_CAND2}"
  exit 1
fi

# 輸出檔名（帶 EXT_SUFFIX，優先於舊的 .so）
OUT_SO="${LIB_DIR}/histUtils${EXT_SUFFIX}"

echo "[build_histutils] EXT_SUFFIX: ${EXT_SUFFIX}"
echo "[build_histutils] PY_INC_FLAGS:${PY_INC_FLAGS}"
echo "[build_histutils] ROOT_CFLAGS: ${ROOT_CFLAGS}"
echo "[build_histutils] Building: ${OUT_SO}"
mkdir -p "${LIB_DIR}"

# 與 CMSSW 相容的 flags
CXX="${CXX:-g++}"
CXXSTD="${CXXSTD:-c++17}"
CXXFLAGS="-O3 -pipe -fPIC -Wall -Wextra -Wno-unused-parameter -Wno-sign-compare -Wno-unused-variable -DNDEBUG"

# 編譯&連結
${CXX} ${CXXFLAGS} -std=${CXXSTD} \
  ${ROOT_CFLAGS} ${PY_INC_FLAGS} \
  -shared -o "${OUT_SO}" "${SRC}" \
  ${ROOT_LIBS}

echo "[build_histutils] Success: ${OUT_SO}"

#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pkg_dir="$(cd "$here/.." && pwd)"
cd "$pkg_dir/libPython"

echo "[build_histutils] building histUtils from $(pwd)"

# 依賴檢查
if ! command -v root-config >/dev/null 2>&1; then
  echo "[build_histutils][ERROR] root-config not found. Please do 'cmsenv' first."
  exit 1
fi

py=${PYTHON:-python3}
if ! command -v "$py" >/dev/null 2>&1; then
  echo "[build_histutils][ERROR] python not found."
  exit 1
fi

# 產生 C++ 源碼
if ! python3 -c "import Cython" >/dev/null 2>&1; then
  echo "[build_histutils] installing Cython locally (pip --user) ..."
  "$py" -m pip install --user cython >/dev/null
fi

echo "[build_histutils] cythonizing histUtils.pyx ..."
"$py" -m cython -3 --cplus histUtils.pyx -o histUtils.cpp

# 編譯選項
cxx=${CXX:-g++}
cxxflags="-O2 -fPIC -std=c++17 $(root-config --cflags)"
ldflags="-shared $(root-config --libs)"
pyincs="$("$py" -c 'import sysconfig; print(sysconfig.get_config_var("INCLUDEPY"))')"
if [[ -n "${pyincs:-}" && -d "$pyincs" ]]; then
  cxxflags="$cxxflags -I$pyincs"
fi

# 編譯
echo "[build_histutils] compiling shared object ..."
$cxx $cxxflags -c histUtils.cpp -o histUtils.o
$cxx $ldflags histUtils.o -o "histUtils$(python3 -c 'import sysconfig;import sys; print(sysconfig.get_config_var("EXT_SUFFIX") or ".so")')"

echo "[build_histutils] done."
