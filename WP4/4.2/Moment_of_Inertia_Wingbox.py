import scipy as sp


# Wing Box outer geometry (in chord length)
WB_chord = 0.45
WB_front_height = 0.1347
WB_aft_height = 0.1091

#Thickness To be determined
t = 0.005
E = 1   #To be changed


def chord_length(spanwise_location): #Spanwise location is y/(b/2)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)

    return c

def Moment_of_Inertia_y(spanwise_location_iny):
    spanwise_location = spanwise_location_iny/(b/2)
    chord = chord_length(spanwise_location)
    #Geometrical parameters
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord

    h_inner = h-2*t
    a_inner = a-2*t
    b_inner = b-2*t
    c_inner = c-2*t

    Iperpendicular = ((h**3)*((a**2)*(4*a*b)+b**2))/(36*(a+b))
    Iperpendicular_t = ((h_inner**3)*((a_inner**2)*(4*a_inner*b_inner)+b_inner**2))/(36*(a_inner+b_inner))
    Iperpendicular_wingbox = Iperpendicular - Iperpendicular_t

    Ichord = h*(4*a*b*c**2+3*a**2*b*c-3*a*b**2*c+a**4+b**4+2*a**3*b+a**2*c**2+a**3*c+2*a*b**3-c*b**3 + b**2 * c**2)/\
             (36*(a+b))
    Ichord_t = (h_inner)*(4*a_inner*b_inner*c_inner**2+3*a_inner**2*b_inner*c_inner-3*a_inner*b_inner**2*c_inner+a_inner
                          **4+b_inner**4+2*a_inner**3*b_inner+a_inner**2*c_inner**2+a_inner**3*c_inner+2*a_inner*b_inner
                          **3-c_inner*b_inner** 3 + b_inner**2 * c_inner**2)/(36*(a_inner+b_inner))
    I_chord_wingbox = Ichord - Ichord_t

    return I_chord_wingbox


def Ixx_in_y(spanwise_location_iny):
    Mx = Moment_of_Inertia_y(spanwise_location_iny)+Ixx_stringers(spanwise_location_iny) #error waiting for function

    return Mx

