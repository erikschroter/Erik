import math as m

"""Function to calculate the weight of all structural components of the wing box.
If questions, ask Christoph Pabsch"""

from Definition_stringer_positions import Definition_stringer_position, t_wing_box_spar_cap, a_wing_box_spar_cap, stringer_distribution, t_wing_box_skin, a_stringer, h_stringer, t_stringer
from Rib_Sections_Definition import sections, t_rib, a_rib

root_chord = 11.95  # [m]
tip_chord = 3.59  # [m]
taper_ratio = tip_chord/root_chord
span = 69.92  # [m]
sweep_LE = 31.329  # [degrees]
density_aluminium = 2700 * 10**(-9)  # [kg/mm^3]


def localChord(spanValue):
    localChord = root_chord - (root_chord - tip_chord) / (span / 2) * spanValue
    return localChord


def Wing_Box_Weight(stringer_distribution, sections):
    Weight = 0

    # Add weight of top and bottom panel
    average_spar_ratio = (0.1347 + 0.1091)/2
    half_t_difference_root_tip = 1000 * average_spar_ratio * (root_chord - tip_chord) / 2
    length_top_and_bottom_skin = m.sqrt(half_t_difference_root_tip**2 + (1000*span/2)**2)
    length_top_panel_root = root_chord * m.sqrt(450**2 + 16.3**2)
    length_top_panel_tip = tip_chord * m.sqrt(450**2 + 16.3**2)
    average_top_panel_length = (length_top_panel_root + length_top_panel_tip)/2
    length_bottom_panel_root = root_chord * m.sqrt(450 ** 2 + 9.3 ** 2)
    length_bottom_panel_tip = tip_chord * m.sqrt(450 ** 2 + 9.3 ** 2)
    average_bottom_panel_length = (length_bottom_panel_root + length_bottom_panel_tip) / 2
    area_top_and_bottom_panel = length_top_and_bottom_skin * (average_bottom_panel_length + average_top_panel_length)
    volume_top_and_bottom_panel = area_top_and_bottom_panel * t_wing_box_skin
    weight_top_and_bottom_panel = volume_top_and_bottom_panel * density_aluminium
    print("Weight top and bottom panel: ", weight_top_and_bottom_panel, "kg")
    Weight = Weight + weight_top_and_bottom_panel

    # Add weight of spar caps
    average_chord_length = 1000 * localChord(span/4)
    average_front_spar_cap_height = 0.1347 * average_chord_length - 2 * t_wing_box_skin
    average_rear_spar_cap_height = 0.1091 * average_chord_length - 2 * t_wing_box_skin
    sweep_front_spar_cap = m.atan(m.tan(sweep_LE * m.pi / 180) - 0.15 * 2 * root_chord / span * (1 - taper_ratio))
    sweep_rear_spar_cap = m.atan(m.tan(sweep_LE * m.pi / 180) - 0.6 * 2 * root_chord / span * (1 - taper_ratio))
    length_front_spar_cap = span/(2 * m.cos(sweep_front_spar_cap))
    length_rear_spar_cap = span/(2 * m.cos(sweep_rear_spar_cap))
    area_front_spar_cap = 1000 * length_front_spar_cap * (average_front_spar_cap_height + 2 * a_wing_box_spar_cap - 2 * t_wing_box_spar_cap)
    area_rear_spar_cap = 1000 * length_rear_spar_cap * (average_rear_spar_cap_height + 2 * a_wing_box_spar_cap - 2 * t_wing_box_spar_cap)
    volume_spar_caps = (area_front_spar_cap + area_rear_spar_cap) * t_wing_box_spar_cap
    weight_spar_caps = volume_spar_caps * density_aluminium
    print("Weight spar caps: ", weight_spar_caps, "kg")
    Weight = Weight + weight_spar_caps

    # Add weight of stringers
    reference_chord_length = 1000 * localChord(0.001)
    stringer_positions = Definition_stringer_position(stringer_distribution, 0.001)
    top_stringers_chord_wise_location = []
    # Obtain for all stringers the position and their span-wise end
    for i in range(stringer_distribution[0][0]):
        chord_wise_location = stringer_positions[4+i][0] / reference_chord_length + 0.15
        y = 1
        j = True
        while y < span/2*100 and j == True:
            stringer_positions_test = Definition_stringer_position(stringer_distribution, y/100)
            if not stringer_positions_test[4 + i][3]:
                j = False
            else:
                y = y + 1
        top_stringers_chord_wise_location.append((chord_wise_location, y/100))
    bottom_stringers_chord_wise_location = []
    for i in range(stringer_distribution[0][1]):
        chord_wise_location = stringer_positions[4 + stringer_distribution[0][0] + i][0] / reference_chord_length + 0.15
        y = 1
        j = True
        while y < span / 2 * 100 and j == True:
            stringer_positions_test = Definition_stringer_position(stringer_distribution, y / 100)
            if not stringer_positions_test[4 + stringer_distribution[0][0] + i][3]:
                j = False
            else:
                y = y + 1
        bottom_stringers_chord_wise_location.append((chord_wise_location, y / 100))
    # Calculate length of all stringers combined
    total_stringers_length = 0
    for i in range(len(top_stringers_chord_wise_location)):
        sweep_stringer = m.atan(m.tan(sweep_LE * m.pi / 180) - top_stringers_chord_wise_location[i][0] * 2 * root_chord / span * (1 - taper_ratio))
        preliminary_length_stringer = top_stringers_chord_wise_location[i][1] * 1000 / m.cos(sweep_stringer)
        vertical_stringer_displacement = half_t_difference_root_tip * top_stringers_chord_wise_location[i][1] / (span/2)
        length_stringer = m.sqrt(preliminary_length_stringer**2 + vertical_stringer_displacement**2)
        total_stringers_length = total_stringers_length + length_stringer
    for i in range(len(bottom_stringers_chord_wise_location)):
        sweep_stringer = m.atan(m.tan(sweep_LE * m.pi / 180) - bottom_stringers_chord_wise_location[i][0] * 2 * root_chord / span * (1 - taper_ratio))
        preliminary_length_stringer = bottom_stringers_chord_wise_location[i][1] * 1000 / m.cos(sweep_stringer)
        vertical_stringer_displacement = half_t_difference_root_tip * bottom_stringers_chord_wise_location[i][1] / (span/2)
        length_stringer = m.sqrt(preliminary_length_stringer**2 + vertical_stringer_displacement**2)
        total_stringers_length = total_stringers_length + length_stringer
    # Cross-section stringer and final stringer volume and weight
    A_stringer = h_stringer * t_stringer + 2 * a_stringer * t_stringer
    volume_stringers = A_stringer * total_stringers_length
    weight_stringers = volume_stringers * density_aluminium
    print("Weight stringers: ", weight_stringers, "kg")
    Weight = Weight + weight_stringers


    # Add weight of ribs
    weight_ribs = 0
    for i in range(len(sections)):
        span_location = sections[i]
        ChordLength = 1000 * localChord(span_location)
        height_front_spar = 134.7 / 1000 * ChordLength
        height_rear_spar = 109.1 / 1000 * ChordLength
        top_difference_rear_spar = 16.3 / 1000 * ChordLength
        bottom_difference_rear_spar = 9.3 / 1000 * ChordLength
        area_rib = height_rear_spar * 0.45 * ChordLength + 0.5 * 0.45 * ChordLength * (top_difference_rear_spar + bottom_difference_rear_spar) + (a_rib - t_rib) * (height_front_spar + height_rear_spar + m.sqrt((0.45 * ChordLength) ** 2 + top_difference_rear_spar ** 2) + m.sqrt((0.45 * ChordLength) ** 2 + bottom_difference_rear_spar ** 2))
        volume_rib = area_rib * t_rib
        weight_rib = volume_rib * density_aluminium
        weight_ribs = weight_ribs + weight_rib
    print("Weight ribs: ", weight_ribs, "kg")
    Weight = Weight + weight_ribs

    return Weight


Weight = Wing_Box_Weight(stringer_distribution, sections)
print("--------------------------")
print("Total wing box weight for half a wing:", Weight, "kg")
print("Total wing box weight for full wing", Weight * 2, "kg")
