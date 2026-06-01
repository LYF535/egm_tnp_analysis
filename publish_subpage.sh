#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# publish_subpage.sh  (v2: default /eos/user/p/pelai/www/HZa/sfs)
#
# Purpose: Generate a subpage under /eos/user/p/pelai/www/HZa/sfs
# Features:
#   - Automatically create the subpage structure
#   - (Optional) sync fits/ and summary/ files (PNG only)
#   - Automatically generate index.html
#   - Build an image wall from images and PDFs in summary/
#   - Set public permissions
#
# Environment variables:
#   FORCE_REGEN_SUB=1   Force rebuild subpage index.html
#   FORCE_REGEN_HOME=1  Force rebuild home index.html
#   FORCE_REGEN_FIT=1   Force rebuild fits/index.html
#
# ------------------------------------------------------------
# Required arguments:
#   --dest <relative EOS path for plots>    e.g.: resolve_ph_2022preEE/hza_resolve_phid_2022preEE
#   --title <page title>                     e.g.: "Efficiency / Scale Factor Measurements — hza_resolve_phid_2022preEE"
#
# Optional arguments:
#   --src-fits <source directory for all fit plots>    e.g.: /eos/home-p/pelai/HZa/root_TnP/muon_2023/hzg_muid_2023/fits
#   --src-fits-prefixed <prefix:path>                  e.g.: Nominal:/eos/.../Nominal/NUM_xxx (repeatable)
#   --src-summary <source directory for summary plots> e.g.: /eos/home-p/pelai/HZa/root_TnP/muon_2023/hzg_muid_2023/summary
#   --web-root <root path>                              default: /eos/user/p/pelai/www/HZa/sfs
#   --home-url <home URL>                               default: /HZa/sfs/
#   --section-url <anchor>                              e.g.: "#Resolved_Custom_Photon_ID_2022preEE"
#   --summary-include <glob>                            include filename patterns to sync from summary (repeatable)
#   --summary-exclude <glob>                            exclude filename patterns from summary (repeatable)
#   --summary-order <glob>                              display order on summary page (repeatable; first match first)
#   --copy-pdf                                           sync PDFs from source to web directory
#   --hide-pdf-in-html                                   show PNG only in HTML (even if PDFs exist in directory)
#
# Example:
# ./publish_subpage.sh \
#   --dest photon_2022preEE/hza_resolve_phidfsr_2022preEE \
#   --title "Efficiency / scale factor measurements — hza_resolve_phid_2022preEE" \
#   --src-fits /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2022preEE_sf/plots \
#   --src-summary /eos/home-p/pelai/HZa/root_TnP/hza_resolve_phid_2022preEE_sf \
#   --section-url "#Resolved_Custom_Photon_ID_2022preEE"
# ------------------------------------------------------------

WEB_ROOT="/eos/user/p/pelai/www/HZa/sfs"
HOME_URL="/HZa/sfs/"
SECTION_URL=""
DEST_REL=""
ITEM_TITLE=""
TITLE=""
SRC_FITS=""
SRC_FITS_PREFIXED=()
SRC_SUMMARY=""
SUMMARY_INCLUDE_PATTERNS=()
SUMMARY_EXCLUDE_PATTERNS=()
SUMMARY_ORDER_PATTERNS=()
DID_FITS_SYNC=0
COPY_PDF=0
HIDE_PDF_IN_HTML=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --web-root)     WEB_ROOT="$2"; shift 2;;
    --home-url)     HOME_URL="$2"; shift 2;;
    --section-url)  SECTION_URL="$2"; shift 2;;
    --dest)         DEST_REL="$2"; shift 2;;
    --hometitle)    ITEM_TITLE="$2"; shift 2;;
    --title)        TITLE="$2"; shift 2;;
    --src-fits)     SRC_FITS="$2"; shift 2;;
    --src-fits-prefixed) SRC_FITS_PREFIXED+=("$2"); shift 2;;
    --src-summary)  SRC_SUMMARY="$2"; shift 2;;
    --summary-include) SUMMARY_INCLUDE_PATTERNS+=("$2"); shift 2;;
    --summary-exclude) SUMMARY_EXCLUDE_PATTERNS+=("$2"); shift 2;;
    --summary-order) SUMMARY_ORDER_PATTERNS+=("$2"); shift 2;;
    --copy-pdf)      COPY_PDF=1; shift;;
    --hide-pdf-in-html) HIDE_PDF_IN_HTML=1; shift;;
    -h|--help)
      sed -n '1,80p' "$0"; exit 0;;
    *)
      echo "Unknown parameter: $1"; exit 1;;
  esac
