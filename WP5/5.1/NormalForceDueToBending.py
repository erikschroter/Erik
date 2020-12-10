import os
import sys
directory = os.path.dirname(__file__)+"\\5.1"
sys.path.insert(-1,directory)

from GlobalMomentofInertia import Ixx
print(Ixx_in_y)
#Max moment occurs at MZFW and n = 4.65 (the wing wants to bend upwards so the resulting moment in the root is negative but counterclockwise positive)

M_max = -45430675 #Nm CCW+ if seen from the back of the airplane
y_max = -0.97512 #This is an estimate fix it later

def Force_max(M_x, y_max, I_xx):
    Force_max =  (M_x * y_max)/(I_xx)
    return Force_max

I_xx = Ixx_in_y(0)

Force_max= Force_max(M_max, y_max, I_xx)
print(Force_max)