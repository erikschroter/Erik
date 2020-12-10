# -*- coding: utf-8 -*-


import math as m
from GlobalMomentofInertia import Ixx
"""
Created on Mon Nov 30 14:53:19 2020

@author: Erik Schroter
"""

# Front and rear spar height function

import numpy as np
from Buckling_Coefficient_Figures import clamped_edges_callable_function

taperRatio = 0.3 #[]
rootChord = 11.95 #[m]
wingSpan = 69.92 #[m]


def FrontRearSpar(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    FrontSpar = 0.1347 * localChord
    RearSpar = 0.1091 * localChord
    return FrontSpar, RearSpar

def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord

# Margin of Safety Function
def MoSdef(failure_stress, applied_stress):
    MoS = failure_stress / applied_stress
    if MoS < 1:
        print("\n !!! STRUCTURAL FAILURE !!! \n Margin of Safety: ",  MoS)
    return MoS

# Shear Buckling in spar webs:
# where 𝑡 is the thickness of the spar, 𝑏 the short side of the plate, 𝑘𝑠 a coefficient that depends on the plate aspect ratio 𝑎 /𝑏 (as depicted in Figure 17), and is obtained from Figure 18, and the remaining symbols are the familiar material properties.
def WebBucklingdef(t, b, k_s, E, poisson):
    shear_cr = np.pi ** 2 * k_s * E / (12 * (1 - poisson ** 2)) * (t / b) ** 2
    return shear_cr

# maximum shear stress due to the shear force in the webs
# based on your engineering judgement, choose a reasonable factor 𝑘𝑘𝑣𝑣 such that
def MaxSheardef(k_v, shear_avg):
    shear_max = k_v * shear_avg
    return shear_max

# where the average shear stress in the spar webs due to the shear load is equal to
# where 𝑉 is the shear force at the considered spanwise station of the wing, ℎ𝑓 is the height of the front spar, 𝑡𝑡𝑓 is the thickness of the front spar, ℎ𝑟𝑟 is the height of the rear spar, and 𝑡𝑡𝑟𝑟 is the thickness of the rear spar
def AvgSheardef(V, h_f, t_f, h_r, t_r):
    # only for two spars!!!; requires generalised version for more than 2 spars
    shear_avg = V / (h_f * t_f + h_r * t_r)
    return shear_avg


# shear stress due to torsion still needs to be superimposed to shear_max
# In case you design a multi-cell, the shear flow distribution is computed simultaneously with the torsional stiffness, as explained in Section D.1.3.
# In case of a single-cell, it can be straightforwardly computed from the shear flow distribution due to torsion,
# where 𝐴𝑖 is the enclosed area of the wing box cross section.
def TorsionalSheardef(T, A_i):
    q = T / (2 * A_i)
    return q
# The sum of the maximum shear stress due to the shear force and the shear stress due to torsion can then be compared with the critical buckling stress.


# Skin Buckling wing skin


# Column Buckling of stringers
# 𝐾𝐾 is a factor taking into account the way the end conditions of the column; 𝐾𝐾=1 if both ends are pinned, 𝐾𝐾=4 if both ends are clamped; 𝐾𝐾=1/4 if one end is fixed and one end is free; 1/√𝐾𝐾=0.7 if one end is pinned and one end is free.
def ColBucklingdef(K, E, I, L):
    stress_critical_buckling =  K * np.pi ** 2 * E * I / L ** 2
    return stress_critical_buckling

# Compressive strength failure each component

# =============================================================================
# Web buckling
# =============================================================================
E = 68.8 * 10^9 # Pa
v = 0.33

f
    localChord(y_span)
    



# =============================================================================
# Column buckling
# =============================================================================

sweepAngleWing = 28.77 * m.pi / 180 #rads
LStringer = 6.99

Ixx = Ixx(0)

bucklingStress = ColBucklingdef(1, 68.9 * 10**9,