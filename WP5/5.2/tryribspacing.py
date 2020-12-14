import math as m

requiredRibs = [4, 6, 11, 11.5, 12, 14, 14.5, 22.1, 24, 24.2, 32, 34.96]
maxDistanceTip = 1.9 #m
maxDistanceRoot = .61 #m
minDistanceTip = 0.9 #m
minDistanceRoot = .3 #m
wingSpan = 34.96 #m
resolution = 100

def minDistance (ySpan):
    minDist = (minDistanceTip - minDistanceRoot) / wingSpan * ySpan + 0.3
    return minDist

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
            print("Rib List, j: ", j, ribList)
            ribList.insert(maxi+j+1, ribList[maxi] + (j+1) * newDist)


        #print(maxNumberRibsAdded, minNumberRibsAdded, "yo")
        #print("Rib List: ", ribList)

    return recalculate

def minSpacinginList():
    minSpacing = 0.9
    mini  = 0
    recalculate = False
    for i in range(0, len(ribList)-1 ):
        spacing = ribList[i+1] - ribList[i]

        if spacing < maxSpacing:
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
            print("Rib List, j: ", j, ribList)
            ribList.insert(maxi+j+1, ribList[maxi] + (j+1) * newDist)


        #print(maxNumberRibsAdded, minNumberRibsAdded, "yo")
        #print("Rib List: ", ribList)

    return recalculate


runCalculation = True
while runCalculation:
    runCalculation = maxSpacinginList()


#print((ribList))

