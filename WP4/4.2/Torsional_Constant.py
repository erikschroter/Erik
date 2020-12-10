import sys
import os
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP5\\5.1"
sys.path.insert(-1,directory)

import GlobalMomentofInertia as WB
from matplotlib import pyplot as plt
import scipy as sp

t = WB.t_wing_box_skin/1000
G = 24*10**9

def chord_length(spanwise_location): #Spanwise location is in y/(b/2)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)

    return c

def Torsional_Constant_J(spanwise_location_iny=34.96):
    b = 69.92

    WB_chord = 0.45
    WB_front_height = 0.1347
    WB_aft_height = 0.1091


    spanwise_location = spanwise_location_iny / (b / 2)
    chord = chord_length(spanwise_location)
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord



    A = 0.5*(a+b)*h
    s = a + b + 2 * h
    J = 4*A**2/(s/t)

    return J

def Torsional_Stiffness(spanwise_location_iny=34.96):
    b = 69.92

    GJ_L = G*Torsional_Constant_J(spanwise_location_iny)/(b/2)

    return GJ_L

def Torsional_Stiffness_graph(ystart=0.5, yendmaxb=34.96):
    Xaxis_lst = []  # spanwise_location in y
    Yaxis_lst = []  # Ixx
    for point in range(1, 501):
        spanwise_location_iny = point / 500 * (yendmaxb - ystart) + ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Torsional_Stiffness(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Torsional Stiffness Diagram')
    plt.xlabel('Span [m]')
    plt.ylabel('Torsional Stiffness[Nm/rad]')
    plt.show()

def Torsional_Constant_graph(ystart=0.5, yendmaxb=34.96):
    Xaxis_lst = []  # spanwise_location in y
    Yaxis_lst = []  # Ixx
    for point in range(1, 501):
        spanwise_location_iny = point / 500 * (yendmaxb - ystart) + ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Torsional_Constant_J(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Torsional Constant')
    plt.xlabel('Span')
    plt.ylabel('Torsional Constant')
    plt.show()

Torsional_Constant_graph()