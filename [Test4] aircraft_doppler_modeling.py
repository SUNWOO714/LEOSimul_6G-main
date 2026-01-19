from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem
from LEOVisual import LEOVisual
import matplotlib.pyplot as plt

GRID_ID = 10

ue  = LEOCell(grid_id=GRID_ID)
sat = LEOSatellite(grid_id=GRID_ID)

pos_ue = ue.xyz
vel_ue = ue.vel

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
plt.figure(figsize=(7, 7))

LEOVisual.plot_doppler_cdf_sw(
    dop, cdf_dop
)

LEOVisual.plot_doppler_cdf_sw(
    dop_new, cdf_dop_new
)

plt.plot(dop, cdf_dop, '-', color='blue', linewidth=2.0, label="Baseline SAT velocity")
plt.plot(dop_new, cdf_dop_new, '--', color='red', linewidth=2.0, label="New SAT velocity function")

plt.xlabel("Doppler Frequency [kHz]")
plt.ylabel("CDF")
plt.title("Doppler CDF Comparison")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()