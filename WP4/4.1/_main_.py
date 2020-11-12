
#define constants

filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 1.225
v = 70
span = 69.92
accuracy = 41 

#Maximum takeoff weight [kg]
MTOW = 291_509.2

#Operating empty weight [kg]
OEW = 141_412.4

#Maximum fuel weight [kg]
MaxFuelWeight = MTOW - OEW

#Engine weight for 2 engines [kg]
EngineWeight = 20_87.986

#Undercarriage weight for MLG only [kg]
W_uc_MLG = 7_569.349

#Wing weight including mounts and spoilers [kg]
WingWeight = 3210.55

from intigrate import *
from interpolate import *


f, xdist = liftdistribution(filename, rho, v, span, accuracy)

DrawShearForce(f,xdist)
DrawBendingMoment(f,xdist)