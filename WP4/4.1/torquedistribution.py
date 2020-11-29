# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:47:29 2020

@author: Erik Schroter, Christoph Pabsch
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from ReadingXFLRresults import ReadingXFLR
from TorqueFromThrust import TorqueFromThrust
from scipy import integrate
from scipy.interpolate import interp1d
from ISAdef import ISA

# =============================================================================
# Torque Distribution
# =============================================================================

MTOW = 304636.2789 # kg
MZFW = 161394.7263 # kg
OEW = 147780.3631 # kg

# Definition Load Case Scenario

Thrust_Setting = 100  # from 0 to 100 in percent
Weight_Setting = MTOW * 9.81  # N
n_Setting = -1.5
altitude = 0  # ft

alt = altitude * 0.3048
rho, T = ISA(alt)

def torquedistribution(file, rho, v, span, accuracy, y_thrust, thrust_setting, n, weight):

    # The code below fetches the various aerodynamic data from the XFLR analysis
    CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR(file)
    M_thrust, Misc = TorqueFromThrust(0.367, 0.01254)  # 1106769.7 was old value if needed
    
    # setting variables for wing dimensions and flight conditions
    rho=rho
    v=v
    flexaxis = 0.367
    bprime = 1
    y_thrust = y_thrust
    M_thrust = M_thrust
    
    # create array for pure thrust torque
    Tlst = np.append(np.append([0]*(len(yspan)-3), np.array([M_thrust]*1)), [0]*2)
    x_T = np.append(np.linspace(0, y_thrust, len(yspan)-2), [y_thrust + 0.1, span/2])

    # determining what variables need to be on the x, and y -axis
    q = 1/2 * rho * (v**2)
    x = yspan
    cmlst=[]
    Mlst=[]
    
    for i in range(len(Cl)):
        cmlst.append(CmAirfquarterchord[i] - Cl[i]*(flexaxis-0.25))
        Mlst.append(cmlst[i]*q*(Chord[i]**2)*bprime)

    # # find the closest y span value for the thrust (higher or lower)
    # closest = min(x, key=lambda x:abs(x-y_thrust))
    # closestindex = x.index(closest)
    
    # for i in range(0, closestindex + 1):
    #     Mlst[i] = Mlst[i] + M_thrust
    
    # interpolating the data in a cubic manner
    g = interp1d(x,Mlst,kind="cubic", fill_value="extrapolate")
    # estimateg, errorg = sp.integrate.quad(g, 0, len(x))
    # h = interp1d(x_T,Tlst,kind="linear", fill_value="extrapolate")

    # determining the factor by which the lift needs to be multiplied

    Llst = []

    for i in range(len(Cl)):
        Llst.append(q * Chord[i] * Cl[i])

    # interpolating the data in a cubic manner
    f = interp1d(x, Llst, kind="cubic", fill_value="extrapolate")

    factor = (n * weight * 0.5) / (sp.integrate.quad(f, 0, span / 2)[0])

    # determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
    xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)

    # superposition of aerodynamic torque and thrust torque

    final_integration_result = []

    # Create list with contribution of aerodynamic torque only

    for j in range(len(xnew)):
        start = xnew[j]
        final_integration_result.append(sp.integrate.quad(g, start, 34.96))

    # Calculate contribution of weight of propulsion group

    W_propulsion_group = 20487.986 * 9.81  # [N]
    root_chord = 11.95  # [m]
    tip_chord = 3.59  # [m]
    span = 69.92  # [m]
    spanwise_position_engine = 11.5  # [m]
    chord_length_engine = root_chord - (root_chord - tip_chord) * spanwise_position_engine / (span / 2)
    T_Weight_pg = - flexaxis * chord_length_engine * W_propulsion_group

    # Calculate contribution of weight of landing gear

    W_landing_gear = 5060.9 * 9.81 # [N]
    d_lg_flexuralaxis = 8.140397 - flexaxis * 10.511222  # [m]
    T_Weight_lg = d_lg_flexuralaxis * W_landing_gear

    # Add contribution of thrust torque for a distance up to 11.5m from the root chord

    for j in range(len(xnew)):
        if xnew[j] < 6:
            torque_aerodynamic = factor * final_integration_result[j][0]
            final_integration_result[j] = M_thrust * thrust_setting/100 + T_Weight_pg + T_Weight_lg + torque_aerodynamic
        elif xnew[j] < 11.5:
            torque_aerodynamic = factor * final_integration_result[j][0]
            final_integration_result[j] = M_thrust * thrust_setting/100 + T_Weight_pg + torque_aerodynamic
        else:
            final_integration_result[j] = factor * final_integration_result[j][0]

    torque_function = interp1d(xnew, final_integration_result, kind="linear", fill_value="extrapolate")

    return xnew, final_integration_result, torque_function

# setting outside function
xnew, final_integration_result, torque_function = torquedistribution('MainWing_a0.00_v10.00ms.csv', rho, 70, 69.92, 100, 11.5, Thrust_Setting, n_Setting, Weight_Setting)

# print(torque_function)

# plotting the datapoints and interpolation because it looks nice

# plt.plot(x,Mlst,"o", xnew, g(xnew), "-")
# plt.plot(x_T,Tlst,"o", xnew, h(xnew), "-")

plt.plot(xnew, torque_function(xnew), "-")

# plt.plot(xnew, final_integration_result, "r")


# plot formatting

plt.title('Torque Distribution')

plt.xlabel('Spanwise location [m]')
plt.ylabel('Torque [Nm]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()