import open3d as o3d

from src.pointcloud import PointCloud


class Viewer:
    def __init__(self, pointcloud: PointCloud):
        self.pointcloud = pointcloud
    
    def view_pointcloud(self):
        # create pointcloud
        o3dpcloud = o3d.geometry.PointCloud()
        o3dpcloud.points = o3d.open3d.utility.Vector3dVector(self.pointcloud.points)

        # create coordinate frame. red: x, green: y, blue: z
        o3dframe = o3d.geometry.TriangleMesh.create_coordinate_frame()

        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(o3dpcloud)
        vis.add_geometry(o3dframe)

        vis.run()
