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
def U_refdef(altitude, V, Vb, V_c, V_D):
    if V >= Vb and V <= V_c:
        # print("false...")
        if altitude <= 4572:
            # print("below...")
            U_ref = (13.41 - 17.07)/(4572 - 0) * altitude + 17.07
        elif altitude > 4572:
            # print("above...")
            U_ref = (6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41
    elif V == V_D:
        # print("true...")
        if altitude <= 4572:
            # print("below...")
            U_ref = 0.5 * ((13.41 - 17.07)/(4572 - 0) * altitude + 17.07)
        elif altitude > 4572:
            # print("above...")
            U_ref = 0.5 * ((6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41)
    else:
        print("U_ref undefined over this interval, taking U_ref as 0")
        U_ref = 0
    return U_ref

# Compute initial U_ref
def U_initialdef(altitude):
    if altitude <= 4572:
        # print("below...")
        U_ref = (13.41 - 17.07)/(4572 - 0) * altitude + 17.07
    elif altitude > 4572:
        # print("above...")
        U_ref = (6.36 - 13.41)/(18288 - 4572) * (altitude - 4572) + 13.41
    return U_ref

# Computation of design speed for maximum gust intensity
def V_s1def(W, rho, S, C_L):
    V_s1 = (2*W/(rho*S*C_L))**0.5
    return V_s1

def V_cEASdef(rho, rho_0, V_c):
    V_cEAS = V_c * (rho/rho_0)**0.5
    return V_cEAS

def Wloadingdef(W, S):
    Wloading = W / S * 9.80665
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

M_c = 0.77 # Mach
h_cruise = 31000 * 0.3048 # m

W = MTOW # Flight condition being evaluated

dbug = False

# =============================================================================
# Iterations for to find most critical condition
# =============================================================================

Nmaxlst = []

# Flight condition for all altitudes till cruise altitude
# for i in range(0, int(h_cruise) + 1, 250): 1219,9449
for i in range(0, 0 + 1, 250):
    altitude = i
    
    # Initialising datalists
    deltaNlst2 = []
    
    Vlst1 = []
    Vlst2 = []
    
    Nlst1p = []
    Nlst1n = []
    
    Nlst2p = []
    Nlst2n = []

    # Begin Calculations
    
    rho, T = ISA(altitude)
    debug("rho", rho, dbug)
    debug("T", T, dbug)
    
    a = (1.4 * 287 * T)**0.5
    debug("a", a, dbug)
    
    V_D = V_Ddef(M_c, a)
    debug("V_D", V_D, dbug)
    
    H = Hdef(MAC)
    debug("H", H, dbug)
    
    V_s1 = V_s1def(W, rho_0, S, C_L) # (EAS) changes with weight
    debug("V_s1", V_s1, dbug)
    
    V_cEAS = V_cEASdef(rho, rho_0, V_c)
    debug("Vc", V_cEAS, dbug)
    
    Wloading = Wloadingdef(W, S) # changes with weight
    debug("W/S", Wloading, dbug)
    
    Kg = Kgdef(Wloading, rho, MAC, dCLdalpha, 9.80665)[1]
    debug("Kg", Kg, dbug)
    
    U_initial = U_initialdef(altitude)
    
    Vb = Vbdef(V_s1, Kg, rho_0, U_initial, V_cEAS, dCLdalpha, Wloading)
    debug("Vb", Vb, dbug)
    
    
    # Flight condition for the 3 Velocities
    for i in [Vb, V_c, V_D]:
        V = i # m/s
        
        Vlst1.append(V)
        
        U_ref = U_refdef(altitude, V, Vb, V_c, V_D)
        debug("Uref", U_ref, dbug)
        
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
        
        deltaNlst2.append((max(deltaN), altitude, Vb, V, V_D, V_s1))
        debug("iterate", (altitude, V, max(deltaN)), dbug)
        
        Nlst1p.append(1 + max(deltaN))
        Nlst1n.append(1 - max(deltaN))
        
    # Appending V_D to different list and removing from old list
    Vlst2.append(Vlst1[-1])
    Nlst2p.append(Nlst1p[-1])
    Nlst2n.append(Nlst1n[-1])
    
    del Vlst1[-1]
    del Nlst1p[-1]
    del Nlst1n[-1]

    # Append to list the maximum load factors
    Nmaxlst.append((max(deltaNlst2)[0] + 1, max(deltaNlst2)[1], Vlst1, Vlst2, Nlst1p, Nlst2p, Nlst1n, Nlst2n, max(deltaNlst2)[2], max(deltaNlst2)[4], max(deltaNlst2)[5]))
    
    print("Considered Flight Condition : Altitude ", altitude, " [m] | Weight ", W, " [kg]")
    print("    Max Load Factor ", round(max(deltaNlst2)[0] + 1, 3), " [-] | Vb ", max(deltaNlst2)[2], " [m/s] | V ", max(deltaNlst2)[3], " [m/s] =============================================================================")

print("\n Maximum N ", max(Nmaxlst)[0], " at ", max(Nmaxlst)[1], " m ")

MaxV1 = max(Nmaxlst)[2]
MaxV2 = max(Nmaxlst)[3]

MaxN1p = max(Nmaxlst)[4]
MaxN2p = max(Nmaxlst)[5]

MaxN1n = max(Nmaxlst)[6]
MaxN2n = max(Nmaxlst)[7]

MaxVb = max(Nmaxlst)[8]
MaxVd = max(Nmaxlst)[9]
MaxVs = max(Nmaxlst)[10]

# =============================================================================
# Graphing
# =============================================================================

# Plotting the datapoints and interpolation because it looks nice
# plt.plot(Vlst1, Nlst1p, color='r')
# plt.plot(Vlst1, Nlst1n, color='r')
# plt.plot(Vlst2, Nlst2p, "o", color='r')
# plt.plot(Vlst2, Nlst2n, "o", color='r')

plt.plot(MaxV1, MaxN1p, label = 'V - n Diagram', color='r')
plt.plot(MaxV1, MaxN1n, color='r')
plt.plot(MaxV2, MaxN2p, "x", color='r')
plt.plot(MaxV2, MaxN2n, "x", color='r')

# Plot formatting
plt.title('V - n Diagram')

plt.xlabel('Flight velocity (EAS) [m/s]')
plt.ylabel('Load factor, n [-]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.axvline(x=MaxVs, color='k', linestyle="-.")
plt.text(5,-1.8,'V_S',rotation=0)
plt.axvline(x=MaxVb, color='k', linestyle="-.")
plt.text(50.1,3.5,'V_B',rotation=0)
plt.axvline(x=V_c, color='k', linestyle="-.")
plt.text(205.1,3.5,'V_C',rotation=0)
plt.axvline(x=MaxVd, color='k', linestyle="-.")
plt.text(300.1,3.5,'V_D',rotation=0)

plt.ylim(-1.5, 4.0)
plt.xlim(0, 350)

# plt.legend(loc = "upper right")

plt.show()

# =============================================================================
# FIN
# =============================================================================

