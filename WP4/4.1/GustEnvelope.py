# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:19:16 2020

@author: Erik Schroter
"""


from CS25Loads import DesignGustVelocity, GustVelocity
from ISAdef import ISA
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math

# =============================================================================
# Function defintions
# =============================================================================

# Computation of gust design velocity
def Hdef(MAC):
    if 12.5 * MAC >= 107:
        H = 12.5 * MAC
    elif 12.5 * MAC < 107:
        H = 107
    return H

# Calculation Dive Speed
def V_Ddef(M_c, a):
    M_d = M_c / 0.8
    if M_d > 1.0:
        V_D = M_c * 1.05 * a
    else:
        V_D = M_d * a
    return V_D

# Computation of gust reference velocity
def U_refdef(altitude, V_D=False):
    if V_D==False:
        # print("false...")
        if altitude <= 4572:
            # print("below...")
            U_ref = (13.41 - 17.07)/(4572 - 0) * altitude + 17.07
        elif altitude > 4572:
            # print("above...")
            U_ref = (6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41
    elif V_D==True:
        # print("true...")
        if altitude <= 4572:
            print("below...")
            U_ref = 0.5 * ((13.41 - 17.07)/(4572 - 0) * altitude + 17.07)
        elif altitude > 4572:
            # print("above...")
            U_ref = 0.5 * ((6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41)
    return U_ref

# Computation of design speed for maximum gust intensity
def V_s1def(W, rho, S, C_L):
    V_s1 = (2*W/(rho*S*C_L))**0.5
    return V_s1

def V_cEASdef(rho, rho_0, V_c):
    V_cEAS = V_c * (rho/rho_0)**0.5
    return V_cEAS

def Wloadingdef(W, S):
    Wloading = W / S
    return Wloading

def Kgdef(Wloading, rho, c, dCLdalpha, g):
    mu = 2 * Wloading / (rho * c * dCLdalpha * g)
    Kg = 0.88 * mu / (5.3 + mu)
    return mu, Kg

def Vbdef(V_s1, Kg, rho_0, U_ref, V_cEAS, dCLdalpha, Wloading):
    Vb = V_s1 * (1 + Kg * rho_0 * U_ref * V_cEAS * dCLdalpha / (2 * Wloading))**0.5
    return Vb

# Computation of flight profile alleviation factor
def Fgmdef(MLW, MTOW, MZFW):
    R1 = MLW / MTOW
    R2 = MZFW / MTOW
    Fgm = (R2 * np.tan(np.pi * R1 / 4))**0.5
    return R1, R2, Fgm

def Fgdef(Fgz, Fgm, Zmo, altitude):
    Fg0 = 0.5 * (Fgz + Fgm)
    Fg = (1 - Fg0)/(Zmo - 0) * altitude + Fg0
    return Fg0, Fg

# Computation of load factor change
def V_TASdef(rho, rho_0, V_EAS):
    V_TAS = V_EAS * (rho/rho_0)**-0.5
    return V_TAS

def omegadef(V_TAS, H):
    omega = np.pi * V_TAS / H
    return omega

def timeconstantdef(Wloading, dCLdalpha, rho, V_TAS, g):
    timeconstant = 2 * Wloading / (dCLdalpha * rho * V_TAS * g)
    return timeconstant

def deltaNdef(U_ds, g, omega, t, timeconstant):
    deltaN = U_ds / (2 * g) * (omega * np.sin(omega * t) + 1 / (1 + (omega * timeconstant) ** -2) * (1 / timeconstant * np.exp(-t / timeconstant) - 1 / timeconstant * np.cos(omega * t)  - omega * np.sin(omega * t)))
    return deltaN

# Debug 
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

MTOW = 304636.2789 # kg
C_L = 1.3962 # (maximum C_L with flaps retracted)

MLW = 0.85 * MTOW # kg (!!!CHECK THIS!!!)
MZFW = 161394.7263 # kg

OEW = 147780.3631 # kg

Zmo = 40000 * 0.3048 # ft (-> m)
Fgz = 1 - Zmo / 76200

M_c = 0.77

# =============================================================================
# Iterations for altitude
# =============================================================================

deltaNlst1 = []

for i in range(0,int(Zmo+1)):
    V = 63 # m/s (max @ 63 m/s)
    
    altitude = i # m (max @ 10146 m)

    rho, T = ISA(altitude)
    debug("rho", rho, dbug)
    debug("T", T, dbug)
    
    a = (1.4 * 287 * T)**0.5
    debug("a", a, dbug)
    
    V_D = V_Ddef(M_c, a)
    debug("V_D", V_D, dbug)
    
    H = Hdef(MAC)
    debug("H", H, dbug)
    
    U_ref = U_refdef(altitude, False)
    debug("Uref", U_ref, dbug)
    
    V_s1 = V_s1def(MTOW, rho_0, S, C_L) # (EAS)
    debug("V_s1", V_s1, dbug)
    
    V_cEAS = V_cEASdef(rho, rho_0, V_c)
    debug("Vc", V_cEAS, dbug)
    
    Wloading = Wloadingdef(MZFW, S)
    debug("W/S", Wloading, dbug)
    
    Kg = Kgdef(Wloading, rho, MAC, dCLdalpha, 9.80665)[1]
    debug("Kg", Kg, dbug)
    
    Vb = Vbdef(V_s1, Kg, rho_0, U_ref, V_cEAS, dCLdalpha, Wloading)
    debug("Vb", Vb, dbug)
    
    Fgm = Fgmdef(MLW, MTOW, MZFW)[2]
    debug("Fgm", Fgm, dbug)
    
    Fg = Fgdef(Fgz, Fgm, Zmo, altitude)[1]
    debug("Fg", Fg, dbug)
    
    # Calculate U_ds
    U_ds = DesignGustVelocity(U_ref, Fg, H)
    debug("U_ds", U_ds, dbug)
    
    # Calculate U
    s = np.arange(0, 2*H+1)
    debug("s", s, dbug)
    
    U = GustVelocity(U_ds, s, H)
    debug("U", U, dbug)
    
    # Calculate load factor change deltaN
    omega = omegadef(V, H)
    debug("omega", omega, dbug)
    
    t = np.arange(0, 2*np.pi/omega + 1, 0.01)
    debug("t", t, dbug)
    
    timeconstant = timeconstantdef(Wloading, dCLdalpha, rho, V, 9.80665)
    debug("lambda", timeconstant, dbug)
    
    deltaN = deltaNdef(V_TASdef(rho, rho_0, U_ds), 9.80655, omega, t, timeconstant)
    debug("deltaN", deltaN, dbug)
    
    deltaNlst1.append((max(deltaN), altitude, Vb, V))
    debug("iterate", (altitude, max(deltaN)), dbug)
    
print("max load factor: ", round(max(deltaNlst1)[0], 3), " [-] | altitude: ", max(deltaNlst1)[1], " [m] | Vb ", max(deltaNlst1)[2], " [m/s] | V ", max(deltaNlst1)[3], " [m/s]")

# =============================================================================
# Iterations for speed
# =============================================================================

deltaNlst2 = []

Vlst = np.array([0])

deltaNlstp = np.array([0])
deltaNlstn = np.array([0])

for i in range(1,int(max(deltaNlst1)[2])):
    V = i # m/s (max @ 63 m/s)
    
    np.append(Vlst, i)
    
    altitude = max(deltaNlst1)[1] # m (max @ 10146 m)
    
    rho, T = ISA(altitude)
    debug("rho", rho, dbug)
    debug("T", T, dbug)
    
    a = (1.4 * 287 * T)**0.5
    debug("a", a, dbug)
    
    H = Hdef(MAC)
    debug("H", H, dbug)
    
    U_ref = U_refdef(altitude, False)
    debug("Uref", U_ref, dbug)
    
    V_s1 = V_s1def(MTOW, rho_0, S, C_L) # (EAS)
    debug("V_s1", V_s1, dbug)
    
    V_cEAS = V_cEASdef(rho, rho_0, V_c)
    debug("Vc", V_cEAS, dbug)
    
    Wloading = Wloadingdef(MZFW, S)
    debug("W/S", Wloading, dbug)
    
    Kg = Kgdef(Wloading, rho, MAC, dCLdalpha, 9.80665)[1]
    debug("Kg", Kg, dbug)
    
    Vb = Vbdef(V_s1, Kg, rho_0, U_ref, V_cEAS, dCLdalpha, Wloading)
    debug("Vb", Vb, dbug)
    
    Fgm = Fgmdef(MLW, MTOW, MZFW)[2]
    debug("Fgm", Fgm, dbug)
    
    Fg = Fgdef(Fgz, Fgm, Zmo, altitude)[1]
    debug("Fg", Fg, dbug)
    
    # Calculate U_ds
    U_ds = DesignGustVelocity(U_ref, Fg, H)
    debug("U_ds", U_ds, dbug)
    
    # Calculate U
    s = np.arange(0, 2*H+1)
    debug("s", s, dbug)
    
    U = GustVelocity(U_ds, s, H)
    debug("U", U, dbug)
    
    # Calculate load factor change deltaN
    omega = omegadef(V, H)
    debug("omega", omega, dbug)
    
    t = np.arange(0, 2*np.pi/omega + 1, 0.01)
    debug("t", t, dbug)
    
    timeconstant = timeconstantdef(Wloading, dCLdalpha, rho, V, 9.80665)
    debug("lambda", timeconstant, dbug)
    
    deltaN = deltaNdef(V_TASdef(rho, rho_0, U_ds), 9.80655, omega, t, timeconstant)
    debug("deltaN", deltaN, dbug)
    
    deltaNlst2.append((max(deltaN), altitude, Vb, V))
    debug("iterate", (altitude, max(deltaN)), dbug)
    
    np.append(deltaNlstp, 1 + deltaN)
    np.append(deltaNlstn, 1 - deltaN)
    
    
print("max load factor: ", round(max(deltaNlst2)[0], 3), " [-] | altitude: ", max(deltaNlst2)[1], " [m] | Vb ", max(deltaNlst2)[2], " [m/s] | V ", max(deltaNlst2)[3], " [m/s]")\
    
# =============================================================================
# Graphing
# =============================================================================

# plotting the datapoints and interpolation because it looks nice
g = interp1d(s,U,kind="cubic", fill_value="extrapolate")
h = interp1d(t, 1 + deltaN, kind="cubic", fill_value="extrapolate")
i = interp1d(t, 1 - deltaN, kind="cubic", fill_value="extrapolate")

# plt.plot(s,U,"o", s, g(s), "-")
# plt.plot(s,U,"o")

# plt.plot(s, g(s), "-")
# plt.plot(t, h(t), "-")
# plt.plot(t, i(t), "-")
plt.plot(Vlst, deltaNlstp, "-")


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

