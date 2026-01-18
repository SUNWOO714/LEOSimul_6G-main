import h3
import numpy as np
from shapely.geometry import Point
from LEOBase import LEOBase
from LEOSystem import LEOSystem

class LEOCell(LEOBase):
    
    def __init__(self, grid_id: int):
        
        super().__init__(grid_id)
        
        # ------------ 지정된 grid 영역 내 UE의 ID, ECEF 좌표, 위도/경도/고도, 속도 생성 -------------
        Res4 = 4
        h3_cells = h3.polygon_to_cells(self.bbox, res=Res4)
        
        rows = []
        groundUE_alt = 0 # 지상 UE altitude [km]

        for h in h3_cells:
            lat, lon = h3.cell_to_latlng(h)
            if self.GRID_AREA.covers(Point(lon, lat)):
                rows.append((h, lat, lon, groundUE_alt))

        cell_lat = np.array([r[1] for r in rows])
        cell_lon = np.array([r[2] for r in rows])
        cell_alt = np.array([r[3] for r in rows]) # [km]

        # UE의 ID
        self.id  = [r[0] for r in rows]
        # UE의 ECEF 좌표
        self.xyz = np.array([
            LEOSystem.latlonalt2ecef(lat, lon, alt=groundUE_alt)
            for lat, lon in zip(cell_lat, cell_lon)
        ])  # [km]
        # UE의 위도/경도/고도
        self.latlonalt = np.column_stack((cell_lat, cell_lon, cell_alt))
        # UE의 속도
        self.vel = np.zeros((len(self.xyz), 3))