eos2022 = '/eos/cms/store/group/phys_egamma/ec/nkasarag/EGM_comm/TnP_samples/2022'
Run3_2022preEE = {
    'DY_MC_NLO_2022preEE': {
        'path': eos2022 + '/sim/DY_NLO/merged_Run3Summer22MiniAODv4-130X_mcRun3_2022_realistic_v5-v2.root',
        'isMC': True,
        'nEvts': 7286732,
    },
    'DY_MC_LO_2022preEE': {
        'path': eos2022 + '/sim/DY_LO/merged_DYJetsToLL_M_50_Run3Summer22MiniAODv4-forPOG_130X_mcRun3_2022_realistic_v5-v2.root',
        'isMC': True,
        'nEvts': 3595138,
    },
    'Data_2022preEE': {
        'path': eos2022 + '/data/merged_Run2022_BCD_ReReco_updated.root',
        'lumi': 7.98,
    },
}
Run3_2022postEE = {
    'DY_MC_NLO_2022postEE': {
        'path': eos2022 + '/sim/DY_NLO/merged_Run3Summer22EEMiniAODv4-130X_mcRun3_2022_realistic_postEE_v6-v2.root',
        'isMC': True,
        'nEvts': 27397320,
    },
    'DY_MC_LO_2022postEE': {
        'path': eos2022 + '/sim/DY_LO/merged_DYJetsToLL_M_50_Run3Summer22EEMiniAODv4-forPOG_130X_mcRun3_2022_realistic_postEE_v6-v2.root',
        'isMC': True,
        'nEvts': 12144692,
    },
    'Data_2022postEE': {
        'path': eos2022 + '/data/merged_Run2022_EReReco_FG_PromptReco_updated.root',
        'lumi': 26.67,
    },
}

eos2023 = '/eos/cms/store/group/phys_egamma/ec/tnpTuples/Prompt2023'
Run3_2023preBPix = {
    'DY_MC_NLO_2023preBPix': {
        'path': eos2023 + '/DY_NLO_2023preBPIX.root',
        'isMC': True,
        'nEvts': 21841873,
    },
    'DY_MC_LO_2023preBPix': {
        'path': eos2023 + '/DY_LO_2023preBPIX.root',
        'isMC': True,
        'nEvts': 18539920,
    },
    'Data_2023preBPix': {
        'path': eos2023 + '/data_2023C.root',
        'lumi': 17.79,
    },
}
Run3_2023postBPix = {
    'DY_MC_NLO_2023postBPix': {
        'path': eos2023 + '/DY_NLO_2023postBPIX.root',
        'isMC': True,
        'nEvts': 27397320,
    },
    'DY_MC_LO_2023postBPix': {
        'path': eos2023 + '/DY_LO_2023postBPIX.root',
        'isMC': True,
        'nEvts': 12144692,
    },
    'Data_2023postBPix': {
        'path': eos2023 + '/data_2023D.root',
        'lumi': 9.45,
    },
}

# 2024 lumi needs to be updated
eos2024 = '/eos/cms/store/group/phys_egamma/ScaleFactors/Data2024/PhoID/tnp_ntuples/merged_era'
Run3_2024 = {
    'DY_MC_NLO_2024': {
        'path': eos2024 + '/TnPTree_mc_amcatnlo.root',
        'isMC': True,
        'nEvts': 203271136,
    },
    'DY_MC_LO_2024': {
        'path': eos2024 + '/TnPTree_mc_madgraph.root',
        'isMC': True,
        'nEvts': 202883601,
    },
    'Data_2024B': {'path': eos2024 + '/TnPTree_data_B.root', 'lumi': 26.67},
    'Data_2024C': {'path': eos2024 + '/TnPTree_data_C.root', 'lumi': 26.67},
    'Data_2024D': {'path': eos2024 + '/TnPTree_data_D.root', 'lumi': 26.67},
    'Data_2024E': {'path': eos2024 + '/TnPTree_data_E.root', 'lumi': 26.67},
    'Data_2024F': {'path': eos2024 + '/TnPTree_data_F.root', 'lumi': 26.67},
    'Data_2024G': {'path': eos2024 + '/TnPTree_data_G.root', 'lumi': 26.67},
    'Data_2024H': {'path': eos2024 + '/TnPTree_data_H.root', 'lumi': 26.67},
    'Data_2024I': {'path': eos2024 + '/TnPTree_data_I.root', 'lumi': 26.67},
}

