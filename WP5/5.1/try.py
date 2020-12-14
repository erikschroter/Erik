import math as m, numpy as np
from GlobalMomentofInertia import Ixx


def ColBucklingdef(K, E, L, y_span, A):
    print(y_span)
    Ixx = 3882083.333 * 10**(-12)
    stress_critical_buckling =  K * (np.pi) ** 2 * E * Ixx / (A * L ** 2)
    return stress_critical_buckling

# Compressive strength failure each component

sweepAngleWing = 28.77 * m.pi / 180 #rads
LStringer = 6.99 / m.cos(sweepAngleWing) #m
Emod = 68.9 * 10**9
AreaStringer = 1650 * 10**(-6)
print(LStringer)

bucklingStress = []
for i in range(0, round(69.92/ 2) * 10 ):
    bucklingStress.append(ColBucklingdef(1, 68.9 * 10**9, LStringer, i / 10, AreaStringer))
print(bucklingStress)



