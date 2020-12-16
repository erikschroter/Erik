# -*- coding: utf-8 -*-
Runtime_forever=True
import os
import sys
import matplotlib.pyplot as plt
import math as m
from GlobalMomentofInertia import Ixx
from Definition_stringer_positions import t_wing_box_spar_cap, stringer_distribution, t_wing_box_skin, a_stringer, h_stringer, t_stringer
from Buckling_Coefficient_Figures import hinged_edges_function, figure_19_c_simply_supported_function
from Top_Bottom_Skin_Buckling import Top_Bottom_Skin_Buckling
from Rib_Sections_Definition import sections


directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1,directory)
from shearInWebs import maxShear, scipyMaxShear
from Shear_from_torque import shear_stress_from_torque_positive_function as shear_stress_torq_front, shear_stress_from_torque_negative_function as shear_stress_torq_rear

import scipy as sp
from scipy import integrate
from scipy.interpolate import interp1d
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

# rib_spacing = 0.61
# sections = np.arange(0, 34.96, 0.61)

# req_rib_location = np.array([4, 6, 11, 11.5, 12, 14, 14.5, 22.1, 24, 24.2, 32, 34.96])

# sections = np.append(sections, req_rib_location)
# sections = np.unique(sections)
# sections = [4.0, 4.5, 5.0, 5.5, 6.0, 6.714285714285714, 7.428571428571429, 8.142857142857142, 8.857142857142858, 9.571428571428571, 10.285714285714285, 11.0, 11.5, 12.0, 12.666666666666666, 13.333333333333334, 14.0, 14.5, 15.585714285714285, 16.67142857142857, 17.757142857142856, 18.84285714285714, 19.92857142857143, 21.014285714285716, 22.1, 22.733333333333334, 23.366666666666667, 24.0, 24.2, 25.5, 26.8, 28.1, 29.4, 30.7, 32.0, 32.986666666666665, 33.973333333333336, 34.96]

t_f = t_wing_box_spar_cap # mm # CHANGE IN DEFINITION STRINGER POSITION FILE
t_r = t_wing_box_spar_cap # mm

y_mid_seg_lst = []

tau_cr_flst = []
tau_cr_rlst = []

y_section_lst = []

for i in range(1, len(sections)):
    y_section = sections[i] - sections[i-1] # m
    if WebPrint==True:
        print("iteration ", i, "section width ", round(y_section, 1))
    y_midspan = (y_section / 2) + sections[i-1] # m
    
    y_mid_seg_lst.append(y_midspan-(y_section/2))
    y_mid_seg_lst.append(y_midspan+(y_section/2)-0.01)
    
# =============================================================================
#     FOR COLUMN BUCKLING
    y_section_lst.append(y_section)
    y_section_lst.append(y_section)
# =============================================================================
    
    h_f = FrontRearSpar(y_midspan)[0]*1000 # mm
    h_r = FrontRearSpar(y_midspan)[1]*1000 # mm
    
    if y_section*1000 >= h_f:
        x_f = y_section*1000 / h_f
    elif y_section*1000 < h_f:
        x_f = h_f/(y_section*1000)

    if y_section*1000 >= h_r:
        x_r = y_section*1000 / h_r
    elif y_section*1000 < h_r:
        x_r = h_r /(y_section*1000)
        
    if WebPrint==True:
        print("Front Aspect ", x_f)
        print("Rear Aspect ", x_r, "\n")
    
    if x_f < 1 or x_f > 5:
        print("\n !!! UNDEFINED ASPECT RATIO !!! \n Front Aspect Ratio: ",  x_f)
    if x_r < 1 or x_r > 5:
        print("\n !!! UNDEFINED ASPECT RATIO !!! \n Rear Aspect Ratio: ",  x_r)

    
    k_sf = hinged_edges_function(x_f)
    k_sr = hinged_edges_function(x_r)
    
    if y_section*1000 >= h_f:
        tau_cr_f = WebBucklingdef(t_f, h_f, k_sf, E, v)/10**6 # MPa
    elif y_section*1000 < h_f:
        tau_cr_f = WebBucklingdef(t_f, y_section*1000, k_sf, E, v)/10**6 # MPa

    if y_section*1000 >= h_r:
        tau_cr_r = WebBucklingdef(t_r, h_r, k_sr, E, v)/10**6 # MPa
    elif y_section*1000 < h_r:
        tau_cr_r = WebBucklingdef(t_r, y_section*1000, k_sr, E, v)/10**6 # MPa

    tau_cr_flst.append(round(tau_cr_f, 2))
    tau_cr_flst.append(round(tau_cr_f, 2))
    tau_cr_rlst.append(round(tau_cr_r, 2))
    tau_cr_rlst.append(round(tau_cr_r, 2))

