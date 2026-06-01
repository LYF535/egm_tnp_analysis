# -*- coding: utf-8 -*-
### python specific import
import argparse
import os
import sys
import pickle
import shutil
from multiprocessing import Pool
import math, json

parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
parser.add_argument('--fitSample'  , default=None         , help = 'choose which sample to run fits on', choices=['data', 'mcNom', 'mcAlt', 'tagSel'])
parser.add_argument('--altSig'     , action='store_true'  , help = 'alternate signal model fit')
parser.add_argument('--addGaus'    , action='store_true'  , help = 'add gaussian to alternate signal model failing probe')
parser.add_argument('--altBkg'     , action='store_true'  , help = 'alternate background model fit')
parser.add_argument('--altSigBkg'  , action='store_true'  , help = 'alternate signal and background model fit')
parser.add_argument('--doFit'      , action='store_true'  , help = 'fit sample (sample should be defined in settings.py)')
parser.add_argument('--mcSig'      , action='store_true'  , help = 'fit MC nom [to init fit parama]')
parser.add_argument('--doPlot'     , action='store_true'  , help = 'plotting')
parser.add_argument('--sumUp'      , action='store_true'  , help = 'sum up efficiencies')
parser.add_argument('--iBin'       , dest = 'binNumber'   , type = int,  default=-1, help='bin number (to refit individual bin)')
parser.add_argument('--flag'       , default = None       , help ='WP to test')
parser.add_argument('settings'     , default = "egm_tnp_analysis"       , help = 'setting file [mandatory]')
parser.add_argument('--exportJson' , action='store_true', help='export scale factors JSON (schema_version=2)')


args = parser.parse_args()

print('===> settings %s <===' % args.settings)
tnpConf = None
_settings_arg = args.settings
# --- begin: robust settings loader (replace imp) ---
import importlib
import importlib.util

settings_source = None
try:
    # Prefer explicit file path if it exists (also accepts ending with .py)
    if _settings_arg.endswith('.py') and os.path.isfile(_settings_arg):
        spec = importlib.util.spec_from_file_location('tnpConf', _settings_arg)
        if spec is None or spec.loader is None:
            raise ImportError('Could not create spec for settings file: %s' % _settings_arg)
        tnpConf = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tnpConf)
        settings_source = getattr(tnpConf, '__file__', _settings_arg)
    else:
        # Treat input as module path (allow .py suffix or '/' separators)
        mod_path = _settings_arg[:-3] if _settings_arg.endswith('.py') else _settings_arg
        mod_path = mod_path.replace('/', '.')
        tnpConf = importlib.import_module(mod_path)
        settings_source = getattr(tnpConf, '__file__', 'module:' + mod_path)
    print('[tnpEGM_fitter] loaded settings module: %s' % settings_source)
except Exception as e:
    print('[tnpEGM_fitter] Failed to import settings: %s' % str(e))
    sys.exit(1)
# --- end: robust settings loader (replace imp) ---

### tnp library
CMSSW_BASE = os.getenv('CMSSW_BASE')
if CMSSW_BASE:
    _src = os.path.join(CMSSW_BASE, 'src')
    if _src not in sys.path:
        sys.path.insert(0, _src)

from egm_tnp_analysis.libPython import binUtils  as tnpBiner
from egm_tnp_analysis.libPython import rootUtils as tnpRoot


if args.flag is None:
    print('[tnpEGM_fitter] flag is MANDATORY, this is the working point as defined in the settings.py')
    sys.exit(0)
    
if not args.flag in tnpConf.flags.keys() :
    print('[tnpEGM_fitter] flag %s not found in flags definitions' % args.flag)
    print('  --> define in settings first')
    print('  In settings I found flags: ')
    print(tnpConf.flags.keys())
    sys.exit(1)

outputDirectory = '%s/%s/' % (tnpConf.baseOutDir,args.flag)

print('===>  Output directory: ')
print(outputDirectory)


####################################################################
##### Create (check) Bins
####################################################################
if args.checkBins:
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    for ib in range(len(tnpBins['bins'])):
        print(tnpBins['bins'][ib]['name'])
        print('  - cut: ',tnpBins['bins'][ib]['cut'])
    sys.exit(0)
    
if args.createBins:
    if os.path.exists( outputDirectory ):
            shutil.rmtree( outputDirectory )
    os.makedirs( outputDirectory )
    tnpBins = tnpBiner.createBins(tnpConf.biningDef,tnpConf.cutBase)
    tnpBiner.tuneCuts( tnpBins, tnpConf.additionalCuts )
    pickle.dump( tnpBins, open( '%s/bining.pkl'%(outputDirectory),'wb') )
    print('created dir: %s ' % outputDirectory)
    print('bining created successfully... ')
    print('Note than any additional call to createBins will overwrite directory %s' % outputDirectory)
    sys.exit(0)

