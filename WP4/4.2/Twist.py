import Torsional_Constant as TC
from matplotlib import pyplot as plt
import scipy as sp
from scipy import integrate
from torquedistribution import torque_function as TD
from torquedistribution2 import torque_function as TD2
import math


def dth_dy(spanwise_location_iny=34.96):
    T = TD(spanwise_location_iny)
    G = TC.G
    J = TC.Torsional_Constant_J(spanwise_location_iny)

    Span = 69.92
    y2 = Span / 2
    y1 = 0

    dth_dy = T / G / J
    return  dth_dy

def Twist(spanwise_location_iny=34.96):
    b = 69.92
    Span = 69.92
    y2 = Span / 2
    y1 = 0.5
    th_y2 = (0, 0)
    th_y3 = (0, 0)

    if spanwise_location_iny<=6:
        th_y1 = sp.integrate.quad(dth_dy,y1,spanwise_location_iny, limit=100)
        th_y = th_y1[0]

    elif spanwise_location_iny<=11.5:
        th_y1 = sp.integrate.quad(dth_dy, y1, 6, limit=100)
        th_y2 = sp.integrate.quad(dth_dy, 6, spanwise_location_iny, limit=100)
        th_y = th_y1[0] + th_y2[0]

    else:
        th_y1 = sp.integrate.quad(dth_dy, y1, 6, limit=100)
        th_y2 = sp.integrate.quad(dth_dy, 6, 11.5, limit=100)
        th_y3 = sp.integrate.quad(dth_dy, 11.5, spanwise_location_iny, limit=100)
        th_y = th_y1[0] + th_y2[0] + th_y3[0]

    return th_y

def dth_dy2(spanwise_location_iny=34.96):
    T = TD2(spanwise_location_iny)
    G = TC.G
    J = TC.Torsional_Constant_J(spanwise_location_iny)

    Span = 69.92
    y2 = Span / 2
    y1 = 0

    dth_dy = T / G / J
    return  dth_dy

def Twist2(spanwise_location_iny=34.96):
    b = 69.92
    Span = 69.92
    y2 = Span / 2
    y1 = 0.5
    th_y2 = (0, 0)
    th_y3 = (0, 0)

    if spanwise_location_iny<=6:
        th_y1 = sp.integrate.quad(dth_dy2,y1,spanwise_location_iny, limit=100)
        th_y = th_y1[0]

    elif spanwise_location_iny<=11.5:
        th_y1 = sp.integrate.quad(dth_dy2, y1, 6, limit=100)
        th_y2 = sp.integrate.quad(dth_dy2, 6, spanwise_location_iny, limit=100)
        th_y = th_y1[0] + th_y2[0]

    else:
        th_y1 = sp.integrate.quad(dth_dy2, y1, 6, limit=100)
        th_y2 = sp.integrate.quad(dth_dy2, 6, 11.5, limit=100)
        th_y3 = sp.integrate.quad(dth_dy2, 11.5, spanwise_location_iny, limit=100)
        th_y = th_y1[0] + th_y2[0] + th_y3[0]

    return th_y

def Twist_graph(ystart=0.5, yendmaxb=69.92):
    Xaxis_lst1 = []  # spanwise_location in y
    Yaxis_lst1 = []  # Ixx
    for point in range(1, 101):
        spanwise_location_iny = point / 100 * (yendmaxb - ystart) / 2 + ystart
        Xaxis_lst1.append(spanwise_location_iny)
        Yaxis_lst1.append(math.degrees((Twist(spanwise_location_iny))))

    Xaxis_lst2 = []  # spanwise_location in y
    Yaxis_lst2 = []  # Ixx
    for point in range(1, 101):
        spanwise_location_iny = point / 100 * (yendmaxb - ystart) / 2 + ystart
        Xaxis_lst2.append(spanwise_location_iny)
        Yaxis_lst2.append(math.degrees(Twist2(spanwise_location_iny)))

    plt.plot(Xaxis_lst1, Yaxis_lst1)
    plt.plot(Xaxis_lst2, Yaxis_lst2)
    plt.hlines(10, -5, 40)
    plt.hlines(-10, -5, 40)
    plt.title('Twist Distribution')
    plt.xlabel('Span [m]')
    plt.ylabel('Twist [deg]')
    plt.show()





Twist_graph()


