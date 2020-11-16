import numpy as np, scipy as sp
import Constants


MaxFuelWeight = Constants.MaxFuelWeight
MTOW = Constants.MTOW
EngineWeight = Constants.EngineWeight
W_uc_MLG = Constants.W_uc_MLG

WingWeight = 24_821.18761
span = 69.92

def calculateInertialLoading (spanValue, nValue, fuelMass):
    inertialLoading = WingStructuralWeight(spanValue) +fuelLoading(spanValue. fuelMass)

def WingStructuralWeight (spanValue):
    #structural weight in [N]
    localWingWeight = WingWeight -  spanValue / (span /2) * WingWeight
    return localWingWeight

def fuelLoading (spanValue, fuelMass):
    #find values
    D_fuselageOuter = 6.68 #[m]
    taperRatio = 0.3 #[]

    localFuelWeight = 0
    beginFuelTank = 2
    endFuelTank  = 32
    if spanValue <= D_fuselageOuter:
        widthTank
        localFuelWeight =