import os
import ROOT
import re
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

# ==== 繪圖樣式常數 (參考 signal_eff_sumw.py) ====
OFFSET = 0.01
MARKER_SIZE = 1.3
LINE_WIDTH = 3

LUMI_MAP = {
    '2022preEE': 7.98,
    '2022postEE': 26.70,
    '2023preBPix': 17.79,
    '2023postBPix': 9.45,
    '2024':109,
    'combined_run3': 61.89,
}
# 初始化為空，於 main 迴圈中指定
YEAR = None
LUMI_FB = 0.0

# 新增欲處理年份清單與映射
YEAR_LIST = ['2022preEE', '2022postEE', '2023preBPix', '2023postBPix', '2024']
SAMPLES = {
    '2022preEE': Run3_2022preEE,
    '2022postEE': Run3_2022postEE,
    '2023preBPix': Run3_2023preBPix,
    '2023postBPix': Run3_2023postBPix,
    '2024': Run3_2024,
}

_KEEP = []

def _ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def _make_hist(name, title, nbins, xmin, xmax, color):
    h = ROOT.TH1F(name, title, nbins, xmin, xmax)
    h.SetDirectory(0)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetLineWidth(LINE_WIDTH)  # 改用統一樣式常數
    return h

# ==== 軸樣式統一函式 ====
def _style_axes(h):
    ax = h.GetXaxis()
    ay = h.GetYaxis()
    for axis in (ax, ay):
        axis.CenterTitle(True)
        axis.SetTitleFont(42)
        axis.SetLabelFont(42)
        axis.SetTitleSize(0.055)
        axis.SetLabelSize(0.05)
    ax.SetTitleOffset(1.15)
    ay.SetTitleOffset(1.1 + 10 * OFFSET)
    ax.SetLabelOffset(0.009)

def _sanitize(name):
    return re.sub(r'[^A-Za-z0-9_]', '_', name)

def _get_branch_names(chain):
    return [b.GetName() for b in chain.GetListOfBranches()]

def _check_branches(chain, needed):
    names = set(_get_branch_names(chain))
    missing = [n for n in needed if n not in names]
    return missing

