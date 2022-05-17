from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Circumvent circular import issues
    from src.pointcloud import PointCloud


def convert_camera_to_velodyne_coordinates(pointcloud: PointCloud) -> PointCloud:
    x_c, y_c, z_c = np.moveaxis(pointcloud.points, 1, 0)

    x_v = z_c
    y_v = -x_c
    z_v = -y_c
    pointcloud.points = np.stack((x_v, y_v, z_v), axis=1)
    return pointcloud

def rearrange_coordinates(pointcloud: PointCloud, axes: list) -> PointCloud:
    i_x, i_y, i_z = axes
    x_new = pointcloud.points[:, i_x]
    y_new = pointcloud.points[:, i_y]
    z_new = pointcloud.points[:, i_z]
    pointcloud.points = np.stack((x_new, y_new, z_new), axis=1)

    return pointcloud


