# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:47:29 2020

@author: Erik Schroter
"""
from scipy.interpolate import interp1d
import scipy as sp
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from ReadingXFLRresults import ReadingXFLR


# =============================================================================
# Torque Distribution
# =============================================================================

def torquedistribution(file, rho, v, span, accuracy, y_thrust, M_thrust):

    # The code below fetches the various aerodynamic data from the XFLR analysis
    CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR(file)
    
    # setting variables for wing dimensions and flight conditions
    rho=rho
    v=v
    flexaxis = 0.367
    bprime = 1
    y_thrust = y_thrust
    M_thrust = M_thrust
    
    # create array for pure thrust torque
    Tlst = np.append(np.array([M_thrust]*(len(yspan)-2)), [0]*2)
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
    h = interp1d(x_T,Tlst,kind="linear", fill_value="extrapolate")
    
    #determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
    xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)

    return x, Mlst, xnew, g, span/2, x_T, Tlst, h

# setting outside function
TDist = torquedistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100, 11.5, 1106769.7)

x = TDist[0]
Mlst = TDist[1]
xnew = TDist[2]
g = TDist[3]

x_T = TDist[5]
Tlst = TDist[6]
h = TDist[7]

# superposition of aerodynamic torque and thrust torque
def i(x):
    return g(x) + h(x)

# plotting the datapoints and interpolation because it looks nice

# plt.plot(x,Mlst,"o", xnew, g(xnew), "-")
# plt.plot(x_T,Tlst,"o", xnew, h(xnew), "-")

plt.plot(xnew, i(xnew), "-")


# plot formatting

plt.title('Torque Distribution')

plt.xlabel('Spanwise location [m]')
plt.ylabel('Torque [Nm]')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()