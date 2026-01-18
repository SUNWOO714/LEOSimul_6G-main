import numpy as np
from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem
from LEOVisual import LEOVisual
from LEOAircraft import LEOAircraft

GRID_ID = 10 # Fixed index for testing – do NOT modify
AIR_ALT = 10.0 # [km]
AIR_SPEED = 0.25 # [km/s]

ue  = LEOCell(grid_id=GRID_ID)
sat = LEOSatellite(grid_id=GRID_ID)

pos_sat = sat.xyz           # (NSAT, 3)
vel_sat = sat.vel           # (NSAT, 3)
pos_ue = ue.xyz 
vel_ue = ue.vel

doppler_all = LEOSystem.cal_doppler(pos_sat, pos_ue, vel_sat, vel_ue)

doppler_flat = doppler_all.flatten() 
dop, cdf_dop = LEOVisual.compute_cdf(doppler_flat)

NAIR = len(pos_ue)
pos_air = np.zeros((NAIR, 3))
vel_air = np.zeros((NAIR, 3))

lat_air = []
lon_air = []
for idx in range(len(pos_ue)):
    lat_air = ue.latlonalt[idx, 0]
    lon_air = ue.latlonalt[idx, 1]
    air = LEOAircraft(grid_id=GRID_ID, lat=lat_air, lon=lon_air, alt=AIR_ALT, vel_abs=AIR_SPEED)
    pos_air[idx, :] = air.xyz
    vel_air[idx, :] = air.vel

doppler_all = LEOSystem.cal_doppler(pos_sat, pos_air, vel_sat, vel_air)

doppler_flat = doppler_all.flatten() 
dop_air, cdf_dop_air = LEOVisual.compute_cdf(doppler_flat)

LEOVisual.plot_doppler_cdf_compare(
    dop, cdf_dop,
    dop_air, cdf_dop_air,
    label1="Ground UE",
    label2="Aircraft (East, 10 km, 0.25 km/s)",
    title="LEO Doppler CDF Comparison (DL Ka-band 20GHz)"
)

# LEOVisual.plot_doppler_cdf_compare(
#     dop, cdf_dop,
#     dop_air, cdf_dop_air,
#     label1="Ground UE",
#     label2="Aircraft (West, 10 km, 0.25 km/s)",
#     title="LEO Doppler CDF Comparison (DL Ka-band 20GHz)"
# )