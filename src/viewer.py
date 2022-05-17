import open3d as o3d

from src.pointcloud import PointCloud


class Viewer:
    def __init__(self, pointcloud: PointCloud):
        self.pointcloud = pointcloud
    
    def view_pointcloud(self, ground_truths: bool = False):
        # Visualizer settings
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        geometries = []

        # create pointcloud
        o3dpcloud = o3d.geometry.PointCloud()
        o3dpcloud.points = o3d.open3d.utility.Vector3dVector(self.pointcloud.points)
        geometries.append(o3dpcloud)

        # create coordinate frame. red: x, green: y, blue: z
        o3dframe = o3d.geometry.TriangleMesh.create_coordinate_frame()
        geometries.append(o3dframe)
        
        if ground_truths:
            if not self.pointcloud.groundtruthset:
                raise ValueError("Ground truth option set but no ground truths available")
            groundtruths = self.pointcloud.groundtruthset.convert_to_line_set()
            geometries.extend(groundtruths)


        for geometry in geometries:
            vis.add_geometry(geometry)

        vis.run()
