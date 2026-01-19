import numpy as np
from LEOSatellite import LEOSatellite
from LEOBase import LEOBase
from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem

GRID_ID = 10 # Fixed index for testing – do NOT modify
UE_ALT = 0
AIR_ALT = 10 # [km]
UE_VEL = 0 # [km/s]
AIR_VEL = 0.25 # [km/s]
LAT = 33.77108773051596
LON = -104.10327967561538

bs  = LEOBase(grid_id=GRID_ID)
sat = LEOSatellite(grid_id=GRID_ID)

# 비행기
(grid_lon_min, grid_lat_min,
    grid_lon_max, grid_lat_max) = bs.GRID_AREA.bounds
LAT = np.random.uniform(grid_lat_min, grid_lat_max) 
LON = np.random.uniform(grid_lon_min, grid_lon_max)

air  = LEOCell(grid_id=GRID_ID, alt=AIR_ALT, lat=LAT, lon=LON, vel_abs=AIR_VEL, heading_deg=0) # 동쪽으로 움직임

# 고정 지상 유저
ue  = LEOCell(grid_id=GRID_ID, alt=UE_ALT, vel_abs=UE_VEL)

pos_sat = sat.xyz
pos_ue  = ue.xyz

vel_sat  = sat.vel
vel_ue = ue.vel
grid_squares = bs.grid_squares
#############################################################
air_idx = 0 # Fixed index for testing – do NOT modify (단일 비행기 시나리오)
ue_idx = 10 # Fixed index for testing – do NOT modify
sat_idx = 0 # Fixed index for testing – do NOT modify
#############################################################
print("\n")
print("======================================== Test3 Results ======================================== ")

# ECEF coordinates of the selected satellite and cell center
print("ECEF position of the selected satellite [km]:", pos_sat[sat_idx])
print("ECEF position of the selected cell center [km]:", pos_ue[ue_idx], "\n")

# Latitude and longitude of the selected satellite
sat_latlon_deg = LEOSystem.ecef2latlon(pos_sat)
print(
    "Latitude / Longitude of the selected satellite [deg]:",
    sat_latlon_deg[sat_idx][0], sat_latlon_deg[sat_idx][1]
)

# Latitude and longitude of the selected cell center
ue_latlon_deg = LEOSystem.ecef2latlon(pos_ue)
print(
    "Latitude / Longitude of the selected cell center [deg]:",
    ue_latlon_deg[ue_idx][0], ue_latlon_deg[ue_idx][1], "\n"
)

# Azimuth and elevation angles (selected satellite -> selected cell center)
elev1, azi1 = LEOSystem.cal_angle(pos_sat[sat_idx], pos_ue[ue_idx], sat_latlon_deg, sat_idx)
print("Elevation / Azimuth from SAT to UE [deg]:", elev1, azi1)

# Azimuth and elevation angles (selected cell center -> selected satellite)
elev2, azi2 = LEOSystem.cal_angle(pos_ue[ue_idx], pos_sat[sat_idx], ue_latlon_deg, ue_idx)
print("Elevation / Azimuth from UE to SAT [deg]:", elev2, azi2, "\n")

# Distance between the selected satellite and the selected cell center
distance = LEOSystem.cal_distance(pos_sat, pos_ue)
print("ECEF distance between the selected satellite and the selected cell center [km]:")
print(distance[sat_idx][ue_idx], "\n")

# Doppler shift for the selected cell with respect to all satellites
doppler = LEOSystem.cal_doppler(pos_sat, pos_ue, vel_sat, vel_ue)
print(f"Doppler shift of the selected cell center for the selected satellite [kHz]:")
print(doppler[sat_idx][ue_idx])

print(" ------------------------------ Aircraft ------------------------------")
# air = LEOAircraft(grid_id=GRID_ID, lat=33.77108773051596, lon=-104.10327967561538, alt=AIR_ALT, vel_abs=AIR_SPEED) # TEST용


pos_air = air.xyz
vel_air  = air.vel

# ECEF coordinates of the selected satellite and aircraft
print("ECEF position of the selected satellite [km]:", pos_sat[sat_idx])
print("ECEF position of the selected aircraft [km]:", pos_air[air_idx], "\n")

# Latitude and longitude of the selected satellite
sat_latlon_deg = LEOSystem.ecef2latlon(pos_sat)
print(
    "Latitude / Longitude of the selected satellite [deg]:",
    sat_latlon_deg[sat_idx][0], sat_latlon_deg[sat_idx][1]
)

# Latitude and longitude of the selected aircraft
air_latlon_deg = LEOSystem.ecef2latlon(pos_air)
print(
    "Latitude / Longitude of the selected aircraft [deg]:",
    air_latlon_deg[air_idx][0], air_latlon_deg[air_idx][1], "\n"
)

# Azimuth and elevation angles (selected satellite -> selected aircraft)
elev1, azi1 = LEOSystem.cal_angle(pos_sat[sat_idx], pos_air[air_idx], sat_latlon_deg, sat_idx)
print("Elevation / Azimuth from SAT to UE [deg]:", elev1, azi1)

# Azimuth and elevation angles (selected aircraft -> selected satellite)
elev2, azi2 = LEOSystem.cal_angle(pos_air[air_idx], pos_sat[sat_idx], air_latlon_deg, air_idx)
print("Elevation / Azimuth from UE to SAT [deg]:", elev2, azi2, "\n")

# Distance between the selected satellite and the selected aircraft
print(pos_ue)
print(pos_air)
distance = LEOSystem.cal_distance(pos_sat, pos_air)
print("ECEF distance between the selected satellite and the selected aircraft [km]:")
print(distance[sat_idx][air_idx], "\n")

# Doppler shift for the selected cell with respect to all satellites
doppler = LEOSystem.cal_doppler(pos_sat, pos_air, vel_sat, vel_air)
print(f"Doppler shift of the selected aircraft for the selected satellite [kHz]:")
print(doppler[sat_idx][air_idx])

# # 비행기와 위성 간 이동 방향이 같은지/ 다른지 내적을 통해 판별
# cos_theta = np.dot(vel_sat[sat_idx], vel_air[air_idx]) / (np.linalg.norm(vel_sat[sat_idx]) * np.linalg.norm(vel_air[air_idx]))
# if cos_theta > 0:
#     print(f"내적 결과: {cos_theta} -> 비행기와 위성은 거의 같은 이동방향")
# else:
#     print(f"내적 결과: {cos_theta} -> 비행기와 위성의 이동방향은 다름")

print(" ======================================== Test3 Results ======================================== ")
print("\n")

