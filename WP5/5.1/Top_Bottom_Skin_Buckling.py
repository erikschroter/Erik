# -*- coding: utf-8 -*-


import math as m
from GlobalMomentofInertia import Ixx
from Definition_stringer_positions import t_wing_box_skin, stringer_distribution
from Buckling_Coefficient_Figures import figure_19_c_simply_supported_function
from Distance_stringers import Distance_Stringers
import sys

sys.setrecursionlimit(10**7)


"""
Created on Thursday Dec 10 16:56:32 2020

@author: Christoph Pabsch
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
    shear_cr = (np.pi ** 2 * k_s * E / (12 * (1 - poisson ** 2))) * (t / b) ** 2
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
# Top and Bottom panel buckling (Reference from reader page 680)
# =============================================================================
E = 68.8 * 10**9 # Pa
v = 0.33 # -

t = t_wing_box_skin  # mm

sections = [0, 2, 4, 6.99, 11.5, 13.98, 20.98, 27.97, 34.96] # INPUT SECTIONS!

critical_bottom_stresses = []
critical_top_stresses = []

for i in range(1, len(sections)):
    y_section = sections[i] - sections[i-1]  # m
    y_midspan = (y_section / 2) + sections[i-1]  # m
    spanwise_location = y_midspan

    distance_top_stringers, distance_bottom_stringers = Distance_Stringers(stringer_distribution, spanwise_location)

    top_stresses = []
    bottom_stresses = []
    critical_top_stress = 0
    critical_bottom_stress = 0

    for n in range(len(distance_top_stringers)):
        b = distance_top_stringers[n][0]
        a = 1000*y_section
        print(a/b)
        k_c = figure_19_c_simply_supported_function(a/b)
        print(k_c)
        top_stresses.append((3.14159265**2 * k_c * E / (12 * (1 - v**2)) * (t/b)**2))
    critical_top_stress = min(top_stresses)

    for n in range(len(distance_bottom_stringers)):
        b = distance_bottom_stringers[n][0]
        a = 1000*y_section
        k_c = figure_19_c_simply_supported_function(a/b)
        bottom_stresses.append((3.14159265**2 * k_c * E / (12 * (1 - v**2)) * (t/b)**2))
    critical_bottom_stress = min(bottom_stresses)

    critical_bottom_stresses.append(critical_bottom_stress)
    critical_top_stresses.append(critical_top_stress)

print(critical_bottom_stresses)
print(critical_top_stresses)
print(min(critical_bottom_stresses))
print(min(critical_top_stresses))


