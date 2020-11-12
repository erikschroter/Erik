from scipy.interpolate import interp1d
import scipy as sp
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from ReadingXFLRresults import ReadingXFLR


def liftdistribution(file, rho, v, span, accuracy):
    #setting variables for wing dimensions and flight conditions
    rho=rho
    v=v

    #The code below fetches the various aerodynamic data from the XFLR analysis
    CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR(file)
    print(Cl)

    #determining what variables need to be on the x, and y -axis
    x = yspan
    lst=Cl
    for i in range(len(Cl)-1):
        lst[i] = 0.5*rho*(v**2)*Chord[i]*Cl[i]
    y=lst

    #interpolating the data in a cubic manner
    f = interp1d(x,y,kind="cubic", fill_value="extrapolate")

    #determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
    xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)

    #plotting the datapoints and interpolation because it looks nice
    plt.plot(x,y,"o", xnew, f(xnew), "-")
    plt.show()

    return f, span/2

f, xdist = liftdistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100)
print(f(9.23))