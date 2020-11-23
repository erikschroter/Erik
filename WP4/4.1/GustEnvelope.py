# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:19:16 2020

@author: Erik Schroter
"""


from CS25Loads import DesignGustVelocity, GustVelocity
import numpy as np

# Computation of gust design velocity
MAC = 8.51495 # m

if 12.5 * MAC >= 107:
    H = 12.5 * MAC
elif 12.5 * MAC < 107:
    H = 107

# Computation of gust reference velocity
def U_ref(altitude, V_D=False):
    if V_D==False:
        print("false...")
        if altitude <= 4572:
            print("below...")
            U_ref = (13.41 - 17.07)/(4572 - 0) * altitude + 17.07
        elif altitude > 4572:
            print("above...")
            U_ref = (6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41
    elif V_D==True:
        print("true...")
        if altitude <= 4572:
            print("below...")
            U_ref = 0.5 * ((13.41 - 17.07)/(4572 - 0) * altitude + 17.07)
        elif altitude > 4572:
            print("above...")
            U_ref = 0.5 * ((6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41)
    return U_ref

# Computation of design speed for maximum gust intensity
def V_s1(W, rho, S, C_L):
    V_s1 = (2*W/(rho*S*C_L))**0.5
    return V_s1

def V_cEAS(rho, rho_0, V_c):
    V_cEAS = V_c * (rho/rho_0)**0.5
    return V_cEAS

def Wloading(W, S):
    Wloading = W / S
    return Wloading

def Kg(Wloading, rho, c, dCLdalpha, g):
    mu = 2 * Wloading / (rho * c * dCLdalpha * g)
    Kg = 0.88 * mu / (5.3 + mu)
    return mu, Kg

def Vb(V_s1, Kg, rho_0, U_ref, V_cEAS, dCLdalpha, Wloading):
    Vb = V_s1 * (1 + Kg * rho_0 * U_ref * V_cEAS * dCLdalpha / (2 * Wloading))**0.5
    return Vb

# Computation of flight profile alleviation factor


def Fgm(MLW, MTOW, MZFW):
    R1 = MLW / MTOW
    R2 = MZFW / MTOW
    Fgm = (R2 * np.tan(np.pi * R1 / 4))**0.5
    return R1, R2, Fgm

def Fg(Fgz, Fgm, Zmo, altitude):
    Fg0 = 0.5 * (Fgz + Fgm)
    Fg = (1 - Fg0)/(Zmo - 0) * altitude + Fg0
    return Fg0, Fg

# =============================================================================
# 
# =============================================================================
rho_0 = 1.225 # kg/m^3
V_c = 232.46 # m/s
dCLdalpha = 0.095 * 180/ np.pi # 1/rad
S = 543.25 # m^2


altitude = 18288 # m 
W = 304636.2789 # kg
rho = 1.225 # kg/m^3
C_L = 2.3 # (maximum C_L)

Zmo = 40000 * 0.3048 # m
Fgz = 1 - Zmo / 76200

U_ref = U_ref(altitude, False)
print("Uref is ", U_ref)

V_s1 = V_s1(W, rho, S, C_L)
print("V_s1 is ", V_s1)

