# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:28:41 2020

@author: Erik Schroter
"""
import os
import csv
import numpy as np

f = open('MainWing_a0.00_v10.00ms.csv')

csv_f = csv.reader(f)

ylst = []
clst = []
Ailst = []
Cllst = []
Cdlst = []
Cmlst = []

for columns in csv_f:
    ylst.append(columns[0])
    clst.append(columns[1])
    Ailst.append(columns[2])
    Cllst.append(columns[3])
    Cdlst.append(columns[5])
    Cmlst.append(columns[7])

row_begin = 21
row_end = 59

ylst = ylst[row_begin:row_end]
clst = clst[row_begin:row_end]
Ailst = Ailst[row_begin:row_end]
Cllst = Cllst[row_begin:row_end]
Cdlst = Cdlst[row_begin:row_end]
Cmlst = Cmlst[row_begin:row_end]

# print(ylst, clst, Ailst, Cllst, Cdlst, Cmlst)


f.close()