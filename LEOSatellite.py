import numpy as np
from shapely.geometry import Point
from LEOBase import LEOBase
from LEOSystem import LEOSystem

class LEOSatellite(LEOBase):

    def __init__(self, grid_id: int, time: int = 1):

        super().__init__(grid_id)
        self.xyz_all     , self.alt_all = self.__sat_positions_all_shells(time)
        self.vel_all     , _ = self.__sat_velocity_all_shells()

        latlon_all = LEOSystem.ecef2latlon(self.xyz_all)  # (N, 2)
        lat = latlon_all[:, 0]
        lon = latlon_all[:, 1]

        self.mask = np.array([
            self.GRID_AREA.covers(Point(lo, la))
            for la, lo in zip(lat, lon)
        ], dtype=bool)
        self.xyz = self.xyz_all[self.mask]          # (NSAT, 3)
        self.latlonalt = np.column_stack(
            (latlon_all[self.mask], self.alt_all[self.mask])
        ) 
        
        self.vel = self.vel_all[self.mask]          # (NSAT, 3)
    # ------------ Single shell ECEF positions -------------
    def __sat_positions_single_shell(self, h_km: int, inc: float, num_plane: int, num_sat: int, time: int) -> np.ndarray:

        R_E = 6371
        G = 6.67430e-11
        M_E = 5.9722e24
        MU_E = G * M_E / 1e9

        R_orbit = R_E + h_km
        v = np.sqrt(MU_E / R_orbit)
        w = v / R_orbit

        phi = np.radians(inc)
        theta = 2 * np.pi / num_plane

        angle_offset = (2 * np.pi / num_sat) * np.arange(num_sat)
        angle = w * time + angle_offset

        x = R_orbit * np.cos(angle)
        y = R_orbit * np.cos(phi) * np.sin(angle)
        z = R_orbit * np.sin(phi) * np.sin(angle)
        sat_xyz = np.array([x, y, z])

        C = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0, 0, 1]
        ])

        theta_earth = 2 * np.pi / (24 * 3600)
        C_EARTH = np.array([
            [np.cos(theta_earth * time), -np.sin(theta_earth * time), 0],
            [np.sin(theta_earth * time),  np.cos(theta_earth * time), 0],
            [0, 0, 1]
        ])

        constell = []
        for _ in range(num_plane):
            sat_xyz = C_EARTH @ C @ sat_xyz
            constell.append(sat_xyz)

        return np.hstack(constell).T

    # ------------ All shells ECEF positions -------------
    def __sat_positions_all_shells(self, time: int = 1) -> np.ndarray:
        
        all_xyz = []
        all_alt = []
        
        self.shells = [
            (340, 53, 48, 110),
            (345, 46, 48, 110),
            (350, 38, 48, 110),
            (360, 96.9, 30, 120),
            (525, 53, 28, 120),
            (530, 43, 28, 120),
            (535, 33, 28, 120),
            (604, 148, 12, 12),
            (614, 115.7, 18, 18),
            (540, 53.2, 72, 22),
            (550, 53,   72, 22),
            (560, 97.6, 6,  58),
            (560, 97.6, 4,  43),
            (570, 70,   36, 20)
        ]

        for h, inc, num_plane, num_sat in self.shells:
            sats = self.__sat_positions_single_shell(
                h, inc, num_plane, num_sat, time
            )                       # (Nshell, 3)

            all_xyz.append(sats)
            all_alt.append(
                np.full(len(sats), h)   # 이 shell의 모든 위성 고도 = h
            )

        return np.vstack(all_xyz), np.concatenate(all_alt)
    
    ########################### SAT velocity ###########################
    # ------------ Single shell ECEF velocity -------------
    def __sat_velocity_single_shell(self, h_km: int, inc: float, num_plane: int, num_sat: int, time: int) -> np.ndarray:

        R_E = 6371
        G = 6.67430e-11
        M_E = 5.9722e24
        MU_E = G * M_E / 1e9

        R_orbit = R_E + h_km
        v = np.sqrt(MU_E / R_orbit)
        w = v / R_orbit

        phi = np.radians(inc)
        theta = 2 * np.pi / num_plane

        angle_offset = (2 * np.pi / num_sat) * np.arange(num_sat)
        angle = w * time + angle_offset

        # time에 대해 미분
        vx = -R_orbit * w * np.sin(angle)
        vy = R_orbit * w * np.cos(phi) * np.cos(angle)
        vz = R_orbit * w * np.sin(phi) * np.cos(angle)

        sat_xyz_vel = np.array([vx, vy, vz])

        C = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0, 0, 1]
        ])

        theta_earth = 2 * np.pi / (24 * 3600)
        C_EARTH = np.array([
            [np.cos(theta_earth * time), -np.sin(theta_earth * time), 0],
            [np.sin(theta_earth * time),  np.cos(theta_earth * time), 0],
            [0, 0, 1]
        ])

        constell_vel = []
        for _ in range(num_plane):
            sat_xyz_vel = C_EARTH @ C @ sat_xyz_vel
            constell_vel.append(sat_xyz_vel)

        return np.hstack(constell_vel).T
    
    # ------------ All shells ECEF velocity -------------
    def __sat_velocity_all_shells(self, time: int = 1) -> np.ndarray:
        
        all_xyz = []
        all_alt = []
        
        self.shells = [
            (340, 53, 48, 110),
            (345, 46, 48, 110),
            (350, 38, 48, 110),
            (360, 96.9, 30, 120),
            (525, 53, 28, 120),
            (530, 43, 28, 120),
            (535, 33, 28, 120),
            (604, 148, 12, 12),
            (614, 115.7, 18, 18),
            (540, 53.2, 72, 22), # gen1
            (550, 53,   72, 22), # gen1
            (560, 97.6, 6,  58), # gen1
            (560, 97.6, 4,  43), # gen1
            (570, 70,   36, 20) # gen1 -> 4,408개 SATs
        ]

        for h, inc, num_plane, num_sat in self.shells:
            sats = self.__sat_velocity_single_shell(
                h, inc, num_plane, num_sat, time
            )                       # (Nshell, 3)

            all_xyz.append(sats)
            all_alt.append(
                np.full(len(sats), h)   # 이 shell의 모든 위성 고도 = h
            )

        return np.vstack(all_xyz), np.concatenate(all_alt)

    ########################### SAT velocity ###########################
    # ------------ Single shell ECEF velocity -------------
    def __sat_velocity_single_shell(self, h_km: int, inc: float, num_plane: int, num_sat: int, time: int) -> np.ndarray:

        R_E = 6371
        G = 6.67430e-11
        M_E = 5.9722e24
        MU_E = G * M_E / 1e9

        R_orbit = R_E + h_km
        v = np.sqrt(MU_E / R_orbit)
        w = v / R_orbit

        phi = np.radians(inc)
        theta = 2 * np.pi / num_plane

        angle_offset = (2 * np.pi / num_sat) * np.arange(num_sat)
        angle = w * time + angle_offset

        # time에 대해 미분
        vx = -R_orbit * w * np.sin(angle)
        vy = R_orbit * w * np.cos(phi) * np.cos(angle)
        vz = R_orbit * w * np.sin(phi) * np.cos(angle)

        sat_xyz_vel = np.array([vx, vy, vz])


        C = np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta),  np.cos(theta), 0],
            [0, 0, 1]
        ])

        theta_earth = 2 * np.pi / (24 * 3600)
        C_EARTH = np.array([
            [np.cos(theta_earth * time), -np.sin(theta_earth * time), 0],
            [np.sin(theta_earth * time),  np.cos(theta_earth * time), 0],
            [0, 0, 1]
        ])

        constell_vel = []
        for _ in range(num_plane):
            sat_xyz_vel = C_EARTH @ C @ sat_xyz_vel
            constell_vel.append(sat_xyz_vel)

        return np.hstack(constell_vel).T
    
    # ------------ All shells ECEF velocity -------------
    def __sat_velocity_all_shells(self, time: int = 1) -> np.ndarray:
        
        all_xyz = []
        all_alt = []
        
        self.shells = [
            (340, 53, 48, 110),
            (345, 46, 48, 110),
            (350, 38, 48, 110),
            (360, 96.9, 30, 120),
            (525, 53, 28, 120),
            (530, 43, 28, 120),
            (535, 33, 28, 120),
            (604, 148, 12, 12),
            (614, 115.7, 18, 18),
            (540, 53.2, 72, 22), # gen1
            (550, 53,   72, 22), # gen1
            (560, 97.6, 6,  58), # gen1
            (560, 97.6, 4,  43), # gen1
            (570, 70,   36, 20) # gen1 -> 4,408개 SATs
        ]

        for h, inc, num_plane, num_sat in self.shells:
            sats = self.__sat_velocity_single_shell(
                h, inc, num_plane, num_sat, time
            )                       # (Nshell, 3)

            all_xyz.append(sats)
            all_alt.append(
                np.full(len(sats), h)   # 이 shell의 모든 위성 고도 = h
            )

        return np.vstack(all_xyz), np.concatenate(all_alt)