if WebPrint==True:
    print("Web buckling: \n Sections: ", sections, "\n Front Spar: ", tau_cr_flst, "\n Rear Spar: ", tau_cr_rlst)

# Margin of Safety

web_buckling_critical_f = interp1d(y_mid_seg_lst, tau_cr_flst, kind="linear", fill_value="extrapolate")
web_buckling_critical_r = interp1d(y_mid_seg_lst, tau_cr_rlst, kind="linear", fill_value="extrapolate")

y = 0
y_list = []
Web_Margin_of_Safety_List_Front = []
Web_Margin_of_Safety_List_Rear = []
for i in range(int(wingSpan/2*100)):
    Maximum_Stress_from_shear = scipyMaxShear(y)
    Maximum_Stress_from_torque_front = shear_stress_torq_front(y)
    Maximum_Stress_from_torque_rear = shear_stress_torq_rear(y)
    Critical_Web_Buckling_Front = 10**6 * web_buckling_critical_f(y)
    Critical_Web_Buckling_Rear = 10**6 * web_buckling_critical_r(y)
    y_list.append(y)
    Web_Margin_of_Safety_List_Front.append(Critical_Web_Buckling_Front/(Maximum_Stress_from_shear+Maximum_Stress_from_torque_front))
    Web_Margin_of_Safety_List_Rear.append(Critical_Web_Buckling_Rear/(Maximum_Stress_from_shear-Maximum_Stress_from_torque_rear))
    y = y + 0.01

web_buckling_margin_of_safety_f = interp1d(y_list, Web_Margin_of_Safety_List_Front, kind="linear", fill_value="extrapolate")
web_buckling_margin_of_safety_r = interp1d(y_list, Web_Margin_of_Safety_List_Rear, kind="linear", fill_value="extrapolate")

# print(web_buckling_margin_of_safety_f)
# print(web_buckling_margin_of_safety_r)

# Plotting

plt.plot(y_list, Web_Margin_of_Safety_List_Rear, "b")
plt.plot(y_list, Web_Margin_of_Safety_List_Front, "r")

# plot formatting

plt.title('Web Margin of Safety (blue rear, red front)')

plt.xlabel('Spanwise location [m]')
plt.ylabel('Web Margin of safety')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')
plt.ylim(-1,6)

plt.show()
"""
# Plotting

plt.plot(y_mid_seg_lst, tau_cr_flst, "r")
plt.plot(y_mid_seg_lst, tau_cr_rlst, "b")

# plot formatting

plt.title('Critical web buckling stresses (blue rear, red front)')

plt.xlabel('Spanwise location [m]')
plt.ylabel('Stress [MPa]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()
"""
# =============================================================================
# Skin buckling
# =============================================================================
if Runtime_forever==True:
    from maximum_compressive_stress import maximum_compressive_stress_bottom, column_maximum_compressive_stress_bottom
    from maximum_compressive_stress_top import maximum_compressive_stress_top, column_maximum_compressive_stress_top

if Runtime_forever==True:
    critical_bottom_stresses_function, critical_top_stresses_function, y_critical_bottom_stresses_function, y_critical_top_stresses_function = Top_Bottom_Skin_Buckling(sections, stringer_distribution)
    

    # Creating plot list
    
    y = [0]

    for i in range(0, round(wingSpan / 2) * 100):
        new_value = y[i] + 0.01
        y.append(new_value)


    plt.plot(y, critical_bottom_stresses_function(y)/(1000*maximum_compressive_stress_bottom(y)), "b")
    plt.plot(y, critical_top_stresses_function(y)/(1000*maximum_compressive_stress_top(y)), "r")

    MoSBottomSkin = []
    MoSTopSkin = []
    yList1=[]
    for j in range(0, round(wingSpan / 2) * 100):
        yList1.append(j/100)
        MoSBottomSkin.append(critical_bottom_stresses_function(j /100) / (1000 * maximum_compressive_stress_bottom(j/100)))
        MoSTopSkin.append(critical_top_stresses_function(j/100) / (1000 * maximum_compressive_stress_top(j/100)))


    # plot formatting
    
    plt.title('Margin of safety for skin buckling stresses (blue bottom, red top)')
    
    plt.xlabel('Spanwise location [m]')
    plt.ylabel('Margin of safety')
    
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.ylim(-1,6)
    
    plt.show()

skin_buckling_margin_of_safety_t = interp1d(yList1, MoSTopSkin, kind="linear", fill_value="extrapolate")
skin_buckling_margin_of_safety_b = interp1d(yList1, MoSBottomSkin, kind="linear", fill_value="extrapolate")
# =============================================================================
# Column buckling
# =============================================================================

sweepAngleWing = 28.77 * m.pi / 180  # rads
LStringer = y_section_lst / np.cos(sweepAngleWing)

