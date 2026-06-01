import math

EPS = 1e-12
def _safe_ratio(num, den, default):
    try:
        if den is None or abs(den) <= EPS:
            return default
        return num / den
    except Exception:
        return default

class efficiency:
    #    altEff = [-1]*7
    iAltBkgModel = 0
    iAltSigModel = 1
    iAltMCSignal = 2
    # iAltTagSelec = 3
    iPUup        = 4
    iPUdown      = 5
    iAltFitRange = 6
    iAltSigBkgModel = 3

    def __init__(self,abin):
        self.ptBin   = abin
        self.effData = -1
        self.effMC   = -1
        self.altEff  = [-1]*7
        self.syst    = [-1]*7
        self.mean    = -1
    
    def __init__(self,ptBin,etaBin,effData,errEffData,effMC,errEffMC,effAltBkgModel,effAltSigModel,effAltMCSignal,effAltSigBkgModel):
        self.ptBin      = ptBin
        self.etaBin     = etaBin
        self.effData    = effData
        self.effMC      = effMC
        self.errEffData = errEffData        
        self.errEffMC   = errEffMC
        self.altEff = [-1]*7
        self.syst   = [-1]*7
        self.altEff[self.iAltBkgModel] = effAltBkgModel
        self.altEff[self.iAltSigModel] = effAltSigModel
        self.altEff[self.iAltMCSignal] = effAltMCSignal
        # self.altEff[self.iAltTagSelec] = effAltTagSel
        self.altEff[self.iAltSigBkgModel] = effAltSigBkgModel
        self.mean=(effAltBkgModel+effAltSigModel+effAltSigBkgModel+effData)/4


    def __str__(self):
        return '%2.3f\t%2.3f\t%2.1f\t%2.1f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f\t%2.4f' % (self.etaBin[0],self.etaBin[1],
                                                                                                       self.ptBin[0] ,self.ptBin[1] ,
                                                                                                       self.effData, self.errEffData, self.effMC, self.errEffMC,
                                                                                                       self.altEff[0],self.altEff[1], self.altEff[2], self.altEff[3] )

    @staticmethod
    def getSystematicNames():
        return [ 'statData', 'statMC', 'altBkgModel', 'altSignalModel', 'altSigBkgModel' ,'nominal','altMC']



    def combineSyst(self,averageEffData,averageEffMC):
        systNom         = self.effData - self.mean
        systAltBkg      = self.altEff[self.iAltBkgModel] - self.mean
        systAltSig      = self.altEff[self.iAltSigModel] - self.mean
        systAltMC       = self.altEff[self.iAltMCSignal] - self.effMC