def _draw_overlay(chain, expr_uncorr, expr_corr, cut=None, nbins=50, xmin=0, xmax=1, title="", leg_pos=(0.17,0.73,0.50,0.88), keep=True):
    uid = ROOT.TUUID().AsString()
    name_unc = _sanitize(f"{expr_uncorr}_unc_{uid}")
    name_cor = _sanitize(f"{expr_corr}_cor_{uid}")

    # 直接讓 ROOT 生成並填充直方圖；避免先建空圖造成指標指向未填充的物件
    draw_opt = "goff"
    # 指定 binning 參數確保 ROOT 建圖
    n_unc = chain.Draw(f"({expr_uncorr})>>{name_unc}({nbins},{xmin},{xmax})", cut if cut else "", draw_opt)
    n_cor = chain.Draw(f"({expr_corr})>>{name_cor}({nbins},{xmin},{xmax})",  cut if cut else "", draw_opt)

    h_unc = ROOT.gROOT.Get(name_unc)
    h_cor = ROOT.gROOT.Get(name_cor)

    if not h_unc or not h_cor:
        print(f"[error] 取得不到直方圖物件: {name_unc}, {name_cor}")
        return

    # 設定樣式
    for h, color in [(h_unc, ROOT.kBlack), (h_cor, ROOT.kRed+1)]:
        h.SetLineColor(color)
        h.SetMarkerColor(color)
        h.SetLineWidth(LINE_WIDTH)   # 統一線寬
        h.SetMarkerStyle(20)
        h.SetMarkerSize(MARKER_SIZE)

    if n_unc == 0 or n_cor == 0 or h_unc.Integral() == 0 or h_cor.Integral() == 0:
        print(f"[warn] histogram empty: raw={expr_uncorr} (filled {n_unc}, integral {h_unc.Integral():.2f}) ; corr={expr_corr} (filled {n_cor}, integral {h_cor.Integral():.2f}) cut='{cut}'")
    else:
        print(f"[info] filled: raw({n_unc}) corr({n_cor}) integral(raw={h_unc.Integral():.2f}, corr={h_cor.Integral():.2f}) expr_corr='{expr_corr[:60]}{'...' if len(expr_corr)>60 else ''}'")

    if h_unc.Integral() > 0: h_unc.Scale(1.0 / h_unc.Integral())
    if h_cor.Integral() > 0: h_cor.Scale(1.0 / h_cor.Integral())

    h_unc.GetYaxis().SetTitle("A.U.")
    h_unc.GetXaxis().SetTitle(title)
    h_unc.SetTitle("")
    ymax = max(h_unc.GetMaximum(), h_cor.GetMaximum())
    h_unc.SetMaximum(1.2 * ymax if ymax > 0 else 1.0)

    # ==== 套用軸樣式 ====
    _style_axes(h_unc)
    # 設定 pad 邊界與 ticks
    pad = ROOT.gPad
    if pad:
        pad.SetMargin(0.12 + OFFSET, 0.035, 0.14, 0.09)
        pad.SetTickx()
        pad.SetTicky()

    h_unc.Draw("hist")
    h_cor.Draw("hist same")

    leg = ROOT.TLegend(*leg_pos)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.045)
    leg.AddEntry(h_unc, "Raw", "l")
    leg.AddEntry(h_cor, "Rho Corrected", "l")
    leg.Draw()

    # ==== 加入 CMS 與 lumi 標註 ====
    lat = ROOT.TLatex()
    lat.SetTextFont(42)
    lat.SetTextAlign(11)  # 左上
    lat.SetNDC()
    lat.SetTextSize(0.05)
    lat.DrawLatex(0.12 + OFFSET, 0.92, "#bf{CMS} #it{Preliminary}")
    lat.SetTextAlign(31)
    x_lumi = 1.0 - (pad.GetRightMargin() if pad else 0.035) - 0.005
    y_lumi = 0.92
    if LUMI_FB > 0:
        lat.DrawLatex(x_lumi, y_lumi, f"{LUMI_FB:.2f} fb^{{-1}} (13.6 TeV)")

    if keep:
        _KEEP.extend([h_unc, h_cor, leg, lat])

def _corr_expr(var, rho, a, b):
    return f"(({var}) - ({rho})*{a:.8f} + ({rho})*({rho})*{b:.10f})"

def _corr_expr_piecewise(var, rho, bins, coeff_list, crack=(1.4442, 1.566)):
    parts = []
    for (lo, hi, _), (a, b) in zip(bins, coeff_list):
        parts.append(
            f"((abs(ph_sc_eta)>={lo} && abs(ph_sc_eta)<{hi})*(({var}) - ({rho})*{a:.8f} + ({rho})*({rho})*{b:.10f}))"
        )
    c_lo, c_hi = crack
    parts.append(f"((abs(ph_sc_eta)>={c_lo} && abs(ph_sc_eta)<{c_hi})*({var}))")
    parts.append(f"(((abs(ph_sc_eta)<{bins[0][0]}) || (abs(ph_sc_eta)>={bins[-1][1]}))*({var}))")
    return "(" + " + ".join(parts) + ")"

def _build_chain(file_path, tree_path="tnpPhoIDs/fitter_tree"):
    ch = ROOT.TChain(tree_path)
    ch.Add(file_path)
    return ch

def _coeffs_all():
    bins = [
        (0.0,   1.0,    "0.0-1.0 (EB)"),
        (1.0,   1.4442, "1.0-1.4442 (EB)"),
        (1.566, 2.0,    "1.566-2.0 (EE)"),
        (2.0,   2.2,    "2.0-2.2 (EE)"),
        (2.2,   2.3,    "2.2-2.3 (EE)"),
        (2.3,   2.4,    "2.3-2.4 (EE)"),
        (2.4,   2.5,    "2.4-2.5 (EE)"),
    ]
    chIso = [
        (0.0342898, 0.000103508),
        (0.0281424, 0.000031494),
        (0.0288533, 0.0000666148),
        (0.0287890, 0.0000684993),
        (0.0264064, 0.0000889189),
        (0.0255870, 0.0000590178),
        (0.0224817, 0.0000422712),
    ]
    neuIso = [
        (0.170050, 0.000835),
        (0.208571, 0.000905),
        (0.246494, 0.000722),
        (0.306529, 0.000608),
        (0.322673, 0.000750),
        (0.315793, 0.000795),
        (0.365310, 0.000439),
    ]
    hoe = [
        (0.00198598, 0.0000115014),
        (0.20857100, 0.0000115014),
        (0.00302416, 0.0000151973),
        (0.30652900, 0.0000149651),
        (0.32267300, 0.0000147232),
        (0.31579300, 0.0000213958),
        (0.36531000, 0.0000280795),
    ]
    return bins, chIso, neuIso, hoe

