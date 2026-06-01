#!/usr/bin/env python

import sys,os
# sys.path.append('/afs/cern.ch/work/p/pelai/HZa/TnP/CMSSW_11_2_0/src/egm_tnp_analysis/libPython')
sys.path.append('/eos/home-l/lyifan/learning/cmsdas__hefei/TnP/CMSSW_11_2_0/src/egm_tnp_analysis/libPython')
from math import sqrt
import ROOT as rt
import CMS_lumi, tdrstyle

from efficiencyUtils import efficiency
from efficiencyUtils import efficiencyList
import efficiencyUtils as effUtil

tdrstyle.setTDRStyle()


effiMin = 0.68
effiMax = 1.07


sfMin = 0.78
sfMax = 1.12


def isFloat( myFloat ):
    try:
        float(myFloat)
        return True
    except:
        return False



graphColors = [rt.kBlack, rt.kGray+1, rt.kRed +1, rt.kRed-2, rt.kAzure+2, rt.kAzure-1, 
               rt.kSpring-1, rt.kYellow -2 , rt.kYellow+1,
               rt.kBlack, rt.kBlack, rt.kBlack, 
               rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack, rt.kBlack ]




def findMinMax( effis ):
    mini = +999
    maxi = -999

    for key in effis.keys():
        for eff in effis[key]:
            if eff['val'] - eff['err'] < mini:
                mini = eff['val'] - eff['err']
            if eff['val'] + eff['err'] > maxi:
                maxi = eff['val'] + eff['err']

    if mini > 0.18 and mini < 0.28:
        mini = 0.18
    if mini > 0.28 and mini < 0.38:
        mini = 0.28
    if mini > 0.38 and mini < 0.48:
        mini = 0.38
    if mini > 0.48 and mini < 0.58:
        mini = 0.48
    if mini > 0.58 and mini < 0.68:
        mini = 0.58
    if mini > 0.68 and mini < 0.78:
        mini = 0.68
    if mini > 0.78 and mini < 0.88:
        mini = 0.78
    if mini > 0.88:
        mini = 0.88
    if mini > 0.92:
        mini = 0.92

        
    if  maxi > 0.95:
        maxi = 1.17        
    elif maxi < 0.87:
        maxi = 0.87
    else:
        maxi = 1.07

    if maxi-mini > 0.5:
        maxi = maxi + 0.2
        
    return (mini,maxi)
    

