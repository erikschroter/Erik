import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
import math

from FunctionsGlobalBucklingAnalysis import segment_1,segment_2,segment_3, segment_4, segment_5
from Definition_stringer_positions import Definition_stringer_position, stringer_distribution

taperRatio = 0.3 #[]
rootChord = 11.95 #[m]
wingSpan = 69.92 #[m]



def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord



#inputs stringer_positions: xpos, ypos, area, existence of stringer

def Ixx (y_span, centroid):
    stringer_positions = Definition_stringer_position(stringer_distribution, y_span)
    Ixx = 0

    if y_span <= segment_1:
        print(stringer_positions[0][3], "kk")
        for i in range(len(stringer_positions)):
            if stringer_positions[i][3]:
                print(stringer_positions[i][3])
                Ixx += (stringer_positions[i][1])**2 * (stringer_positions[i][2])
                print(Ixx, "12")

    elif y_span <= segment_2:
        if stringer_positions[i][3]:
            Ixx += (stringer_positions[i][1]) ** 2 * (stringer_positions[i][2])

    elif y_span <= segment_3:
        if stringer_positions[i][3]:
            Ixx += (stringer_positions[i][1]) ** 2 * (stringer_positions[i][2])

    elif y_span <= segment_4:
        if stringer_positions[i][3]:
            Ixx += (stringer_positions[i][1]) ** 2 * (stringer_positions[i][2])

    elif y_span <= segment_5:
        if stringer_positions[i][3]:
            Ixx += (stringer_positions[i][1]) ** 2 * (stringer_positions[i][2])

    else:
        print("error")

    #print(segment_1)
    print(stringer_positions)
    return Ixx


pos = []

print(Ixx (5,0))