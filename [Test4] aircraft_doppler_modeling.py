from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem
from LEOVisual import LEOVisual
import matplotlib.pyplot as plt

GRID_ID = 10 # Fixed index for testing – do NOT modify
UE_ALT = 0
AIR_ALT = 10 # [km]
UE_VEL = 0 # [km/s]
AIR_VEL = 0.25 # [km/s]
LAT = 33.77108773051596
LON = -104.10327967561538

ue  = LEOCell(grid_id=GRID_ID, lat=LAT, lon=LON, alt=UE_ALT, vel_abs=UE_VEL)
air  = LEOCell(grid_id=GRID_ID, lat=LAT, lon=LON, alt=AIR_ALT, vel_abs=AIR_VEL, heading_deg=0) # 동쪽으로 움직임
sat = LEOSatellite(grid_id=GRID_ID)

pos_ue = ue.xyz
vel_ue = ue.vel
pos_air =air.xyz
vel_air = air.vel

print("baseline xyz ", sat.xyz[0])
print("new xyz ", sat.xyz[0])
print("baseline velocity ", sat.vel_baseline[0])
print("new velocity ", sat.vel[0])

# baseline
doppler_all = LEOSystem.cal_doppler(
    sat.xyz, pos_ue,
    sat.vel_baseline, vel_ue
)
dop, cdf_dop = LEOVisual.compute_cdf(doppler_all.flatten())


print(f"Baseline 0번째 셀-0번째 위성 Doppler shift [kHz]: {dop[0]}")

# new model
doppler_all_new = LEOSystem.cal_doppler(
    sat.xyz, pos_ue,
    sat.vel, vel_ue
)
dop_new, cdf_dop_new = LEOVisual.compute_cdf(doppler_all_new.flatten())
print(f"New 0번째 셀-0번째 위성 Doppler shift [kHz]: {dop_new[0]}")

# new model - aircraft
doppler_all_new_air = LEOSystem.cal_doppler(
    sat.xyz, pos_air,
    sat.vel, vel_air
)
dop_new_air, cdf_dop_new_air = LEOVisual.compute_cdf(doppler_all_new_air.flatten())
print(f"New 0번째 비행기-0번째 위성 Doppler shift [kHz]: {dop_new_air[0]}")


plt.figure(figsize=(7, 7))

LEOVisual.plot_doppler_cdf_sw(
    dop, cdf_dop
)

LEOVisual.plot_doppler_cdf_sw(
    dop_new, cdf_dop_new
)

LEOVisual.plot_doppler_cdf_sw(
    dop_new_air, cdf_dop_new_air
)

plt.plot(dop, cdf_dop, '-', color='blue', linewidth=2.0, label="Baseline_vel groundUE")
plt.plot(dop_new, cdf_dop_new, '--', color='red', linewidth=2.0, label="Theory_vel groundUE")
plt.plot(dop_new_air, cdf_dop_new_air, '-*', color='gray', linewidth=2.0, label="Theory_vel aircraft")

plt.xlabel("Doppler Frequency [kHz]")
plt.ylabel("CDF")
plt.title("Doppler CDF Comparison")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()