#        systAltTagSelec = self.altEff[self.iAltTagSelec] - averageEffData
        systAltSigBkg   = self.altEff[self.iAltSigBkgModel] - self.mean
        # systAltTagSelec = self.altEff[self.iAltTagSelec] - averageEffMC


        if self.altEff[self.iAltBkgModel] < 0:
            systAltBkg = 0

        if self.altEff[self.iAltSigModel] < 0:
            systAltSig = 0

        if self.altEff[self.iAltMCSignal] < 0:
            systAltMC = 0

        if self.altEff[self.iAltSigBkgModel] < 0:
            systAltSigBkg = 0

        # if self.altEff[self.iAltTagSelec] < 0:
        #     systAltTagSelec = 0

        #don't include systMC when smaller than statMC
        if(systAltMC<self.errEffMC):
            systAltMC = 0

        self.syst[ 0                 ] = self.errEffData
        self.syst[ 1                 ] = self.errEffMC
        self.syst[ 2                 ] = systAltBkg
        self.syst[ 3                 ] = systAltSig
        self.syst[ 4                 ] = systAltSigBkg
        self.syst[ 5                 ] = systNom
        self.syst[ 6                 ] = systAltMC
        # self.syst[self.iAltTagSelec+2] = systAltTagSelec
        
        
        self.systCombined = 0
        ##Sum in Q##
        # for isyst in range(6):
        #     self.systCombined += self.syst[isyst]*self.syst[isyst];

        ##NEW PROPOSAL##
        for isyst in range(2,6):
            self.systCombined += self.syst[isyst]*self.syst[isyst] 
        self.systCombined= math.sqrt(self.systCombined/3) #RMS/sqrtN
        self.systCombined = math.sqrt(self.systCombined*self.systCombined/4 + self.syst[6]*self.syst[6] + self.syst[0]*self.syst[0]+ self.syst[1]*self.syst[1]) #sum in quad with syst_altMC, statData and statMC

    def __add__(self,eff):
        if self.effData < 0 :
            return eff.deepcopy()
        if eff.effData < 0 :
            return self.deepcopy()
        
        ptbin  = self.ptBin
        etabin = self.etaBin
        errData2 = 1.0 / (1.0/(self.errEffData*self.errEffData)+1.0/(eff.errEffData*eff.errEffData))
        wData1   = 1.0 / (self.errEffData * self.errEffData) * errData2
        wData2   = 1.0 / (eff .errEffData * eff .errEffData) * errData2
        newEffData      = wData1 * self.effData + wData2 * eff.effData;
        newErrEffData   = math.sqrt(errData2)
        
        #        errMC2 = 1.0 / (1.0/(self.errEffMC*self.errEffMC)+1.0/(eff.errEffMC*eff.errEffMC))
        #wMC1   = 1.0 / (self.errEffMC * self.errEffMC) * errMC2
        #wMC2   = 1.0 / (eff .errEffMC * eff .errEffMC) * errMC2
        newEffMC      = wData1 * self.effMC + wData2 * eff.effMC;
        newErrEffMC   = 0.00001#math.sqrt(errMC2)

        newEffAltBkgModel = wData1 * self.altEff[self.iAltBkgModel] + wData2 * eff.altEff[self.iAltBkgModel]
        newEffAltSigModel = wData1 * self.altEff[self.iAltSigModel] + wData2 * eff.altEff[self.iAltSigModel]
        newEffAltMCSignal = wData1 * self.altEff[self.iAltMCSignal] + wData2 * eff.altEff[self.iAltMCSignal]
        # newEffAltTagSelec = wData1 * self.altEff[self.iAltTagSelec] + wData2 * eff.altEff[self.iAltTagSelec]
        newEffAltSigBkgModel = wData1 * self.altEff[self.iAltSigBkgModel] + wData2 * eff.altEff[self.iAltSigBkgModel]
        
        effout = efficiency(ptbin,etabin,newEffData,newErrEffData,newEffMC,newErrEffMC,newEffAltBkgModel,newEffAltSigModel,newEffAltMCSignal,newEffAltSigBkgModel)
        return effout
    


import ROOT as rt
import numpy as np

def makeTGraphFromList( listOfEfficiencies , keyMin, keyMax ):
    grOut = rt.TGraphErrors(len(listOfEfficiencies))
    
    ip = 0
    for point in listOfEfficiencies:
        grOut.SetPoint(     ip, (point[keyMin]+point[keyMax])/2. , point['val'] )
        grOut.SetPointError(ip, (point[keyMax]-point[keyMin])/2. , point['err'] )
        ip = ip + 1

    #    print "###########################"
    #    print listOfEff
    #    grOut.Print()
    return grOut



