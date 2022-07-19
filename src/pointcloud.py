import numpy as np
from deprecated import deprecated

from src.data.groundtruthset import GroundTruthSet
from src.utils.transformations import (
        convert_camera_to_velodyne_coordinates,
        rearrange_coordinates
        )


class PointCloud():

    groundtruthset: GroundTruthSet

    def __init__(self, pcloud_location: str, format: str, groundtruthset: GroundTruthSet = None, predictionset: GroundTruthSet = None):
        self.pcloud_location = pcloud_location
        self.format = format
        self.points = self._load_pcloud()
        self.groundtruthset = groundtruthset
        self.predictionset = predictionset
        #self.convert_coordinate_system()
    
    def _load_pcloud(self):
        if not self.format == 'bin':
            raise ValueError("Currently only 'bin' format supported")

        points = np.fromfile(self.pcloud_location, dtype=np.float32)
        points = points.reshape([-1, 4])

        return points[:,:3]

    @deprecated(reason='transform_coorinate_system() should be used')
    def convert_coordinate_system(self):
        convert_camera_to_velodyne_coordinates(self)

    def transform_coordinate_system(self, axes: list, factors: list = None):
        """
        :param axes: A list containing the new axis which will take the current index spot.
            E.g. [1, 2, 0] results in (y, z, x)
        :param factors: Optional factors with which the values are multiplied with. Also corresponds with the changed position.
            E.g. [-1, 1, 1] results in (-x, y, z)
        """
        if not len(axes) == 3:
            raise ValueError("axis parameter requires length 3.")
        
        if factors and not len(factors) == 3:
            raise ValueError("factors parameter requires length 3.")

        rearrange_coordinates(self, axes) 

        if factors:
            # bring factors to correct size so they can be multiplied with points
            npfactors = np.array(factors)
            npfactors = np.expand_dims(npfactors, axis=0)
            npfactors = np.broadcast_to(npfactors, (self.points.shape[0], npfactors.shape[1]))
            self.points = self.points * npfactors


    def limit_range(self, minimum: list, maximum: list) -> None:
        """
        :param minimum: Array for minimum point range, should have form [x_min, y_min, z_min]
        :param maximum: Array for maximum point range, should have form [x_max, y_max, z_max]
        """
        x_min, y_min, z_min = minimum
        x_max, y_max, z_max = maximum

        cond_x = np.logical_and(self.points[:,0] >= x_min, self.points[:,0] <= x_max)
        cond_y = np.logical_and(self.points[:,1] >= y_min, self.points[:,1] <= y_max)
        cond_z = np.logical_and(self.points[:,2] >= z_min, self.points[:,2] <= z_max)
        cond = np.logical_and(np.logical_and(cond_x, cond_y), cond_z)
            
        self.points = self.points[cond]
