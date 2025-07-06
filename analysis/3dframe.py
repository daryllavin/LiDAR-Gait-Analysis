import os
import cv2
import numpy as np
import open3d as o3d

folder = input("Folder name: ")
output = input("Output file name: ")

csvmatrix = np.loadtxt(f'{folder}/camera_matrix.csv', delimiter=',')

numframes = len(os.listdir(f"{folder}/depth"))

print(f"Number of frames: {numframes}")
frame = input("Pick a frame (6 digits): ")

depth_mm = cv2.imread(f"{folder}/depth/{frame}.png", cv2.IMREAD_UNCHANGED)

depth_meters = depth_mm / 1000.0

height, width = depth_meters.shape

u, v = np.meshgrid(np.arange(width), np.arange(height))

u_flat = u.flatten()
v_flat = v.flatten()
z_flat = depth_meters.flatten()

scale_x = height / 1440
scale_y = width / 1920

matrixscaled = csvmatrix.copy()
matrixscaled[0, 0] *= scale_x
matrixscaled[1, 1] *= scale_y
matrixscaled[0, 2] *= scale_x
matrixscaled[1, 2] *= scale_y

fx, fy = matrixscaled[0, 0], matrixscaled[1, 1]
cx, cy = matrixscaled[0, 2], matrixscaled[1, 2]

x_flat = (u_flat - cx) * z_flat / fx
y_flat = (v_flat - cy) * z_flat / fy

X = x_flat.reshape(height, width)
Y = y_flat.reshape(height, width)
Z = depth_meters

points = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

o3d.visualization.draw_geometries([pcd])
o3d.io.write_point_cloud(output, pcd)