tnpBins = pickle.load( open( '%s/bining.pkl'%(outputDirectory),'rb') )


####################################################################
##### Create Histograms
####################################################################
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'tree'     ,'%s/fitter_tree' % tnpConf.tnpTreeDir )
    setattr( sample, 'histFile' , '%s/%s_%s.root' % ( outputDirectory , sample.name, args.flag ) )


if args.createHists:

    print(" ======== Creating Histograms ========")
    try:
        from egm_tnp_analysis.libPython import histUtils as tnpHist
    except Exception as e_first:
        print('[tnpEGM_fitter] histUtils import failed: %s' % str(e_first))
        _pkg_dir = os.path.dirname(__file__)
        _builder = os.path.join(_pkg_dir, 'tools', 'build_histutils.sh')
        if os.path.exists(_builder):
            import subprocess as _sp
            print('[tnpEGM_fitter] trying on-demand build via: %s' % _builder)
            try:
                _sp.check_call(['bash', _builder], cwd=_pkg_dir)
            except _sp.CalledProcessError as _be:
                print('[tnpEGM_fitter] build script failed (rc=%s), will retry import anyway' % _be.returncode)
        else:
            print('[tnpEGM_fitter] build script not found at %s' % _builder)
        try:
            import glob, importlib.util as _il_util
            from importlib import machinery as _il_mach
            _lib_dir = os.path.join(_pkg_dir, 'libPython')
            _cands = sorted(glob.glob(os.path.join(_lib_dir, 'histUtils*.so')))
            if not _cands:
                raise ImportError('no histUtils*.so found under %s' % _lib_dir)
            _so_path = _cands[-1]
            _loader = _il_mach.ExtensionFileLoader('egm_tnp_analysis.libPython.histUtils', _so_path)
            _spec = _il_util.spec_from_file_location('egm_tnp_analysis.libPython.histUtils', _so_path, loader=_loader)
            tnpHist = _il_util.module_from_spec(_spec)
            _spec.loader.exec_module(tnpHist)
        except Exception as e_second:
            try:
                import glob, importlib.util as _il_util
                from importlib import machinery as _il_mach
                _lib_dir = os.path.join(_pkg_dir, 'libPython')
                _cands = sorted(glob.glob(os.path.join(_lib_dir, 'histUtils*.so')))
                if not _cands:
                    raise ImportError('no histUtils*.so found under %s' % _lib_dir)
                _so_path = _cands[-1]
                _loader = _il_mach.ExtensionFileLoader('histUtils', _so_path)
                _spec = _il_util.spec_from_file_location('histUtils', _so_path, loader=_loader)
                tnpHist = _il_util.module_from_spec(_spec)
                _spec.loader.exec_module(tnpHist)
                sys.modules['egm_tnp_analysis.libPython.histUtils'] = tnpHist
                print('[tnpEGM_fitter] loaded histUtils as top-level module and aliased into egm_tnp_analysis.libPython.histUtils')
            except Exception as e_third:
                print('[tnpEGM_fitter] histUtils still not importable after build: %s' % str(e_third))
                print('  -> Hint: 確認已在正確的 CMSSW/ROOT 環境下，亦可手動執行: tools/build_histutils.sh')
                sys.exit(1)

    def _ensure_str(v):
        if isinstance(v, bytes):
            return v.decode('utf-8', errors='ignore')
        return v
    def _ensure_bytes(v):
        if isinstance(v, str):
            return v.encode('utf-8', errors='ignore')
        return v

    class _SampleProxy:
        def __init__(self, obj, str_attrs=('tnpTree', 'name', 'path', 'histFile', 'puTree', 'weight', 'cut'),
                           bytes_attrs=('tree',)):
            self.__obj = obj
            self.__str_attrs = set(str_attrs)
            self.__bytes_attrs = set(bytes_attrs)
        def __getattr__(self, name):
            v = getattr(self.__obj, name)
            if name in self.__bytes_attrs:
                if isinstance(v, (list, tuple)):
                    return [ _ensure_bytes(x) for x in v ]
                return _ensure_bytes(v)
            if name in self.__str_attrs:
                if isinstance(v, (list, tuple)):
                    return [ _ensure_str(x) for x in v ]
                return _ensure_str(v)
            return v
        def __repr__(self):
            return "<SampleProxy of %r>" % (self.__obj,)

    def parallel_hists(sampleType):
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : return
        if sampleType == args.sample or args.sample == 'all' :
            print('creating histogram for sample ')
            sample.dump()
            var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            if sample.mcTruth:
                var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }


            sample_p = _SampleProxy(sample)
            var_t = dict(var)
            var_t['name'] = _ensure_str(var_t.get('name'))

            try:
                tnpHist.makePassFailHistograms(sample_p, tnpConf.flags[args.flag], tnpBins, var_t)
            except TypeError as te:
                print('[tnpEGM_fitter] makePassFailHistograms TypeError: %s' % te)
                print('  -> Check sample.tree whether bytes, and histUtils*.so whether need to be make again。')
                raise
    
    for k in tnpConf.samplesDef.keys(): parallel_hists(k)

    sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################
