import math as m
import matplotlib.pyplot as plt

altitude = 31000  # ft
Weight_kg = 304636  # kg

def Manoeuvre_Envelope(altitude, Weight_kg):

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

    height = [0, 11000, 20000, 32000, 47000, 51000, 71000, 86000]
    grad = [-0.0065, 0, 0.0010, 0.0028, 0, -0.0028, -0.0020]

    # for command to allow calculate the temperature, pressure and density at the given altitude.

    for i in range(len(height) - 1):
        a = grad[i]
        minimum = height[i]
        maximum = height[i + 1]

        if minimum <= alt <= maximum:
            difference = alt - minimum

        else:
            if alt <= minimum:
                break
            else:
                if maximum <= alt:
                    difference = maximum - minimum

        if abs(a) <= 0.0001:
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

    # Calculation n_max
    Weight_lb = Weight_kg / 0.454
    n_max = 2.1 + 24000 / (Weight_lb + 10000)
    if Weight_lb > 50000:
        n_max = 2.5
    n_max_flaps = 2.0

    # Calculation stall speed flaps retracted
    C_L_max = 1.3962
    S = 543.25
    W_S = Weight_kg * 9.81 / S
    rho_0 = rho
    V_A = m.sqrt(n_max * W_S / C_L_max * 2 / rho_0)
    V_iterate = 0
    n_stall_speed_clean = []
    while V_iterate < V_A:
        n_stall_speed_clean.append((0.5 * rho_0 * V_iterate * V_iterate * C_L_max / W_S))
        V_iterate = V_iterate + 1
    V_F = m.sqrt(2.0 * W_S / C_L_max * 2 / rho_0)

    # Calculation stall speed flaps extended
    C_L_max = 2.3
    S = 543.25
    W_S = Weight_kg * 9.81 / S
    rho_0 = rho
    V_A_flaps = m.sqrt(n_max_flaps * W_S / C_L_max * 2 / rho_0)
    V_iterate = 0
    n_stall_speed_flaps = []
    while V_iterate < V_A_flaps:
        n_stall_speed_flaps.append((0.5 * rho_0 * V_iterate * V_iterate * C_L_max / W_S))
        V_iterate = V_iterate + 1

    # Calculation Dive Speed
    M_c = 0.77
    V_D = M_c * a /0.8

    # Definition n_min
    n_min = -1

    # Calculation opposite stall speed flaps extended
    C_L_max = 1.3962
    S = 543.25
    W_S = Weight_kg * 9.81 / S
    rho_0 = rho
    V_A_min = m.sqrt(-n_min * W_S / C_L_max * 2 / rho_0)
    V_iterate = 0
    n_min_stall_speed_clean = []
    while V_iterate < V_A_min:
        n_min_stall_speed_clean.append((-0.5 * rho_0 * V_iterate * V_iterate * C_L_max / W_S))
        V_iterate = V_iterate + 1

    # Definition design cruise speed
    V_C = 232.46

    return V_D, n_max, n_stall_speed_clean, n_min_stall_speed_clean, V_A, V_A_min, V_C, n_stall_speed_flaps, V_A_flaps, V_F

V_D, n_max, n_stall_speed_clean, n_min_stall_speed_clean, V_A, V_A_min, V_C, n_stall_speed_flaps, V_A_flaps, V_F = Manoeuvre_Envelope(altitude, Weight_kg)

plt.plot(n_stall_speed_clean, "b")
plt.plot(n_min_stall_speed_clean, "b")
plt.plot([m.floor(V_A), V_A], [n_stall_speed_clean[-1], 2.5], "b")
plt.plot([m.floor(V_A_min), V_A_min], [n_min_stall_speed_clean[-1], -1], "b")
plt.plot([V_A, V_D], [2.5, 2.5], "b")
plt.plot([V_D, V_D], [0, 2.5], "b")
plt.plot([V_C, V_D], [-1, 0], "b")
plt.plot([V_A_min, V_C], [-1, -1], "b")
plt.plot(n_stall_speed_flaps, "b")
plt.plot([m.floor(V_A_flaps), V_A_flaps], [n_stall_speed_flaps[-1], 2.0], "b")
plt.plot([V_A_flaps, V_F], [2.0, 2.0], "b")

# plot formatting

plt.title('Manoeuvre Envelope')

plt.xlabel('V')
plt.ylabel('n')

plt.grid(True, which='both')
plt.axhline(y=0, color='k')

plt.show()