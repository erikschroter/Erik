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

figure_19_a_clamped = [(1, 15), (1.1, 13.8), (1.2, 13), (1.25, 12.5), (1.5, 11.5), (1.66, 11.3), (1.75, 10.7), (2, 10.3),
                 (2.25, 10.1), (2.5, 9.9), (2.75, 9.8), (3, 9.8), (3.5, 9.7), (4, 9.6), (5, 9.6)]
x_clamped = []
y_clamped = []
for i in range(len(clamped_edges)):
    x_clamped.append(clamped_edges[i][0])
    y_clamped.append(clamped_edges[i][1])
clamped_edges_function = sp.interpolate.interp1d(x_clamped, y_clamped, kind="quadratic", fill_value="extrapolate")


def clamped_edges_callable_function(x):
    return clamped_edges_function(x)


def hinged_edges_callable_function(x):
    return hinged_edges_function(x)


"""
plt.plot(x_hinged, clamped_edges_function(x_hinged), "-")
plt.plot(x_hinged, hinged_edges_function(x_hinged), "-")

# plot formatting

plt.title('Spanwise C_y')

plt.xlabel('Spanwise location [m]')
plt.ylabel('C_y [mm]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()"""