class efficiencyList: 
    effList = {}

    def __init__(self):
        self.effList = {}

    
    def __str__(self):
        outStr = ''
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                outStr += str(self.effList[ptBin][etaBin])
                outStr += '\n'
        return outStr

    
    def addEfficiency( self, eff ):
        if eff.ptBin not in self.effList:
            self.effList[eff.ptBin] = {}
        self.effList[eff.ptBin][eff.etaBin] = eff

    def combineSyst(self):
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                if etaBin[0] >= 0 and etaBin[1] >= 0:
                    etaBinPlus  = etaBin
                    etaBinMinus = (-etaBin[1],-etaBin[0])
                    
                    effPlus  = self.effList[ptBin][etaBinPlus]
                    effMinus = None
                    if etaBinMinus in self.effList[ptBin]:
                        effMinus =  self.effList[ptBin][etaBinMinus] 

                    if effMinus is None:
                        print(" ---- efficiencyList: I did not find -eta bin!!!")

                        try:
                            effPlus.combineSyst(effPlus.effData, effPlus.effMC)
                        except Exception as _e:

                            if not hasattr(effPlus, "systCombined"):
                                effPlus.systCombined = 0.0
                    else:                        
                        averageData = (effPlus.effData + effMinus.effData)/2.
                        averageMC   = (effPlus.effMC   + effMinus.effMC  )/2.
                        self.effList[ptBin][etaBinMinus].combineSyst(averageData,averageMC)
                        self.effList[ptBin][etaBinPlus ].combineSyst(averageData,averageMC)
                        

                        
    def symmetrizeSystVsEta(self):
        for ptBin in self.effList.keys():
            for etaBin in list(self.effList[ptBin].keys()):
                print("etaBin:  ",etaBin)
                if etaBin[0] >= 0 and etaBin[1] > 0:
                    etaBinPlus  = etaBin
                    etaBinMinus = (-etaBin[1],-etaBin[0])
                    
                    effPlus  = self.effList[ptBin][etaBinPlus]
                    effMinus = None
                    if etaBinMinus in self.effList[ptBin]:
                        effMinus =  self.effList[ptBin][etaBinMinus] 

                    if effMinus is None:
                        self.effList[ptBin][etaBinMinus] = effPlus
                        print(" ---- efficiencyList: I did not find -eta bin!!!")
                    else:
                        #### fix statistical errors if needed
                        if    effPlus.errEffData <= 0.00001 and effMinus.errEffData > 0.00001: 
                            self.effList[ptBin][etaBinPlus ].errEffData = effMinus.errEffData
                        elif effMinus.errEffData <= 0.00001 and effPlus .errEffData > 0.00001: 
                            self.effList[ptBin][etaBinMinus].errEffData = effPlus.errEffData
                        else:
                            self.effList[ptBin][etaBinPlus ].errEffData = (effMinus.errEffData+effPlus.errEffData)/2.
                            self.effList[ptBin][etaBinMinus].errEffData = (effMinus.errEffData+effPlus.errEffData)/2.

                        if   effPlus.errEffMC <= 0.00001 and effMinus.errEffMC > 0.00001: 
                            self.effList[ptBin][etaBinPlus ].errEffMC = effMinus.errEffMC
                        elif effMinus.errEffMC <= 0.00001 and effPlus.errEffMC > 0.00001: 
                            self.effList[ptBin][etaBinMinus].errEffMC = effPlus.errEffMC
                        else:
                            self.effList[ptBin][etaBinPlus ].errEffMC = (effMinus.errEffMC+effPlus.errEffMC)/2.
                            self.effList[ptBin][etaBinMinus].errEffMC = (effMinus.errEffMC+effPlus.errEffMC)/2.

                            
                        for isyst in range(4):
                            if abs(effPlus.altEff[isyst] - effMinus.altEff[isyst]) < 0.10:
                                averageSyst = (effPlus.altEff[isyst] +  effMinus.altEff[isyst]) / 2
                                self.effList[ptBin][etaBinPlus ].altEff[isyst] = averageSyst
                                self.effList[ptBin][etaBinMinus].altEff[isyst] = averageSyst
                            else:
                                averageSyst = (effPlus.altEff[isyst] +  effMinus.altEff[isyst]) / 2
                                print("issue, I am averaging but the efficiencies are quite different in 2 etaBins")
                                print(" --- syst: ", isyst)
                                print(str(self.effList[ptBin][etaBinPlus ]))
                                print(str(self.effList[ptBin][etaBinMinus]))
                                print("   eff[+] = ",  self.effList[ptBin][etaBinPlus ].altEff[isyst])
                                print("   eff[-] = ",  self.effList[ptBin][etaBinMinus].altEff[isyst])                                
                                self.effList[ptBin][etaBinPlus ].altEff[isyst] = averageSyst
                                self.effList[ptBin][etaBinMinus].altEff[isyst] = averageSyst

    def ptEtaScaleFactor_2DHisto(self, onlyError, relError = False):
