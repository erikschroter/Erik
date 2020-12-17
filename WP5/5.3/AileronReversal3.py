import math
import os
import sys
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(__file__))+"\\5.1"
sys.path.insert(-1,directory)

from Torsional_Constant import Torsional_Constant_J as TCJ
from WP5.ISAdef import ISA
from Centroid import CentroidX

def full(y_span):
    G = 26 * 10**9

    dclda = 3.5
    dclde = 0.8
    dcmde = -0.25
    S = 30


    def constants(y_span, altitude, G ):
        # stifness
        J = TCJ(y_span)
        K = 1.93*10**6

        # chord
        half_span = 34.96
        Cr = 11.95
        Ct = 3.59
        Taper = 0.3
        c = 3


        stringer_distribution = [(14, 14, 6.99), (12, 12, 13.98), (10, 10, 20.98), (8, 8, 27.97),
                                 (6, 6, 34.96)]  # from root to tip, (top, bottom)
        Cx = (CentroidX(stringer_distribution, y_span))/1000
        e = 0.25      # Cx position relative to chord + front spar distance - quarter chord
        return K, c, e
    K, c, e = constants(32, 31000*0.3048, G)

    def Vrdef(K, dclde, rho, S, c, dcmde, dclda):

        Vr = math.sqrt((-K * dclde)/(0.5 * rho * S * c * dcmde * dclda))

        return Vr


    def Aedef(rho, V, S, c, dcmde, dclda, K, dclde, e ):

        Ae = (0.5* rho* V**2* S* c* dcmde* dclda + K* dclde)/((K- 0.5* rho* V**2* S* c * e* dclda)*dclde)        #Change 1 by actual dCm/dE & dCL/dE from Xfoil
        return Ae
    print('ae', Aedef(1.225, 150, S, c, dcmde, dclda, K, dclde, e))


    def Aileron_effectiveness_graph(y_span):
        Vlst = []
        ae_sea_lst = []
        ae_cruise_lst = []
        for v in range (0, 150):
            Vlst.append(v)
            ae_sea_lst.append(Aedef(1.225, v, S, c, dcmde, dclda, K, dclde, e))
            ae_cruise_lst.append(Aedef(0.441653, v, S, c, dcmde, dclda, K, dclde, e))

        plt.plot(Vlst, ae_sea_lst, 'b')
        plt.plot(Vlst, ae_cruise_lst, 'r')
        plt.title('Aileron effectiveness diagram')
        plt.xlabel('Freestream velocity [m/s]')
        plt.ylabel('Aileron effectiveness')

        blue_patch = mpatches.Patch(color='blue', label='Sea-Level')
        red_patch = mpatches.Patch(color='red', label='Cruise Altitude')
        plt.legend(handles=[red_patch, blue_patch])

        plt.show()


    print(Vrdef(K, dclde, 0.441653, S, c, dcmde, dclda))
    print(Vrdef(K, dclde, 1.226,S,c,dcmde,dclda))
    Aileron_effectiveness_graph(y_span)

full(32)
full(13)


