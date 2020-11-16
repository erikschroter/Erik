from scipy.interpolate import interp1d
import scipy as sp
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from ReadingXFLRresults import ReadingXFLR


# =============================================================================
# Lift Distribution
# =============================================================================
def liftdistribution(file, rho, v, span, accuracy):

    # The code below fetches the various aerodynamic data from the XFLR analysis
    CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR(file)
    
    # setting variables for wing dimensions and flight conditions
    rho=rho
    v=v

    # determining what variables need to be on the x, and y -axis
    q = 1/2 * rho * (v**2)
    x = yspan
    Llst=[]
    
    for i in range(len(Cl)):
        Llst.append(q*Chord[i]*Cl[i])
    
    # interpolating the data in a cubic manner
    f = interp1d(x,Llst,kind="cubic", fill_value="extrapolate")

    #determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
    xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)

    return x, Llst, xnew, f, span/2

# x, Llst, xnew, f = liftdistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100) 

# def plotting(x, y, xnew, f(xnew)):
    
# f, xdist = liftdistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100)
# print(f(9.23))

#     #plotting the datapoints and interpolation because it looks nice
#     plt.plot(x,y,"o", xnew, f(xnew), "-")
    
#     # plot formatting
    
#     plt.title('Lift distribution')
    
#     plt.xlabel('span location')
#     plt.ylabel('Distribution magnitude')
    
#     plt.grid(True, which='both')
#     plt.axhline(y=0, color='k')
    
#     plt.show()

# =============================================================================
# Torque Distribution
# =============================================================================

def torquedistribution(file, rho, v, span, accuracy):

    # The code below fetches the various aerodynamic data from the XFLR analysis
    CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR(file)
    
    # setting variables for wing dimensions and flight conditions
    rho=rho
    v=v
    flexaxis = 0.367
    bprime = 1
    y_thrust = 11.5 # m
    M_thrust = 11106769.7 # Nm

    # determining what variables need to be on the x, and y -axis
    q = 1/2 * rho * (v**2)
    x = yspan
    cmlst=[]
    Mlst=[]
    
    for i in range(len(Cl)):
        cmlst.append(CmAirfquarterchord[i] - Cl[i]*(flexaxis-0.25))
        Mlst.append(cmlst[i]*q*(Chord[i]**2)*bprime)

    # find the closest y span value for the thrust (higher or lower)
    closest = min(x, key=lambda x:abs(x-y_thrust))
    closestindex = x.index(closest)
    
    for i in range(0, closestindex + 1):
        Mlst[i] = Mlst[i] + M_thrust
    
    # interpolating the data in a cubic manner
    g = interp1d(x,Mlst,kind="cubic", fill_value="extrapolate")

    #determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
    xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)

    return x, Mlst, xnew, g, span/2

# def interpolate(file, rho, v, span, accuracy):
    
#     # The code below fetches the various aerodynamic data from the XFLR analysis
#     CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR(file)
    
#     # setting variables for wing dimensions and flight conditions
#     rho=rho
#     v=v

#     # determining what variables need to be on the x, and y -axis
#     q = 1/2 * rho * (v**2)
#     x = yspan
#     lst=[]
    
#     for i in range(len(Cl)):
#         lst.append(q*Chord[i]*Cl[i])
    
#     # interpolating the data in a cubic manner
#     f = interp1d(x,Llst,kind="cubic", fill_value="extrapolate")

#     #determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
#     xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)

#     return x, Llst, xnew, f, span/2

g, xdist = gendistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100)
# print(g(9.23))

<<<<<<< Updated upstream
=======
    # #plotting the datapoints and interpolation because it looks nice
    # plt.plot(x,Mlst,"o", xnew, g(xnew), "-")
    
    # # plot formatting
    
    # plt.title('Torque distribution')
    
    # plt.xlabel('span location')
    # plt.ylabel('Distribution magnitude')
    
    # plt.grid(True, which='both')
    # plt.axhline(y=0, color='k')
    
    # plt.show()
>>>>>>> Stashed changes
