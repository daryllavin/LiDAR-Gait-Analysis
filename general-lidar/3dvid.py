import os
import cv2
import numpy as np
import open3d as o3d

#retrieve files
folder = input("Folder name: ")
outfile = input("Output filename: ")
csvmatrix = np.loadtxt(f'../{folder}/camera_matrix.csv', delimiter=',')
depth_folder = os.path.join("..", folder, "depth")
depth_files = sorted(os.listdir(depth_folder))

#get shape and scale
sample_depth = cv2.imread(os.path.join(depth_folder, depth_files[0]), cv2.IMREAD_UNCHANGED)
height, width = sample_depth.shape
scale_x = height / 1440
scale_y = width / 1920

#scale intrinsics
matrixscaled = csvmatrix.copy()
matrixscaled[0, 0] *= scale_x
matrixscaled[1, 1] *= scale_y
matrixscaled[0, 2] *= scale_x
matrixscaled[1, 2] *= scale_y

fx, fy = matrixscaled[0, 0], matrixscaled[1, 1]
cx, cy = matrixscaled[0, 2], matrixscaled[1, 2]

#get video ready
frame_index = 0

def get_point_cloud(filename):
    depth_mm = cv2.imread(os.path.join(depth_folder, filename), cv2.IMREAD_UNCHANGED)
    depth_meters = depth_mm / 1000.0
    u, v = np.meshgrid(np.arange(width), np.arange(height))
    z = depth_meters.flatten()
    x = (u.flatten() - cx) * z / fx
    y = (v.flatten() - cy) * z / fy
    points = np.column_stack((x, y, z))
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd

#set up video window
vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window()
render_option = vis.get_render_option()
render_option.background_color = np.asarray([0, 0, 0])
render_option.point_size = 4
pcd = get_point_cloud(depth_files[0])
vis.add_geometry(pcd)

out = None
#move thru frames
def animation_callback(vis):
    global frame_index, pcd
    if frame_index >= len(depth_files):
        vis.close()
        return False
    pcd.points = get_point_cloud(depth_files[frame_index]).points
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

    img = vis.capture_screen_float_buffer(do_render=True)
    img = (255 * np.asarray(img)).astype(np.uint8)

    global out
    if out is None:
        height, width, _ = img.shape
        size = (width, height)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(outfile, fourcc, 60, size)

    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    out.write(img_bgr)

    frame_index += 1
    return False

#show
vis.register_animation_callback(animation_callback)
vis.run()
vis.destroy_window()

out.release()