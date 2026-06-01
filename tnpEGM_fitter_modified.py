# -*- coding: utf-8 -*-
### python specific import
import argparse
import os
import sys
import pickle
import shutil
from multiprocessing import Pool


parser = argparse.ArgumentParser(description='tnp EGM fitter')
parser.add_argument('--checkBins'  , action='store_true'  , help = 'check  bining definition')
parser.add_argument('--createBins' , action='store_true'  , help = 'create bining definition')
parser.add_argument('--createHists', action='store_true'  , help = 'create histograms')
parser.add_argument('--sample'     , default='all'        , help = 'create histograms (per sample, expert only)')
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
    # 先嘗試正常匯入；若失敗就動態建置 C++ 擴充並重試
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
        # 第二段回退：直接以絕對路徑載入 .so（包路徑）
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
            # 第三段回退：以頂層模組名載入，並註冊別名到封包路徑，繞過 PyROOT import hook 的干擾
            try:
                import importlib.util as _il_util
                from importlib import machinery as _il_mach
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

    # 只在必要屬性上做 bytes 轉換（其餘維持 str）
    def _to_bytes_if_str(v):
        return v.encode('utf-8') if isinstance(v, str) else v

    class _BytesProxy:
        """僅對指定屬性在取用時轉為 bytes，其他維持原樣。"""
        def __init__(self, obj, attrs=('tnpTree','tree')):
            self.__obj = obj
            self.__attrs = set(attrs)
        def __getattr__(self, name):
            v = getattr(self.__obj, name)
            if name in self.__attrs:
                return _to_bytes_if_str(v)
            return v
        def __repr__(self):
            return "<BytesProxy of %r>" % (self.__obj,)

    def parallel_hists(sampleType):
        sample =  tnpConf.samplesDef[sampleType]
        if sample is None : return
        if sampleType == args.sample or args.sample == 'all' :
            print('creating histogram for sample ')
            sample.dump()
            var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            if sample.mcTruth:
                var = { 'name' : 'pair_mass', 'nbins' : 80, 'min' : 50, 'max': 130 }
            # 僅代理 sample 的 tnpTree、tree -> bytes；其餘參數保持為 str
            sample_b = _BytesProxy(sample, attrs=('tnpTree','tree'))
            tnpHist.makePassFailHistograms(sample_b, tnpConf.flags[args.flag], tnpBins, var)
    
    for k in tnpConf.samplesDef.keys(): parallel_hists(k)

    sys.exit(0)


####################################################################
##### Actual Fitter
####################################################################
sampleToFit = tnpConf.samplesDef['data']
if sampleToFit is None:
    print('[tnpEGM_fitter, prelim checks]: sample (data or MC) not available... check your settings')
    sys.exit(1)

sampleMC = tnpConf.samplesDef['mcNom']

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



### change the sample to fit is mc fit
if args.mcSig :
    sampleToFit = tnpConf.samplesDef['mcNom']

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
    effFileName ='%s/egammaEffi.txt' % outputDirectory 
    fOut = open( effFileName,'w')
    
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
