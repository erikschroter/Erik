import os
import sys
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.1"
sys.path.insert(-1,directory)
directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+"\\WP4\\4.2"
sys.path.insert(-1,directory)



import math as m

from Definition_stringer_positions import Definition_stringer_position, stringer_distribution

spanwise_location = 5

def Distance_Stringers(stringer_distribution, spanwise_location):
    stringer_positions = Definition_stringer_position(stringer_distribution, spanwise_location)
    stringer_positions.pop(0)
    stringer_positions.pop(0)
    stringer_positions.pop(0)
    stringer_positions.pop(0)
    n = len(stringer_positions) / 2
    list_top_stringers = []
    list_bottom_stringers = []
    for i in range(int(n)):
        if not stringer_positions[0][3]:
            stringer_positions.pop(0)
        else:
            list_top_stringers.append(stringer_positions.pop(0))
    for i in range(int(n)):
        if not stringer_positions[0][3]:
            stringer_positions.pop(0)
        else:
            list_bottom_stringers.append(stringer_positions.pop(0))

    angle_top_plate = 2.08 * 3.14/180
    angle_bottom_plate = 1.18 * 3.14/180
    distance_top_stringers = []
    distance_bottom_stringers = []

    while len(list_top_stringers) > 1.5:
        distance_top_stringers.append(((list_top_stringers[1][0]-list_top_stringers[0][0])/m.cos(angle_top_plate), (list_top_stringers[0][1]+list_top_stringers[1][1])/2))
        list_top_stringers.pop(0)

    while len(list_bottom_stringers) > 1.5:
        distance_bottom_stringers.append(((list_bottom_stringers[1][0]-list_bottom_stringers[0][0])/m.cos(angle_bottom_plate), (list_bottom_stringers[0][1]+list_bottom_stringers[1][1])/2))
        list_bottom_stringers.pop(0)

    return distance_top_stringers, distance_bottom_stringers

print(Distance_Stringers(stringer_distribution, spanwise_location))
