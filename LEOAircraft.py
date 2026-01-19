import numpy as np
from LEOBase import LEOBase
from LEOSystem import LEOSystem
np.random.seed(42) # 시뮬 진행 시 매번 같은 랜덤값 생성


class LEOAircraft(LEOBase):

    # def __init__(self, grid_id: int, alt: float, vel_abs: float):
    #     super().__init__(grid_id)
    #     # 비행기 시나리오를 위한 initializaer야 lat, lon은 그리드 내에서 랜덤하게 설정되도록 코드를 구현해줘

    #     # ------------ 지정된 grid 영역 내 Aircraft의 ECEF 좌표, 위도/경도/고도, 속도 생성 -------------
    #     (grid_lon_min,grid_lat_min,
    #      grid_lon_max,grid_lat_max) = self.GRID_AREA.bounds
    #     lat = np.random.uniform(grid_lat_min, grid_lat_max) 
    #     lon = np.random.uniform(grid_lon_min, grid_lon_max)

    #     # Aircraft의 ECEF 좌표
    #     self.xyz = np.array([LEOSystem.latlonalt2ecef(lat, lon, alt)])

    #     z = np.array([0.0, 0.0, 1.0]) # Earth rotation axis (ECEF)
    #     r = self.xyz[0] # r: aircraft ECEF position (3,)
    #     east = np.cross(z, r)
    #     east = east / np.linalg.norm(east)
    #     # Aircraft의 위도/경도/고도
    #     self.latlonalt = np.column_stack((lat, lon, alt))
    #     # Aircraft의 속도
    #     self.vel = np.array([vel_abs * east])
        
    def __init__(self, grid_id: int, lat: float, lon: float, alt: float, vel_abs: float):
        super().__init__(grid_id)
        # 비행기 시나리오를 위한 initializaer야. 이건 테스트 용도로 만드려고 해 lat, lon을 동일하게 설정하는거지

        # ------------ 지정된 grid 영역 내 Aircraft의 ECEF 좌표, 위도/경도/고도, 속도 생성 -------------
        # Aircraft의 ECEF 좌표
        self.xyz = np.array([LEOSystem.latlonalt2ecef(lat, lon, alt)])

        z = np.array([0.0, 0.0, 1.0]) # Earth rotation axis (ECEF)
        r = self.xyz[0] # r: aircraft ECEF position (3,)
        east = np.cross(z, r) # East
        east = east / np.linalg.norm(east)
        # Aircraft의 위도/경도/고도
        self.latlonalt = np.column_stack((lat, lon, alt))
        # Aircraft의 속도
        self.vel = np.array([vel_abs * east])



