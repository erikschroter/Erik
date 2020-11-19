import Moment_of_Inertia_Wingbox as WB
from matplotlib import pyplot as plt

t = WB.t
G = 24*10**9 #Change

def Torsional_Constant_J(spanwise_location_iny):
    b = 69.92

    WB_chord = 0.45
    WB_front_height = 0.1347
    WB_aft_height = 0.1091


    spanwise_location = spanwise_location_iny / (b / 2)
    chord = WB.chord_length(spanwise_location)
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord
    hpt = (h**2 + ((b-a)/2)**2)**0.5


    A = 0.5*(a+b)*h
    s = a + b + 2 * hpt
    J = 4*A**2/(s/t)

    return J

def Torsional_Stiffness(spanwise_location_iny):
    b = 69.92

    GJ_L = G*Torsional_Constant_J(spanwise_location_iny)/(spanwise_location_iny)

    return GJ_L

def Torsional_Stiffness_graph(ystart=0.5, yendmaxb=69.92):
    Xaxis_lst = []  # spanwise_location in y
    Yaxis_lst = []  # Ixx
    for point in range(1, 501):
        spanwise_location_iny = point / 500 * (yendmaxb - ystart) / 2 + ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Torsional_Stiffness(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Torsional Stiffness')
    plt.show()