def EffiGraph1D(effDataList, effMCList, sfList ,nameout, xAxis = 'pT', yAxis = 'eta'):
            
    W = 800
    H = 800
    yUp = 0.45
    canName = 'toto' + xAxis

    c = rt.TCanvas(canName,canName,50,50,H,W)
    c.SetTopMargin(0.055)
    c.SetBottomMargin(0.13)
    c.SetLeftMargin(0.15)
    
    
    p1 = rt.TPad( canName + '_up', canName + '_up', 0, yUp, 1,   1, 0,0,0)
    p2 = rt.TPad( canName + '_do', canName + '_do', 0,   0, 1, yUp, 0,0,0)
    p1.SetBottomMargin(0.0077)
    p1.SetTopMargin(   c.GetTopMargin()*1/(1-yUp))
    p2.SetTopMargin(   0.0077)
    p2.SetBottomMargin( c.GetBottomMargin()*1/yUp)
    p1.SetLeftMargin( c.GetLeftMargin() )
    p2.SetLeftMargin( c.GetLeftMargin() )
    p1.SetTicks(1, 1)
    p2.SetTicks(1, 1)
    firstGraph = True

    p1.cd()

    def _chooseLegendCoords(effDataList, xAxis):
        nkeys = len(effDataList)
        if 'pT' in xAxis or 'pt' in xAxis:
            if nkeys == 3:
                return (0.51, 0.80, 0.94, 0.92)
            elif nkeys == 2:
                return (0.51, 0.84, 0.94, 0.92)
            elif nkeys == 1:
                return (0.51, 0.88, 0.94, 0.92)
            else:
                return (0.51, 0.74, 0.94, 0.92)
        elif 'eta' in xAxis or 'Eta' in xAxis:
            if nkeys == 1:
                return (0.53, 0.88, 0.94, 0.92)
            else:
                return (0.53, 0.80, 0.94, 0.92)
        # fallback
        return (0.51, 0.80, 0.94, 0.92)

    legx1, legy1, legx2, legy2 = _chooseLegendCoords(effDataList, xAxis)
    leg = rt.TLegend(legx1, legy1, legx2, legy2)
    print("Legend coords (NDC):", legx1, legy1, legx2, legy2)

    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.035)


    legStyle = rt.TLegend(0.35,0.84,0.73,0.92)
    legStyle.SetBorderSize(0)
    legStyle.SetFillStyle(0)
    legStyle.SetTextSize(0.035)
    lineData = rt.TLine(0, 0, 1, 0)
    lineData.SetLineColor(rt.kBlack)
    lineData.SetLineWidth(2)
    lineData.SetLineStyle(rt.kSolid)
    lineMC = rt.TLine(0, 0, 1, 0)
    lineMC.SetLineColor(rt.kBlack)
    lineMC.SetLineWidth(2)
    lineMC.SetLineStyle(rt.kDashed)
    legStyle.AddEntry(lineData, "Data", "L")
    legStyle.AddEntry(lineMC, "MC", "L")

    dummyLines = [lineData, lineMC]

    igr = 0
    listOfTGraph1 = []
    listOfTGraph2 = []
    listOfMC      = []

    xMin = 10
    xMax = 200
    if 'pT' in xAxis or 'pt' in xAxis:
        # p1.SetLogx()
        # p2.SetLogx()    
        xMin = 10
        xMax = 80
    elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
        xMin =  3
        xMax = 42
    elif 'eta' in xAxis or 'Eta' in xAxis:
        xMin = -2.60
        xMax = +2.60
    
    if 'abs' in xAxis or 'Abs' in xAxis:
        xMin = 0.0

    effminmax =  findMinMax( effDataList )
    effiMin = effminmax[0]
    effiMax = effminmax[1]
    effiMin = 0.10 
    effiMax = 1.55

    sfminmax =  findMinMax( sfList )
    sfMin = sfminmax[0]
    sfMax = sfminmax[1]
    sfMin = 0.45
    sfMax = 1.45


    for key in sorted(effDataList.keys()):
            
        nData = len(effDataList.get(key, []))
        nSF   = len(sfList.get(key, []))
        nMC   = len(effMCList.get(key, [])) if effMCList is not None else -1
        print("key:", key, "nData:", nData, "nSF:", nSF, "nMC:", nMC)


        if nData == 0 or nSF == 0:
            print(f"[WARN] Empty bin for key={key}: nData={nData}, nSF={nSF} (skip)")
            continue
        
        grBinsEffData = effUtil.makeTGraphFromList(effDataList[key], 'min', 'max')
        grBinsSF      = effUtil.makeTGraphFromList(sfList[key]     , 'min', 'max')


        if grBinsEffData is None or grBinsEffData.GetN() == 0:
            print(f"[WARN] Empty Data graph for key={key} (skip)")
            continue
        if grBinsSF is None or grBinsSF.GetN() == 0:
            print(f"[WARN] Empty SF graph for key={key} (skip)")
            continue

        grBinsEffMC = None
        if not effMCList is None:
            grBinsEffMC = effUtil.makeTGraphFromList(effMCList[key], 'min', 'max')
            if grBinsEffMC is None or grBinsEffMC.GetN() == 0:
                print(f"[WARN] Empty MC graph for key={key} (set to None)")
                grBinsEffMC = None

        if not effMCList is None:
            grBinsEffMC = effUtil.makeTGraphFromList(effMCList[key], 'min', 'max')
            grBinsEffMC.SetLineStyle( rt.kDashed )
            grBinsEffMC.SetLineColor( graphColors[igr] )
            grBinsEffMC.SetMarkerSize( 0 )
            grBinsEffMC.SetLineWidth( 2 )

        grBinsSF     .SetMarkerColor( graphColors[igr] )
        grBinsSF     .SetLineColor(   graphColors[igr] )
        grBinsSF     .SetLineWidth(2)
        grBinsEffData.SetMarkerColor( graphColors[igr] )
        grBinsEffData.SetLineColor(   graphColors[igr] )
        grBinsEffData.SetLineWidth(2) 
                
        grBinsEffData.GetHistogram().SetMinimum(effiMin)
        grBinsEffData.GetHistogram().SetMaximum(effiMax)

        grBinsEffData.GetHistogram().GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram()     .GetXaxis().SetLimits(xMin,xMax)
        grBinsSF.GetHistogram().SetMinimum(sfMin)
        grBinsSF.GetHistogram().SetMaximum(sfMax)
        
        grBinsSF.GetHistogram().GetXaxis().SetTitleOffset(1)
        if 'eta' in xAxis or 'Eta' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("SuperCluster #eta")
        elif 'pt' in xAxis or 'pT' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("p_{T}  [GeV]")  
        elif 'vtx' in xAxis or 'Vtx' in xAxis or 'PV' in xAxis:
            grBinsSF.GetHistogram().GetXaxis().SetTitle("N_{vtx}")  
            
        grBinsSF.GetHistogram().GetYaxis().SetTitle("Data / MC " )

        grBinsEffData.GetHistogram().GetYaxis().SetTitleOffset(1)
        grBinsEffData.GetHistogram().GetYaxis().SetTitle("Efficiency" )
        grBinsEffData.GetHistogram().GetYaxis().SetRangeUser( effiMin, effiMax )

            
        ### to avoid loosing the TGraph keep it in memory by adding it to a list
        listOfTGraph1.append( grBinsEffData )
        listOfTGraph2.append( grBinsSF ) 
        listOfMC.append( grBinsEffMC   )
        if 'eta' in yAxis or 'Eta' in yAxis:
            leg.AddEntry( grBinsEffData, '%1.3f #leq | #eta | #leq  %1.3f' % (float(key[0]),float(key[1])), "PL")        
        elif 'pt' in yAxis or 'pT' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq p_{T} #leq  %3.0f GeV' % (float(key[0]),float(key[1])), "PL")        
        elif 'vtx' in yAxis or 'Vtx' in yAxis or 'PV' in yAxis:
            leg.AddEntry( grBinsEffData, '%3.0f #leq nVtx #leq  %3.0f'      % (float(key[0]),float(key[1])), "PL")        
    

    if len(listOfTGraph1) == 0:
        print("[ERROR] No valid graphs to draw (all bins empty).")
        return []


    for igr in range(len(listOfTGraph1)):
        option = "AP" if igr == 0 else "P"
        use_igr = igr
        
        if use_igr == len(listOfTGraph1):
            use_igr = 0
            
        listOfTGraph1[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph1[use_igr].SetMarkerColor(graphColors[use_igr])
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].SetLineColor(graphColors[use_igr])

        listOfTGraph1[use_igr].GetHistogram().SetMinimum(effiMin)
        listOfTGraph1[use_igr].GetHistogram().SetMaximum(effiMax)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetTitleFont(42)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetLabelFont(42)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetTitleSize(0.085)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetLabelSize(0.08)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetTitleOffset(0.9)
        listOfTGraph1[use_igr].GetHistogram().GetYaxis().SetNdivisions(809)
        p1.cd()
        listOfTGraph1[use_igr].Draw(option)
        if not listOfMC[use_igr] is None:
            listOfMC[use_igr].Draw("ez")

        p2.cd()            
        listOfTGraph2[use_igr].SetLineColor(graphColors[use_igr])
        listOfTGraph2[use_igr].SetMarkerColor(graphColors[use_igr])
        listOfTGraph2[use_igr].GetHistogram().SetMinimum(sfMin)
        listOfTGraph2[use_igr].GetHistogram().SetMaximum(sfMax)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleFont(42)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetLabelFont(42)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleSize(0.105)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetLabelSize(0.1)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetTitleOffset(0.75)
        listOfTGraph2[use_igr].GetHistogram().GetYaxis().SetNdivisions(506)

        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleFont(42)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetLabelFont(42)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleSize(0.105)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetLabelSize(0.1)
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetTitleOffset(1.2)

        if 'pT' in xAxis or 'pt' in xAxis :
            listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetMoreLogLabels()
        listOfTGraph2[use_igr].GetHistogram().GetXaxis().SetNoExponent()
        listOfTGraph2[use_igr].Draw(option)
        

    lineAtOne = rt.TLine(xMin,1,xMax,1)
    lineAtOne.SetLineStyle(rt.kDashed)
    lineAtOne.SetLineWidth(2)
    
    p2.cd()
    lineAtOne.Draw()

    c.cd()
    p2.Draw()
    p1.Draw()

    leg.Draw()    
    legStyle.Draw()
    CMS_lumi.CMS_lumi(c, 5, 10)

    c.Print(nameout)
    listName = nameout.split('/')
    # for iext in ["pdf","C","png"]:
    for iext in ["pdf","png"]:
        tmp = nameout
        tmp = tmp.replace('egammaLowptEffi_postBPixHole.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SFvs'+xAxis+'_'+listName[-3])
        tmp = tmp.replace('egammaEffi_postBPixHole.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SFvs'+xAxis+'_'+listName[-3])
        tmp = tmp.replace('egammaLowptEffi.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SFvs'+xAxis+'_'+listName[-3])
        tmp = tmp.replace('egammaEffi.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SFvs'+xAxis+'_'+listName[-3])

        c.SaveAs(tmp.replace('pdf', iext))
        # c.SaveAs(nameout.replace('egammaEffi.txt_egammaPlots',listName[-6].replace('tnp','')+'_SFvs'+xAxis+'_'+listName[-3]).replace('pdf',iext))

    return listOfTGraph2

    #################################################    


