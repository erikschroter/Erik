# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import math as m
from GlobalMomentofInertia import Ixx
from Definition_stringer_positions import t_wing_box_spar_cap, stringer_distribution
from Buckling_Coefficient_Figures import hinged_edges_function, figure_19_c_simply_supported_function
from Top_Bottom_Skin_Buckling import Top_Bottom_Skin_Buckling
import numpy as np

"""
Created on Mon Nov 30 14:53:19 2020

@author: Erik Schroter
"""

# Front and rear spar height function
taperRatio = 0.3 #[]
rootChord = 11.95 #[m]
wingSpan = 69.92 #[m]

def FrontRearSpar(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    FrontSpar = 0.1347 * localChord
    RearSpar = 0.1091 * localChord
    return FrontSpar, RearSpar

# Local Chord function
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
def SkinBucklingdef(k_c, E, poisson, t, b):
    F_cr = np.pi * k_c * E / (12 * (1 - poisson**2)) * (t/b)**2
    return F_cr
# where 𝑘𝑘𝑐𝑐 may be deduced from Figure 19, and all other symbols have their previously defined meanings.


# Column Buckling of stringers
# 𝐾𝐾 is a factor taking into account the way the end conditions of the column; 𝐾𝐾=1 if both ends are pinned, 𝐾𝐾=4 if both ends are clamped; 𝐾𝐾=1/4 if one end is fixed and one end is free; 1/√𝐾𝐾=0.7 if one end is pinned and one end is free.
def ColBucklingdef(K, E, I, L):
    stress_critical_buckling =  K * np.pi ** 2 * E * I / L ** 2
    return stress_critical_buckling

# Compressive strength failure each component

# =============================================================================
# Web buckling
# =============================================================================
WebPrint=False

# Material Properties
E = 68.8 * 10**9 # Pa
v = 0.33 # -

t_f = t_wing_box_spar_cap # mm
t_r = t_wing_box_spar_cap # mm

sections = [0, 4, 7.00, 11.5, 14, 17.5, 21, 24.5, 26, 28, 29, 31.5, 33, 34.96] # INPUT SECTIONS!

tau_cr_flst = []
tau_cr_rlst = []

for i in range(1, len(sections)):
    y_section = sections[i] - sections[i-1] # m
    if WebPrint==True:
        print("iteration ", i, "section width ", round(y_section, 1))
    y_midspan = (y_section / 2) + sections[i-1] # m
    
    h_f = FrontRearSpar(y_midspan)[0]*1000 # mm
    h_r = FrontRearSpar(y_midspan)[1]*1000 # mm
    
    x_f = y_section*1000 / h_f
    x_r = y_section*1000 / h_r
    if WebPrint==True:
        print("Front Aspect ", x_f)
        print("Rear Aspect ", x_r, "\n")
    
    if x_f < 1 or x_f > 5:
        print("\n !!! UNDEFINED ASPECT RATIO !!! \n Front Aspect Ratio: ",  x_f)
    if x_r < 1 or x_r > 5:
        print("\n !!! UNDEFINED ASPECT RATIO !!! \n Rear Aspect Ratio: ",  x_r)

    
    k_sf = hinged_edges_function(x_f)
    k_sr = hinged_edges_function(x_r)
    
    tau_cr_f = WebBucklingdef(t_f, h_f, k_sf, E, v)/10**6 # MPa
    tau_cr_r = WebBucklingdef(t_r, h_r, k_sr, E, v)/10**6 # MPa

    tau_cr_flst.append(round(tau_cr_f,2))
    tau_cr_rlst.append(round(tau_cr_r,2))

if WebPrint==True:
    print("Web buckling: \n Sections: ", sections, "\n Front Spar: ", tau_cr_flst, "\n Rear Spar: ", tau_cr_rlst)

# =============================================================================
# Skin buckling
# =============================================================================

critical_bottom_stresses_function, critical_top_stresses_function = Top_Bottom_Skin_Buckling(sections,
                                                                                             stringer_distribution)

# Creating plot list

y = [0]
for i in range(round(wingSpan / 2 * 100)):
    new_value = y[i] + 0.01
    y.append(new_value)

plt.plot(y, critical_bottom_stresses_function(y), "b")
plt.plot(y, critical_top_stresses_function(y), "r")

# plot formatting

plt.title('Margin of safety for skin buckling (blue bottom, red top)')

plt.xlabel('Spanwise location [m]')
plt.ylabel('Margin of safety')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()

# =============================================================================
# Column buckling
# =============================================================================

sweepAngleWing = 28.77 * m.pi / 180 #rads
LStringer = 6.99

Ixx = Ixx(0)

bucklingStress = ColBucklingdef(1, 68.9 * 10**9, 3882083.333 ** (10^-12), LStringer)
