import numpy as np, scipy as sp


def ReferenceGustVelocity(altitude, velocity):
    
    return
    

def FlightAlleviationFactor (R1, R2, Z_mo):
    """" Inputs for function:     
    R1, ratio: maximum landing weight / maximum take-off weight []
    R2, ratio: maximum zero fuel weight / maximum take-off weight []
    Z_mo, maximum operating altitude [m]
    
    Outputs for function:              
    F_g, flight alleviation factor [] """""

    F_gm = (R2* np.tan(np.pi * R1 / 4)) **0.5
    F_gz = 1 - Z_mo/76200
    F_g = 0.5 * (F_gz + F_gm)

    return F_g


def DesignGustVelocity(U_ref, F_g, H):
     """" Inputs for function:
     U_ref, reference gust velocity [m/s]
     F_g, flight alleviation factor []
     H,  gust gradient distance [m]    
     
     Outputs for function: 
     U_ds, design gust velocity [m] """""

     U_ds = U_ref * F_g * (H/107)**(1/6)

     return U_ds



def GustVelocity(U_ds, s, H):
    """" Inputs for function:
    U_ds,  design gust velocity
    H, gust gradient distance
    s, distance penetrated into gust
    
    Outputs for function:
     U, gust velocity [m/s] """""

    U = U_ds / 2 * (1-np.cos(np.pi * s / H))

    return U





print(FlightAlleviationFactor(0.8, .6,20000 ))