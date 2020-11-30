# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:22:34 2020

@author: michi
"""

E = 8.9*(10**9)
dt=0.1
filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 0.4416
v = 232
span = 69.92
accuracy = 41 
 
#Loading factor [-]
n=4.65

#Maximum takeoff weight [kg]
MTOW = 291_509.2

#Operating empty weight [kg]
OEW = 141_412.4
#Maximum zero fuel weight [kg]
MZFW = 161394.73

#Maximum fuel weight [kg]
MaxFuelWeight = MTOW - OEW

#Engine weight for 2 engines [kg]
EngineWeight = 20_87.986

#Undercarriage weight for MLG only [kg]
W_uc_MLG = 7_569.349

#Wingbox thickness versus cord lengt
wtvcl = 0.1347
#tensile yield stress [MPA]
sigma_y = 276

#Wing weight including mounts and spoilers [kg]
WingWeight = 3210.55
import numpy as np
from scipy import integrate
import sys
import matplotlib.patches as mpatches
import os
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)
import scipy as sp
import matplotlib.pyplot as plt
from InertialLoading import inertialForce

from liftdistribution import liftdistribution
from Moment_of_Inertia_Wingbox import Ixx_in_y
from Moment_of_Inertia_Wingbox import chord_length

x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy,MZFW*9.81,n)
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
def y(x):
    return (wtvcl * chord_length(x/34.96)/2)
i=0
while i < len(a):
  
    BendingStress.append(abs((Moment[i]*y(a[i]))/(10**6*Ixx_in_y(a[i]))))
    i +=1
print(len(BendingStress),len(a))
g = sp.interpolate.interp1d(a,BendingStress,kind="linear", fill_value="extrapolate")
i=0
safty_margine = []
while i < len(a):
    if BendingStress[i] >= 0.001:
        safty_margine.append((sigma_y/BendingStress[i]))
    else:
        safty_margine.append(safty_margine[-1])
    i += 1
plt.plot(a,(BendingStress))
plt.title("Bending Stress diagram")
plt.grid(b=None,which='Major',axis='both')
plt.ylabel("Bending Stress [MPa]")
plt.xlabel("spanwise location [m]")
plt.show()
plt.plot(a,safty_margine)
plt.title("Tension safty margin diagram")
plt.grid(b=None,which='Major',axis='both')
plt.ylabel("Safty margin [-]")
plt.xlabel("spanwise location [m]")
plt.ylim(0,15)
plt.show()

