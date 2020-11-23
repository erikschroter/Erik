import math

def ISA(h):
    # Needed constants for the ISA calculations
    g_0 = 9.80665  # m/s
    R = 287.0  # J/kgK
    T_0 = 288.15  # K
    p_0 = 101325.0  # Pa
    h_0 = 0  # m
    rho_0 = 1.225
    poop = 0

    # Temperature gradients (K/m)
    a_1 = -0.0065
    a_2 = 0
    a_3 = 0.001
    a_4 = 0.0028
    a_5 = 0
    a_6 = -0.0028
    a_7 = -0.002

    # Temperature calculations with the new altitude input

    if h <= 11000:
        T_1 = (T_0 + a_1 * (h - h_0))
        p_1 = (p_0 * ((T_1 / T_0) ** (-((g_0) / (a_1 * R)))))
        rho_1 = (p_1) / (R * T_1)
        rho=rho_1
    else:
        T_1 = T_0 + a_1 * (11000 - h_0)
        p_1 = p_0 * ((T_1 / T_0) ** (-((g_0) / (a_1 * R))))

    if h <= 20000 and h > 11000:
        T_2 = T_1 + a_1 * (h - 11000)
        p_2 = p_1 * (math.exp((-(g_0) / (R * T_2)) * (h - 11000)))
        rho_2 = (p_2) / (R * T_2)
        rho=rho_2
    else:
        T_2 = T_1 + a_2 * (20000 - 11000)
        p_2 = p_1 * (math.exp((-(g_0) / (R * T_2)) * (20000 - 11000)))

    if h <= 32000 and h > 20000:
        T_3 = T_2 + a_3 * (h - 20000)
        p_3 = p_2 * ((T_3 / T_2) ** (-((g_0) / (a_3 * R))))
        rho_3 = (p_3) / (R * T_3)
        rho=rho_3
    else:
        T_3 = T_2 + a_3 * (32000 - 20000)
        p_3 = p_2 * ((T_3 / T_2) ** (-((g_0) / (a_3 * R))))

    if h <= 47000 and h > 32000:
        T_4 = T_3 + a_4 * (h - 32000)
        p_4 = p_3 * ((T_4 / T_3) ** (-((g_0) / (a_4 * R))))
        rho_4 = (p_4) / (R * T_4)
        rho=rho_4
    else:
        T_4 = T_3 + a_4 * (47000 - 32000)
        p_4 = p_3 * ((T_4 / T_3) ** (-((g_0) / (a_4 * R))))

    if h <= 51000 and h > 47000:
        T_5 = T_4 + a_5 * (h - 47000)
        p_5 = p_4 * (math.exp((-(g_0) / (R * T_5)) * (h - 47000)))
        rho_5 = (p_5) / (R * T_5)
        rho=rho_5
    else:
        T_5 = T_4 + a_5 * (51000 - 47000)
        p_5 = p_4 * (math.exp((-(g_0) / (R * T_2)) * (51000 - 47000)))

    if h <= 71000 and h > 51000:
        T_6 = T_5 + a_6 * (h - 51000)
        p_6 = p_5 * ((T_6 / T_5) ** (-((g_0) / (a_6 * R))))
        rho_6 = (p_6) / (R * T_6)
        rho=rho_6
    else:
        T_6 = T_5 + a_6 * (71000 - 51000)
        p_6 = p_5 * ((T_6 / T_5) ** (-((g_0) / (a_6 * R))))

    if h <= 86000 and h >= 71000:
        T_7 = T_6 + a_7 * (h - 71000)
        p_7 = p_6 * ((T_7 / T_6) ** (-((g_0) / (a_7 * R))))
        rho_7 = (p_7) / (R * T_7)
        rho=rho_7
    else:
        T_7 = T_6 + a_7 * (86000 - 71000)
        p_7 = p_6 * ((T_7 / T_6) ** (-((g_0) / (a_7 * R))))

    if h > 86000:
        print('You have reached space sadly, we cannot speak of any pressure here try again.')

    return rho

print(ISA(11))
