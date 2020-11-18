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
wingWeight = Constants.wingWeight
maxFuelMass = Constants.maxFuelMass
g = Constants.g

beginFuelTank = 2
endFuelTank  = 32
lengthFuelTank =  .46 * wingSpan
fuelPackingFactorinWingbox = 0.75
fuelDensity = 800 #kg / m^3


def calculateInertialLoading (spanValue, nValue, fuelMass):
    inertialLoading = WingStructuralWeight(spanValue) + fuelLoading(spanValue, fuelMass)

def wingStructuralWeight (spanValue):
    #structural weight in [N]
    localWingWeight = wingWeight * g -  spanValue / (wingSpan /2) * wingWeight * g
    return localWingWeight


def wingVolume(spanValue):
    #approximate trapezoidal structural volume in half wing

def fuelVolume (spanValue, fuelMass):
    # fuel in half wing
    wingFuelWeight = 0.5 * fuelMass
    requiredFuelVolume = 0.5 * fuelMass / fuelDensity

    totalAvailableFuelVolume = 0
    resolution = 500
    for i in range(0, int(wingSpan / 2 * resolution)):
        totalAvailableFuelVolume += localWingboxArea(i / resolution) * fuelPackingFactorinWingbox * 1 / resolution
    print(requiredFuelVolume)
    print(totalAvailableFuelVolume)
    return(totalAvailableFuelVolume, requiredFuelVolume)


def fuelLoading (spanValue, fuelMass):
    #fuel weight in [N]
    #localFuelWeight = fuelMass - fuelVolumeOutsideWing / 2 * fuelDensity - fuelVolume(spanValue, fuelMass) * fuelDensity

    return #localFuelWeight




def localWingboxArea (spanValue):
    localChord = 0

    if spanValue <= D_fuselageOuter:
        localChord = 0

    elif spanValue < wingSpan / 2 * lengthFuelTank / wingSpan:
        localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2 ) * spanValue

    else:
        localChord = 0

    #area of trapezoid
    areaBetweenSparsOverChordSquared = (.1347 + .1091)/2 * .45
    areaBetweenSpars = areaBetweenSparsOverChordSquared * localChord**2

    return areaBetweenSpars




halfWingAvailableFuelVolume, halfWingRequiredFuelVolume = fuelVolume(wingSpan / 2, maxFuelMass)
fuelVolumeOutsideWing = 2 * (halfWingRequiredFuelVolume - halfWingAvailableFuelVolume)

print(fuelLoading(0, maxFuelMass))
