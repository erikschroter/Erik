import sys
import os
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)

from Torsional_Constant import Torsional_Constant_J as TCJ
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
directory = os.path.dirname(os.path.dirname(__file__))+"\\5.1"
sys.path.insert(-1,directory)
from Centroid import CentroidX, CentroidY
import math

def chord_length(Span_in_y): #Spanwise location is in y/(b/2)
    spanwise_location = Span_in_y/(34.96)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)

    return c

#Low speed aileron in m
b1 = 2413
b2 = 32

#High speed aileron in m
b3 = 12
b4 = 14

G = 26 * 10**9

dCLdal = 6.304
dCLdE = 5.6526
dCmdE = -0.90846
S = 543.25

def Vr(Span_in_y, altitude): #Only 31000 or 0
    if altitude == 31000:
        rho = 0.441653

    if altitude == 0:
        rho = 1.225

    J = TCJ(Span_in_y)
    K = G * J
    c = chord_length(Span_in_y)

    VR = ((-K * dCLdE) / (0.5* rho* S* c* dCmdE* dCLdal))**0.5
    return VR

stringer_distribution = [(14,14,6.99),(12,12,13.98),(10,10,20.98),(8,8,27.97),(6,6,34.96)]  # from root to tip, (top, bottom)

def Aileron_effectiveness(Vfreestream, altitude, Span_in_y): #Altitude Only 31000 or 0
    if altitude == 31000:
        rho = 0.441653

    if altitude == 0:
        rho = 1.225


    J = TCJ(Span_in_y)
    K = G * J
    V = Vfreestream * math.cos(math.radians(28.77))
    Cx = (CentroidX(stringer_distribution, Span_in_y))/1000
    Cy = (CentroidY(stringer_distribution, Span_in_y))/1000


    e = -((Cx/ (chord_length(Span_in_y)*1000) + 0.15) -0.25)     # Cx position relative to chord + front spar distance - quarter chord
    c = chord_length(Span_in_y)

    ae = (0.5* rho* V**2* S* c* dCmdE* dCLdal+ K* dCLdE)/((K- 0.5* rho* V**2* S* c* e* dCLdal)*dCLdE)        #Change 1 by actual dCm/dE & dCL/dE from Xfoil

    return ae

def Aileron_effectiveness_graph(Span_in_y):

    Vlst = []
    ae_sea_lst = []
    ae_cruise_lst = []
    for v in range (50, 300):
        Vlst.append(v)
        ae_sea_lst.append(Aileron_effectiveness(v, 0, Span_in_y))
        ae_cruise_lst.append(Aileron_effectiveness(v, 31000, Span_in_y))

    plt.plot(Vlst, ae_sea_lst, 'b')
    plt.plot(Vlst, ae_cruise_lst, 'r')
    plt.title('Aileron effectiveness diagram')
    plt.xlabel('Freestream velocity [m/s]')
    plt.ylabel('Aileron effectiveness')

    blue_patch = mpatches.Patch(color='blue', label='Sea-Level')
    red_patch = mpatches.Patch(color='red', label='Cruise Altitude')
    plt.legend(handles=[red_patch, blue_patch])

    plt.show()

print('low-speed aileron cruise', Vr(28, 31000))
print('low-speed aileron sea', Vr(28, 0))
print('high-speed aileron cruise', Vr(13, 31000))
print('high-speed aileron sea', Vr(13, 0))

Aileron_effectiveness_graph(28)     #Low speed ailerons
Aileron_effectiveness_graph(13)     #High speed ailerons



