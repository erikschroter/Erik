import os
import sys
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)


import scipy as sp
import math
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
from ReadingXFLRresults import ReadingXFLR
from liftdistribution import liftdistribution

from Definition_stringer_positions import Definition_stringer_position

# Wing Box outer geometry (in chord length)
WB_chord = 0.45
WB_front_height = 0.1347
WB_aft_height = 0.1091

#Variables to change
t = 0.010       #WB thickness
tS = 0.010      #Stringer thickness
HS = 0.100        #Stringer depth
Spanwise = [0, 6.992, 13.984, 20.976, 27.968]
Stringersno = [18, 16, 12, 8, 6]

def chord_length(spanwise_location): #Spanwise location is in y/(b/2)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)
    return c

""" 
def CentroidX(spanwise_location_iny, ntop, nlower):       #Centroid entire wingbox
    b = 69.92 #Span
    spanwise_location = spanwise_location_iny / (b / 2)
    chord = chord_length(spanwise_location)

    # Geometrical parameters
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord

    #Dimensions stringers
    n1= sp.interpolate.interp1d(Spanwise,Stringersno,kind="previous",fill_value="extrapolate")     #number of stringers

    #values trapezoid
    Cchord=(h/3)*((2*a+b)/(a+b))
    Cperpendicular=(2*a*c+a**2+c*b+a*b+b**2)/(3*(a+b))
    A = (a+b+math.sqrt(h**2+c**2)+math.sqrt(h**2+(b-a-c)**2))

    #Values Stringer
    Astringer=tS*(HS*3-2*t)
    CyS=0.5*HS
    CxS=0.5*HS

    #Parrallel axis stringers
    Ctopchord=[]
    halfn1=int(ntop/2)
    n1=int(ntop)
    halfn2=int(nlower/2)
    n2=int(nlower)
    for i in range(0, halfn1):
        ParAxisOne=(h/(ntop-1)*i+CyS)*Astringer
        Ctopchord.append(ParAxisOne)
        
    for i in range(halfn1, n1):
        ParAxisTwo=(h/(ntop-1)*i-CyS)*Astringer
        Ctopchord.append(ParAxisTwo)
        
    for i in range(0, halfn2):
        ParAxisThree=(h/(nlower-1)*i+CyS)*Astringer
        Ctopchord.append(ParAxisThree)
        
    for i in range(halfn2, n2):
        ParAxisFour=(h/(nlower-1)*i-CyS)*Astringer
        Ctopchord.append(ParAxisFour)
        
        
    Ctopchordtotal=sum(Ctopchord)+Cchord*A
    Atotchord=(ntop+nlower)*Astringer+A
    Cx=Ctopchordtotal/Atotchord
    
    return Cx
   
def CentroidY(spanwise_location_iny, ntop, nlower):       #Centroid entire wingbox
    b = 69.92 #Span
    spanwise_location = spanwise_location_iny / (b / 2)
    chord = chord_length(spanwise_location)

    # Geometrical parameters
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord

    #Dimensions stringers
    n1= sp.interpolate.interp1d(Spanwise,Stringersno,kind="previous",fill_value="extrapolate")     #number of stringers
    n = n1(spanwise_location_iny)

    #values trapezoid
    Cchord=(h/3)*((2*a+b)/(a+b))
    Cperpendicular=(2*a*c+a**2+c*b+a*b+b**2)/(3*(a+b))
    A = (a+b+math.sqrt(h**2+c**2)+math.sqrt(h**2+(b-a-c)**2))
    
    #Values Stringer
    Astringer=tS*(HS*3-2*t)
    CyS=0.5*HS
    CxS=0.5*HS

    #Parrallel axis stringers
    Ctopperp=[]
    halfn1=int(ntop/2)
    n1=int(ntop)
    halfn2=int(nlower/2)
    n2=int(nlower)
    for i in range(0, halfn1):
        ParAxisOne=((c/h)*(h/(ntop-1)*i)+CxS)*Astringer
        Ctopperp.append(ParAxisOne)
        
    for i in range(halfn1, n1):
        ParAxisTwo=((c/h)*(h/(ntop-1)*i)-CxS)*Astringer
        Ctopperp.append(ParAxisTwo)
        
    for i in range(0, halfn2):
        ParAxisThree=(b-(c/h)*(h/(nlower-1)*i)-CxS)*Astringer
        Ctopperp.append(ParAxisThree)
        
    for i in range(halfn2, n2):
        ParAxisFour=(b-(c/h)*(h/(nlower-1)*i)+CxS)*Astringer
        Ctopperp.append(ParAxisFour)
        
        
    Ctopperptotal=sum(Ctopperp)+Cperpendicular*A
    Atotperp=(ntop+nlower)*Astringer+A
    Cy=Ctopperptotal/Atotperp
    
    return Cy
"""

def CentroidY(stringer_distribution, spanwise_location):

    top = 0
    bottom = 0

    stringer_positions = Definition_stringer_position(stringer_distribution, spanwise_location)
    for i in range(len(stringer_positions)):
        if stringer_positions[i][3]:
            top = top + stringer_positions[i][2] * stringer_positions[i][1]
            bottom = bottom + stringer_positions[i][2]

    Cy = top/bottom

    return Cy

def CentroidX(stringer_distribution, spanwise_location):

    top = 0
    bottom = 0

    stringer_positions = Definition_stringer_position(stringer_distribution, spanwise_location)
    for i in range(len(stringer_positions)):
        if stringer_positions[i][3]:
            top = top + stringer_positions[i][2] * stringer_positions[i][0]
            bottom = bottom + stringer_positions[i][2]

    Cx = top/bottom

    return Cx

stringer_distribution = [(14,14,6.99),(12,12,13.98),(10,10,20.98),(8,8,27.97),(6,6,34.96)]  # from root to tip, (top, bottom)

def SpanwiseCentroidY(stringer_distribution):
    spanwise_position = []
    y = []
    n = 0
    d = 6.99
    for i in range(5):
        while n < d:
            y.append(CentroidY(stringer_distribution, n))
            spanwise_position.append(n)
            n = n + 0.25
        d += 6.99
    y_spanwise = sp.interpolate.interp1d(spanwise_position, y, kind="linear", fill_value="extrapolate")
    return y_spanwise

print(CentroidY(stringer_distribution, 0))

""""""
y_spanwise = SpanwiseCentroidY(stringer_distribution)
print(SpanwiseCentroidY(stringer_distribution))


spanwise_position = []
n = 0
d = 6.99
for i in range(5):
    while n < d:
        spanwise_position.append(n)
        n = n + 0.25
    d += 6.99

plt.plot(spanwise_position, y_spanwise(spanwise_position), "-")

# plot formatting

plt.title('Spanwise C_y')

plt.xlabel('Spanwise location [m]')
plt.ylabel('C_y [Nm]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()


