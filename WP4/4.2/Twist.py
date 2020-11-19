import Torsional_Constant as TC
from matplotlib import pyplot as plt
import scipy as sp
import torquedistribution as TD

M_thrust = TD.M_thrust
TD.torquedistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100, 11.5, M_thrust)

def Twist(spanwise_location_iny=69.92):
    b = 69.92

    M_thrust = TD.M_thrust
    T = TD.torquedistribution('MainWing_a0.00_v10.00ms.csv', 1.225, 70, 69.92, 100, 11.5, M_thrust)
    G = TC.G
    J = TC.Torsional_Constant_J(spanwise_location_iny)

    Span = 69.92
    y2 = Span / 2
    y1 = -Span / 2

    dth_dy = T/G/J
    th_y = sp.integrate.quad(dth_dy,y1,y2)

    return th_y


def Twist_graph(ystart=0.5, yendmaxb=69.92):
    Xaxis_lst = []  # spanwise_location in y
    Yaxis_lst = []  # Ixx
    for point in range(1, 501):
        spanwise_location_iny = point / 500 * (yendmaxb - ystart) / 2 + ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Twist(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Twist')
    plt.show()

Twist_graph()