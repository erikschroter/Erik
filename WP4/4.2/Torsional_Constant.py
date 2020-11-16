import Moment of Inertia

#Thickness To be determined
t = 0.005

def chord_length(spanwise_location): #Spanwise location is y/(b/2)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)

    return c

def Torsional_Constant_J(spanwise_location):
    WB_chord = 0.45
    WB_front_height = 0.1347
    WB_aft_height = 0.1091

    chord = chord_length(spanwise_location)
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord
    hpt = (h**2 + ((b-a)/2)**2)**0.5

    A = 0.5*(a+b)*h
    s = a + b + 2 * hpt
    J = 4*A**2/(s/t)

    return J