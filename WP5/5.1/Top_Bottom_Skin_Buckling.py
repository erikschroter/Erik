# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from Definition_stringer_positions import t_wing_box_skin, stringer_distribution
from Buckling_Coefficient_Figures import figure_19_c_simply_supported_function
from Distance_stringers import Distance_Stringers
from scipy.interpolate import interp1d
import sys
sys.setrecursionlimit(10 ** 7)

"""
Created on Thursday Dec 10 16:56:32 2020

@author: Christoph Pabsch
"""

taperRatio = 0.3  # []
rootChord = 11.95  # [m]
wingSpan = 69.92  # [m]

# =============================================================================
# Top and Bottom panel buckling (Reference from reader page 680)
# =============================================================================
E = 68.8 * 10 ** 9  # Pa
v = 0.33  # -

t = t_wing_box_skin  # mm

# sections = [0, 2, 4, 6.99, 11.5, 13.98, 20.98, 27.97, 34.96] # INPUT SECTIONS!
# sections = [0, 4, 6, 6.99, 11, 11.5, 12, 14, 14.5, 20.98, 22.1, 24, 27.97, 32, 33.2, 34.96]  # INPUT SECTIONS!


# Function to calculate Top and Bottom Skin Buckling from rib and stringer distribution

def Top_Bottom_Skin_Buckling(section, stringer_distribution):
    critical_bottom_stresses = []
    critical_top_stresses = []

    # Define the critical skin stresses for all inter-rib positions

    for i in range(1, len(section)):
        # Define inter-rib sections
        y_section = section[i] - section[i - 1]  # m
        y_midspan = (y_section / 2) + section[i - 1]  # m
        spanwise_location = y_midspan

        # Obtain inter-stringer distances
        distance_top_stringers, distance_bottom_stringers = Distance_Stringers(stringer_distribution, spanwise_location)

        top_stresses = []
        bottom_stresses = []
        critical_top_stress = 0
        critical_bottom_stress = 0

        # Calculate top skin panel stresses for all possible locations
        for n in range(len(distance_top_stringers)):
            b = distance_top_stringers[n][0]
            a = 1000 * y_section
            k_c = figure_19_c_simply_supported_function(a / b)
            top_stresses.append((3.14159265 ** 2 * k_c * E / (12 * (1 - v ** 2)) * (t / b) ** 2))
        critical_top_stress = min(top_stresses)

        # Calculate bottom skin panel stresses for all possible locations
        for n in range(len(distance_bottom_stringers)):
            b = distance_bottom_stringers[n][0]
            a = 1000 * y_section
            k_c = figure_19_c_simply_supported_function(a / b)
            bottom_stresses.append((3.14159265 ** 2 * k_c * E / (12 * (1 - v ** 2)) * (t / b) ** 2))
        critical_bottom_stress = min(bottom_stresses)

        # Determine most critical buckling stress for top and bottom skin panel in inter-rib section
        critical_bottom_stresses.append(critical_bottom_stress)
        critical_top_stresses.append(critical_top_stress)

    # Define lists for final interpolation
    spanwise_location_stress = []
    bottom_stress_list = []
    top_stress_list = []

    for i in range(len(section) - 1):
        spanwise_location_stress.append(section[i])
        spanwise_location_stress.append(section[i + 1] - 0.001)
        bottom_stress_list.append(critical_bottom_stresses[i])
        bottom_stress_list.append(critical_bottom_stresses[i])
        top_stress_list.append(critical_top_stresses[i])
        top_stress_list.append(critical_top_stresses[i])

    # Obtain functions for critical top and bottom skin panel buckling
    critical_bottom_stresses_function = interp1d(spanwise_location_stress, bottom_stress_list, kind="linear",
                                                 fill_value="extrapolate")
    critical_top_stresses_function = interp1d(spanwise_location_stress, top_stress_list, kind="linear",
                                              fill_value="extrapolate")

    return critical_bottom_stresses_function, critical_top_stresses_function


# critical_bottom_stresses_function, critical_top_stresses_function = Top_Bottom_Skin_Buckling(sections,
#                                                                                             stringer_distribution)
"""
# Creating plot list

y = [0]
for i in range(round(wingSpan / 2 * 100)):
    new_value = y[i] + 0.01
    y.append(new_value)

plt.plot(y, critical_bottom_stresses_function(y), "b")
plt.plot(y, critical_top_stresses_function(y), "r")

# plot formatting

plt.title('Critical skin buckling stresses (blue bottom, red top)')

plt.xlabel('Spanwise location [m]')
plt.ylabel('Stress [Pa]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()
"""