import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import h3
from shapely.geometry import Point, Polygon
from LEOBase import LEOBase
from LEOSystem import LEOSystem
 
class LEOVisual:

    # ------------ Visualization -------------
    def draw_map(grid_id: int, grid_squares: dict, sats_xyz: np.ndarray):
        grid_area = grid_squares[grid_id]
        (grid_lon_min,grid_lat_min,
         grid_lon_max,grid_lat_max) = grid_area.bounds
        fig = plt.figure(figsize=(12, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.set_extent([
            grid_lon_min, grid_lon_max,
            grid_lat_min, grid_lat_max
        ])
        ax.add_feature(cfeature.LAND, facecolor='lightgray')
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.STATES)

        bbox = h3.LatLngPoly([
            (LEOBase.US_LAT_MIN, LEOBase.US_LON_MIN),
            (LEOBase.US_LAT_MIN, LEOBase.US_LON_MAX),
            (LEOBase.US_LAT_MAX, LEOBase.US_LON_MAX),
            (LEOBase.US_LAT_MAX, LEOBase.US_LON_MIN),
            (LEOBase.US_LAT_MIN, LEOBase.US_LON_MIN)
        ])

        Res4 = 4
        h3_cells = h3.polygon_to_cells(bbox, res=Res4)

        ax.add_geometries(
            [Polygon([(lon, lat) for lat, lon in h3.cell_to_boundary(h)])
             for h in h3_cells],
            crs=ccrs.PlateCarree(),
            edgecolor='black',
            facecolor='none',
            linewidth=0.3
        )

        # sats_xyz = sat.sat_positions_all_shells(1)[0]
        sat_latlon = LEOSystem.ecef2latlon(sats_xyz)   # (N, 2)

        mask = np.array([
            grid_area.covers(Point(lon, lat))
            for lat, lon in zip(sat_latlon[:, 0], sat_latlon[:, 1])
        ], dtype=bool)

        ax.scatter(
            sat_latlon[mask, 1],  # lon
            sat_latlon[mask, 0],  # lat
            s=12,
            color='black'
        )
        ax.add_geometries(
            [grid_area],
            crs=ccrs.PlateCarree(),
            edgecolor='green',
            facecolor='none',
            linewidth=2
        )
        ax.set_title(f"Grid {grid_id}", fontsize=16, weight='bold')
        plt.show()

    # ------------ CDF -------------
    @staticmethod
    def compute_cdf(data: np.ndarray):
        data_sorted = np.sort(data)
        cdf = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
        return data_sorted, cdf
    
    # ------------ Elevation & Azimuth CDF -------------
    @staticmethod
    def plot_angle_cdf(
        e1: np.ndarray, cdf_e1: np.ndarray,
        e2: np.ndarray, cdf_e2: np.ndarray,
        a1: np.ndarray, cdf_a1: np.ndarray,
        a2: np.ndarray, cdf_a2: np.ndarray
    ):

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Elevation CDF
        axes[0].plot(e1, cdf_e1, label="SAT → UE", linewidth=2)
        axes[0].plot(e2, cdf_e2, '--', label="UE → SAT", linewidth=2)
        axes[0].set_xlabel("Elevation angle [deg]")
        axes[0].set_ylabel("CDF")
        axes[0].set_title("Elevation Angle CDF")
        axes[0].grid(True)
        axes[0].legend()

        # Azimuth CDF
        axes[1].plot(a1, cdf_a1, label="SAT → UE", linewidth=2)
        axes[1].plot(a2, cdf_a2, '--', label="UE → SAT", linewidth=2)
        axes[1].set_xlabel("Azimuth angle [deg]")
        axes[1].set_ylabel("CDF")
        axes[1].set_title("Azimuth Angle CDF")
        axes[1].grid(True)
        axes[1].legend()

        plt.tight_layout()
        plt.show()

    # ------------ Doppler CDF -------------
    @staticmethod
    def plot_doppler_cdf(dop: np.ndarray, cdf_dop: np.ndarray):

        plt.figure(figsize=(6, 6))
        plt.plot(dop, cdf_dop, linewidth=2)
        plt.xlabel("Doppler shift [kHz]")
        plt.ylabel("CDF")
        plt.title("Doppler Shift CDF (All SAT → All UE)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
