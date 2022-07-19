import numpy as np
import open3d as o3d
import math

from src.utils.boxutils import box3d_camera_to_velodyne_coords

class Box3D:

    x: float
    y: float
    z: float
    h: float
    w: float
    l: float
    theta: float

    def __init__(self, center: list, size: list, angle: np.float32, to_velodyne: bool = False):
        """
        :param center: A list containing the box center (x,y,z)
        :param size: A list containing the box size (h,w,l)
        :param angle: Represents the angle arround the z axis in velodyne coordinates
        """
        if not len(center) == 3:
            raise ValueError("center list must be of size 3 (x,y,z)")

        if not len(size) == 3:
            raise ValueError("size list must be of size 3 (h,w,l)")

        self.set_center(center)
        self.set_size(size)
        self.theta = angle
        if to_velodyne:
            box3d_camera_to_velodyne_coords(self)


    def __str__(self):
        return f"Box3D[{self.x},{self.y},{self.z},{self.h},{self.w},{self.l},{self.theta}]"

    def get_center(self):
        return [self.x, self.y, self.z]

    def set_center(self, center: list):
        self.x, self.y, self.z = center

    def set_size(self, size: list):
        self.h, self.w, self.l = size

    def convert_to_line_set(self, color: list = (255, 0, 0)) -> o3d.geometry.LineSet:
        """
        :param box: Array(1,7) with x,y,z,h,w,l,theta
        :param colors: list [3] with the rgb values between 0 and 1
        :return: LineSet as bounding box
        """
        
        #dh = 0.5 * self.h
        dw = 0.5 * self.w
        dl = 0.5 * self.l

        p0 = [self.x - dl, self.y + dw, self.z]
        p1 = [self.x - dl, self.y - dw, self.z]
        p2 = [self.x + dl, self.y - dw, self.z]
        p3 = [self.x + dl, self.y + dw, self.z]
        p4 = [self.x - dl, self.y + dw, self.z + self.h]
        p5 = [self.x - dl, self.y - dw, self.z + self.h]
        p6 = [self.x + dl, self.y - dw, self.z + self.h]
        p7 = [self.x + dl, self.y + dw, self.z + self.h]

        points = [p0, p1, p2, p3, p4, p5, p6, p7]
        points = self.rotate_points_around_z(points, [self.x, self.y, self.z], self.theta)
        # indices which corners have a connection with each other
        lines = [[0, 1], [0, 3], [2, 1], [2, 3], [4, 7], [4, 5], [6, 5], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

        colors = [color for i in range(len(lines))]

        line_set = o3d.geometry.LineSet()
        line_set.points = o3d.utility.Vector3dVector(points)
        line_set.lines =  o3d.utility.Vector2iVector(lines)
        line_set.colors = o3d.utility.Vector3dVector(colors)

        return line_set

    def rotate_points_around_z(self, points: list, center: list, theta: float):
        """
        Rotates corner points by an angle theta around the z axes.
        The formulas are: Rv = (xcos(theta) - ysin(theta))e_x + (xsin(theta) + ycos(theta))e_y

        :param points: a list containing all points in format [[x1,y1,z1], [x2,y2,z2], ...]
        :param center: a list containing the center of the bbox [x,y,z]
        :param theta: angle by which to rotate. Given in rad.

        :returns: list containing the newly rotated points in format [[xn1,yn1,z1], [xn2,yn2,z2], ...]
        """
        # move box to center of coord-system, rotate, move back to orig pos
        xc, yc, zc = center
        for i, point in enumerate(points):
            xp, yp, zp = point
            # move to coord sys origin
            xp = xp - xc
            yp = yp - yc

            x_new = yp * math.cos(theta) + xp * math.sin(theta)
            y_new = -yp * math.sin(theta) + xp * math.cos(theta)

            # move back to original pos
            x_new = x_new + xc
            y_new = y_new + yc

            point = [x_new, y_new, zp]
            points[i] = point

        return points
