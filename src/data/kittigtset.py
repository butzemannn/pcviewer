import open3d as o3d
from typing import List

from src.data.groundtruthset import GroundTruthSet
from src.data.box3d import Box3D


class KittiGTSet(GroundTruthSet):

    ground_truths: List[Box3D] = []

    def add_Box3D(self, center, size, angle):
        box3d = Box3D(center, size, angle, to_velodyne=True)
        self.ground_truths.append(box3d)

    def load(self, gt_location: str, categories: list = ['Car']):
        """Load the kitti label files from folder given on class init"""

        label = []
        with open(gt_location, 'r') as f:
            for line in f:
                ln = line[:-1].split(" ")
                # unpack label file given in cam coordinates
                category, trun, occ, alpha, bbox, size, center, angle = \
                    ln[0], ln[1], ln[2], ln[3], ln[4:8], ln[8:11], ln[11:14], ln[14]

                if category in categories:
                    center = [float(x) for x in center]
                    size = [float(x) for x in size]
                    self.add_Box3D(center, size, float(angle))

    def convert_to_line_set(self) -> List[o3d.geometry.LineSet]:
        if not self.ground_truths:
            return [] 

        line_set_list = []
        for box3d in self.ground_truths:
            line_set_list.append(box3d.convert_to_line_set())

        return line_set_list