done

if [[ -z "$DEST_REL" || -z "$TITLE" ]]; then
  echo "❌ Missing required parameters --dest or --title"
  exit 1
fi

# Additional guard: prevent empty WEB_ROOT from breaking HOME_INDEX
if [[ -z "${WEB_ROOT:-}" ]]; then
  echo "❌ WEB_ROOT is empty, please provide --web-root"
  exit 1
fi

DEST_DIR="${WEB_ROOT%/}/${DEST_REL%/}"
FITSD="${DEST_DIR}/fits"
SUMMD="${DEST_DIR}/summary"

echo ">>> Destination: ${DEST_DIR}"
mkdir -p "$FITSD" "$SUMMD"

# Sync sources (if provided)
if [[ "${#SRC_FITS_PREFIXED[@]}" -gt 0 ]]; then
  DID_FITS_SYNC=1
  echo ">>> Synchronizing fits/ source (prefixed filenames): ${SRC_FITS_PREFIXED[*]}"
  # In prefixed mode, clean old PNGs first to avoid mixing with legacy (non-prefixed) filenames.
  find "${FITSD}" -type f -iname '*.png' -delete
  for spec in "${SRC_FITS_PREFIXED[@]:-}"; do
    prefix="${spec%%:*}"
    src="${spec#*:}"
    if [[ -z "${prefix}" || -z "${src}" || "${src}" == "${spec}" ]]; then
      echo "⚠️ Skipping invalid --src-fits-prefixed parameter: ${spec}"
      continue
    fi
    if [[ ! -d "${src}" ]]; then
      echo "⚠️ fits source does not exist (skipping ${prefix}): ${src}"
      continue
    fi
    echo ">>> Synchronizing fits source [${prefix}]: ${src}"
    while IFS= read -r -d '' f; do
      rel="${f#${src%/}/}"
      case "${rel}" in
        *1p44To1p57*|*m1p57Tom1p44*) continue ;;
      esac
      rel_dir="$(dirname "${rel}")"
      base="$(basename "${rel}")"
      out_dir="${FITSD}/${rel_dir}"
      mkdir -p "${out_dir}"
      cp -f "${f}" "${out_dir}/${prefix}_${base}"
    done < <(
      if [[ "$COPY_PDF" == "1" ]]; then
        find "${src}" -type f \( -iname '*.png' -o -iname '*.pdf' \) -print0
      else
        find "${src}" -type f -iname '*.png' -print0
      fi
    )
  done
elif [[ -n "${SRC_FITS}" && -d "${SRC_FITS}" ]]; then
  DID_FITS_SYNC=1
  echo ">>> Synchronizing fits/ source (PNG only): ${SRC_FITS}"
  fits_rsync_args=(
    -avL
    "--include=*/"
    "--exclude=**1p44To1p57**"
    "--exclude=**m1p57Tom1p44**"
    "--include=*.png"
  )
  if [[ "$COPY_PDF" == "1" ]]; then
    fits_rsync_args+=("--include=*.pdf")
  fi
  fits_rsync_args+=("--exclude=*")
  rsync "${fits_rsync_args[@]}" "${SRC_FITS%/}/" "${FITSD}/"
fi

