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
from torquedistribution import torquedistribution
from ISAdef import ISA


# =============================================================================
# Torque Distribution
# =============================================================================

taperRatio = 0.3  # []
rootChord = 11.95  # [m]
wingSpan = 69.92  # [m]

MTOW = 304636.2789 # kg
MZFW = 161394.7263 # kg
OEW = 147780.3631 # kg

# Definition Load Case Scenario

Thrust_Setting = 100  # from 0 to 100 in percent
Weight_Setting = MTOW * 9.81  # N
n_Setting = 3.75
altitude = 0  # ft

alt = altitude * 0.3048
rho, T = ISA(alt)

xnew, final_integration_result, torque_function_positive = torquedistribution('MainWing_a0.00_v10.00ms.csv', rho, 70, 69.92, 100, 11.5, 100, -1.5, Weight_Setting)
xnew, final_integration_result, torque_function_negative = torquedistribution('MainWing_a0.00_v10.00ms.csv', rho, 70, 69.92, 100, 11.5, 0, 3.75, Weight_Setting)

def localChord(spanValue):
    localChord = rootChord - (rootChord - taperRatio * rootChord) / (wingSpan / 2) * spanValue
    return localChord

y_list = []
shear_stresses_positive = []
shear_stresses_negative = []

y = 0
for i in range(int(wingSpan / 2 * 100)):
    ChordLength = localChord(y)
    WingBoxLength = 0.450 * localChord(y)
    LocalWingBoxArea = 0.1091 * ChordLength * WingBoxLength + (0.0163 + 0.0093) * ChordLength / 2 * WingBoxLength
    AppliedTorque = torque_function_positive(y)
    shear_stress = AppliedTorque / (2 * LocalWingBoxArea * t_wing_box_spar_cap/1000)
    y_list.append(y)
    shear_stresses_positive.append(shear_stress)
    y = y + 0.01

y_list = []
y = 0
for i in range(int(wingSpan / 2 * 100)):
    ChordLength = localChord(y)
    WingBoxLength = 0.450 * localChord(y)
    LocalWingBoxArea = 0.1091 * ChordLength * WingBoxLength + (0.0163 + 0.0093) * ChordLength / 2 * WingBoxLength
    AppliedTorque = torque_function_negative(y)
    shear_stress = AppliedTorque / (2 * LocalWingBoxArea * t_wing_box_spar_cap/1000)
    y_list.append(y)
    shear_stresses_negative.append(shear_stress)
    y = y + 0.01

shear_stress_from_torque_positive_function = interp1d(y_list, shear_stresses_positive, kind="linear", fill_value="extrapolate")
shear_stress_from_torque_negative_function = interp1d(y_list, shear_stresses_negative, kind="linear", fill_value="extrapolate")
# print(shear_stress_from_torque_positive_function)
# print(shear_stress_from_torque_negative_function)
# print(shear_stresses_positive)
# print(shear_stresses_negative)
