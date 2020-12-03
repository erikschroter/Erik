import math as m

"""Function to calculate the position of the stringers for a given stringer distribution from the bottom left corner of 
the wing box
If questions, ask Christoph Pabsch"""

stringer_distribution = [(14,14),(12,12),(10,10),(8,8),(6,6)]  # from root to tip, (top, bottom)


def Definition_stringer_position(stringer_distribution, spanwise_position):

    root_chord = 11.95  # [m]
    tip_chord = 3.59  # [m]
    span = 69.92  # [m]
    chord_length = 1000 * (root_chord - (root_chord - tip_chord) * spanwise_position / (span / 2))

    # wing box dimensions
    t_wing_box_skin = 10
    wing_box_length = 45/100 * chord_length
    height_front_spar = 134.7/1000 * chord_length
    height_rear_spar = 109.1/1000 * chord_length
    top_difference_rear_spar = 16.3/1000 * chord_length
    bottom_difference_rear_spar = 9.3/1000 * chord_length

    # Spar caps dimensions
    t_wing_box_spar_cap = 10
    a_wing_box_spar_cap = 110

    # stringer dimensions
    a_stringer = 110
    h_stringer = 110
    t_stringer = 5

    A_stringer = h_stringer * t_stringer + 2 * a_stringer * t_stringer

    stringer_positions = []
    present = True

    # Position front spar
    A_front_spar = t_wing_box_spar_cap * (height_front_spar - 2 * t_wing_box_skin - 2 * t_wing_box_spar_cap + 2 *
                                          a_wing_box_spar_cap)
    x = (t_wing_box_spar_cap/2 * t_wing_box_spar_cap * (height_front_spar - 2 * t_wing_box_skin - 2 *
                                                        t_wing_box_spar_cap) + a_wing_box_spar_cap/2 *
         a_wing_box_spar_cap * t_wing_box_spar_cap) / A_front_spar
    y = height_front_spar/2
    stringer_positions.append((x, y, A_front_spar, present))

    # Position rear spar
    A_rear_spar = t_wing_box_spar_cap * (height_rear_spar - 2 * t_wing_box_skin - 2 * t_wing_box_spar_cap + 2 *
                                         a_wing_box_spar_cap)
    x = wing_box_length - (t_wing_box_spar_cap/2 * t_wing_box_spar_cap * (height_rear_spar - 2 * t_wing_box_skin - 2 *
                                                                          t_wing_box_spar_cap) + a_wing_box_spar_cap/2 *
                           a_wing_box_spar_cap * t_wing_box_spar_cap) / A_rear_spar
    y = bottom_difference_rear_spar + height_rear_spar / 2
    stringer_positions.append((x, y, A_rear_spar, present))

    # Position top skin
    length_top_skin = m.sqrt(wing_box_length**2 + top_difference_rear_spar**2)
    A_top_skin = length_top_skin * t_wing_box_skin
    x = wing_box_length/2
    y = height_front_spar - top_difference_rear_spar/2 - t_wing_box_skin/2
    stringer_positions.append((x, y, A_top_skin, present))

    # Position bottom skin
    length_bottom_skin = m.sqrt(wing_box_length ** 2 + bottom_difference_rear_spar ** 2)
    A_bottom_skin = length_bottom_skin * t_wing_box_skin
    x = wing_box_length / 2
    y = bottom_difference_rear_spar / 2 + t_wing_box_skin / 2
    stringer_positions.append((x, y, A_bottom_skin, present))

    # Positions top stringers
    n = 0
    for i in range(stringer_distribution[0][0]+2):
        distance_between_stringers = (wing_box_length - a_stringer - 2*t_wing_box_skin) / (stringer_distribution[0][0]+2)
        x = a_stringer/2 + n * distance_between_stringers
        y = height_front_spar - t_wing_box_skin - h_stringer/2 - top_difference_rear_spar * x / wing_box_length
        stringer_positions.append((x, y, A_stringer, present))
        n = n + 1

    # Positions bottom stringers
    n = 0
    for i in range(stringer_distribution[0][1] + 2):
        distance_between_stringers = (wing_box_length - a_stringer - 2*t_wing_box_skin) / (stringer_distribution[0][1]+2)
        x = a_stringer / 2 + n * distance_between_stringers
        y = t_wing_box_skin + h_stringer / 2 + bottom_difference_rear_spar * x / wing_box_length
        stringer_positions.append((x, y, A_stringer, present))
        n = n + 1

    return stringer_positions


print(Definition_stringer_position(stringer_distribution, 0))