sampleToFit = tnpConf.samplesDef['data']
sampleMC = tnpConf.samplesDef.get('mcNom', None)

if args.fitSample is not None:
    # --fitSample should choose the actual sample being fitted
    sampleToFit = tnpConf.samplesDef[args.fitSample]
    # data fits still need an MC reference for line-shape templates
    if args.fitSample == 'data':
        sampleMC = tnpConf.samplesDef.get('mcNom', None)
    else:
        sampleMC = sampleToFit
elif args.mcSig:
    sampleToFit = tnpConf.samplesDef['mcNom']
    sampleMC = sampleToFit

if sampleMC is None:
    print('[tnpEGM_fitter, prelim checks]: MC sample not available... check your settings')
    sys.exit(1)
for s in tnpConf.samplesDef.keys():
    sample =  tnpConf.samplesDef[s]
    if sample is None: continue
    setattr( sample, 'mcRef'     , sampleMC )
    setattr( sample, 'nominalFit', '%s/%s_%s.nominalFit.root' % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altSigFit' , '%s/%s_%s.altSigFit.root'  % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altBkgFit' , '%s/%s_%s.altBkgFit.root'  % ( outputDirectory , sample.name, args.flag ) )
    setattr( sample, 'altSigBkgFit' , '%s/%s_%s.altSigBkgFit.root'  % ( outputDirectory , sample.name, args.flag ) )

if  args.doFit:
    print(" ======== Fitting ========")
    sampleToFit.dump()
    def parallel_fit(ib):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            if args.altSig and not args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit )
            elif args.altSig and args.addGaus:
                tnpRoot.histFitterAltSig(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigFit_addGaus, 1)
            elif args.altBkg:
                tnpRoot.histFitterAltBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltBkgFit )
            elif args.altSigBkg:
                tnpRoot.histFitterAltSigBkg(  sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParAltSigBkgFit )
            else:
                tnpRoot.histFitterNominal( sampleToFit, tnpBins['bins'][ib], tnpConf.tnpParNomFit )
    pool = Pool()
    pool.map(parallel_fit, range(len(tnpBins['bins'])))

    args.doPlot = True
     
####################################################################
##### dumping plots
####################################################################
if  args.doPlot:
    fileName = sampleToFit.nominalFit
    fitType  = 'nominalFit'
    if args.altSig : 
        fileName = sampleToFit.altSigFit
        fitType  = 'altSigFit'
    if args.altBkg : 
        fileName = sampleToFit.altBkgFit
        fitType  = 'altBkgFit'
    if args.altSigBkg : 
        fileName = sampleToFit.altSigBkgFit
        fitType  = 'altSigBkgFit'
        
    os.system('hadd -f %s %s' % (fileName, fileName.replace('.root', '-*.root')))

    plottingDir = '%s/plots/%s/%s' % (outputDirectory,sampleToFit.name,fitType)
    if not os.path.exists( plottingDir ):
        os.makedirs( plottingDir )
    _pkg_dir = os.path.dirname(__file__)
    shutil.copy(os.path.join(_pkg_dir, 'etc', 'inputs', 'index.php.listPlots'),
                os.path.join(plottingDir, 'index.php'))

    for ib in range(len(tnpBins['bins'])):
        if (args.binNumber >= 0 and ib == args.binNumber) or args.binNumber < 0:
            tnpRoot.histPlotter( fileName, tnpBins['bins'][ib], plottingDir )

    print(' ===> Plots saved in <=======')
    pool.close()
    pool.join()
#    print 'localhost/%s/' % plottingDir


