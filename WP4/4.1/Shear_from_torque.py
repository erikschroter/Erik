# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 15:47:29 2020

@author: Erik Schroter, Christoph Pabsch
"""

import sys
import os

directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "\\WP4\\5.3"
sys.path.insert(-1, directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "\\WP4\\5.2"
sys.path.insert(-1, directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "\\WP5\\5.1"
sys.path.insert(-1, directory)

import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import integrate
from scipy.interpolate import interp1d
from Definition_stringer_positions import t_wing_box_spar_cap
from torquedistribution import torque_function


# =============================================================================
# Torque Distribution
# =============================================================================

taperRatio = 0.3  # []
rootChord = 11.95  # [m]
wingSpan = 69.92  # [m]


def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord

y_list = []
shear_stresses = []

y = 0
for i in range(int(wingSpan / 2 * 100)):
    ChordLength = localChord(y)
    WingBoxLength = 0.450 * localChord(y)
    LocalWingBoxArea = 0.1091 * ChordLength * WingBoxLength + (0.0163 + 0.0093) * ChordLength / 2 * WingBoxLength
    AppliedTorque = torque_function(y)
    shear_stress = AppliedTorque / (2 * LocalWingBoxArea * t_wing_box_spar_cap/1000)
    y_list.append(y)
    shear_stresses.append(shear_stress)
    y = y + 0.01

shear_stress_from_torque_function = interp1d(y_list, shear_stresses, kind="linear", fill_value="extrapolate")
print(shear_stress_from_torque_function)