if [[ -n "${SRC_SUMMARY}" && -d "${SRC_SUMMARY}" ]]; then
  echo ">>> Synchronizing summary/ source (PNG only): ${SRC_SUMMARY}"
  summary_rsync_args=(
    -avL
    --delete
    "--include=*/"
  )
  if [[ "${#SUMMARY_INCLUDE_PATTERNS[@]}" -gt 0 ]]; then
    for pat in "${SUMMARY_INCLUDE_PATTERNS[@]:-}"; do
      summary_rsync_args+=("--include=${pat}")
    done
  else
    # Keep the legacy default electron/photon behavior.
    summary_rsync_args+=(
      "--include=**/HZa_SF2D_hza_*.png"
      "--include=**/HZa_SFvseta_*.png"
      "--include=**/HZa_SFvspT_*.png"
    )
  fi
  for pat in "${SUMMARY_EXCLUDE_PATTERNS[@]:-}"; do
    summary_rsync_args+=("--exclude=${pat}")
  done
  summary_rsync_args+=("--exclude=*")
  rsync "${summary_rsync_args[@]}" "${SRC_SUMMARY%/}/" "${SUMMD}/"
  if [[ "$COPY_PDF" == "1" ]]; then
    echo ">>> 額外同步 summary PDF：${SRC_SUMMARY}"
    rsync -avL --delete \
      --include='*/' \
      --include='*.pdf' \
      --exclude='*' \
      "${SRC_SUMMARY%/}/" "${SUMMD}/"
  fi
fi

INDEX="${DEST_DIR}/index.html"
FORCE_REGEN_SUB="${FORCE_REGEN_SUB:-0}"
FORCE_REGEN_HOME="${FORCE_REGEN_HOME:-0}"
FORCE_REGEN_FIT="${FORCE_REGEN_FIT:-0}"  # Added: control forced rebuild of fits/index.html
if [[ ! -f "$INDEX" || "$FORCE_REGEN_SUB" == "1" ]]; then
  echo ">>> Generated Sub-page index.html"
  cat > "$INDEX" <<HTML
