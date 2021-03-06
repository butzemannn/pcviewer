#!/bin/env python3
import argparse

from src.pointcloud import PointCloud
from src.viewer import Viewer
from src.data.kittigtset import KittiGTSet

def init_args():
    parser = argparse.ArgumentParser(description='A generic point cloud viewer.')
    parser.add_argument('pcloud_location', type=str, help='The point cloud [folder] location')
    parser.add_argument('--format', type=str, choices=['bin'], help='File format in which the point clouds are provided in')
    parser.add_argument('--gt', type=str, help='Point cloud ground truth [folder] location. Currently only KITTI ground truth format is supported')
    parser.add_argument('--pred', type=str, help='Ground truth location. Must be in correct format')
    args = parser.parse_args()
    return args


def main() -> None:
    args = init_args()
    gts, predictions = None, None
    view_gts, view_preds = False, False

    if args.gt:
        # ground truths should be viewed
        gts = KittiGTSet()
        gts.load(args.gt)
        view_gts = True

    if args.pred:
        # predictions are viewed
        predictions = KittiGTSet()
        gts.load(args.pred)
        view_preds = True


    # TOOD: change format to formats.BINARY
    pointcloud = PointCloud(args.pcloud_location, args.format, groundtruthset=gts, predictionset=predictions)
    #pointcloud.transform_coordinate_system([2,0,1], factors=[1,-1,-1])
    #pointcloud.limit_range([-5, -200, -10], [200, 200, 10])
    #pointcloud.convert_to_velodyne_coordinates()

    viewer = Viewer(pointcloud)
    viewer.view_pointcloud(view_ground_truths=view_gts, view_predictions=view_preds)



if __name__ == "__main__":
    main()
