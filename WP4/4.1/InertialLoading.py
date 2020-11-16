import numpy as np, scipy as sp
import Constants



MaxFuelWeight = Constants.MaxFuelWeight
MTOW = Constants.MTOW
EngineWeight = Constants.EngineWeight
W_uc_MLG = Constants.W_uc_MLG
D_fuselageOuter = Constants.D_fuselageOuter
taperRatio = Constants.taperRatio
rootChord= Constants.rootChord
beginFuelTank = 2
endFuelTank  = 32

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
    if spanValue <= D_fuselageOuter:
        localFuelWeight = 0



def localWingboxArea (spanValue):
    localChord = 0
    if spanValue <= D_fuselageOuter:
        localChord =



