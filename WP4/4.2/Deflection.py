import Moment_of_Inertia_Wingbox as WB
from matplotlib import pyplot as plt

import scipy as sp
import Moment as M
from scipy import integrate

def d2v_dy2_y(span_position_in_y=69.92/2):
    b = WB.b
    E = WB.E
    spanwise_location = span_position_in_y / (b / 2)  # spanwise_location is in y/(b/2)

    Mx_y = M.moment(span_position_in_y)  # error waiting for function
    Ixx_y = WB.Ixx_in_y(span_position_in_y)

    return  -Mx_y / (E * Ixx_y)

def dv_dy_y(span_position_in_y=69.92/2):
    Span = 69.92
    y1 = 0
    dv_dyy,error1 = sp.integrate.quad(d2v_dy2_y,y1,span_position_in_y)
    return dv_dyy

def Deflection(span_position_in_y=69.92/2):
    Span = 69.92
    y1 = 0
    v_y,error2 = sp.integrate.quad(dv_dy_y, y1, span_position_in_y)
    return v_y


def Deflection_graph(ystart=0, yendmaxb=69.92):
    Xaxis_lst = []  # spanwise_location in y
    Yaxis_lst = []  # Ixx
    for point in range(1, 101):
        spanwise_location_iny = point / 100 * (yendmaxb - ystart) / 2 + ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Deflection(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Deflection')
    plt.show()


print(Deflection(69.92/2))
