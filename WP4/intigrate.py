# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 16:21:58 2020

@author: michi
"""

import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt

def ShearForce(LoadingFunction,x):
    return sp.integrate.quad(LoadingFunction,0,x)[0]
    
def DrawShearForce(LoadingFunction,Maxx):
    Xlist = [0]
    Ylist = [0]
    dt=0.01
    while Xlist[-1]<=Maxx:
        Xlist.append(Xlist[-1]+dt)
        Ylist.append(ShearForce(LoadingFunction,Xlist[-1]))
    plt.plot(Xlist,Ylist)
    plt.title('Shear Force diagram')
    plt.show()
    
    
def f(x):
    return 6*x
DrawShearForce(f,5)