Ixx_stringer = h_stringer ** 3 * t_stringer / 12 + 2 * a_stringer * t_stringer** 3 / 12 + 2 * a_stringer * t_stringer * (h_stringer/2 + t_stringer/2)**2

bucklingStress = ColBucklingdef(1, 68.9 * 10 ** 9, Ixx_stringer * (10 ** -12), LStringer)


col_buckling_critical = interp1d(y_mid_seg_lst, bucklingStress, kind="linear", fill_value="extrapolate")

y = 0
y_list = []
col_buckling_lst_top = []
col_buckling_lst_bottom = []

if Runtime_forever==True:

    for i in range(int(wingSpan/2*100)):
        Failure_col_buckling = col_buckling_critical(y)
        
        Applied_col_bottom = column_maximum_compressive_stress_bottom(y)
        Applied_col_top = column_maximum_compressive_stress_top(y)
        y_list.append(y)
        col_buckling_lst_top.append(Failure_col_buckling/Applied_col_top)
        col_buckling_lst_bottom.append(Failure_col_buckling/Applied_col_bottom)
        y = y + 0.01
    
    col_buckling_margin_of_safety_top = interp1d(y_list, col_buckling_lst_top, kind="linear", fill_value="extrapolate")
    col_buckling_margin_of_safety_bottom = interp1d(y_list, col_buckling_lst_bottom, kind="linear", fill_value="extrapolate")
    
    # Plotting
    
    plt.plot(y_list, col_buckling_lst_bottom, "b")
    plt.plot(y_list, col_buckling_lst_top, "r")
    
    # plot formatting
    
    plt.title('Margin of safety for column buckling (blue bottom, red top)')
    
    plt.xlabel('Spanwise location [m]')
    plt.ylabel('Margin of safety')
    
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.ylim(0, 30)
    
    plt.show()


# =============================================================================
# Design options
# =============================================================================


print("\n\nDESIGN OPTION: \n\n t_spar: ", t_wing_box_spar_cap, "||| rib sections: ", sections, "||| stringer distances: ", stringer_distribution, "||| width stringer: ", a_stringer, "||| height stringer: ", h_stringer, "||| t_stringer: ", t_stringer, "||| t_skin: ", t_wing_box_skin, "||| LStringer: ", LStringer)


# =============================================================================
#AVERAGE MoS CALCULATION
# =============================================================================

consideredLengthHalfWingSpan = wingSpan /2 * 0.9
from maximum_compressive_stress import maximum_compressive_stress_bottom, column_maximum_compressive_stress_bottom
from maximum_compressive_stress_top import maximum_compressive_stress_top, column_maximum_compressive_stress_top
critical_bottom_stresses_function, critical_top_stresses_function, y_critical_bottom_stresses_function, y_critical_top_stresses_function = Top_Bottom_Skin_Buckling(sections, stringer_distribution)

resolution = 100


#Average MoS for web buckling
frontWebMoS = 0
rearWebMoS = 0
for i in range(0, round(consideredLengthHalfWingSpan *resolution)):
    frontWebMoS += web_buckling_margin_of_safety_f(i/resolution)
    rearWebMoS += web_buckling_margin_of_safety_r(i/resolution)

averageFrontWebMoS = frontWebMoS / (round(consideredLengthHalfWingSpan *resolution) + 1)
averageRearWebMoS = rearWebMoS / (round(consideredLengthHalfWingSpan *resolution) + 1)


#Average MoS for skin buckling
topSkinMoS = 0
bottomSkinMoS = 0

for i in range(0, round(consideredLengthHalfWingSpan *resolution)):
    topSkinMoS += skin_buckling_margin_of_safety_t(i / resolution)
    bottomSkinMoS += skin_buckling_margin_of_safety_b(i / resolution)

averageTopSkinMoS = topSkinMoS / (round(consideredLengthHalfWingSpan *resolution) + 1)
averageBottomSkinMoS = bottomSkinMoS / (round(consideredLengthHalfWingSpan *resolution) + 1)



#Average MoS for column buckling
topColumnMoS = 0
bottomColumnMoS = 0

for i in range(0, round(consideredLengthHalfWingSpan * resolution)):
    topColumnMoS += col_buckling_margin_of_safety_top(i / resolution)
    bottomColumnMoS += col_buckling_margin_of_safety_bottom(i / resolution)

averageTopColumn = topColumnMoS / (round(consideredLengthHalfWingSpan * resolution) + 1)
averageBottomColumn = bottomColumnMoS / (round(consideredLengthHalfWingSpan * resolution) + 1)





print("average MoS Front Web : ", averageFrontWebMoS)
print("average MoS Rear Web : ", averageRearWebMoS)

print("average MoS Top Skin : ", averageTopSkinMoS)
print("average MoS Bottom Skin :  ", averageBottomSkinMoS)

print("average MoS Top Column : ", averageTopColumn)
print("average MoS Bottom Column : ", averageBottomColumn)