def diagnosticErrorPlot( effgr, ierror, nameout ):
    errorNames = efficiency.getSystematicNames()
    c2D_Err = rt.TCanvas('canScaleFactor_%s' % errorNames[ierror] ,'canScaleFactor: %s' % errorNames[ierror],1000,600)    
    c2D_Err.Divide(2,1)
    # c2D_Err.GetPad(1).SetLogy()
    # c2D_Err.GetPad(2).SetLogy()
    c2D_Err.GetPad(1).SetRightMargin(   0.18)
    c2D_Err.GetPad(1).SetLeftMargin(    0.16)
    c2D_Err.GetPad(1).SetTopMargin(     0.10)
    c2D_Err.GetPad(1).SetBottomMargin(  0.13)
    c2D_Err.GetPad(2).SetRightMargin(   0.16)
    c2D_Err.GetPad(2).SetLeftMargin(    0.16)
    c2D_Err.GetPad(2).SetTopMargin(     0.10)
    c2D_Err.GetPad(2).SetBottomMargin(  0.13)

    h2_sfErrorAbs = effgr.ptEtaScaleFactor_2DHisto(ierror+1, False )
    h2_sfErrorRel = effgr.ptEtaScaleFactor_2DHisto(ierror+1, True  )
    h2_sfErrorAbs.SetMinimum(0)
    h2_sfErrorAbs.SetMaximum(min(h2_sfErrorAbs.GetMaximum(),0.2))
    h2_sfErrorRel.SetMinimum(0)
    h2_sfErrorRel.SetMaximum(1)
    h2_sfErrorAbs.SetTitle('e/#gamma absolute SF syst: %s ' % errorNames[ierror])
    h2_sfErrorRel.SetTitle('e/#gamma relative SF syst: %s ' % errorNames[ierror])
    c2D_Err.cd(1)
    h2_sfErrorAbs.DrawCopy("colz TEXT45")
    c2D_Err.cd(2)
    h2_sfErrorRel.DrawCopy("colz TEXT45")
    
    c2D_Err.Print(nameout)

    listName = nameout.split('/')
    # for iext in ["pdf","C","png"]:
    for iext in ["pdf","png"]:
        tmp = nameout
        tmp = tmp.replace('egammaLowptEffi_postBPixHole.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+errorNames[ierror]+listName[-3])
        tmp = tmp.replace('egammaEffi_postBPixHole.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+errorNames[ierror]+listName[-3])
        tmp = tmp.replace('egammaLowptEffi.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+errorNames[ierror]+listName[-3])
        tmp = tmp.replace('egammaEffi.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+errorNames[ierror]+listName[-3])

        c2D_Err.SaveAs(tmp.replace('pdf', iext))
        # c2D_Err.SaveAs(nameout.replace('egammaEffi.txt_egammaPlots',listName[-6].replace('tnp','')+'_SF2D'+'_'+errorNames[ierror]+listName[-3]).replace('pdf',iext))
    
    return h2_sfErrorAbs

def doEGM_SFs(filein, lumi, axis = ['pT','eta'] ):
    print(" Opening file: %s (plot lumi: %3.1f)" % ( filein, lumi ))
    CMS_lumi.lumi_13TeV = "%+3.1f fb^{-1}" % lumi 

    nameOutBase = filein 
    if not os.path.exists( filein ) :
        print('file %s does not exist' % filein)
        sys.exit(1)


    fileWithEff = open(filein, 'r')
    effGraph = efficiencyList()
    
    for line in fileWithEff :
        modifiedLine = line.lstrip(' ').rstrip(' ').rstrip('\n')
        numbers = modifiedLine.split('\t')

        if len(numbers) > 0 and isFloat(numbers[0]):
            etaKey = ( float(numbers[0]), float(numbers[1]) )
            ptKey  = ( float(numbers[2]), min(500,float(numbers[3])) )
            myeff = efficiency(ptKey,etaKey,
                               float(numbers[4]),float(numbers[5]),float(numbers[6] ),float(numbers[7] ),
                               float(numbers[8]),float(numbers[9]),float(numbers[10]),float(numbers[11]) )
#                           float(numbers[8]),float(numbers[9]),float(numbers[10]), -1 )

            effGraph.addEfficiency(myeff)

    fileWithEff.close()
#   ## massage the numbers a bit
    # effGraph.symmetrizeSystVsEta()# ----- REMOVING SYMM ETA AS DISCUSSED WITH RICCARDO
    effGraph.combineSyst()


    _patched = 0
    try:
        _all_eff = getattr(effGraph, "efficiencies", None)
        if _all_eff is None:
            _all_eff = getattr(effGraph, "effList", None)
        if _all_eff is None:
            _all_eff = getattr(effGraph, "listOfEfficiencies", None)

        if _all_eff:
            for _eff in _all_eff:
                if not hasattr(_eff, "systCombined"):

                    _fallback = 0.0
                    if hasattr(_eff, "syst") and isinstance(getattr(_eff, "syst"), (int, float)):
                        _fallback = float(getattr(_eff, "syst"))
                    setattr(_eff, "systCombined", _fallback)
                    _patched += 1


                if not hasattr(_eff, "systTot"):
                    setattr(_eff, "systTot", getattr(_eff, "systCombined"))
                if not hasattr(_eff, "systTotal"):
                    setattr(_eff, "systTotal", getattr(_eff, "systCombined"))
    except Exception as _e:
        print("[WARN] Failed to patch missing systCombined fields:", _e)

    if _patched > 0:
        print(f"[WARN] Patched {_patched} efficiency object(s) missing systCombined (set to fallback).")

    print(" ------------------------------- ")

    customEtaBining = []

    if ("Lowpt" in filein) and ("Hole" in filein):
        customEtaBining.append((0.000, 1.444))

    elif "Lowpt" in filein:
        customEtaBining.append((0.000, 1.444))
        customEtaBining.append((1.566, 2.000))
        customEtaBining.append((2.000, 2.500))

    elif "Hole" in filein:
        customEtaBining.append((0.000, 0.800))
        customEtaBining.append((0.800, 1.444))

    else:
        customEtaBining.append((0.000, 0.800))
        customEtaBining.append((0.800, 1.444))
        customEtaBining.append((1.566, 2.000))
        customEtaBining.append((2.000, 2.500))

#    customEtaBining.append( (1.444,1.566)) #gap region
    # customEtaBining.append( (1.566,2.000))
    # customEtaBining.append( (2.000,2.500))
    #HZZ bins - can be deleted
    # customEtaBining.append( (0.000,0.500))
    # customEtaBining.append( (0.500,1.0))    
    # customEtaBining.append( (1.000,1.5))
    # customEtaBining.append( (1.5,2.000))
    # customEtaBining.append( (2.000,2.500))



    pdfout = nameOutBase + '_egammaPlots.pdf'
    cDummy = rt.TCanvas()
    cDummy.Print( pdfout + "[" )

    #---------------------------------------------------------------
    EffiGraph1D( effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, 0 ) ,  # Data
                 effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, -1 ) , # MC
                 effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, 1 ) ,  # SF
                 pdfout,
                 xAxis = axis[0], yAxis = axis[1] )
    #---------------------------------------------------------------
    # EffiGraph1D( effGraph.pt_1DGraph_list(typeGR=0),   # eff Data
    #              effGraph.pt_1DGraph_list(typeGR=-1),  # eff MC
    #              effGraph.pt_1DGraph_list(typeGR=+1),  # SF
    #              pdfout,
    #              xAxis = axis[0], yAxis = axis[1] )
    # EffiGraph1D( effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, 0 ) , # eff Data
    #              None,
    #              effGraph.pt_1DGraph_list_customEtaBining(customEtaBining, 1 ) , # SF
    #              pdfout,
    #              xAxis = axis[0], yAxis = axis[1] )
    #---------------------------------------------------------------
    # EffiGraph1D( effGraph.pt_1DGraph_list_customEtaBining(customEtaBining,False) , 
    #         effGraph.pt_1DGraph_list_customEtaBining(customEtaBining,True)   , False, pdfout )
    # EffiGraph1D( effGraph.eta_1DGraph_list(False), effGraph.eta_1DGraph_list(True), True , pdfout )
    listOfSF1D = EffiGraph1D( effGraph.eta_1DGraph_list( typeGR =  0 ) , # eff Data
                              effGraph.eta_1DGraph_list( typeGR = -1 ) , # eff MC
                              effGraph.eta_1DGraph_list( typeGR = +1 ) , # SF
                              pdfout, 
                              xAxis = axis[1], yAxis = axis[0] ) or []

    h2EffData = effGraph.ptEtaScaleFactor_2DHisto(-3)
    h2EffMC   = effGraph.ptEtaScaleFactor_2DHisto(-2)
    h2SF      = effGraph.ptEtaScaleFactor_2DHisto(-1)
    h2Error   = effGraph.ptEtaScaleFactor_2DHisto( 0)  ## only error bars

    rt.gStyle.SetPalette(1)
    rt.gStyle.SetPaintTextFormat('1.3f');
    rt.gStyle.SetOptTitle(1)

    c2D = rt.TCanvas('canScaleFactor','canScaleFactor',900,600)
    c2D.Divide(2,1)
    c2D.GetPad(1).SetRightMargin(   0.18)
    c2D.GetPad(1).SetLeftMargin(    0.16)
    c2D.GetPad(1).SetTopMargin(     0.10)
    c2D.GetPad(1).SetBottomMargin(  0.13)
    c2D.GetPad(2).SetRightMargin(   0.18)
    c2D.GetPad(2).SetLeftMargin(    0.16)
    c2D.GetPad(2).SetTopMargin(     0.10)
    c2D.GetPad(2).SetBottomMargin(  0.13)
    # c2D.GetPad(1).SetLogy()
    # c2D.GetPad(2).SetLogy()
    

    c2D.cd(1)
    dmin = 1.0 - h2SF.GetMinimum()
    dmax = h2SF.GetMaximum() - 1.0
    dall = max(dmin,dmax)
    h2SF.SetMinimum(1-dall)
    h2SF.SetMaximum(1+dall)
    h2SF.DrawCopy("colz TEXT45")
    
    c2D.cd(2)
    h2Error.SetMinimum(0)
    h2Error.SetMaximum(min(h2Error.GetMaximum(),0.2))    
    h2Error.DrawCopy("colz TEXT45")

    c2D.Print( pdfout )
    listName = pdfout.split('/')
    # for iext in ["pdf","C","png"]:
    for iext in ["pdf","png"]:
        tmp = pdfout
        tmp = tmp.replace('egammaLowptEffi_postBPixHole.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+listName[-3])
        tmp = tmp.replace('egammaEffi_postBPixHole.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+listName[-3])
        tmp = tmp.replace('egammaLowptEffi.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+listName[-3])
        tmp = tmp.replace('egammaEffi.txt_egammaPlots', 
                        listName[-6].replace('tnp','')+'_SF2D'+'_'+listName[-3])

        c2D.SaveAs(tmp.replace('pdf', iext))
        # c2D.SaveAs(pdfout.replace('egammaEffi.txt_egammaPlots',listName[-6].replace('tnp','')+'_SF2D'+'_'+listName[-3]).replace('pdf',iext))

    rootout = rt.TFile(nameOutBase + '_EGM2D.root','recreate')
    rootout.cd()
    h2SF.Write('EGamma_SF2D',rt.TObject.kOverwrite)
    h2EffData.Write('EGamma_EffData2D',rt.TObject.kOverwrite)
    h2EffMC  .Write('EGamma_EffMC2D'  ,rt.TObject.kOverwrite)
    for igr in range(len(listOfSF1D)):
        listOfSF1D[igr].Write( 'grSF1D_%d' % igr, rt.TObject.kOverwrite)


    errorNames = efficiency.getSystematicNames()
    for isyst in range(len(errorNames)):
        h2_isyst = diagnosticErrorPlot( effGraph, isyst, pdfout )
        h2_isyst.Write( errorNames[isyst],rt.TObject.kOverwrite)
    cDummy.Print( pdfout + "]" )
    rootout.Close()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='tnp EGM scale factors')
    parser.add_argument('--lumi'  , type = float, default = -1, help = 'Lumi (just for plotting purpose)')
    parser.add_argument('txtFile' , default = None, help = 'EGM formatted txt file')
    parser.add_argument('--PV'    , action  = 'store_true', help = 'plot 1 vs nVtx instead of pT' )
    args = parser.parse_args()

    if args.txtFile is None:
        print(' - Needs EGM txt file as input')
        sys.exit(1)
    

    CMS_lumi.lumi_13TeV = "5.5 fb^{-1}"
    CMS_lumi.writeExtraText = 1
    CMS_lumi.lumi_sqrtS = "13.6 TeV"
    
    axis = ['pT','eta']
    if args.PV:
        axis = ['nVtx','eta']

    doEGM_SFs(args.txtFile, args.lumi,axis)
