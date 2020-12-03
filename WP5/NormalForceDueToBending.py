

#Max moment occurs at MZFW and n = 4.65 (the wing wants to bend upwards so the resulting moment in the root is negative but counterclockwise positive)

M_max = -45430675 #Nm CCW+ if seen from the back of the airplane

def Sigma_z(M_x, I_xx, I_yy,y):
    Sigma_z = (M_x * I_yy * y)/(I_xx*I_yy)
    return Sigma_z

#y_max at max distance from centre line

y_max = 0.97512 #This is a

def Force_max(M_x, y_max, I_xx):
    Force_max =  (M_x * y_max)/(I_xx)
    return Force_max