#        self.symmetrizeSystVsEta()
        self.combineSyst()

        ### first define bining
        xbins = []
        ybins = []
        for ptBin in self.effList.keys():
            if not ptBin[0] in ybins:
                ybins.append(ptBin[0])                
            if not ptBin[1] in ybins:
                ybins.append(ptBin[1])

            for etaBin in self.effList[ptBin].keys():
                if not etaBin[0] in xbins:
                    xbins.append(etaBin[0])                
                if not etaBin[1] in xbins:
                    xbins.append(etaBin[1])

        xbins.sort()
        ybins.sort()
        ## transform to numpy array for ROOT
        xbinsTab = np.array(xbins)
        ybinsTab = np.array(ybins)

        htitle = 'e/#gamma scale factors'
        hname  = 'h2_scaleFactorsEGamma' 
        if onlyError >= 0:
            htitle = 'e/#gamma uncertainties'
            hname  = 'h2_uncertaintiesEGamma'             

        h2 = rt.TH2F(hname,htitle,xbinsTab.size-1,xbinsTab,ybinsTab.size-1,ybinsTab)

        ## init histogram efficiencies and errors to 100%
        for ix in range(1,h2.GetXaxis().GetNbins()+1):
            for iy in range(1,h2.GetYaxis().GetNbins()+1):
                h2.SetBinContent(ix,iy, 1)
                h2.SetBinError  (ix,iy, 1)
        
        for ix in range(1,h2.GetXaxis().GetNbins()+1):
            for iy in range(1,h2.GetYaxis().GetNbins()+1):

                for ptBin in self.effList.keys():
                    if h2.GetYaxis().GetBinLowEdge(iy) < ptBin[0] or h2.GetYaxis().GetBinUpEdge(iy) > ptBin[1]:
                        continue
                    for etaBin in self.effList[ptBin].keys():
                        if h2.GetXaxis().GetBinLowEdge(ix) < etaBin[0] or h2.GetXaxis().GetBinUpEdge(ix) > etaBin[1]:
                            continue

                        ## average MC efficiency
                        etaBinPlus  = etaBin
                        etaBinMinus = (-etaBin[1],-etaBin[0])
                    
                        effPlus  = self.effList[ptBin][etaBinPlus]
                        effMinus = None
                        if etaBinMinus in self.effList[ptBin]:
                            effMinus =  self.effList[ptBin][etaBinMinus] 

                        averageMC = None
                        if effMinus is None:
                            averageMC = effPlus.effMC
                            print(" ---- efficiencyList: I did not find -eta bin!!!")
                        else:                        
                            averageMC   = (effPlus.effMC   + effMinus.effMC  )/2.
                        ### so this is h2D bin is inside the bining used by e/gamma POG
                        _syst_combined = getattr(self.effList[ptBin][etaBin], "systCombined", 0.0)

                        h2.SetBinContent(ix,iy, _safe_ratio(self.effList[ptBin][etaBin].mean, self.effList[ptBin][etaBin].effMC, default=1.0))
                        h2.SetBinError  (ix,iy, _safe_ratio(_syst_combined, self.effList[ptBin][etaBin].effMC, default=0.0))

                        if onlyError == 0:
                            h2.SetBinContent(ix,iy, _safe_ratio(_syst_combined, self.effList[ptBin][etaBin].effMC, default=0.0))

                        if onlyError == -3:
                            h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].mean)
                            h2.SetBinError  (ix,iy, _safe_ratio(_syst_combined * self.effList[ptBin][etaBin].effMC, self.effList[ptBin][etaBin].effMC, default=0.0))
                        elif onlyError == -2:
                            h2.SetBinContent(ix,iy, self.effList[ptBin][etaBin].effMC)
                            h2.SetBinError  (ix,iy, 0 )
                        elif onlyError == -1:
                            h2.SetBinContent(ix,iy, _safe_ratio(self.effList[ptBin][etaBin].mean, self.effList[ptBin][etaBin].effMC, default=1.0))
                            h2.SetBinError  (ix,iy, _safe_ratio(_syst_combined, self.effList[ptBin][etaBin].effMC, default=0.0))

                        if onlyError == 0:
                            h2.SetBinContent(ix,iy, _safe_ratio(_syst_combined, self.effList[ptBin][etaBin].effMC, default=0.0))
                        elif onlyError >= 1 and onlyError <= 6:
                            denominator = averageMC
                            if relError:
                                denominator = _syst_combined
                            h2.SetBinContent(ix,iy, _safe_ratio(abs(self.effList[ptBin][etaBin].syst[onlyError-1]), denominator, default=0.0))

        h2.SetTitle("%s;%s;%s" % (htitle, "SuperCluster #eta", "p_{T} [GeV]"))
        h2.SetMarkerSize(1.8)

        h2.GetYaxis().SetTitleFont(42)
        h2.GetYaxis().SetLabelFont(42)
        h2.GetYaxis().SetTitleSize(0.06)
        h2.GetYaxis().SetLabelSize(0.05)
        h2.GetYaxis().SetTitleOffset(1.2)

        h2.GetXaxis().SetTitleFont(42)
        h2.GetXaxis().SetLabelFont(42)
        h2.GetXaxis().SetTitleSize(0.06)
        h2.GetXaxis().SetLabelSize(0.05)
        h2.GetXaxis().SetTitleOffset(1.1)
        h2.GetXaxis().SetLabelOffset(0.01)

        h2.GetZaxis().SetTitleFont(42)
        h2.GetZaxis().SetLabelFont(42)
        h2.GetZaxis().SetTitleSize(0.055)
        h2.GetZaxis().SetLabelSize(0.05)
        h2.GetZaxis().SetTitleOffset(0.75)

        return h2
        
                                
    def pt_1DGraph_list(self, doScaleFactor):
