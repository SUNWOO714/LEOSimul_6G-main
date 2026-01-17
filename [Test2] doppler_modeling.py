import numpy as np
import matplotlib.pyplot as plt
from LEOCell import LEOCell
from LEOSatellite import LEOSatellite
from LEOSystem import LEOSystem
from LEOVisual import LEOVisual

GRID_ID = 10 # Fixed index for testing – do NOT modify

ue  = LEOCell(grid_id=GRID_ID)
sat = LEOSatellite(grid_id=GRID_ID)

pos_sat = sat.xyz
pos_ue  = ue.xyz
vel_sat  = sat.vel
       
doppler_all = LEOSystem.cal_doppler(pos_sat, pos_ue, vel_sat)
doppler_flat = doppler_all.flatten() 
dop, cdf_dop = LEOVisual.compute_cdf(doppler_flat)
LEOVisual.plot_doppler_cdf(dop, cdf_dop)