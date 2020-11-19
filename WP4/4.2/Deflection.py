import Moment_of_Inertia_Wingbox as WB
from matplotlib import pyplot as plt
import scipy as sp


def Deflection(span_position_in_y):
    b = WB.b
    E = WB.E

    spanwise_location = span_position_in_y/(b/2)     #spanwise_location is in y/(b/2)

    Mx_y =  WB.Mx(span_position_in_y)  #error waiting for function
    Ixx_y = WB.Ixx_in_y(span_position_in_y)

    Span = 69.92
    y2 = Span/2
    y1 = -Span/2

    d2v_dy2_y = -Mx_y/(E*Ixx_y)
    dv_dy_y = sp.integrate.quad(d2v_dy2_y,y1,y2)

    v_y = sp.integrate.quad(dv_dy_y,y1,y2)

    return v_y

def Deflection_graph(ystart=0.5, yendmaxb=69.92):
    Xaxis_lst = []  # spanwise_location in y
    Yaxis_lst = []  # Ixx
    for point in range(1, 501):
        spanwise_location_iny = point / 500 * (yendmaxb - ystart) / 2 + ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Deflection(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Torsional Constant')
    plt.show()