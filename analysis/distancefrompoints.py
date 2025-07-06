import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Select input video folder
folder = input("Folder name: ")
output_filename = input("Output file name: ")

#Load camera intrinsics
csvmatrix = np.loadtxt(f'{folder}/camera_matrix.csv', delimiter=',')

#Display total frame count
numframes = len(os.listdir(f"{folder}/depth"))
print(f"Number of frames: {numframes}")

#Select a frame
frame = input("Pick a frame (6 digits): ")

#Read depth values and properly rotate (video is initally saved 90 degrees counterclockwise) 
depth_mm = cv2.imread(f"{folder}/depth/{frame}.png", cv2.IMREAD_UNCHANGED)
depth_meters = depth_mm / 1000.0
depth_meters = np.rot90(depth_meters, k=3)

#Get first point (this is what the distances on the depth map will be calculated from)
x1 = int(input("x coordinate 1: "))
y1 = int(input("y coordinate 1: "))

#Get second point with which the distance to the first point will be printed
x2 = int(input("x coordinate 2: "))
y2 = int(input("y coordinate 2: "))

#Get dimensions of image
height, width = depth_meters.shape
u, v = np.meshgrid(np.arange(width), np.arange(height))

#Create 1D arrays
u_flat = u.flatten()
v_flat = v.flatten()
z_flat = depth_meters.flatten()

#Set rgb image scale
scale_x = height / 1920
scale_y = width / 1440

#Scale intrinsics
matrixscaled = csvmatrix.copy()
matrixscaled[0, 0] *= scale_x
matrixscaled[1, 1] *= scale_y
matrixscaled[0, 2] *= scale_x
matrixscaled[1, 2] *= scale_y

#Focal lengths
fx, fy = matrixscaled[0, 0], matrixscaled[1, 1]
#Camera center
cx, cy = matrixscaled[0, 2], matrixscaled[1, 2]

#Get x and y coordinates
x_flat = (u_flat - cx) * z_flat / fx
y_flat = (v_flat - cy) * z_flat / fy

#Reshape into 2D arrays
#First point
X1 = x_flat.reshape(height, width)[y1][x1]
Y1 = y_flat.reshape(height, width)[y1][x1]
Z1 = depth_meters[y1][x1]

#All points (np arrays)
X2 = x_flat.reshape(height, width)
Y2 = y_flat.reshape(height, width)
Z2 = depth_meters

#Distance between point 1 and all other points (np array)
distance = np.sqrt((X1-X2)**2 + (Y1-Y2)**2 + (Z1-Z2)**2)

#Print distance between two input points
print(distance[y2,x2])

#Plot distance map from point 1
plt.imshow(distance, cmap='plasma')
plt.colorbar(label='Distance (m)')
plt.title('LiDAR Distance Map')
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
plt.show()