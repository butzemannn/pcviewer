import argparse

from src.pointcloud import PointCloud
from src.viewer import Viewer

def init_args():
    parser = argparse.ArgumentParser(description='A generic point cloud viewer.')
    parser.add_argument('pcloud_location', type=str, help='The point cloud [folder] location')
    parser.add_argument('--format', type=str, choices=['bin'], help='File format in which the point clouds are provided in')
    args = parser.parse_args()
    return args


def main() -> None:
    args = init_args()
    # TOOD: change format to formats.BINARY
    pointcloud = PointCloud(args.pcloud_location, args.format)
    pointcloud.transform_coordinate_system([2,0,1])
    #pointcloud.limit_range([-5, -100, -10], [100, 100, 10])

    viewer = Viewer(pointcloud)
    viewer.view_pointcloud()



if __name__ == "__main__":
    main()