#        self.symmetrizeSystVsEta()
        self.combineSyst()
        listOfGraphs = {}

        
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                # --- FIX: 接受負 eta；以 |eta| 合併 ---
                absEtaBin = (abs(etaBin[0]), abs(etaBin[1]))
                absEtaBin = (min(absEtaBin), max(absEtaBin))
                if absEtaBin[0] == absEtaBin[1]:
                    continue

                etaBinPlus  = absEtaBin
                etaBinMinus = (-absEtaBin[1], -absEtaBin[0])

                effPlus  = self.effList[ptBin].get(etaBinPlus)
                effMinus = self.effList[ptBin].get(etaBinMinus)

                effAverage = effPlus or effMinus
                if effPlus is not None and effMinus is not None:
                    effAverage = effPlus + effMinus

                if effAverage is None:
                    continue

                if etaBinPlus not in listOfGraphs:
                    listOfGraphs[etaBinPlus] = []

                effAverage.combineSyst(effAverage.effData, effAverage.effMC)
                aValue  = effAverage.mean
                anError = getattr(effAverage, "systCombined", 0.0)
                if doScaleFactor:
                    aValue  = _safe_ratio(effAverage.mean, effAverage.effMC, default=1.0)
                    anError = _safe_ratio(anError, effAverage.effMC, default=0.0)

                listOfGraphs[etaBinPlus].append({'min': ptBin[0], 'max': ptBin[1], 'val': aValue, 'err': anError})

        return listOfGraphs

    def pt_1DGraph_list_customEtaBining(self, etaBining, typeGR = 0 ):
        """
        typeGR: 0=Data (mean), +1=ScaleFactor (mean/MC), -1=MC
        """

        self.combineSyst()
        listOfGraphs = {}

        for abin in etaBining:
            listOfGraphs[abin] = []
            for ptBin in self.effList.keys():

                seenAbsEta = set()

                for etaBin in self.effList[ptBin].keys():
                    absEtaBin = (abs(etaBin[0]), abs(etaBin[1]))
                    absEtaBin = (min(absEtaBin), max(absEtaBin))
                    if absEtaBin in seenAbsEta:
                        continue
                    seenAbsEta.add(absEtaBin)


                    if abin[0] < absEtaBin[0] or abin[1] > absEtaBin[1]:
                        continue

                    etaBinPlus  = absEtaBin
                    etaBinMinus = (-absEtaBin[1], -absEtaBin[0])

                    effPlus  = self.effList[ptBin].get(etaBinPlus)
                    effMinus = self.effList[ptBin].get(etaBinMinus)

                    effAverage = effPlus or effMinus
                    if effPlus is not None and effMinus is not None:
                        effAverage = effPlus + effMinus

                    if effAverage is None:
                        continue

                    effAverage.combineSyst(effAverage.effData, effAverage.effMC)

                    aValue  = effAverage.mean
                    anError = getattr(effAverage, "systCombined", 0.0)

                    if typeGR == 1:      # SF
                        aValue  = _safe_ratio(effAverage.mean, effAverage.effMC, default=1.0)
                        anError = _safe_ratio(anError, effAverage.effMC, default=0.0)
                    elif typeGR == -1:   # MC
                        aValue  = effAverage.effMC
                        anError = 0.0

                    listOfGraphs[abin].append({'min': ptBin[0], 'max': ptBin[1], 'val': aValue, 'err': anError})

        return listOfGraphs

    
    def eta_1DGraph_list(self, typeGR = 0 ):
#        self.symmetrizeSystVsEta()
        self.combineSyst()
        listOfGraphs = {}
        
        for ptBin in self.effList.keys():
            for etaBin in self.effList[ptBin].keys():
                if ptBin not in listOfGraphs:                        
                    ### init average efficiency 
                    listOfGraphs[ptBin] = []
                effAverage = self.effList[ptBin][etaBin]
                aValue  = effAverage.mean
                try:
                    anError = getattr(effAverage, "systCombined", None)
                    if anError is None:
                        anError = getattr(effAverage, "systTot", None)
                    if anError is None:
                        anError = getattr(effAverage, "systTotal", None)
                    if anError is None:
                        anError = 0.0
                except Exception:
                    anError = 0.0
                if typeGR == 1:
                    aValue  = _safe_ratio(effAverage.mean, effAverage.effMC, default=1.0)
                    anError = _safe_ratio(anError, effAverage.effMC, default=0.0)
                if typeGR == -1:
                    aValue  = effAverage.effMC
                    anError = 0#effAverage.errEffMC
                    
                listOfGraphs[ptBin].append( {'min': etaBin[0], 'max': etaBin[1],
                                             'val': aValue  , 'err': anError } )

        return listOfGraphs


