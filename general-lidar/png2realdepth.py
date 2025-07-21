import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

folder = input("Folder name: ")
output_filename = input("Output file name: ")

csvmatrix = np.loadtxt(f'../{folder}/camera_matrix.csv', delimiter=',')

numframes = len(os.listdir(f"../{folder}/depth"))

print(f"Number of frames: {numframes}")
frame = input("Pick a frame (6 digits): ")

depth_mm = cv2.imread(f"../{folder}/depth/{frame}.png", cv2.IMREAD_UNCHANGED)

depth_meters = depth_mm / 1000.0

x = int(input("x coordinate: "))
y = int(input("y coordinate: "))

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

real_depth = np.sqrt(X**2 + Y**2 + Z**2)

real_depth = np.rot90(real_depth, k=3)

print(f"Depth value at {x}, {y}: {real_depth[y, x]:.3f}")

plt.imshow(real_depth, cmap='plasma')
plt.colorbar(label='Depth (m)')
plt.title('LiDAR Depth Map')
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.show()