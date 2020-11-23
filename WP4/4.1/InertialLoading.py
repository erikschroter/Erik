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
mainLandingGearMass = Constants.mainLandingGearMass
g = Constants.g

beginFuelTank = 2
endFuelTank  = 32
lengthFuelTank =  .95 * wingSpan
fuelPackingFactorinWingbox = 0.75
fuelDensity = 800 #kg / m^3
enginePosition = 0.33 * wingSpan / 2 #m
engineMass = 7549 #kg


def calculateInertialLoading (spanValue):
    inertialLoading = -1 * wingStructuralWeight(spanValue) + -1 * engineWeight(spanValue) + -1 * fuelLoading(spanValue) + -1 * landingGearWeight(spanValue)
    return inertialLoading

def calculateInertialLoadingonGround (spanValue):
    inertialLoadingonGround =calculateInertialLoading(spanValue) + landingGearForceonGround(spanValue)
    return inertialLoadingonGround

def landingGearForceonGround(spanValue):
    distanceToFuselageInner2x4 = 1.8  # [m]
    distanceToFuselageInner1x4 = 0  # [m]
    distanceToFuselageOuter2x4 = 7.8  # [m]
    distanceToFuselageOuter2x4Num2 = 6  # [m]
    mainLandingGearMassPerWheel = mainLandingGearMass / (2 * (8 + 8 + 4 + 8))
    massInner2x4 = 8 * mainLandingGearMassPerWheel
    massInner1x4 = 4 * mainLandingGearMassPerWheel
    massOuter2x4 = 8 * mainLandingGearMassPerWheel
    massOuter2x4Num2 = 8 * mainLandingGearMassPerWheel

    return


def landingGearWeight(spanValue):
    distanceToFuselageInner2x4 = 1.8 #[m]
    distanceToFuselageInner1x4 = 0  # [m]
    distanceToFuselageOuter2x4 = 7.8  # [m]
    distanceToFuselageOuter2x4Num2 = 6  # [m]
    mainLandingGearMassPerWheel = mainLandingGearMass / (2 *  (8 + 8 + 4 + 8))
    massInner2x4 = 8 * mainLandingGearMassPerWheel
    massInner1x4 = 4 * mainLandingGearMassPerWheel
    massOuter2x4 = 8 * mainLandingGearMassPerWheel
    massOuter2x4Num2 = 8 * mainLandingGearMassPerWheel

    if spanValue == 0:
        landingGearWeight = g * mainLandingGearMass / 2

    elif spanValue < distanceToFuselageInner2x4:
        landingGearWeight = g * mainLandingGearMass / 2 - g * massInner1x4

    elif spanValue < distanceToFuselageOuter2x4Num2:
        landingGearWeight = g * mainLandingGearMass/2  - g * (massInner1x4 + massInner2x4)
    elif spanValue < distanceToFuselageOuter2x4:
        landingGearWeight = g * mainLandingGearMass/2 - g * (massInner1x4 + massInner2x4 + massOuter2x4Num2)
    elif spanValue <= wingSpan /2:
        landingGearWeight = g * mainLandingGearMass/2 - g * (massInner1x4 + massInner2x4 + massOuter2x4Num2 + massOuter2x4)

    return landingGearWeight



def engineWeight(spanValue):
    localEngineWeight = 0
    if spanValue <= enginePosition:
        localEngineWeight = engineMass * g
    else:
        localEngineWeight = 0

    return localEngineWeight

def wingStructuralWeight (spanValue):
    #structural weight in [N]
    specificWingWeight = wingWeight / 2 / wingArea(0) * g
    localWingWeight = wingWeight / 2 * g - (wingArea(wingSpan/2 - spanValue) * specificWingWeight)
    return localWingWeight

def fuelLoading (spanValue):
    #structural weight in [N]
    specificFuelWeight = maxFuelMass / 2 / halfWingRequiredFuelVolume * g
    localFuelWeight = maxFuelMass / 2 * g  - ((containedWingboxVolume(spanValue)) *fuelPackingFactorinWingbox * specificFuelWeight) * g
    if localFuelWeight <= 0:
        localFuelWeight = 0

    return localFuelWeight

def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord

def containedWingboxVolume(spanValue):
    resolution = 100
    volume = 0
    for i in range (0, round(spanValue) *resolution):
        volume += wingArea(i/resolution) * 1 /(resolution)
    return volume

def wingArea(spanValue):
    #approximate trapezoidal structural volume in half wing
    # area of trapezoid
    areaBetweenSparsOverChordSquared = (.1347 + .1091) / 2 * .45
    areaBetweenSpars = areaBetweenSparsOverChordSquared * localChord(spanValue) ** 2
    return areaBetweenSpars

def fuelVolume (spanValue, fuelMass):
    # fuel in half wing
    wingFuelWeight = 0.5 * fuelMass
    requiredFuelVolume = 0.5 * fuelMass / fuelDensity

    totalAvailableFuelVolume = 0
    resolution = 500
    for i in range(0, round(wingSpan / 2 * resolution)):
        totalAvailableFuelVolume += localWingboxArea(i / resolution) * fuelPackingFactorinWingbox * 1 / resolution

    return totalAvailableFuelVolume, requiredFuelVolume


def localWingboxArea (spanValue):
    localChord = 0
    if spanValue <= D_fuselageOuter:
        localChord = rootChord

    elif spanValue < wingSpan / 2 * lengthFuelTank / wingSpan:
        localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2 ) * spanValue

    else:
        localChord = 0

    #area of trapezoid
    areaBetweenSparsOverChordSquared = (.1347 + .1091)/2 * .45
    areaBetweenSpars = areaBetweenSparsOverChordSquared * localChord**2

    return areaBetweenSpars



halfWingAvailableFuelVolume, halfWingRequiredFuelVolume = fuelVolume(0, maxFuelMass)
fuelVolumeOutsideWing = 2 * (halfWingRequiredFuelVolume - halfWingAvailableFuelVolume)
xList = []
yList = []


for i in range(0, round(wingSpan / 2) * 10):
    xList.append(i/10)
    yList.append(calculateInertialLoading(i / 10))

plt.title('Inertial Loading vs Span [N], [m] ')
plt.plot(xList, yList)
plt.show()

dx = wingSpan /2 / len(xList)
dy = np.diff(yList)/ dx
xList2 = xList
del xList2[-1]

plt.title('Inertial Loading vs Span [N], [m] ')
plt.plot(xList2, dy)
plt.show()



inertialForce = []
for i in range(-1, round(wingSpan/2) * 10):
    inertialForce.append(calculateInertialLoading(i /10))

