E = 8.9 * (10 ** 9)
dt = 0.1
filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 0.4416
v = 232
span = 69.92
accuracy = 41

# Loading factor [-]
n = -1.5

# Maximum takeoff weight [kg]
MTOW = 291_509.2

# Operating empty weight [kg]
OEW = 141_412.4
# Maximum zero fuel weight [kg]
MZFW = 161394.73

# Maximum fuel weight [kg]
MaxFuelWeight = MTOW - OEW

# Engine weight for 2 engines [kg]
EngineWeight = 20_87.986

# Undercarriage weight for MLG only [kg]
W_uc_MLG = 7_569.349

# Wing weight including mounts and spoilers [kg]
WingWeight = 3210.55
import numpy as np
from scipy import integrate
import sys
import matplotlib.patches as mpatches
import os
import scipy as sp
import matplotlib.pyplot as plt


directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1, directory)
from liftdistribution import liftdistribution
from InertialLoading import inertialForce


x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy, MTOW * 9.81, n)
a = [0]
Aerosheer = [-sp.integrate.quad(f, 0, 0)[0] + sp.integrate.quad(f, 0, xdist)[0]]
while a[-1] <= xdist:
    a.append(a[-1] + dt)
    Aerosheer.append(-sp.integrate.quad(f, 0, a[-1])[0] + sp.integrate.quad(f, 0, xdist)[0])

totalsheer = []
i = 0
while i < len(Aerosheer):
    totalsheer.append(Aerosheer[i] + inertialForce[i])
    i += 1

f = sp.interpolate.interp1d(a, totalsheer, kind="linear", fill_value="extrapolate")



i = 0
Moment = []
while i < len(a):
    Moment.append(sp.integrate.quad(f, 0, a[i])[0] - sp.integrate.quad(f, 0, xdist)[0])
    if i % 10 == 0:
        print("bending moment calculation: (1/2) ", round(100 * a[i] / xdist), "%")
    i += 1


directory = os.path.dirname(os.path.dirname(__file__))+"\\WP5\\5.1"
sys.path.insert(-1, directory)
from GlobalMomentofInertia import Ixx

i = 1
Deflectioncalculation = [0]
print(Moment)
while i < len(a):
    Deflectioncalculation.append(-Moment[i] / ((E * Ixx(a[i]))/(1000**4)))
    i += 1
print(Deflectioncalculation)
g = sp.interpolate.interp1d(a, Deflectioncalculation, kind="linear", fill_value="extrapolate")

i = 0
firstintegration = []

while i < len(a):

    firstintegration.append(sp.integrate.quad(g, 0, a[i])[0])
    if i % 10 == 0:
        print("Deflection Calculation (2/2): ", round((100 * a[i] / xdist) * 0.5), "%")
    i += 1
h = sp.interpolate.interp1d(a, firstintegration, kind="linear", fill_value="extrapolate")
i = 0
deflection = []
c = (sp.integrate.quad(h, 0, 0)[0])
while i < len(a):

    deflection.append(sp.integrate.quad(h, 0, a[i])[0] - c)
    if i % 10 == 0:
        print("Deflection Calculation (2/2): ", round((100 * a[i] / xdist) * 0.5 + 50), "%")
    i += 1



#Second calculation

a1 = a
deflection1 = deflection
n1 = 4.65

x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy, MZFW * 9.81, n1)
a = [0]
Aerosheer = [-sp.integrate.quad(f, 0, 0)[0] + sp.integrate.quad(f, 0, xdist)[0]]
while a[-1] <= xdist:
    a.append(a[-1] + dt)
    Aerosheer.append(-sp.integrate.quad(f, 0, a[-1])[0] + sp.integrate.quad(f, 0, xdist)[0])

totalsheer = []
i = 0
while i < len(Aerosheer):
    totalsheer.append(Aerosheer[i] + inertialForce[i])
    i += 1

f = sp.interpolate.interp1d(a, totalsheer, kind="linear", fill_value="extrapolate")




i = 0
Moment = []
while i < len(a):
    Moment.append(sp.integrate.quad(f, 0, a[i])[0] - sp.integrate.quad(f, 0, xdist)[0])
    if i % 10 == 0:
        print("bending moment calculation: (1/2) ", round(100 * a[i] / xdist), "%")
    i += 1


i = 1
Deflectioncalculation = [0]
print(Moment)
while i < len(a):
    Deflectioncalculation.append(-Moment[i] / ((E * Ixx(a[i]))/(1000**4)))
    i += 1
print(Deflectioncalculation)
g = sp.interpolate.interp1d(a, Deflectioncalculation, kind="linear", fill_value="extrapolate")

i = 0
firstintegration = []

while i < len(a):

    firstintegration.append(sp.integrate.quad(g, 0, a[i])[0])
    if i % 10 == 0:
        print("Deflection Calculation (2/2): ", round((100 * a[i] / xdist) * 0.5), "%")
    i += 1
h = sp.interpolate.interp1d(a, firstintegration, kind="linear", fill_value="extrapolate")
i = 0
deflection = []
c = (sp.integrate.quad(h, 0, 0)[0])
while i < len(a):

    deflection.append(sp.integrate.quad(h, 0, a[i])[0] - c)
    if i % 10 == 0:
        print("Deflection Calculation (2/2): ", round((100 * a[i] / xdist) * 0.5 + 50), "%")
    i += 1

plt.plot(a, deflection)
plt.hlines(xdist * 0.3, -5, 40)
plt.hlines(-69.92*0.15, -5, 40)
plt.plot(a1, deflection1)
plt.title("Deflection")
plt.xlabel('Span [m]')
plt.ylabel('Deflection[m]')
plt.show()

plt.plot(a, deflection)

plt.xlim(0, xdist)
plt.ylim(0, xdist)
plt.gca().set_aspect('equal', adjustable='box')