import numpy as np
import matplotlib.pyplot as plt

# Parameter Sistem Dinamik Suhu Ruangan (ODE Orde-1)
C = 100.0       # Kapasitas kalor efektif ruangan (kJ/degC)
UA = 0.5        # Konduktansi termal efektif dinding x luas (kW/degC)
T_amb = 30.0    # Suhu lingkungan luar / gangguan konstan (degC)
T_init = 30.0   # Kondisi awal suhu ruangan pada t = 0 (degC)

def simulasi_euler(u_input, dt_step, T0=T_init):
    T_hist = np.zeros_like(u_input, dtype=float)
    T_hist[0] = T0
    for i in range(1, len(u_input)):
        # Neraca energi: C * (dT/dt) = Q_ctrl(t) - UA * (T(t) - T_amb)
        dT_dt = (u_input[i - 1] - UA * (T_hist[i - 1] - T_amb)) / C
        T_hist[i] = T_hist[i - 1] + dT_dt * dt_step
    return T_hist

# 1. Simulasi Steady State (t = 0..1000, dt = 0.5)
dt_ss = 0.5
t_ss = np.arange(0.0, 1000.0 + dt_ss, dt_ss)
u_steady = np.full_like(t_ss, -5.0)
T_steady = simulasi_euler(u_steady, dt_ss)
T_ss_analitik = T_amb + (-5.0) / UA
print(f"Suhu Steady State Analitik : {T_ss_analitik:.2f} degC")
print(f"Suhu Simulasi (t=1000)     : {T_steady[-1]:.2f} degC")

# 2. Simulasi Respon Sinyal Kontrol (t = 0..400, dt = 0.5)
dt_c = 0.5
t_c = np.arange(0.0, 400.0 + dt_c, dt_c)

u_step = np.where(t_c >= 40.0, -5.0, 0.0)
T_step = simulasi_euler(u_step, dt_c)

u_impulse = np.where((t_c >= 40.0) & (t_c < 45.0), -60.0, 0.0)
T_impulse = simulasi_euler(u_impulse, dt_c)

u_ramp = np.zeros_like(t_c)
for idx, waktu in enumerate(t_c):
    if waktu < 40.0:
        u_ramp[idx] = 0.0
    elif waktu <= 140.0:
        u_ramp[idx] = -6.0 * ((waktu - 40.0) / 100.0)
    else:
        u_ramp[idx] = -6.0
T_ramp = simulasi_euler(u_ramp, dt_c)

u_sinusoid = -4.0 + 3.0 * np.sin(2.0 * np.pi * t_c / 100.0)
T_sinusoid = simulasi_euler(u_sinusoid, dt_c)

print(f"Suhu Step akhir (t=400)     : {T_step[-1]:.2f} degC")
print(f"Suhu Impulse akhir (t=400)  : {T_impulse[-1]:.2f} degC")
print(f"Suhu Ramp akhir (t=400)     : {T_ramp[-1]:.2f} degC")
print(f"Suhu Sinusoid akhir (t=400) : {T_sinusoid[-1]:.2f} degC")
