import os
import sys
import math

directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(__file__))+"\\5.1"
sys.path.insert(-1,directory)
from Centroid import CentroidX, CentroidY
from Torsional_Constant import Torsional_Constant_J as TCJ
from WP5.ISAdef import ISA

##Constants
#Low speed aileron in m
b1 = 24
b2 = 32

#High speed aileron in m
b3 = 12
b4 = 14

G = 24 * 10**9
dCLdal = 6.304
dCLdE = 7.5224
dCmdE = -0.2331
S = 543.25

def chord_length(Span_in_y): #Spanwise location is in y/(b/2)
    spanwise_location = Span_in_y/(34.96)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)

    return c

def Vr(altitude, y_span ):
    rho, T = ISA(altitude)
    J = TCJ(y_span)
    K = G * J
    c = chord_length(y_span)

    Vr = math.sqrt((-K*dCLdE)/(0.5* rho * S * c * dCmdE * dCLdal))
    return Vr, rho
Vr, rho,

def Aileff():

    ae = (0.5* rho* V**2* S* c* dCmdE* dCLdal+ K* dCLdE)/((K- 0.5* rho* V**2* S* c* e* dCLdal)*dCLdE)        #Change 1 by actual dCm/dE & dCL/dE from Xfoil


    return

Vr(31000*.3048, 32)