####################################################################
##### dumping egamma txt file 
####################################################################
if args.sumUp:
    sampleToFit.dump()
    info = {
        'data'        : sampleToFit.histFile,
        'dataNominal' : sampleToFit.nominalFit,
        'dataAltSig'  : sampleToFit.altSigFit ,
        'dataAltBkg'  : sampleToFit.altBkgFit ,
        'dataAltSigBkg'  : sampleToFit.altSigBkgFit ,
        'mcNominal'   : sampleToFit.mcRef.histFile,
        'mcAlt'       : None,
        'tagSel'      : None
        }

    if not tnpConf.samplesDef['mcAlt' ] is None:
       info['mcAlt'    ] = tnpConf.samplesDef['mcAlt' ].histFile
    # if not tnpConf.samplesDef['tagSel'] is None:
    #     info['tagSel'   ] = tnpConf.samplesDef['tagSel'].histFile

    effis = None
    flag = args.flag

    is_lowpt = "lowpt" in flag
    is_postBPixHole = "2023postBPixHole" in flag

    if is_postBPixHole and is_lowpt:
        effFileName = f"{outputDirectory}/egammaLowptEffi_postBPixHole.txt"

    elif is_postBPixHole and not is_lowpt:
        effFileName = f"{outputDirectory}/egammaEffi_postBPixHole.txt"

    elif not is_postBPixHole and is_lowpt:
        effFileName = f"{outputDirectory}/egammaLowptEffi.txt"

    else:
        effFileName = f"{outputDirectory}/egammaEffi.txt"

    fOut = open( effFileName,'w')
    
    # 用來組合 JSON 的暫存
    _binTuples = []          # (v1_low,v1_high,v2_low,v2_high)
    _sf_pass   = []
    _unc_pass  = []
    _sf_fail   = []
    _unc_fail  = []
    _var1_name = None
    _var2_name = None

    for ib in range(len(tnpBins['bins'])):
        effis = tnpRoot.getAllEffi( info, tnpBins['bins'][ib] )

        ### formatting assuming 2D bining -- to be fixed        
        v1Range = tnpBins['bins'][ib]['title'].split(';')[1].split('<')
        v2Range = tnpBins['bins'][ib]['title'].split(';')[2].split('<')
        if ib == 0 :
            astr = '### var1 : %s' % v1Range[1]
            print(astr)
            fOut.write( astr + '\n' )
            astr = '### var2 : %s' % v2Range[1]
            print(astr)
            fOut.write( astr + '\n' )
            
        astr =  '%+8.5f\t%+8.5f\t%+8.5f\t%+8.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f\t%5.5f' % (
            float(v1Range[0]), float(v1Range[2]),
            float(v2Range[0]), float(v2Range[2]),
            effis['dataNominal'][0],effis['dataNominal'][1],
            effis['mcNominal'  ][0],effis['mcNominal'  ][1],
            effis['dataAltBkg' ][0],
            effis['dataAltSig' ][0],
            effis['mcAlt' ][0],
            # effis['tagSel'][0],
            effis['dataAltSigBkg' ][0],
            )
        print(astr)
        fOut.write( astr + '\n' )

        # 取得變數名稱 (首次)
        if _var1_name is None: _var1_name = v1Range[1] if len(v1Range) > 1 else 'var1'
        if _var2_name is None: _var2_name = v2Range[1] if len(v2Range) > 1 else 'var2'
        # 正規化變數命名（映射 ph_et -> pt；ph_sc_eta -> eta）
        if _var1_name is not None:
            _var1_name = _var1_name.strip()
            if _var1_name == 'ph_sc_eta':
                _var1_name = 'eta'
        if _var2_name is not None:
            _var2_name = _var2_name.strip()
            if _var2_name == 'ph_et':
                _var2_name = 'pt'
        # 效率與不確定度
        eff_data, unc_data = effis['dataNominal'][0], effis['dataNominal'][1]
        eff_mc  , unc_mc   = effis['mcNominal'  ][0], effis['mcNominal'  ][1]
        # 保護除以零
        if eff_mc <= 0: 
            sf_pass = 1.0
            unc_pass = 0.0
        else:
            sf_pass = eff_data / eff_mc
            # 誤差傳播: f = A/B
            unc_pass = math.sqrt( (unc_data/eff_mc)**2 + (eff_data*unc_mc/(eff_mc**2))**2 )
        # Fail 區 (互補)
        eff_data_fail = 1.0 - eff_data
        eff_mc_fail   = 1.0 - eff_mc
        if eff_mc_fail <= 0:
            sf_fail = 1.0
            unc_fail = 0.0
        else:
            sf_fail = eff_data_fail / eff_mc_fail
            # f = (1-A)/(1-B) -> 對 A, B 的偏微分做近似 (線性誤差傳播)
            # df/dA = -1/(1-B), df/dB = (1-A)/(1-B)^2
            dfdA = -1.0 / max(1e-12, (1 - eff_mc))
            dfdB = (1 - eff_data) / max(1e-12, (1 - eff_mc)**2)
            unc_fail = math.sqrt( (dfdA * unc_data)**2 + (dfdB * unc_mc)**2 )
        _sf_pass.append(sf_pass)
        _unc_pass.append(unc_pass)
        _sf_fail.append(sf_fail)
        _unc_fail.append(unc_fail)
        _binTuples.append( (float(v1Range[0]), float(v1Range[2]), float(v2Range[0]), float(v2Range[2])) )

    fOut.close()

    print('Effis saved in file : ',  effFileName)
    # 同樣加入回退匯入，避免 PyROOT 攔截
    try:
        from egm_tnp_analysis.libPython import EGammaID_scaleFactors as egm_sf
    except Exception:
        import importlib.util as _il_util
        _pkg_dir = os.path.dirname(__file__)
        _sf_path = os.path.join(_pkg_dir, 'libPython', 'EGammaID_scaleFactors.py')
        _spec = _il_util.spec_from_file_location('egm_tnp_analysis.libPython.EGammaID_scaleFactors', _sf_path)
        egm_sf = _il_util.module_from_spec(_spec)
        _spec.loader.exec_module(egm_sf)
    egm_sf.doEGM_SFs(effFileName,sampleToFit.lumi)

    if args.exportJson:
        # 邊界重建
        edges1_lows = sorted({b[0] for b in _binTuples})
        edges2_lows = sorted({b[2] for b in _binTuples})
        last_high1 = max(b[1] for b in _binTuples)
        last_high2 = max(b[3] for b in _binTuples)
        edges1 = edges1_lows + ([last_high1] if edges1_lows[-1] != last_high1 else [])
        edges2 = edges2_lows + ([last_high2] if edges2_lows[-1] != last_high2 else [])
        out_json = {
            "schema_version": 2,
            "description": "auto-generated scale factors",
            "corrections": [
                {
                    "name": "sf_pass",
                    "version": 1,
                    "inputs": [
                        {"name": _var1_name, "type": "real", "description": _var1_name},
                        {"name": _var2_name, "type": "real", "description": _var2_name}
                    ],
                    "output": {"name": "sf", "type": "real", "description": "data/MC scale factor (pass)"},
                    "data": {
                        "nodetype": "multibinning",
                        "inputs": [_var1_name, _var2_name],
                        "edges": [edges1, edges2],
                        "content": _sf_pass,
                        "flow": "clamp"
                    }
                },
                {
                    "name": "unc_pass",
                    "version": 1,
                    "inputs": [
                        {"name": _var1_name, "type": "real", "description": _var1_name},
                        {"name": _var2_name, "type": "real", "description": _var2_name}
                    ],
                    "output": {"name": "sf", "type": "real", "description": "uncertainty (pass)"},
                    "data": {
                        "nodetype": "multibinning",
                        "inputs": [_var1_name, _var2_name],
                        "edges": [edges1, edges2],
                        "content": _unc_pass,
                        "flow": "clamp"
                    }
                },
                {
                    "name": "sf_fail",
                    "version": 1,
                    "inputs": [
                        {"name": _var1_name, "type": "real", "description": _var1_name},
                        {"name": _var2_name, "type": "real", "description": _var2_name}
                    ],
                    "output": {"name": "sf", "type": "real", "description": "data/MC scale factor (fail)"},
                    "data": {
                        "nodetype": "multibinning",
                        "inputs": [_var1_name, _var2_name],
                        "edges": [edges1, edges2],
                        "content": _sf_fail,
                        "flow": "clamp"
                    }
                },
                {
                    "name": "unc_fail",
                    "version": 1,
                    "inputs": [
                        {"name": _var1_name, "type": "real", "description": _var1_name},
                        {"name": _var2_name, "type": "real", "description": _var2_name}
                    ],
                    "output": {"name": "sf", "type": "real", "description": "uncertainty (fail)"},
                    "data": {
                        "nodetype": "multibinning",
                        "inputs": [_var1_name, _var2_name],
                        "edges": [edges1, edges2],
                        "content": _unc_fail,
                        "flow": "clamp"
                    }
                }
            ]
        }
        _json_path = os.path.join(outputDirectory, f'{args.flag}.json')
        with open(_json_path, 'w') as jf:
            json.dump(out_json, jf, indent=2)
        print('[exportJson] JSON written:', _json_path)
