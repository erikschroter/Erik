import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
import math

from FunctionsGlobalBucklingAnalysis import segment_1,segment_2,segment_3, segment_4, segment_5
from Definition_stringer_positions import Definition_stringer_position, stringer_distribution
from Centroid import CentroidY

taperRatio = 0.3 #[]
rootChord = 11.95 #[m]
wingSpan = 69.92 #[m]

print("vb")

def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord



#inputs stringer_positions: xpos, ypos, area, existence of stringer

def Ixx (y_span, centroid):
    print("b")
    stringer_positions = Definition_stringer_position(stringer_distribution, y_span)
    print("w")
    print("v")
    centroidY = CentroidY(stringer_distribution, y_span)
    print("k")
    Ixx = 0
    for i in range(len(stringer_positions)):
        if stringer_positions[i][3]:
            #print(stringer_positions[i][3])
            Ixx += ((stringer_positions[i][1])-centroidY)**2 * (stringer_positions[i][2])
            print(Ixx)



    print(stringer_positions)
    return Ixx


pos = []
print("qs")
print(Ixx (0,0), "hello")
print("bvsdc")