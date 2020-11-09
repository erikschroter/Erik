import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt
dt = 0.1
xlist = [0]
flist = [0]
ilist = [0]
def f(x):
    if x<0:
        return 0
    if x>=0 and x < 2:
        return x**2
    if x>=2 and x< 4:
        return 6-x
    if x>=4 and x<=5:
        return (-2*x**3)/61+(250/61)
    if x>=5:
        return 0

while xlist[-1]<=10:
    xlist.append(xlist[-1]+dt)
    flist.append(f((xlist[-1])))
    ilist.append(sp.integrate.quad(f,0,xlist[-1])[0])


plt.plot(xlist,flist,'r')
plt.plot(xlist,ilist,'b')

plt.show()