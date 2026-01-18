from LEOSatellite import LEOSatellite
from LEOBase import LEOBase
from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem

GRID_ID = 10 # Fixed index for testing – do NOT modify

bs  = LEOBase(grid_id=GRID_ID)
ue  = LEOCell(grid_id=GRID_ID)
sat = LEOSatellite(grid_id=GRID_ID)

pos_sat = sat.xyz
pos_ue  = ue.xyz

vel_sat  = sat.vel
vel_ue = ue.vel
grid_squares = bs.grid_squares
#############################################################
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