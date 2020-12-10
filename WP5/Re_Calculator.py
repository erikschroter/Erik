from ISAdef import ISA

def Re(V,L,alt):
    T_0 = 518.7
    mu_0 = 1.789*10**-5
    rho, T_k = ISA(alt)
    T_r = (T_k)*(9/5)
    mu = mu_0 * (T_r/T_0)
    nu = mu / rho
    Re = (V * L) / nu
    return Re
print(Re( 203.6, 8.52, 31000*.3048))