import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
import math as m

from FunctionsGlobalBucklingAnalysis import segment_1,segment_2,segment_3, segment_4, segment_5
from Definition_stringer_positions import Definition_stringer_position, stringer_distribution, a_stringer, h_stringer, t_stringer
from Centroid import CentroidY
import Definition_stringer_positions
t_wing_box_spar_cap = Definition_stringer_positions.t_wing_box_spar_cap
t_wing_box_skin = Definition_stringer_positions.t_wing_box_skin
a_wing_box_spar_cap = Definition_stringer_positions.a_wing_box_spar_cap

taperRatio = 0.3 #[]
rootChord = 11.95 #[m]
wingSpan = 69.92 #[m]



def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord



#inputs stringer_positions: xpos, ypos, area, existence of stringer

def Ixx (y_span):
    stringer_positions = Definition_stringer_position(stringer_distribution, y_span)
    centroidY = CentroidY(stringer_distribution, y_span)

    #steinerTerms
    number_stringers = -4
    Ixx = 0
    for i in range(0, len(stringer_positions)):
        if stringer_positions[i][3]:
            #print(stringer_positions[i][3])
            Ixx += ((stringer_positions[i][1])-centroidY)**2 * (stringer_positions[i][2])
            number_stringers = number_stringers + 1
            #print("stringer pos: ", stringer_positions[i][1])
            #print("area: ", stringer_positions[i][2])
            #print("centroid: ", centroidY)


    #Non-steiner terms
    chord = localChord(y_span) * 1000 #chord in mm

    heightFrontSpar = 134.7 / 1000 * chord
    heightRearSpar = 109.1 / 1000 * chord
    frontSparCentroidY = heightFrontSpar / 2
    rearSparCentroidY = heightRearSpar / 2

    #spars contribution
    Ixx += (heightFrontSpar ** 3 * t_wing_box_spar_cap / 12) + 2 * (a_wing_box_spar_cap * t_wing_box_spar_cap ** 3 / 12 + a_wing_box_spar_cap * t_wing_box_spar_cap * (heightFrontSpar/2)**2)
    Ixx += (heightRearSpar **3 * t_wing_box_spar_cap / 12) + 2 * (a_wing_box_spar_cap * t_wing_box_spar_cap ** 3 / 12 + a_wing_box_spar_cap * t_wing_box_spar_cap * (heightRearSpar/2)**2)

    lengthSkin = 450 / 1000 * chord
    angleTopSkin = 2.08 * m.pi / 180
    angleBottomSkin = 1.18 * m.pi  / 180

    #skin contribution
    Ixx += t_wing_box_skin * (lengthSkin/m.cos(angleTopSkin)) ** 3 * m.sin(angleTopSkin) ** 2 / 12
    Ixx += t_wing_box_skin * (lengthSkin/m.cos(angleBottomSkin)) ** 3 * m.sin(angleBottomSkin) ** 2 / 12

    #stringer contribution
    Ixx_stringer = h_stringer ** 3 * t_stringer / 12 + 2 * a_stringer * t_stringer** 3 / 12 + 2 * a_stringer * t_stringer * (h_stringer/2 + t_stringer/2)**2
    Ixx += number_stringers * Ixx_stringer
    return Ixx





listResolution = 80
xList = []
yList = []

for i in range(0, round(wingSpan / 2) * listResolution - 3):
    xList.append(i/listResolution)
    yList.append(Ixx(i / listResolution))
"""
plt.title('Moment of Inertia')
plt.ylabel('Ixx [mm^4]')
plt.xlabel('Span [m]')
plt.plot(xList, yList)
plt.show()
"""

"""
print("0:",Ixx(0))
print("5:", Ixx(5))
print("10:", Ixx(10))
print("15:", Ixx(15))
print("end - .5:", Ixx(wingSpan /2 - .5))
print("end -0.1 :", Ixx(wingSpan /2 - .1))
print("end:", Ixx(wingSpan /2))
"""