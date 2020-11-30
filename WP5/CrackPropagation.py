# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 15:00:00 2020

@author: Christoph Pabsch
"""

import math as m


def TensilePropagationStress(c):
    K_1c = 29 * 10 ^ 6  # Pa, material property of 
    Y = 1
    Tensile_Propagation_Stress = K_1c / (Y * m.sqrt(m.pi * c))
    return Tensile_Propagation_Stress
