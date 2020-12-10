import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
import math


# Wing Box outer geometry (in chord length)
WB_chord = 0.45
WB_front_height = 0.1347
WB_aft_height = 0.1091


b = 69.92
E = 68.9*10**9

#Variables to change
t = 0.010       #WB thickness
tS = 0.005      #Stringer thickness
aS = 0.110        #Stringer depth
hS = 0.110
Spanwise = [0, 6.992, 13.984, 20.976, 27.968]
Stringersnolow = [18, 16, 12, 8, 6]             #Stringers number lower WB
Stringersnoupp = [18, 16, 12, 8, 6]             #Stringers number upper WB



def chord_length(spanwise_location): #Spanwise location is in y/(b/2)
    Cr = 11.95
    Ct = 3.59
    Taper = 0.3
    c = Cr - Cr*(1-Taper)*(spanwise_location)

    return c

def Moment_of_Inertia_y(spanwise_location_iny):     #WB Ixx
    b = 69.92  # Span
    spanwise_location = spanwise_location_iny/(b/2)
    chord = chord_length(spanwise_location)

    # Geometrical parameters
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord

    h_inner = h - 2 * t
    a_inner = a - 2 * t
    b_inner = b - 2 * t
    c_inner = c - 2 * t


    Ichord = h*(4*a*b*c**2+3*a**2*b*c-3*a*b**2*c+a**4+b**4+2*a**3*b+a**2*c**2+a**3*c+2*a*b**3-c*b**3 + b**2 * c**2)/\
             (36*(a+b))
    Ichord_t = (h_inner)*(4*a_inner*b_inner*c_inner**2+3*a_inner**2*b_inner*c_inner-3*a_inner*b_inner**2*c_inner+a_inner
                          **4+b_inner**4+2*a_inner**3*b_inner+a_inner**2*c_inner**2+a_inner**3*c_inner+2*a_inner*b_inner
                          **3-c_inner*b_inner** 3 + b_inner**2 * c_inner**2)/(36*(a_inner+b_inner))
    I_chord_wingbox = Ichord - Ichord_t

    return I_chord_wingbox


def Ixx_stringers_lower(spanwise_location_iny):       #Stringers Ixx lower WB
    b = 69.92 #Span
    spanwise_location = spanwise_location_iny / (b / 2)
    chord = chord_length(spanwise_location)

    # Geometrical parameters
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord
    c = 0.0163 * chord

    n1= sp.interpolate.interp1d(Spanwise,Stringersnolow,kind="previous",fill_value="extrapolate")     #number of stringers
    n = n1(spanwise_location_iny)

    #Centroid Wingbox
    Cchord=(h/3)*((2*a+b)/(a+b))

    #Values Stringer
    Astringer=tS*(2*aS + hS)      #Area
    CentroidxS = 0.5*aS
    CentroidyS = 0.5*hS

    StringerIxx = 1 / 12 * tS * hS ** 3 + (2 * (a * tS) *(hS/2-tS/2)**2)

    #Parrallel axis stringers
    I=[]
    n=int(n)
    for i in range(1, n+1):
        ParAxisOne=Astringer*(Cchord - CentroidyS - i/(n+1) * math.tan(math.radians(1.18)))**2
        I.append(ParAxisOne)
    SumI=sum(I) + StringerIxx*n

    return SumI


def Ixx_stringers_upper(spanwise_location_iny):       #Stringers Ixx upper WB
    b = 69.92 #Span
    spanwise_location = spanwise_location_iny / (b / 2)
    chord = chord_length(spanwise_location)

    # Geometrical parameters
    h = WB_chord * chord
    a = WB_aft_height * chord
    b = WB_front_height * chord


    n1= sp.interpolate.interp1d(Spanwise,Stringersnoupp,kind="previous",fill_value="extrapolate")     #number of stringers
    n = n1(spanwise_location_iny)

    #Centroid Wingbox
    Cchord=(h/3)*((2*a+b)/(a+b))

    #Values Stringer
    Astringer = tS * (2 * aS + hS)  # Area
    CentroidxS = 0.5 * aS
    CentroidyS = 0.5 * hS

    StringerIxx2 = 1 / 12 * tS * hS ** 3 + (2 * (a * tS) * (hS / 2 - tS / 2) ** 2)

    #Parrallel axis stringers
    I2=[]
    n=int(n)
    for i in range(1, n+1):
        ParAxisTwo=Astringer*(Cchord - CentroidyS - i/(n+1) * math.tan(math.radians(2.08)))**2
        I2.append(ParAxisTwo)
    SumI2=sum(I2) + StringerIxx2 * n

    return SumI2

def Ixx_stringers(spanwise_location_iny):
    return Ixx_stringers_upper(spanwise_location_iny) + Ixx_stringers_lower(spanwise_location_iny)

def Ixx_in_y(spanwise_location_iny):        #Ixx at a point
    Ixx = Moment_of_Inertia_y(spanwise_location_iny) + Ixx_stringers(spanwise_location_iny)

    return Ixx


def Ixx_graph(ystart=0.5,yendmaxb=69.92):
    Xaxis_lst = []  #spanwise_location in y
    Yaxis_lst = []  #Ixx
    for point in range(1, 501):
        spanwise_location_iny = point/500*(yendmaxb-ystart)/2 +ystart
        Xaxis_lst.append(spanwise_location_iny)
        Yaxis_lst.append(Ixx_in_y(spanwise_location_iny))

    plt.plot(Xaxis_lst, Yaxis_lst)
    plt.title('Ixx diagram')
    plt.xlabel('Span [m]')
    plt.ylabel(f'Ixx [m\N{SUPERSCRIPT FOUR}]')
    plt.show()


#Total values at span
def Ixx(span_position_in_y=69.92/2):
    Span = 69.92
    y1 = 0
    v_y,error2 = sp.integrate.quad(Ixx_in_y,y1, span_position_in_y)
    return v_y

def Ixxstringers(span_position_in_y=69.92/2):
    Span = 69.92
    y1 = 0
    v_y, error2 = sp.integrate.quad(Ixx_stringers, y1, span_position_in_y)
    return v_y

