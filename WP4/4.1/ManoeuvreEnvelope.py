import math as m

altitude = 31000 # ft

def Manoeuvre_Envelope(altitude):

    # Calculation n_max
    MTOW_kg = 304636
    MTOW_lb = MTOW_kg / 0.454
    n_max = 2.1 + 24000 / (MTOW_lb + 10000)
    if MTOW_lb > 50000:
        n_max = 2.5

    # Calculation stall speed flaps extended
    C_L_max = 2.3
    S = 543.25
    W_S = MTOW_kg / S
    rho_0 = 1.225
    V_A = m.sqrt(n_max * W_S / C_L_max * 2 / rho_0)
    V_iterate = 0
    n_stall_speed_clean = []
    while V_iterate < V_A:
        n_stall_speed_clean.append((V_iterate, 0.5 * rho_0 * V_iterate * V_iterate * C_L_max / W_S))
        V_iterate = V_iterate + 1

    # Calculation Dive Speed

    # ------------------------------------------------------------------------------------------------------------------
    # ISA Calculator

    alt = altitude * 0.3048

    T0 = 288.15
    T = T0
    h0 = 0
    p0 = 101325
    p = p0
    g0 = 9.80665
    R = 287
    rho0 = p0 / (R * T0)

    height = [0, 11000, 20000, 32000, 47000, 51000, 71000, 86000]
    grad = [-0.0065, 0, 0.0010, 0.0028, 0, -0.0028, -0.0020]

    # for command to allow calculate the temperature, pressure and density at the given altitude.

    for i in range(len(height) - 1):
        a = grad[i]
        minimum = height[i]
        maximum = height[i + 1]

        if minimum < alt < maximum:
            difference = alt - minimum

        else:
            if alt < minimum:
                break
            else:
                if maximum < alt:
                    difference = maximum - minimum

        if abs(a) < 0.0001:
            T = T
            p = p * exp(-g0 / (R * T) * (difference))
            rho = p / (R * T)


        else:
            Tmin = T
            T = T + a * difference
            p = p * (T / Tmin) ** (-g0 / (a * R))
            rho = p / (R * T)

    a = 20.05 * m.sqrt(T)
    # ------------------------------------------------------------------------------------------------------------------

    M_c = 0.77
    V_D = M_c * a /0.8

    # Calculation opposite stall speed flaps extended
    n_min = -1

    C_L_max = 2.3
    S = 543.25
    W_S = MTOW_kg / S
    rho_0 = 1.225
    V_A_min = m.sqrt(-n_min * W_S / C_L_max * 2 / rho_0)
    V_iterate = 0
    n_min_stall_speed_clean = []
    while V_iterate < V_A_min:
        n_min_stall_speed_clean.append((V_iterate, -0.5 * rho_0 * V_iterate * V_iterate * C_L_max / W_S))
        V_iterate = V_iterate + 1

    return V_D, n_max, n_stall_speed_clean, n_min_stall_speed_clean

print(Manoeuvre_Envelope(altitude))