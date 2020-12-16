# Definition Rib Sections
import math as m
sections = [0.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.714285714285714, 7.428571428571429, 8.142857142857142, 8.857142857142858, 9.571428571428571, 10.285714285714285, 11.0, 11.5, 12.0, 12.666666666666666, 13.333333333333334, 14.0, 14.5, 15.585714285714285, 16.67142857142857, 17.757142857142856, 18.84285714285714, 19.92857142857143, 21.014285714285716, 22.1, 22.733333333333334, 23.366666666666667, 24.0, 24.2, 25.5, 26.8, 28.1, 29.4, 30.7, 32.0, 32.986666666666665, 33.973333333333336, 34.96]
additional_sections = [0.5, 1.0, 1.6, 2.2, 2.8, 3.4]
for i in range(len(additional_sections)):
    sections.append(additional_sections[i])
sections.sort()

t_rib = 3  # mm
a_rib = 103  # mm

#define constants, max and min distances can be adjusted
requiredRibs = [4, 6, 11, 11.5, 12, 14, 14.5, 22.1, 24, 24.2, 32, 34.96]
maxDistanceTip = 1.9 #m
maxDistanceRoot = .61 #m
minDistanceTip = 0.9 #m
minDistanceRoot = .3 #m
wingSpan = 34.96 #m
resolution = 100

#defines min preferred distance between ribs (may be violated near required ribs)
def minDistance (ySpan):
    minDist = (minDistanceTip - minDistanceRoot) / wingSpan * ySpan + 0.3
    return minDist

#defines min preferred distance between ribs
def maxDistance (ySpan):
    maxDist = (maxDistanceTip - maxDistanceRoot) / wingSpan * ySpan + 0.61
    return maxDist


ribList = []
for i in range (0, round(resolution * wingSpan) + 1):
    if requiredRibs.count(i / resolution) > 0:
        ribList.append(i/resolution)

#print(ribList)

def maxSpacinginList():
    maxSpacing = 0
    maxi  = 0
    recalculate = False
    for i in range(0, len(ribList)-1 ):
        spacing = ribList[i+1] - ribList[i]

        if spacing > maxSpacing:
            maxSpacing = spacing
            spanVal = (ribList[i + 1] + ribList[i]) / 2
            minDist = minDistance(spanVal)
            maxDist = maxDistance(spanVal)
            #print(maxSpacing)
            maxi = i
    if maxSpacing > maxDist:
        recalculate = True
        maxNumberRibsAdded = maxSpacing / minDist
        minNumberRibsAdded = maxSpacing / maxDist
        segments = 0
        if m.ceil(minNumberRibsAdded) <= maxNumberRibsAdded:
            segments = m.ceil(minNumberRibsAdded)
        newDist = maxSpacing / (segments +1)

        for j in range(0, segments):
            #print("Rib List, j: ", j, ribList)
            ribList.insert(maxi+j+1, ribList[maxi] + (j+1) * newDist)


        #print(maxNumberRibsAdded, minNumberRibsAdded, "yo")
        #print("Rib List: ", ribList)

    return recalculate

runCalculation = True
while runCalculation:
    runCalculation = maxSpacinginList()