import h3
import numpy as np
from shapely.geometry import Point
from LEOBase import LEOBase
from LEOSystem import LEOSystem

class LEOCell(LEOBase):
    
    def __init__(self, grid_id: int):
        
        super().__init__(grid_id)
        
        # ------------ 지정된 grid 영역 내 UE의 ID, ECEF 좌표, 위도/경도 생성 -------------
        Res4 = 4
        h3_cells = h3.polygon_to_cells(self.bbox, res=Res4)

        rows = []

        # 지상 UE altitude
        alt = 0 # [km]

        for h in h3_cells:
            lat, lon = h3.cell_to_latlng(h)
            if self.GRID_AREA.covers(Point(lon, lat)):
                rows.append((h, lat, lon, alt))

        cell_lat = np.array([r[1] for r in rows])
        cell_lon = np.array([r[2] for r in rows])
        cell_alt = np.array([r[3] for r in rows]) # [km]

        self.id  = [r[0] for r in rows]

        self.xyz = np.array([
            LEOSystem.latlonalt2ecef(lat, lon, alt=0)   # 지상 UE altitude = 0
            for lat, lon in zip(cell_lat, cell_lon)
        ])  # [km]
        self.latlonalt = np.column_stack((cell_lat, cell_lon, cell_alt))
        # 여기에 self.vel에는 0의 벡터를 갖도록 설정해줘 3 by 생성된 셀 수
        self.vel = ??

    def __init__(self, grid_id: int, alt: float, vel_abs: float):
        super().__init__(grid_id)
        # 비행기 시나리오를 위한 initializaer야 lat, lon은 그리드 내에서 랜덤하게 설정되도록 코드를 구현해줘

    def __init__(self, grid_id: int, lat: float, lon: float, alt: float, vel_abs: float):
        super().__init__(grid_id)
        # 비행기 시나리오를 위한 initializaer야. 이건 테스트 용도로 만드려고 해 lat, lon을 동일하게 설정하는거지
