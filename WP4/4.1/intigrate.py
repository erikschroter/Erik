"""
Created on Mon Nov  9 16:21:58 2020

@author: michi
"""


import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt

def ShearForce(LoadingFunction,x,Maxx):
    return sp.integrate.quad(LoadingFunction,0,x)[0]-sp.integrate.quad(LoadingFunction,0,Maxx)[0]
    
def DrawShearForce(LoadingFunction,Maxx):
    Xlist = [0]
    Ylist = [0]
    dt=0.1
    while Xlist[-1]<=Maxx:
        Xlist.append(Xlist[-1]+dt)
        Ylist.append(ShearForce(LoadingFunction,Xlist[-1],Maxx))
    plt.plot(Xlist,Ylist)
    plt.title('Shear Force diagram')
    plt.show()
    
def BendingMoment(LoadingFunction,x,Maxx):
   global c

   if c == 0:
       c = sp.integrate.quad(lambda x: sp.integrate.quad(LoadingFunction,0,x)[0],0,Maxx)[0] 
       
   

   print("bending moment calculation: ",round(100*x/Maxx),"%")
   return sp.integrate.quad(lambda x: sp.integrate.quad(LoadingFunction,0,x)[0],0,x)[0]-c

 
    
def DrawBendingMoment(LoadingFunction,Maxx):
    Xlist = [0]
    Ylist = [0]
    dt=0.1
    global c
    c = 0
    while Xlist[-1]<=Maxx:
        Xlist.append(Xlist[-1]+dt)
        Ylist.append(BendingMoment(LoadingFunction,Xlist[-1],Maxx))
    plt.plot(Xlist,Ylist)
    plt.title('Bending Moment diagram')
    plt.show()  
    

def f(x):
    return x**2
