# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:19:16 2020

@author: Erik Schroter
"""


from CS25Loads import DesignGustVelocity, GustVelocity
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import math

# =============================================================================
# Function defintions
# =============================================================================

# Density
def ISA(h):
    # Needed constants for the ISA calculations
    g_0 = 9.80665  # m/s
    R = 287.0  # J/kgK
    T_0 = 288.15  # K
    p_0 = 101325.0  # Pa
    h_0 = 0  # m

    # Temperature gradients (K/m)
    a_1 = -0.0065
    a_2 = 0
    a_3 = 0.001
    a_4 = 0.0028
    a_5 = 0
    a_6 = -0.0028
    a_7 = -0.002

    # Temperature calculations with the new altitude input

    if h <= 11000:
        T_1 = (T_0 + a_1 * (h - h_0))
        p_1 = (p_0 * ((T_1 / T_0) ** (-((g_0) / (a_1 * R)))))
        rho_1 = (p_1) / (R * T_1)
        rho=rho_1
    else:
        T_1 = T_0 + a_1 * (11000 - h_0)
        p_1 = p_0 * ((T_1 / T_0) ** (-((g_0) / (a_1 * R))))

    if h <= 20000 and h > 11000:
        T_2 = T_1 + a_1 * (h - 11000)
        p_2 = p_1 * (math.exp((-(g_0) / (R * T_2)) * (h - 11000)))
        rho_2 = (p_2) / (R * T_2)
        rho=rho_2
    else:
        T_2 = T_1 + a_2 * (20000 - 11000)
        p_2 = p_1 * (math.exp((-(g_0) / (R * T_2)) * (20000 - 11000)))

    if h <= 32000 and h > 20000:
        T_3 = T_2 + a_3 * (h - 20000)
        p_3 = p_2 * ((T_3 / T_2) ** (-((g_0) / (a_3 * R))))
        rho_3 = (p_3) / (R * T_3)
        rho=rho_3
    else:
        T_3 = T_2 + a_3 * (32000 - 20000)
        p_3 = p_2 * ((T_3 / T_2) ** (-((g_0) / (a_3 * R))))

    if h <= 47000 and h > 32000:
        T_4 = T_3 + a_4 * (h - 32000)
        p_4 = p_3 * ((T_4 / T_3) ** (-((g_0) / (a_4 * R))))
        rho_4 = (p_4) / (R * T_4)
        rho=rho_4
    else:
        T_4 = T_3 + a_4 * (47000 - 32000)
        p_4 = p_3 * ((T_4 / T_3) ** (-((g_0) / (a_4 * R))))

    if h <= 51000 and h > 47000:
        T_5 = T_4 + a_5 * (h - 47000)
        p_5 = p_4 * (math.exp((-(g_0) / (R * T_5)) * (h - 47000)))
        rho_5 = (p_5) / (R * T_5)
        rho=rho_5
    else:
        T_5 = T_4 + a_5 * (51000 - 47000)
        p_5 = p_4 * (math.exp((-(g_0) / (R * T_2)) * (51000 - 47000)))

    if h <= 71000 and h > 51000:
        T_6 = T_5 + a_6 * (h - 51000)
        p_6 = p_5 * ((T_6 / T_5) ** (-((g_0) / (a_6 * R))))
        rho_6 = (p_6) / (R * T_6)
        rho=rho_6
    else:
        T_6 = T_5 + a_6 * (71000 - 51000)
        p_6 = p_5 * ((T_6 / T_5) ** (-((g_0) / (a_6 * R))))

    if h <= 86000 and h >= 71000:
        T_7 = T_6 + a_7 * (h - 71000)
        p_7 = p_6 * ((T_7 / T_6) ** (-((g_0) / (a_7 * R))))
        rho_7 = (p_7) / (R * T_7)
        rho=rho_7
    else:
        T_7 = T_6 + a_7 * (86000 - 71000)
        p_7 = p_6 * ((T_7 / T_6) ** (-((g_0) / (a_7 * R))))

    if h > 86000:
        print('You have reached space sadly, we cannot speak of any pressure here try again.')

    return rho

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

# Computation of load factor change
def V_TAS(rho, rho_0, V_EAS):
    V_TAS = V_EAS * (rho/rho_0)**-0.5
    return V_TAS

def omega(V_TAS, H):
    omega = np.pi * V_TAS / H
    return omega

def timeconstant(Wloading, dCLdalpha, rho, V_TAS, g):
    timeconstant = 2 * Wloading / (dCLdalpha * rho * V_TAS * g)
    return timeconstant

def deltaN(U_ds, g, omega, t, timeconstant):
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
alt_lst = []

for i in range(9900, 11001):
    MAC = 8.51495 # m
    
    rho_0 = 1.225 # kg/m^3
    V_c = 232.46 # m/s
    dCLdalpha = 0.095 * 180/ np.pi # 1/rad
    S = 543.25 # m^2

    altitude = i # m (the lower increases load factor)
    MTOW = 304636.2789 # kg
    rho = ISA(altitude) # kg/m^3
    C_L = 1.3962 # (maximum C_L with flaps retracted)
    
    MLW = 0.85 * MTOW # kg (!!!CHECK THIS!!!)
    MZFW = 161394.7263 # kg
    
    OEW = 147780.3631 # kg
    
    Zmo = 40000 * 0.3048 # ft (-> m)
    Fgz = 1 - Zmo / 76200
    
    V = V_c # m/s
    
    H = H(MAC)
    debug("H", H, dbug)
    
    U_ref = U_ref(altitude, False)
    debug("Uref", U_ref, dbug)
    
    V_s1 = V_s1(MTOW, rho_0, S, C_L) # (EAS)
    debug("V_s1", V_s1, dbug)
    
    V_cEAS = V_cEAS(rho, rho_0, V_c)
    debug("Vc", V_cEAS, dbug)
    
    Wloading = Wloading(MZFW, S)
    debug("W/S", Wloading, dbug)
    
    Kg = Kg(Wloading, rho, MAC, dCLdalpha, 9.80665)[1]
    debug("Kg", Kg, dbug)
    
    Vb = Vb(V_s1, Kg, rho_0, U_ref, V_cEAS, dCLdalpha, Wloading)
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
    
    # Calculate load factor change deltaN
    omega = omega(V, H)
    debug("omega", omega, dbug)
    
    t = np.arange(0, 2*np.pi/omega + 1, 0.01)
    debug("t", t, dbug)
    
    timeconstant = timeconstant(Wloading, dCLdalpha, rho, V, 9.80665)
    debug("lambda", timeconstant, dbug)
    
    deltaN = deltaN(V_TAS(rho, rho_0, U_ds), 9.80655, omega, t, timeconstant)
    debug("deltaN", deltaN, dbug)
    
    
    print(max(deltaN))
    

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
plt.plot(t, h(t), "-")
plt.plot(t, i(t), "-")


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