<!doctype html>
<html lang="en" id="top">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Summary Plots</title>
<style>
  :root{--mx:22px}
  html,body{margin:0;padding:0}
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#222;background:#fff}
  header{position:sticky;top:0;background:#fff;border-bottom:1px solid #eee;padding:14px var(--mx);z-index:10}
  header h1{margin:0;font-size:1.2rem}
  main{max-width:1200px;margin:0 auto;padding:18px var(--mx) 28px}
  p{line-height:1.55;margin:0 0 12px}
  .muted{color:#666}
  a{color:#0b5bd3;text-decoration:none}
  a:hover{text-decoration:underline}

  /* Card grid: min width per card from 260px to 340px */
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(1000px,1fr));gap:20px}

  /* Card style: larger border radius and wider spacing */
  .card{border:1px solid #e0e0e0;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.06);min-height:600px;}

  /* Increase image area height */
  .card img{width:100%;height:580px;object-fit:contain;background:#fafafa}

  /* Larger filename text */
  .name{font-size:1.05rem;padding:12px 14px;border-top:1px solid #eee;word-break:break-all}

  /* Enlarge PDF center text to match the visual scale */
  .pdf{display:flex;align-items:center;justify-content:center;height:320px;background:#fafafa;font-size:1.1rem}

  .toplink{position:fixed;right:16px;bottom:16px;background:#0b5bd3;color:#fff;padding:8px 12px;border-radius:999px;text-decoration:none}
  .caption{color:#555;font-size:.92rem;margin-top:8px}
  nav.breadcrumb{margin:8px 0 0;font-size:1.3rem}
</style>

<header>
  <h1>${TITLE}</h1>
  <nav class="breadcrumb">
    <a href="${HOME_URL}">← Back to Home</a>
  </nav>
</header>

<main>
  <p class="muted">This page was auto-generated. Last updated: <span id="ts"></span></p>

  <h2>All fit plots can be found <a href="fits/">here</a>.</h2>

  <h2>Summary Plots</h2>

  <div class="grid">
    <!-- AUTO SUMMARY START -->
    <!-- AUTO SUMMARY END -->
  </div>

</main>

<a class="toplink" href="#top">Back to Top</a>

<script>
  document.getElementById('ts').textContent = new Date().toLocaleString();
</script>
</html>
HTML
else
  echo ">>> Using existing index.html (will update card section)"
fi

# Generate card list
TMP_CARDS="$(mktemp)"

# Switch to the destination directory first so relative paths resolve correctly.
cd "$DEST_DIR"

python3 - "$TMP_CARDS" "$HIDE_PDF_IN_HTML" "${SUMMARY_ORDER_PATTERNS[@]:-}" <<'PY'
import fnmatch
import html
import pathlib
import sys

cards_path = pathlib.Path(sys.argv[1])
hide_pdf_in_html = sys.argv[2] == "1"
order_patterns = [p for p in sys.argv[3:] if p]
summary_dir = pathlib.Path("summary")
if not summary_dir.exists():
    cards_path.write_text("")
    raise SystemExit(0)

suffixes = {".png"} if hide_pdf_in_html else {".png", ".pdf"}
files = sorted(
    str(p).replace("\\", "/")
    for p in summary_dir.rglob("*")
    if p.is_file() and p.suffix.lower() in suffixes
)

ordered = []
remaining = files.copy()

for pattern in order_patterns:
    candidate_patterns = [pattern]
    if "/" not in pattern:
        candidate_patterns.append(f"summary/{pattern}")
    matched = []
    for fpath in remaining:
        if any(fnmatch.fnmatch(fpath, pat) for pat in candidate_patterns):
            matched.append(fpath)
    for m in matched:
        ordered.append(m)
        remaining.remove(m)

files = ordered + remaining
lines = []
for name in files:
    esc = html.escape(name)
    if name.lower().endswith(".pdf"):
        lines.append(
            f'<a class="card" href="{esc}"><div class="pdf">📄 {esc}</div>'
            f'<div class="name">{esc}</div></a>'
        )
    else:
        lines.append(
            f'<a class="card" href="{esc}"><img loading="lazy" src="{esc}" alt="{esc}">'
            f'<div class="name">{esc}</div></a>'
        )

cards_path.write_text("\n".join(lines))
PY

# Insert cards into placeholders
python3 - "$INDEX" "$TMP_CARDS" <<'PY'
import re, sys, pathlib
index_path = pathlib.Path(sys.argv[1])
cards_path = pathlib.Path(sys.argv[2])
html = index_path.read_text()
cards = cards_path.read_text()
replacement = "<!-- AUTO SUMMARY START -->\n" + cards
if cards:
    replacement += "\n"
replacement += "    <!-- AUTO SUMMARY END -->"

if "<!-- AUTO SUMMARY START -->" in html and "<!-- AUTO SUMMARY END -->" in html:
    html = re.sub(
        r"<!-- AUTO SUMMARY START -->.*?<!-- AUTO SUMMARY END -->",
        replacement,
        html,
        count=1,
        flags=re.S,
    )
elif "<!-- AUTO SUMMARY -->" in html:
    html = re.sub(r"<!-- AUTO SUMMARY -->", replacement, html, count=1)
else:
    html = re.sub(
        r"(<div class=\"grid\">\s*).*?(\s*</div>\s*</main>)",
        r"\1" + replacement + r"\2",
        html,
        count=1,
        flags=re.S,
    )
index_path.write_text(html)
print("index.html updated.")
PY

# ---- Update home page (WEB_ROOT/index.html) ----
HOME_INDEX="${WEB_ROOT%/}/index.html"
NEW_ITEM="<li><a href=\"./${DEST_REL%/}/\">${ITEM_TITLE}</a></li>"
HOME_ITEMS_TMP="$(mktemp)"

if [[ -f "$HOME_INDEX" && "$FORCE_REGEN_HOME" == "1" ]]; then
  python3 - "$HOME_INDEX" "$HOME_ITEMS_TMP" <<'PY'
import pathlib
import re
import sys

home = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
html = home.read_text()

match = re.search(
    r'<ul[^>]*class="[^"]*\bauto-list\b[^"]*"[^>]*>(.*?)</ul>',
    html,
    flags=re.S | re.I,
)
if not match:
    match = re.search(r"<ul[^>]*>(.*?)</ul>", html, flags=re.S | re.I)

items = []
seen = set()
if match:
    for item in re.findall(r"<li\b.*?</li>", match.group(1), flags=re.S | re.I):
        cleaned = item.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            items.append(cleaned)

out.write_text("\n".join(items))
PY
fi

if [[ ! -f "$HOME_INDEX" || "$FORCE_REGEN_HOME" == "1" ]]; then
  echo ">>> Established homepage: ${HOME_INDEX}"
  cat > "$HOME_INDEX" <<HTML
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>HZa SF</title>
<style>
  ul.auto-list li a {
    font-size: 1.5rem;     /* Can be changed to 18px or larger */
    font-weight: 500;      /* Slightly bolder, optional */
  }
  .center { text-align: center; }
  .center ul { display: inline-block; text-align: left; }
  li {
    margin-bottom: 16px;  /* Controls item spacing; units can be px/em/rem */
  }
</style>
<div class="center">
  <h2>Welcome to H -> Za -> ll gamma gamma efficiency and scale factors measurement.</h2>
  <h2>
    This page contains links to the scale factor measurement fits and results for the Run 3 2022+2023+2024 Higgs to Za analysis.<br>
  </h2>
  <h2>
    Presentations will be given to the MUO POG
    <a href="https://indico.cern.ch/event/XXXXXXX" target="_blank">here</a>
    and to the EGM POG
    <a href="https://indico.cern.ch/event/YYYYYYY" target="_blank">here</a>.
    (Left the space for the future)<br>
  </h2>
  <h2>See below links for plots.</h2>
  <ul class="auto-list">
    <!-- AUTO LIST START -->
$(sed 's/^/    /' "$HOME_ITEMS_TMP")
    <!-- AUTO LIST END -->
  </ul>
</div>
</html>
HTML
fi  # Added missing fi to avoid shell syntax errors

python3 - "$HOME_INDEX" "$NEW_ITEM" <<'PY'
import sys, pathlib, re
home = pathlib.Path(sys.argv[1])
item = sys.argv[2].strip()
if not home.exists():
    print(f">>> Homepage file does not exist: {home}")
    sys.exit(1)
html = home.read_text()

# Added: if legacy home page is missing auto-list class, patch it automatically
if 'class="auto-list"' not in html:
    html = re.sub(r"<ul(\s*)>", r"<ul class=\"auto-list\">", html, count=1)

if re.search(re.escape(item), html):
    print(">>> Homepage already contains this item, skipping addition")
    sys.exit(0)

if "<!-- AUTO LIST START -->" in html and "<!-- AUTO LIST END -->" in html:
    html = re.sub(
        r"(<!-- AUTO LIST START -->)(.*?)(<!-- AUTO LIST END -->)",
        lambda m: f"{m.group(1)}{m.group(2)}\n    {item}\n    {m.group(3)}",
        html,
        count=1,
        flags=re.S,
    )
elif "<!-- AUTO LIST -->" in html:
    html = html.replace("<!-- AUTO LIST -->", f"<!-- AUTO LIST -->\n  {item}", 1)
else:
    m = re.search(
        r'(<ul[^>]*class="[^"]*\bauto-list\b[^"]*"[^>]*>)(.*?)(</ul>)',
        html,
        flags=re.IGNORECASE | re.S,
    )
    if m:
        html = html[: m.start(3)] + f"    {item}\n" + html[m.start(3) :]
    else:
        html += f"\n<ul class=\"auto-list\">\n  {item}\n</ul>\n"
home.write_text(html)
print(">>> Homepage updated")
PY

rm -f "$HOME_ITEMS_TMP"
rm -f "$TMP_CARDS"

# Function to build fits/index.html (PNG only)
build_fits_index() {
  local dir="$1"
  local out="${dir}/index.html"
  # Added: skip if file exists and no forced rebuild is requested.
  if [[ -f "$out" && "$FORCE_REGEN_FIT" != "1" && "$DID_FITS_SYNC" != "1" ]]; then
    echo ">>> fits/index.html already exists (skipping, set FORCE_REGEN_FIT=1 to force rebuild)"
    return 0
  fi
  if [[ ! -d "$dir" ]]; then
    echo "⚠️ fits directory does not exist: $dir"
    return 1
  fi
  local tmp_cards
  tmp_cards="$(mktemp)"

  (
    cd "$dir"
    # PNG only; if no files are found, write an empty-state hint below.
    # Use -print -quit to avoid false failure under pipefail when grep -q exits early.
    if ! find . -type f -iname '*.png' -print -quit | LC_ALL=C grep -q .; then
      cat > "$tmp_cards" <<'EMPTY'
<div class="card">
  <div class="pdf" style="height:240px;font-size:1rem">No PNG files found.</div>
  <div class="name">—</div>
</div>
EMPTY
    else
      python3 - "$tmp_cards" <<'PY'
import sys, html, pathlib
cards_path = pathlib.Path(sys.argv[1])
root = pathlib.Path(".")
pngs = sorted(
    str(p.relative_to(root)).replace("\\", "/")
    for p in root.rglob("*")
    if p.is_file() and p.suffix.lower() == ".png"
)
lines=[]
for raw in pngs:
    if not raw.strip(): continue
    name = raw.strip()
    esc = html.escape(name)
    lines.append(f'<a class="card" href="./{esc}">'
                 f'<img loading="lazy" src="./{esc}" alt="{esc}">'
                 f'<div class="name">{esc}</div></a>')
cards_path.write_text("\n".join(lines))
PY
    fi
  ) || { echo "❌ Cannot list PNG"; rm -f "$tmp_cards"; return 1; }

  cat > "$out" <<HTML
<!doctype html>
<html lang="en" id="top">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Fit plots</title>
<style>
  :root{--mx:22px} html,body{margin:0;padding:0}
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#222;background:#fff}
  header{position:sticky;top:0;background:#fff;border-bottom:1px solid #eee;padding:14px var(--mx);z-index:10}
  header h1{margin:0;font-size:1.1rem}
  main{max-width:1400px;margin:0 auto;padding:18px var(--mx) 34px}
  a{color:#0b5bd3;text-decoration:none} a:hover{text-decoration:underline}
  nav.breadcrumb{font-size:1.1rem;margin:0 0 12px}
  
  /* Card grid: min width per card from 260px to 340px */
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(1000px,1fr));gap:10px}

  /* Card style: larger border radius and wider spacing */
  .card{border:1px solid #e0e0e0;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.06);min-height:800px;line-height:0;margin:0;}

  /* Increase image area height */
  .card img{width:103%;height:780px;object-fit:contain;object-position:center;background:#fafafa;margin:0;padding:0;}

  /* Larger filename text */
  .name{font-size:1.05rem;padding:5px 6px;border-top:1px solid #eee;word-break:break-all;}

  /* Enlarge PDF center text to match the visual scale */
  .pdf{display:flex;align-items:center;justify-content:center;height:320px;background:#fafafa;font-size:1.1rem}

  .toplink{position:fixed;right:16px;bottom:16px;background:#0b5bd3;color:#fff;padding:8px 12px;border-radius:999px;text-decoration:none}
  .caption{color:#555;font-size:.92rem;margin-top:8px}
  nav.breadcrumb{margin:8px 0 0;font-size:1.3rem}

</style>
<header>
  <h1>Fit Plots</h1>
  <nav class="breadcrumb">
    <a href="../">← Back to Previous Page</a>
  </nav>
</header>
<main>
  <div class="grid">
$(cat "$tmp_cards")
  </div>
</main>
<a class="toplink" href="#top">Back to Top</a>
</html>
HTML

  if [[ ! -s "$out" ]]; then
    echo "❌ Generated ${out} failed"
    rm -f "$tmp_cards"
    return 1
  fi
  rm -f "$tmp_cards"
  echo "✅ Generated ${out}"
}

rm -f "$TMP_CARDS"

# Rebuild fits/index.html
build_fits_index "$FITSD"

HOME_PATH="/${HOME_URL#/}"
HOME_PATH="${HOME_PATH%/}/"
DEST_PATH="${DEST_REL%/}/"
echo "🌐 Link：https://pelai.web.cern.ch${HOME_PATH}${DEST_PATH}"
echo "🏠 Homepage：https://pelai.web.cern.ch${HOME_PATH}"
