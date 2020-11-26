# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:31:39 2020

@author: michi
"""
E = 8.9*(10**9)
dt=0.1
filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 0.4416
v = 232
span = 69.92
accuracy = 41 
 

#Maximum takeoff weight [kg]
MTOW = 291_509.2

#Operating empty weight [kg]
OEW = 141_412.4

#Maximum fuel weight [kg]
MaxFuelWeight = MTOW - OEW

#Engine weight for 2 engines [kg]
EngineWeight = 20_87.986

#Undercarriage weight for MLG only [kg]
W_uc_MLG = 7_569.349

#Wing weight including mounts and spoilers [kg]
WingWeight = 3210.55
import numpy as np
from scipy import integrate
import sys
import matplotlib.patches as mpatches
import os
import scipy as sp
import matplotlib.pyplot as plt
from InertialLoading import inertialForce
directory = os.path.dirname(os.path.dirname(__file__))+"\\4.2"
sys.path.insert(-1,directory)
from liftdistribution import liftdistribution
from Moment_of_Inertia_Wingbox import Ixx_in_y

x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy)
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

plt.plot(a,Aerosheer,'r')
plt.plot(a,inertialForce,'g')
plt.plot(a,totalsheer,'b')
plt.hlines(-5,0,40)
plt.title("Shear forces")
red_patch = mpatches.Patch(color='r', label='Aerodynamic forces')
green_patch = mpatches.Patch(color='g', label='Inertial forces')
blue_patch = mpatches.Patch(color='b', label='Total Shear force')
plt.legend(handles=[red_patch,green_patch,blue_patch])

plt.show()

i = 0
Moment = []
while i < len(a):
    Moment.append(sp.integrate.quad(f,0,a[i])[0]-sp.integrate.quad(f,0,xdist)[0])
    if i%10==0:
        print("bending moment calculation: (1/2) ",round(100*a[i]/xdist),"%")
    i += 1
plt.plot(a,Moment)
plt.title("Bending Moment diagram")
plt.show()

i=1
Deflectioncalculation=[0]
print(Moment)
while i < len(a):
  
    Deflectioncalculation.append(-Moment[i]/(E*Ixx_in_y(a[i])))
    i +=1
print(Deflectioncalculation)
g = sp.interpolate.interp1d(a,Deflectioncalculation,kind="linear", fill_value="extrapolate")



i =0
firstintegration = []

while i < len(a):
    
    firstintegration.append(sp.integrate.quad(g,0,a[i])[0])
    if i%10==0:
        print("Deflection Calculation (2/2): ",round((100*a[i]/xdist)*0.5),"%")
    i+=1
h = sp.interpolate.interp1d(a,firstintegration,kind="linear",fill_value="extrapolate")
i =0
deflection = []
c =(sp.integrate.quad(h,0,0)[0])
while i < len(a):
    
    deflection.append(sp.integrate.quad(h,0,a[i])[0]-c)
    if i%10==0:
        print("Deflection Calculation (2/2): ",round((100*a[i]/xdist)*0.5+50),"%")
    i+=1

plt.plot(a,deflection)
plt.hlines(xdist*0.3,-5,40)
plt.title("Deflection")
plt.show()

plt.plot(a,deflection)
plt.title("Deflection to scale")
plt.xlim(0, xdist)
plt.ylim(0, xdist)
plt.gca().set_aspect('equal', adjustable='box')

