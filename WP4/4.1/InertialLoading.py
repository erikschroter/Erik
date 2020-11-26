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
propulsionGroupMass = 20487.986 #kg


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
    mainLandingGearMassPerWheel = mainLandingGearMass / (2 * (8 + 8 + 4 + 8))
    massInner2x4 = 8 * mainLandingGearMassPerWheel
    massInner1x4 = 4 * mainLandingGearMassPerWheel
    massOuter2x4 = 8 * mainLandingGearMassPerWheel
    massOuter2x4Num2 = 8 * mainLandingGearMassPerWheel

    landingGearWeight = 0

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
        localEngineWeight = engineMass * g /2
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
    fuelVolumeInWing = halfWingRequiredFuelVolume
    if halfWingRequiredFuelVolume > halfWingAvailableFuelVolume:
        fuelVolumeInWing = halfWingAvailableFuelVolume

    specificFuelWeight = maxFuelMass / 2 / fuelVolumeInWing * g

#edit next line
    localFuelWeight = maxFuelMass / 2 * g  - ((containedFuelVolume(spanValue)) *fuelPackingFactorinWingbox * specificFuelWeight)

    if localFuelWeight < 0:
        localFuelWeight = 0

    return localFuelWeight

def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord

def containedFuelVolume(spanValue):
    newresolution = 50
    volume = 0
    for i in range (0, round(spanValue * newresolution)):
        volume += localWingboxArea(i/ newresolution) * 1 /(newresolution)
    return volume

def containedWingboxVolume(spanValue):
    resolution = 50
    volume = 0
    for i in range (0, round(spanValue *resolution)):
        volume += wingArea(i/resolution) * 1 / (resolution)
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
    resolution = 40
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


listResolution = 80
xList = []
yList = []


"""
for i in range(0, round(wingSpan / 2) * listResolution):
    xList.append(i/listResolution)
    yList.append(calculateInertialLoading(i / listResolution))

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
for i in range(-1, round(wingSpan/2) * listResolution):
    inertialForce.append(calculateInertialLoading(i /listResolution))



fuelList = []
for i in range(1, round(wingSpan / 2) * listResolution):
    fuelList.append(fuelLoading(i / listResolution))

plt.title('Fuel Loading vs Span [N], [m] ')
plt.plot(xList, fuelList)
plt.show()

wingList = []
for i in range(1, round(wingSpan / 2) * listResolution):
    wingList.append(wingStructuralWeight(i / listResolution))

plt.title('wing Loading vs Span [N], [m] ')
plt.plot(xList, wingList)
plt.show()

propList = []
for i in range(1, round(wingSpan / 2) * listResolution):
    propList.append(engineWeight(i / listResolution))

plt.title('propulsion Loading vs Span [N], [m] ')
plt.plot(xList, propList)
plt.show()

landingGearList = []
for i in range(1, round(wingSpan / 2) * listResolution):
    landingGearList.append(landingGearWeight(i / listResolution))

plt.title('landing gear Loading vs Span [N], [m] ')
plt.plot(xList, landingGearList)
plt.show()



fuelVolumeList = []
for i in range(1, round(wingSpan / 2) * listResolution):
    fuelVolumeList.append(containedFuelVolume(i / listResolution))

plt.title('fuel vol  vs Span [N], [m] ')
plt.plot(xList, fuelVolumeList)
plt.show()
"""