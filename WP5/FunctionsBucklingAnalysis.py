# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 14:53:19 2020

@author: Erik Schroter
"""


# Margin of Safety Function
def MoSdef(failure_stress, applied_stress):
    MoS = failure_stress / applied_stress
    if MoS < 1:
        print("\n !!! STRUCTURAL FAILURE !!!")
    return MoS

# Shear Buckling
# Skin Buckling
# Column Buckling
# Compressive strength failure
