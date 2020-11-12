from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from ReadingXFLRresults import ReadingXFLR

#The code below fetches the various aerodynamic data from the XFLR analysis
CL, yspan, Chord, Ai, Cl, ICd, CmAirfquarterchord = ReadingXFLR('MainWing_a0.00_v10.00ms.csv')

#determining what variables need to be on the x, and y -axis
x = yspan
y = Cl

print(x)
print(y)

#interpolating the data in a cubic manner
f = interp1d(x,y,kind="cubic")

#determining over which range the interpolation needs to be determined, here num= determines the accuracy of the interpolation.
xnew = np.linspace(x[0], x[len(x)-1], num=41, endpoint=True)

#plotting the datapoints and interpolation because it looks nice
plt.plot(x,y,"o", xnew, f(xnew), "-")
plt.show()

#If an exact value needs to be known you can determine it here
print(f(2.3))

