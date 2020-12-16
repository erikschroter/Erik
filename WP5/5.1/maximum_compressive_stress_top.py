# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:22:34 2020

@author: michi
"""


dt=0.1
filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 0.4416
v = 232
span = 69.92
accuracy = 41 
 

#Maximum takeoff weight [kg]
MTOW = 304636

#Operating empty weight [kg]
OEW = 147780
#Maximum zero fuel weight [kg]
MZFW = 161394.73

#Maximum fuel weight [kg]
MaxFuelWeight = MTOW - OEW

#Loading factor [-]
n= 4.65
# n_second= -1.5

#critical weight
WC = MZFW
# WC_second = MTOW

import numpy as np
from scipy import integrate
from Definition_stringer_positions import stringer_distribution
import sys
import matplotlib.patches as mpatches
import os
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP5\\5.2"
sys.path.insert(-1,directory)
import scipy as sp
import matplotlib.pyplot as plt
from InertialLoading import inertialForce

from liftdistribution import liftdistribution
from GlobalMomentofInertia import Ixx
from Centroid import y_spanwise, SpanwiseCentroidY
from Top_Bottom_Skin_Buckling import Top_Bottom_Skin_Buckling
from Rib_Sections_Definition import sections


x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy,WC*9.81,n)
a = [0]
Aerosheer = [-sp.integrate.quad(f,0,0)[0]+sp.integrate.quad(f,0,xdist)[0]]
while a[-1] <= xdist:
    a.append(a[-1]+dt)
    Aerosheer.append(-sp.integrate.quad(f,0,a[-1])[0]+sp.integrate.quad(f,0,xdist)[0])
    
totalsheer = []
i=0
while i < len(Aerosheer):
    totalsheer.append(Aerosheer[i]+inertialForce[i])
    i += 1
    
f = sp.interpolate.interp1d(a,totalsheer,kind="linear", fill_value="extrapolate")



i = 0
Moment = []
while i < len(a):
    Moment.append(sp.integrate.quad(f,0,a[i])[0]-sp.integrate.quad(f,0,xdist)[0])
    if i%10==0:
        print("bending moment calculation: ",round(100*a[i]/xdist),"%")
    i += 1
'''plt.plot(a,Moment)

plt.title("Bending Moment diagram")
plt.grid(b=None,which='Major',axis='both')
plt.ylabel("Bending Moment [Nm]")
plt.xlabel("spanwise location [m]")
plt.hlines(-5,0,40)

plt.show()'''
BendingStress=[]
Column_BendingStress=[]
fy = SpanwiseCentroidY(stringer_distribution)
critical_bottom_stresses_function, critical_top_stresses_function, y_critical_bottom_stresses_function, y_critical_top_stresses_function = Top_Bottom_Skin_Buckling(sections, stringer_distribution)


def y(x):
    if n >= 0:
        # print('top in compression')
        return y_critical_top_stresses_function(x)
    else:
        # print('bottom in compression')
        return y_critical_bottom_stresses_function(x)
i=0
while i < len(a):
  
    BendingStress.append(abs((Moment[i]*y(a[i]))/(10**(-6)*Ixx(a[i]))))
    i +=1

taperRatio = 0.3 #[]
rootChord = 11.95 #[m]
wingSpan = 69.92 #[m]

def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord

def y_column(x):
    if n >= 0:
        # print('top in compression')
        return 134.7 * localChord(x) - y_spanwise(x)
    else:
        # print('bottom in compression')
        return y_spanwise(x)
i=0
while i < len(a):
    Column_BendingStress.append(abs((Moment[i]*y_column(a[i]))/(10**(-6)*Ixx(a[i]))))
    i +=1

maximum_compressive_stress_top = sp.interpolate.interp1d(a,BendingStress,kind="linear", fill_value="extrapolate")
column_maximum_compressive_stress_top = sp.interpolate.interp1d(a,Column_BendingStress,kind="linear", fill_value="extrapolate")

print(maximum_compressive_stress_top)
print(column_maximum_compressive_stress_top)

"""

plt.plot(a,(BendingStress))
plt.title("Bending Stress diagram")
plt.grid(b=None,which='Major',axis='both')
plt.ylabel("Bending Stress [MPa]")
plt.xlabel("spanwise location [m]")
plt.show()
print("bendingstress:",BendingStress[0])

"""