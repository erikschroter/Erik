from liftdistribution import liftdistribution
from intigrate import BendingMoment

filename = 'MainWing_a0.00_v10.00ms.csv'
rho = 1.225
v = 70
span = 69.92
accuracy = 41

x, Llst, xnew, f, xdist = liftdistribution(filename, rho, v, span, accuracy)

def moment(x):
    return BendingMoment(f,x,xdist,0,False)



