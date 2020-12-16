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
n=4.65
#n=-1.65

#critical weight
#WC = MTOW
WC = MZFW


#Wingbox thickness versus cord lengt
wtvcl = 0.1347

#tensile ULTIMATE stress [MPA]
sigma_y = 310

import numpy as np
from scipy import integrate
import sys
import matplotlib.patches as mpatches
import os
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP5\\5.1"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)
import scipy as sp
import matplotlib.pyplot as plt
from InertialLoading import inertialForce

from liftdistribution import liftdistribution
from GlobalMomentofInertia import Ixx
from Moment_of_Inertia import chord_length
from Centroid import SpanwiseCentroidY, y_spanwise


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
fy = y_spanwise

def y(x):
    if n >= 0:
        return fy(x)
    else:
        return (wtvcl * chord_length(x/34.96))-fy(x)
i=0
while i < len(a):
  
    BendingStress.append(abs((Moment[i]*y(a[i]))/(10**(-6)*Ixx(a[i]))))
    i +=1

g = sp.interpolate.interp1d(a,BendingStress,kind="linear", fill_value="extrapolate")
i=0
safty_margine = []
while i < len(a):
    if BendingStress[i] >= 0.001:
        safty_margine.append((1000*sigma_y/BendingStress[i]))
    else:
        safty_margine.append(safty_margine[-1])
    i += 1
plt.plot(a,(BendingStress))
plt.title("Bending Stress diagram")
plt.grid(b=None,which='Major',axis='both')
plt.ylabel("Bending Stress [MPa]")
plt.xlabel("spanwise location [m]")
plt.show()
print("bendingstress:",BendingStress[0])
plt.plot(a,safty_margine)
plt.title("Tension safety margin diagram")
plt.grid(b=None,which='Major',axis='both')
plt.ylabel("Safety margin [-]")
plt.xlabel("spanwise location [m]")
plt.ylim(-1,6)
plt.show()

