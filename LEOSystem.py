import numpy as np

GRID_ID = 10 # Fixed index for testing – do NOT modify

class LEOSystem:

    # ------------ ECEF 좌표를 위도/경도로 변환 (빈칸1) -------------
    @staticmethod
    def ecef2latlon(xyz: np.ndarray) -> np.ndarray:

        x, y, z = xyz[:,0], xyz[:,1], xyz[:,2]
        r = np.linalg.norm(xyz, axis=1)
        lat = np.degrees(np.arcsin(z/r))
        lon = np.degrees(np.arctan2(y, x))
        latlon = np.column_stack((lat, lon))

        return latlon
    
    # ------------ 위도/경도 기준으로 ENU 좌표계 반환 (빈칸2) -------------
    @staticmethod
    def latlon2enu(lat_deg: float, lon_deg: float) -> tuple:

        lat = np.deg2rad(lat_deg)
        lon = np.deg2rad(lon_deg)

        e = np.array([-np.sin(lon), 
                      np.cos(lon), 
                      0])
        n = np.array([-np.cos(lon)*np.sin(lat),
                      -np.sin(lon)*np.sin(lat),
                       np.cos(lat)])
        u = np.array([ np.cos(lon)*np.cos(lat),
                       np.sin(lon)*np.cos(lat),
                       np.sin(lat)])

        return e, n, u

    # ------------ 위도/경도/고도 기준으로 ECEF 좌표계 반환 (빈칸3) -------------
    @staticmethod
    def latlonalt2ecef(lat: float, lon: float, alt: float) -> np.ndarray:

        lat, lon = np.radians(lat), np.radians(lon)

        R_E = 6371  # Earth radius [km]
        R = R_E + alt # [km]

        return np.array([
                R * np.cos(lat) * np.cos(lon),
                R * np.cos(lat) * np.sin(lon),
                R * np.sin(lat)
        ])
    
    # ------------ ENU 좌표계 기반 elevation/azimuth angle 계산 (빈칸4) -------------
    def cal_angle(r_ref: np.ndarray, r_target: np.ndarray, ref_latlon: int, ref_idx: int) -> float:
        
        e, n, u = LEOSystem.latlon2enu(ref_latlon[ref_idx][0], ref_latlon[ref_idx][1])
        p = r_ref - r_target

        enu_position = np.array([
        np.dot(p, e),
        np.dot(p, n),
        np.dot(p, u)
        ])

        elevation = np.arctan2(enu_position[2], np.sqrt(enu_position[0]**2 + enu_position[1]**2))
        azimuth = np.arctan2(enu_position[0], enu_position[1])

        return float(np.rad2deg(elevation)), float((np.rad2deg(azimuth) + 360) % 360) # [deg]
    
    # ------------ Doppler shift 계산 (SAT -> UE) (빈칸5) -------------  # 20 GHz : DL Ka-band setting
    @staticmethod
    def cal_doppler(pos_sat: np.ndarray, pos_ue: np.ndarray, vel_sat: np.ndarray, vel_cell: np.ndarray) -> np.ndarray:
        
        c = 3e8 # [m/s]
        fc_Hz = 20e9 # [Hz] : DL Ka-band
        lam_km = c / fc_Hz / 1e3 # 0.000015 [km] 

        NSAT = len(pos_sat)
        NUE  = len(pos_ue)

        doppler = np.zeros((NSAT, NUE))

        for sat_idx in range(NSAT):
            for ue_idx in range(NUE):
                # vel_cell 사용해서 도플러 계산하는 함수 업데이트 해줘!
                r_sat = pos_sat[sat_idx]
                r_ue  = pos_ue[ue_idx]
                v_sat = vel_sat[sat_idx]
                los = r_ue - r_sat
                los_hat = los / np.linalg.norm(los)
                v_rad = np.dot(v_sat, los_hat)
                doppler[sat_idx, ue_idx] = (v_rad / lam_km) / 1e3

        return doppler   # (NSAT, NUE)
    
    # ------------ ECEF 좌표계 기준 distance 계산 -------------   
    @staticmethod
    def cal_distance(pos_sat: np.ndarray, pos_cell: np.ndarray) -> np.ndarray:
        
        NSAT = len(pos_sat)
        NCell = len(pos_cell)
        dis_matrix = np.zeros((NSAT, NCell))

        for sat_idx in range(len(pos_sat)):
            for ue_idx in range(len(pos_cell)):
                dis = np.linalg.norm(pos_sat[sat_idx]- pos_cell[ue_idx])
                dis_matrix[sat_idx][ue_idx] = dis

        return dis_matrix # [km]