# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:19:16 2020

@author: Erik Schroter
"""


from CS25Loads import DesignGustVelocity, GustVelocity
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# =============================================================================
# Function defintions
# =============================================================================

# Computation of gust design velocity
def H(MAC):
    if 12.5 * MAC >= 107:
        H = 12.5 * MAC
    elif 12.5 * MAC < 107:
        H = 107
    return H

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

def debug(Name, Variable, p=False):
    if p==True:
        return print(Name, " is ", Variable)
    if p==False:
        return 

# =============================================================================
# Calculations
dbug=False
# =============================================================================

MAC = 8.51495 # m

rho_0 = 1.225 # kg/m^3
V_c = 232.46 # m/s
dCLdalpha = 0.095 * 180/ np.pi # 1/rad
S = 543.25 # m^2


altitude = 10000 # m 
MTOW = 304636.2789 # kg
rho = 0.4135 # kg/m^3
C_L = 2.3 # (maximum C_L)

MLW = 161394.7263 # kg (!!!CHECK THIS!!!)
MZFW = 161394.7263 # kg


Zmo = 40000 * 0.3048 # m
Fgz = 1 - Zmo / 76200

H = H(MAC)
debug("H", H, dbug)

U_ref = U_ref(altitude, False)
debug("Uref", U_ref, dbug)

V_s1 = V_s1(MTOW, rho, S, C_L)
debug("V_s1", V_s1, dbug)

V_cEAS = V_cEAS(rho, rho_0, V_c)
debug("Vc", V_cEAS, dbug)

Kg = Kg(MTOW/S, rho, MAC, dCLdalpha, 9.80665)[1]
debug("Kg", Kg, dbug)

Vb = Vb(V_s1, Kg, rho_0, U_ref, V_cEAS, dCLdalpha, MTOW/S)
debug("Vb", Vb, dbug)

Fgm = Fgm(MLW, MTOW, MZFW)[2]
debug("Fgm", Fgm, dbug)

Fg = Fg(Fgz, Fgm, Zmo, altitude)[1]
debug("Fg", Fg, dbug)

# Calculate U_ds
U_ds = DesignGustVelocity(U_ref, Fg, H)
debug("U_ds", U_ds, dbug)

# Calculate U
s = np.arange(0, 2*H+1)
debug("s", s, dbug)

U = GustVelocity(U_ds, s, H)
debug("U", U, dbug)

# =============================================================================
# Graphing
# =============================================================================

# plotting the datapoints and interpolation because it looks nice
g = interp1d(s,U,kind="cubic", fill_value="extrapolate")

# plt.plot(s,U,"o", s, g(s), "-")
# plt.plot(s,U,"o")
plt.plot(s, g(s), "-")


# plot formatting

plt.title('Gust Velocity as function of s')

plt.xlabel('s [m]')
plt.ylabel('Gust velocity, U [m/s]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()

# =============================================================================
# FIN
# =============================================================================
