import math as m

"""Function to calculate the torque contribution from the thrustforce of the engine
If questions ask Christoph Pabsch"""

def TorqueFromThrust(chordwise_location_centroid, height_from_chordline_centroid):
    """Input for function: thrust (one engine!), sweep flexural axis
    Output of function: spanwise torque distribution"""

    sweep_LE = 31.329  # [degrees]
    root_chord = 11.95  # [m]
    tip_chord = 3.59  # [m]
    span = 69.92  # [m]
    taper_ratio = 0.3

    thrust = 432000  # [N]

    distance_engine_center_chordline = 2.569  # [m]
    spanwise_position_engine = 11.5  # [m]
    chord_length_engine = root_chord + (root_chord - tip_chord) - spanwise_position_engine / (span / 2)
    z_dist = height_from_chordline_centroid * chord_length_engine + distance_engine_center_chordline

    sweep_flexural_axis = m.atan(m.tan(sweep_LE * m.pi / 180) - chordwise_location_centroid * 2 * root_chord / span * (1 - taper_ratio))

    torque_contribution_engine = z_dist * thrust * m.cos(sweep_flexural_axis)
    bending_moment_contribution_engine = z_dist * thrust * m.sin(sweep_flexural_axis)

    return [torque_contribution_engine, bending_moment_contribution_engine]


"""
USE THE FOLLOWING LINES TO TEST THE FUNTION

chordwise_location_centroid = 0.367  # *c
height_from_chordline_centroid = 0.1  # *c

result, result2 = TorqueFromThrust(chordwise_location_centroid, height_from_chordline_centroid)
print(result, result2)
"""
