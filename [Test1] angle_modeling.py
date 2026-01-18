import numpy as np
import matplotlib.pyplot as plt
from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem
from LEOVisual import LEOVisual
from LEOAircraft import LEOAircraft

GRID_ID = 10 # Fixed index for testing – do NOT modify

ue  = LEOCell(grid_id=GRID_ID)
sat = LEOSatellite(grid_id=GRID_ID)

pos_sat = sat.xyz
pos_ue  = ue.xyz

elev_sat2ue = []
azi_sat2ue  = []
elev_ue2sat = []
azi_ue2sat  = []

for sat_idx in range(len(pos_sat)):

    sat_latlon_deg = LEOSystem.ecef2latlon(pos_sat)
    lat_sat, lon_sat = sat_latlon_deg[sat_idx][0], sat_latlon_deg[sat_idx][1]
    ue_latlon_deg = LEOSystem.ecef2latlon(pos_ue)

    for ue_idx in range(len(pos_ue)):
        lat_ue, lon_ue = ue_latlon_deg[ue_idx][0], ue_latlon_deg[ue_idx][1]

        # SAT 기준 -> UE 방향
        elev1, azi1 = LEOSystem.cal_angle(pos_sat[sat_idx], pos_ue[ue_idx], sat_latlon_deg, sat_idx)
        elev_sat2ue.append(elev1)
        azi_sat2ue.append(azi1)

        # UE 기준 -> SAT 방향
        elev2, azi2 = LEOSystem.cal_angle(pos_ue[ue_idx], pos_sat[sat_idx], ue_latlon_deg, ue_idx)
        elev_ue2sat.append(elev2)
        azi_ue2sat.append(azi2)

elev_sat2ue = np.array(elev_sat2ue)
azi_sat2ue  = np.array(azi_sat2ue)
elev_ue2sat = np.array(elev_ue2sat)
azi_ue2sat  = np.array(azi_ue2sat)
# LEOVisual.draw_map(grid_id, sat.grid_squares, sat.xyz)
############################## 비행기 시나리오 ##############################
AIR_ALT = 10.0 # [km]
AIR_SPEED = 0.25 # [km/s]
air = LEOAircraft(grid_id=GRID_ID, alt=AIR_ALT, vel_abs=AIR_SPEED)
# LEOVisual.draw_map_air(grid_id, sat.grid_squares, sat.xyz, air.xyz)
############################## 비행기 시나리오 ##############################

e1, cdf_e1 = LEOVisual.compute_cdf(elev_sat2ue)
e2, cdf_e2 = LEOVisual.compute_cdf(elev_ue2sat)
a1, cdf_a1 = LEOVisual.compute_cdf(azi_sat2ue)
a2, cdf_a2 = LEOVisual.compute_cdf(azi_ue2sat)

LEOVisual.plot_angle_cdf(e1, cdf_e1, e2, cdf_e2, a1, cdf_a1, a2, cdf_a2)