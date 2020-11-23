# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:31:39 2020

@author: michi
"""
dt=0.1
filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 1.225
v = 70
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

from scipy import integrate
import sys
import os
import scipy as sp
import matplotlib.pyplot as plt

directory = os.path.dirname(os.path.dirname(__file__))+"\\4.1"
sys.path.insert(-1,directory)
from liftdistribution import liftdistribution

x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy)
a = [0]
Aerosheer = [sp.integrate.quad(f,0,0)[0]-sp.integrate.quad(f,0,xdist)[0]]
while a[-1] <= xdist:
    a.append(a[-1]+dt)
    Aerosheer.append(sp.integrate.quad(f,0,a[-1])[0]-sp.integrate.quad(f,0,xdist)[0])
    
plt.plot(a,Aerosheer)
plt.show()