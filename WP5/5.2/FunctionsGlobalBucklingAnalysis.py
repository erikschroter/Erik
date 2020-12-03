# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:03:40 2020

@author: Erik Schroter
"""
from Definition_stringer_positions import Definition_stringer_position, stringer_distribution

segment_1 = 6.99 # m
segment_2 = 13.98 # m
segment_3 = 20.98 # m
segment_4 = 27.97 # m
segment_5 = 34.96 # m

initial = Definition_stringer_position(stringer_distribution,0)

def GlobalCentroid_def(y_span):
    if y_span > 0 and y_span <= segment_1:
# =============================================================================
# Initialise
# =============================================================================
        x_num = 0
        y_num = 0
        x_denom = 0
        y_denom = 0
# =============================================================================
# Iteration over Elements
# =============================================================================
        for num_el in range(0, len(initial)):
# =============================================================================
# For elements still existing
# =============================================================================
            if initial[num_el][3]==True:
# =============================================================================
# X - Numerator and Denominator
# =============================================================================                
                x_num_i = initial[num_el][0]
                x_num = x_num + x_num_i
                
                x_denom_i = initial[num_el][0] * initial[num_el][2]
                x_denom = x_denom + x_denom_i
# =============================================================================
# Y - Numerator and Denominator
# =============================================================================
                y_num_i = initial[num_el][1]
                y_num = y_num + y_num_i

                y_denom_i = initial[num_el][1] * initial[num_el][2]
                y_denom = y_denom + y_denom_i
# =============================================================================
# X - Y Centroids
# =============================================================================
        centroid_x1 = x_num / x_denom
        
        centroid_y1 = y_num / y_denom

    return centroid_x1, centroid_y1

    if y_span > segment_1 and y_span <= segment_2:
# =============================================================================
# Initialise
# =============================================================================
        x_num = 0
        y_num = 0
        x_denom = 0
        y_denom = 0
# =============================================================================
# Iteration over Elements
# =============================================================================
        for num_el in range(0, len(initial)):
# =============================================================================
# For elements still existing
# =============================================================================
            if initial[num_el][3]==True:
# =============================================================================
# X - Numerator and Denominator
# =============================================================================                
                x_num_i = initial[num_el][0]
                x_num = x_num + x_num_i
                
                x_denom_i = initial[num_el][0] * initial[num_el][2]
                x_denom = x_denom + x_denom_i
# =============================================================================
# Y - Numerator and Denominator
# =============================================================================
                y_num_i = initial[num_el][1]
                y_num = y_num + y_num_i

                y_denom_i = initial[num_el][1] * initial[num_el][2]
                y_denom = y_denom + y_denom_i
# =============================================================================
# X - Y Centroids
# =============================================================================
        centroid_x2 = x_num / x_denom
        
        centroid_y2 = y_num / y_denom

    return centroid_x2, centroid_y2
        
    if y_span > segment_2 and y_span <= segment_3:
# =============================================================================
# Initialise
# =============================================================================
        x_num = 0
        y_num = 0
        x_denom = 0
        y_denom = 0
# =============================================================================
# Iteration over Elements
# =============================================================================
        for num_el in range(0, len(initial)):
# =============================================================================
# For elements still existing
# =============================================================================
            if initial[num_el][3]==True:
# =============================================================================
# X - Numerator and Denominator
# =============================================================================                
                x_num_i = initial[num_el][0]
                x_num = x_num + x_num_i
                
                x_denom_i = initial[num_el][0] * initial[num_el][2]
                x_denom = x_denom + x_denom_i
# =============================================================================
# Y - Numerator and Denominator
# =============================================================================
                y_num_i = initial[num_el][1]
                y_num = y_num + y_num_i

                y_denom_i = initial[num_el][1] * initial[num_el][2]
                y_denom = y_denom + y_denom_i
# =============================================================================
# X - Y Centroids
# =============================================================================
        centroid_x3 = x_num / x_denom
        
        centroid_y3 = y_num / y_denom

    return centroid_x3, centroid_y3
        
    if y_span > segment_3 and y_span <= segment_4:
# =============================================================================
# Initialise
# =============================================================================
        x_num = 0
        y_num = 0
        x_denom = 0
        y_denom = 0
# =============================================================================
# Iteration over Elements
# =============================================================================
        for num_el in range(0, len(initial)):
# =============================================================================
# For elements still existing
# =============================================================================
            if initial[num_el][3]==True:
# =============================================================================
# X - Numerator and Denominator
# =============================================================================                
                x_num_i = initial[num_el][0]
                x_num = x_num + x_num_i
                
                x_denom_i = initial[num_el][0] * initial[num_el][2]
                x_denom = x_denom + x_denom_i
# =============================================================================
# Y - Numerator and Denominator
# =============================================================================
                y_num_i = initial[num_el][1]
                y_num = y_num + y_num_i

                y_denom_i = initial[num_el][1] * initial[num_el][2]
                y_denom = y_denom + y_denom_i
# =============================================================================
# X - Y Centroids
# =============================================================================
        centroid_x4 = x_num / x_denom
        
        centroid_y4 = y_num / y_denom

    return centroid_x4, centroid_y4

    if y_span > segment_4 and y_span <= segment_5:
# =============================================================================
# Initialise
# =============================================================================
        x_num = 0
        y_num = 0
        x_denom = 0
        y_denom = 0
# =============================================================================
# Iteration over Elements
# =============================================================================
        for num_el in range(0, len(initial)):
# =============================================================================
# For elements still existing
# =============================================================================
            if initial[num_el][3]==True:
# =============================================================================
# X - Numerator and Denominator
# =============================================================================                
                x_num_i = initial[num_el][0]
                x_num = x_num + x_num_i
                
                x_denom_i = initial[num_el][0] * initial[num_el][2]
                x_denom = x_denom + x_denom_i
# =============================================================================
# Y - Numerator and Denominator
# =============================================================================
                y_num_i = initial[num_el][1]
                y_num = y_num + y_num_i

                y_denom_i = initial[num_el][1] * initial[num_el][2]
                y_denom = y_denom + y_denom_i
# =============================================================================
# X - Y Centroids
# =============================================================================
        centroid_x5 = x_num / x_denom
        
        centroid_y5 = y_num / y_denom
        
    return centroid_x5, centroid_y5