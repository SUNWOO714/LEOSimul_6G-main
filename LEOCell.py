import numpy as np
import h3
from shapely.geometry import Point
from LEOBase import LEOBase
from LEOSystem import LEOSystem

class LEOCell(LEOBase):
    
    def __init__(self, grid_id: int, alt: float, vel_abs: float, lat: float = False, lon: float = False, heading_deg: float = None): # 비행기 위도/경도는 이 클래스 내에서 만들어주기로 함
    
        super().__init__(grid_id)

        # Aircraft (moving UE)
        if vel_abs > 0:

            # Aircraft의 ECEF 좌표
            self.xyz = np.array([
                LEOSystem.latlonalt2ecef(lat, lon, alt)
            ])
            # Aircraft의 위도/경도/고도
            self.latlonalt = np.column_stack((lat, lon, alt))

            e, n, _ = LEOSystem.latlon2enu(lat, lon)

            if heading_deg is None:
                raise ValueError("Aircraft requires heading_deg")

            heading = np.deg2rad(heading_deg)

            direction = (
                np.cos(heading) * e +
                np.sin(heading) * n
            )

            direction = direction / np.linalg.norm(direction)

            self.vel = np.array([vel_abs * direction])

        # Ground UE (static)
        else:
            Res4 = 4
            h3_cells = h3.polygon_to_cells(self.bbox, res=Res4)
            
            rows = []
            groundUE_alt = 0 # 지상 UE altitude [km]

            for h in h3_cells:
                lat_cell, lon_cell = h3.cell_to_latlng(h)
                if self.GRID_AREA.covers(Point(lon_cell, lat_cell)):
                    rows.append((h, lat_cell, lon_cell, groundUE_alt))

            cell_lat = np.array([r[1] for r in rows])
            cell_lon = np.array([r[2] for r in rows])
            cell_alt = np.array([r[3] for r in rows]) # [km]

            # UE의 ID
            self.id  = [r[0] for r in rows]

            self.xyz = np.array([
                LEOSystem.latlonalt2ecef(lat, lon, alt)
                for lat, lon in zip(cell_lat, cell_lon)
            ])

            self.latlonalt_cell = np.column_stack(
                (cell_lat, cell_lon, cell_alt)
            )

            self.vel = np.zeros((len(self.xyz), 3))