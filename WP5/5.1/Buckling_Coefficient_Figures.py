"""Function to calculate values from figure 18
If questions, ask Christoph Pabsch"""

import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt

clamped_edges = [(1, 15), (1.1, 13.8), (1.2, 13), (1.25, 12.5), (1.5, 11.5), (1.66, 11.3), (1.75, 10.7), (2, 10.3),
                 (2.25, 10.1), (2.5, 9.9), (2.75, 9.8), (3, 9.8), (3.5, 9.7), (4, 9.6), (5, 9.6)]
x_clamped = []
y_clamped = []
for i in range(len(clamped_edges)):
    x_clamped.append(clamped_edges[i][0])
    y_clamped.append(clamped_edges[i][1])
clamped_edges_function = sp.interpolate.interp1d(x_clamped, y_clamped, kind="quadratic", fill_value="extrapolate")

hinged_edges = [(1, 9.8), (1.1, 9), (1.2, 8.3), (1.25, 8), (1.4, 7.3), (1.5, 7.1), (1.66, 6.7), (1.75, 6.6), (2, 6.4),
                (2.25, 6.2), (2.5, 6), (2.75, 5.9), (3, 5.85), (3.5, 5.8), (4, 5.75), (5, 5.6)]
x_hinged = []
y_hinged = []
for i in range(len(hinged_edges)):
    x_hinged.append(hinged_edges[i][0])
    y_hinged.append(hinged_edges[i][1])
hinged_edges_function = sp.interpolate.interp1d(x_hinged, y_hinged, kind="quadratic", fill_value="extrapolate")

figure_19_a_clamped = [(0.7, 15.1), (0.8, 12), (0.9, 10.4), (1, 10.3), (1.1, 10.4), (1.3, 9), (1.5, 8.5), (1.65, 8.3),
                 (1.8, 8.4), (1.9, 8.15), (2, 8), (2.2, 7.8), (2.4, 7.8), (2.6, 7.65), (3, 7.55), (3.4, 7.45), (3.7, 7.4),
                        (4, 7.3), (4.3, 7.4), (4.6, 7.3),(5, 7.2)]
x_a_clamped = []
y_a_clamped = []
for i in range(len(figure_19_a_clamped)):
    x_a_clamped.append(figure_19_a_clamped[i][0])
    y_a_clamped.append(figure_19_a_clamped[i][1])
figure_19_a_clamped_function = sp.interpolate.interp1d(x_a_clamped, y_a_clamped, kind="quadratic", fill_value="extrapolate")

figure_19_c_simply_supported = [(0.4, 8.6), (0.55, 6), (0.7, 4.5), (0.8, 4.15), (0.9, 4.08), (1.0, 4.0),
                 (1.2, 4.1), (1.45, 4.6), (1.6, 4.15), (1.75, 4.1), (2.0, 4.0), (2.2, 4.0), (2.3, 4.08), (2.45, 4.15), (3.0, 4.0),
                        (3.45, 4.08), (4.0, 4.0), (4.5, 4.05), (5.0, 4.0), (6.0, 4.0), (7.0, 4.0), (10.0, 4.0), (35.0, 4.0),]
x_c_simply_supported = []
y_c_simply_supported = []
for i in range(len(figure_19_c_simply_supported)):
    x_c_simply_supported.append(figure_19_c_simply_supported[i][0])
    y_c_simply_supported.append(figure_19_c_simply_supported[i][1])
figure_19_c_simply_supported_function = sp.interpolate.interp1d(x_c_simply_supported, y_c_simply_supported, kind="quadratic", fill_value="extrapolate")

def clamped_edges_callable_function(x):
    return clamped_edges_function(x)


def hinged_edges_callable_function(x):
    return hinged_edges_function(x)


def figure_19_a_clamped_callable_function(x):
    return figure_19_a_clamped_function(x)


def figure_19_c_simply_supported_callable_function(x):
    return figure_19_c_simply_supported_function(x)


"""
plt.plot(x_a_clamped, figure_19_a_clamped_function(x_a_clamped), "-")

# plot formatting

plt.title('Spanwise C_y')

plt.xlabel('Spanwise location [m]')
plt.ylabel('C_y [mm]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()
"""