def main():
    out_dir = "/afs/cern.ch/work/p/pelai/HZa/TnP/CMSSW_11_2_0/src/egm_tnp_analysis/plots"
    _ensure_dir(out_dir)
    bins, chIsoC, neuIsoC, hoeC = _coeffs_all()
    rho = "event_rho"
    var_defs = [
        ("ph_chIso",  "ph_chIso",  80, -10.0, 6.0,  chIsoC),
        ("ph_neuIso", "ph_neuIso", 80, -13.0, 10.0, neuIsoC),
        ("ph_hoe",    "ph_hoe",    80, -18.0, 5.0,  hoeC),
    ]

    for y in YEAR_LIST:
        if y not in SAMPLES:
            print(f"[warn] 年份 {y} 不在 SAMPLES 中，略過")
            continue
        # 取得 LO 樣本路徑
        sample_dict = SAMPLES[y]
        lo_key = next((k for k in sample_dict if "DY_MC_LO" in k), None)
        if not lo_key:
            print(f"[warn] 找不到 {y} 的 DY_MC_LO 樣本，略過")
            continue
        input_file = sample_dict[lo_key]['path']
        tree_path = "tnpPhoIDs/fitter_tree"

        chain = _build_chain(input_file, tree_path)
        total = chain.GetEntries()
        if total == 0:
            print(f"[error] {y} 樣本事件數為 0: {input_file}")
            continue

        needed_branches = ["event_rho", "ph_sc_eta", "ph_et", "ph_chIso", "ph_neuIso", "ph_hoe"]
        missing = _check_branches(chain, needed_branches)
        if missing:
            print(f"[error] {y} 缺少必要分支: {missing}")
            continue

        # 動態設定全域年份與 lumi
        global YEAR, LUMI_FB
        YEAR = y
        if y in LUMI_MAP:
            LUMI_FB = LUMI_MAP[y]
        else:
            # 例如 2024：自動加總所有 data era lumi
            data_lumi = sum(v['lumi'] for k, v in sample_dict.items() if k.startswith("Data_") and 'lumi' in v)
            LUMI_FB = data_lumi
            LUMI_MAP[y] = LUMI_FB
            print(f"[info] 動態計算 {y} lumi = {LUMI_FB:.2f} fb^-1")

        # 僅 2024 年限制最多處理前 1,000,000 筆事件
        cut_str = "Entry$<1000000" if y == '2024' else None

        print(f"[info] === 開始繪圖: {y} (entries={total}) ===")
        for vraw, vtitle, nb, xmin, xmax, coeff_list in var_defs:
            vcorr = _corr_expr_piecewise(vraw, rho, bins, coeff_list)
            cname = f"c_{_sanitize(vraw)}_{YEAR}"
            c = ROOT.TCanvas(cname, f"{vtitle} piecewise corrected {YEAR}", 700, 600)
            _draw_overlay(
                chain,
                expr_uncorr=vraw,
                expr_corr=vcorr,
                cut=cut_str,
                nbins=nb, xmin=xmin, xmax=xmax,
                title=vtitle,
                keep=True
            )
            c.Update()
            base = f"DY_LO_{YEAR}_{_sanitize(vraw)}"
            c.SaveAs(os.path.join(out_dir, base + ".pdf"))
            c.SaveAs(os.path.join(out_dir, base + ".png"))
        print(f"[info] === 完成: {y} ===")

    print(f"Saved individual plots to: {out_dir}")

if __name__ == "__main__":
    main()
