from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Circumvent circular import issues
    from src.data.box3d import Box3D


def box3d_camera_to_velodyne_coords(box3d: Box3D):
    xc, yc, zc = box3d.get_center()
    xv = zc
    yv = -xc
    zv = -yc
    box3d.set_center([xv,yv,zv])
