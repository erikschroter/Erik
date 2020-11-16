#NOTE: ALL CALCULATIONS PERFORMED FOR HALF-WING

import numpy as np, scipy as sp
import Constants



MaxFuelWeight = Constants.MaxFuelWeight
MTOW = Constants.MTOW
EngineWeight = Constants.EngineWeight
W_uc_MLG = Constants.W_uc_MLG
D_fuselageOuter = Constants.D_fuselageOuter
taperRatio = Constants.taperRatio
rootChord= Constants.rootChord
wingSpan = Constants.wingSpan


beginFuelTank = 2
endFuelTank  = 32
lengthFuelTank = 0.85 * wingSpan
fuelPackingFactorinWingbox = 0.9
fuelDensity = 800 #kg / m^3

WingWeight = 24_821.18761
span = 69.92

def calculateInertialLoading (spanValue, nValue, fuelMass):
    inertialLoading = WingStructuralWeight(spanValue) +fuelLoading(spanValue. fuelMass)

def WingStructuralWeight (spanValue):
    #structural weight in [N]
    localWingWeight = WingWeight -  spanValue / (span /2) * WingWeight
    return localWingWeight

def fuelLoading (spanValue, fuelMass):
    #fuel in half wing
    wingFuelWeight = 0.5 * fuelMass
    requiredFuelVolume = fuelMass / fuelDensity

    totalAvailableFuelVolume = 0
    for i in range (0, int(wingSpan / 2 * 1000) ):
        totalAvailableFuelVolume += localWingboxArea(spanValue) * fuelPackingFactorinWingbox * 1/1000
    #print(requiredFuelVolume)
    #print(totalAvailableFuelVolume)
    #print(requiredFuelVolume / totalAvailableFuelVolume)
    return



    #find values




def localWingboxArea (spanValue):
    localChord = 0
    countCenter = 0
    countOuter = 0

    if spanValue <= D_fuselageOuter:
        localChord = rootChord
        countCenter += 1
    elif spanValue < wingSpan / 2 * lengthFuelTank / wingSpan:
        localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2 ) * spanValue
        countOuter +=1
    else:
        localChord = 0


    #area of trapezoid)
    areaBetweenSparsOverChordSquared = (.1347 + .1091)/2 * .45
    areaBetweenSpars = areaBetweenSparsOverChordSquared * localChord**2
    print("center: ", countCenter)
    print("Outer: ", countOuter)
    return areaBetweenSpars


volume = 0
for i in range(0, int(wingSpan /2 * 1000)):
    volume += localWingboxArea(i/1000) * 1/ (1000)
#print(volume)

#print(localWingboxArea(0))





#print(fuelLoading(0,207251))
