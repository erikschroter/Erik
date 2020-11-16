#chord
croot=11.95
taperratio=0.3
y=41.25
b=69.92
c=croot*(taperratio+(1-taperratio)*y/b)

#Dimensions trapezoid
h=0.45*c
a=0.1091*c
b=0.1347*c
c=0.0163*c
t=0.005

#Dimensions stringers
tS=0.005
aS=10*tS
bS=aS
n=4

#values trapezoid
Cchord=(h/3)*((2*a+b)/(a+b))


#Values Stringer
Astringer=tS*(aS*2-t)
Cy=(aS**2+aS*tS-tS**2)/(2*(2*aS-tS))
Cx=(aS**2+aS*tS-tS**2)/(2*(2*aS-tS))

#Parrallel axis stringers
I=[]
#2 is actually n/2
for i in range(0, 2):
    ParAxisOne=Astringer*(Cchord-h/(n-1)*i-Cy)**2
    I.append(ParAxisOne)

for j in range(2, 4):
    ParAxisTwo=Astringer*(h/(n-1)*j-Cchord-Cy)**2
    I.append(ParAxisTwo)

SumI=sum(I)*2
print(I)
print(SumI)
print(Astringer)
print(Cy)
print(Cchord)

