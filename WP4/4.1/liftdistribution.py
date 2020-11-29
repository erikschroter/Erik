from scipy.interpolate import interp1d
import scipy as sp
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
from ReadingXFLRresults import ReadingXFLR


# =============================================================================
# Lift Distribution
# =============================================================================
def liftdistribution(file, rho, v, span, accuracy,weight,n):

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
    
    #determinging the facter by wich the lift needs to be mulitplied
    factor = (n*weight*0.5)/(sp.integrate.quad(f,0,span/2)[0])
    
    out=[]
    
    for i in range(len(Cl)):
        out.append(q*Chord[i]*Cl[i]*factor)
        
    # interpolating the data in a cubic manner
    o = interp1d(x,out,kind="cubic", fill_value="extrapolate")

    #determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
    xnew = np.linspace(0, (span/2), num=accuracy, endpoint=True)
    
    

    

        
    

    return x, Llst, xnew, o, span/2
'''
x, Llst, xnew, f,xdist = liftdistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100,(2915092),1) 
xlist = []
ylist = []
presision = 1000

for i in range(presision):
    xlist.append(((i*xdist)/presision))
    ylist.append(f(((i*xdist)/presision)))
    
plt.plot(xlist,ylist)
plt.grid(b=None,which='Major',axis='both')
plt.title("Lift distribution")
plt.ylabel("Aerodynamic force [N]")
plt.xlabel("spanwise location [m]")
'''