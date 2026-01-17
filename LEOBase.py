import numpy as np
import h3
from shapely.geometry import Polygon

class LEOBase:
    US_LAT_MIN=24.0   
    US_LAT_MAX=50.0 
    US_LON_MIN=-125.0
    US_LON_MAX=-64.0

    def __init__(self, grid_id: int):
        
        self.grid_id = grid_id
        self.xyz = np.nan
        self.id = np.nan
        self.latlonalt = np.nan
        self.vel = np.nan

    # ------------ 미국 전체 영역을 16개의 grid로 균등 분할한 grid polygon 생성 -------------
        nx, ny = 4, 4 # 4 by 4 = 16 grids
        lon_edges = np.linspace(LEOBase.US_LON_MIN, LEOBase.US_LON_MAX, nx + 1)
        lat_edges = np.linspace(LEOBase.US_LAT_MIN, LEOBase.US_LAT_MAX, ny + 1)

        self.grid_squares = {}
        for i in range(nx):
            for j in range(ny):
                gid = (ny - 1 - j) * nx + i + 1

                self.grid_squares[gid] = Polygon([
                    (lon_edges[i],   lat_edges[j]),
                    (lon_edges[i+1], lat_edges[j]),
                    (lon_edges[i+1], lat_edges[j+1]),
                    (lon_edges[i],   lat_edges[j+1]),
                ])

        self.bbox = h3.LatLngPoly([
            (LEOBase.US_LAT_MIN, LEOBase.US_LON_MIN),
            (LEOBase.US_LAT_MIN, LEOBase.US_LON_MAX),
            (LEOBase.US_LAT_MAX, LEOBase.US_LON_MAX),
            (LEOBase.US_LAT_MAX, LEOBase.US_LON_MIN),
            (LEOBase.US_LAT_MIN, LEOBase.US_LON_MIN)
        ])

        self.GRID_AREA = self.grid_squares[self.grid_id]

        if self.grid_id not in self.grid_squares:
            raise ValueError(f"GRID_ID={self.grid_id} invalid")