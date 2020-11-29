import Moment_of_Inertia_Wingbox as WB

Alrho = 2700    #Aluminium density
t = WB.t
Stringerslength = WB.Stringersno

WB_chord = 0.45
WB_front_height = 0.1347
WB_aft_height = 0.1091

Cr = 11.95  #Root chord
Ct = 3.59   #Root tip

h1 = WB_chord * Cr
a1 = WB_aft_height * Cr
b1 = WB_front_height * Cr

h2 = WB_chord * Ct
a2 = WB_aft_height * Ct
b2 = WB_front_height * Ct

h3 = 34.9   #Half span

Area1 = (2*h1 +a1 +b1) * t  #Base Area
Area2 = (2*h2 +a2 +b2) * t  #Top Area

V = 1/3*h3 *(Area1 +Area2 + (Area1 * Area2)**0.5)
MassWB = 2 * V * Alrho

AreaSt = WB.tS * (2 * WB.aS - WB.tS)    #Cross sectional area for singe stringer

MassSt = 2 * AreaSt * Alrho * sum(Stringerslength) * 34.96/5

print(MassSt + MassWB)
print(MassWB)
print(MassSt)