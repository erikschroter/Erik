import Moment_of_Inertia_Wingbox as WB

t = WB.t

def Torsional_Constant_J(spanwise_location):
    WB_chord = 0.45
    WB_front_height = 0.1347
    WB_aft_height = 0.1091

    chord = WB.chord_length(spanwise_location)
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord
    hpt = (h**2 + ((b-a)/2)**2)**0.5

    G = 1 #to be changed
    A = 0.5*(a+b)*h
    s = a + b + 2 * hpt
    J = 4*A**2/(s/t)

    return J
