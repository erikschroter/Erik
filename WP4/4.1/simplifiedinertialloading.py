#NOTE: ALL CALCULATIONS PERFORMED FOR HALF-WING

import numpy as np, scipy as sp
import Constants, matplotlib
import matplotlib.pyplot as plt


MaxFuelWeight = Constants.MaxFuelWeight
MTOW = Constants.MTOW
EngineWeight = Constants.EngineWeight
W_uc_MLG = Constants.W_uc_MLG
D_fuselageOuter = Constants.D_fuselageOuter
taperRatio = Constants.taperRatio
rootChord= Constants.rootChord
wingSpan = Constants.wingSpan
wingWeight = Constants.wingWeight
maxFuelMass = Constants.maxFuelMass
g = Constants.g

beginFuelTank = 2
endFuelTank  = 32
lengthFuelTank =  .46 * wingSpan
fuelPackingFactorinWingbox = 0.75
fuelDensity = 800 #kg / m^3
enginePosition = 0.33 * wingSpan / 2 #m
engineMass = 7549 #kg


def calculateInertialLoading (spanValue):
    inertialLoading = wingStructuralWeight(spanValue)  + engineWeight(spanValue)
    return inertialLoading

def engineWeight(spanValue):
    localEngineWeight = 0
    if spanValue <= enginePosition:
        localEngineWeight = engineMass * g
    else:
        localEngineWeight = 0

    return localEngineWeight

def wingStructuralWeight (spanValue):
    #structural weight in [N]
    specificWingWeight = wingWeight / 2 / wingVolume(0) * g
    localWingWeight = wingWeight / 2 * g - (wingVolume(spanValue) * specificWingWeight)
    return localWingWeight

