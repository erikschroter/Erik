from math import pi

# Skin Buckling
#For the skin buckling we need to determine at what force normal to the cut plane buckling will occur, this happens at F_critial.

def F_cr(E, v, t, b):
    k_c = input("What is the k_c value?")
    F_cr = (( pi**2 * k_c * E )/( 12 * 1-v**2 ))*(t/b)**2

