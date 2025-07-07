import os
import cv2
import numpy as np
import mediapipe as mp

# Map body part names to mp landmark numbers
landmark_map = {
    "left shoulder": 11,
    "right shoulder": 12,
    "left elbow": 13,
    "right elbow": 14,
    "left wrist": 15,
    "right wrist": 16,
    "left hip": 23,
    "right hip": 24,
    "left knee": 25,
    "right knee": 26,
    "left ankle": 27,
    "right ankle": 28,
}

# Get depth/confidence folder/files by sorting the file numbers
folder = input("Folder name: ")
depth_folder = os.path.join(folder, "depth")
depth_files = sorted(os.listdir(depth_folder))
conf_folder = os.path.join(folder, "confidence")
conf_files = sorted(os.listdir(conf_folder))

# Initialize MediaPipe pose class
mp_pose = mp.solutions.pose

# Load video
video_path = os.path.join(folder, "rgb.mp4")

# Video dimesions
width = 192
height = 256

#scale intrinsics
csvmatrix = np.loadtxt(f'{folder}/camera_matrix.csv', delimiter=',')
scale_x = height / 1440
scale_y = width / 1920
matrixscaled = csvmatrix.copy()
matrixscaled[0, 0] *= scale_x
matrixscaled[1, 1] *= scale_y
matrixscaled[0, 2] *= scale_x
matrixscaled[1, 2] *= scale_y
fx, fy = matrixscaled[0, 0], matrixscaled[1, 1]
cx, cy = matrixscaled[0, 2], matrixscaled[1, 2]

# Insert x, y, z locations of body_part into pos_array
def get_landmark_arr(body_part, pos_array, part_name):
    cap = cv2.VideoCapture(video_path)
    # Set up Pose estimator
    with mp_pose.Pose(static_image_mode=False,
                    model_complexity=2,
                    enable_segmentation=False,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:
        prev = None
        frame_i = 0
        while cap.isOpened():
            # Read frame
            ret, frame = cap.read()
            # Break if not able to be read
            if not ret:
                break

            # Properly format frame
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame = cv2.resize(frame, (width,height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame.flags.writeable = True

            # Perform pose detection
            results = pose.process(frame)

            # If able to get landmarks from frame
            if results.pose_landmarks:
                # get elbow
                landmark = results.pose_landmarks.landmark[body_part]
                landmark_x = int(landmark.x * width)
                landmark_y = int(landmark.y * height)
                pos = (landmark_x, landmark_y)
                prev = pos
            # Otherwise use the same landmark as previous frame
            else:
                pos = prev

            # Only proceed if pos is valid
            if pos:
                # Get depth data from the frame
                depth_path = os.path.join(depth_folder, depth_files[frame_i])
                depth_mm = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
                depth_mm = cv2.rotate(depth_mm, cv2.ROTATE_90_CLOCKWISE)
                # Check that depth data was read properly
                if depth_mm is None:
                    print(f"Could not load depth image {depth_path}")
                    z = None
                else:
                    # Convert depth to meters
                    depth_meters = depth_mm / 1000.0
                    # Re-extract x and y pixel coords from pos
                    pointx, pointy = pos
                    # Clamp coordinates within image bounds
                    pointx = np.clip(pointx, 0, depth_meters.shape[1] - 1)
                    pointy = np.clip(pointy, 0, depth_meters.shape[0] - 1)
                    # Get z value at landmark pixel location
                    if frame_i == 0 or cv2.rotate(cv2.imread(os.path.join(conf_folder, conf_files[frame_i]), cv2.IMREAD_UNCHANGED), cv2.ROTATE_90_CLOCKWISE)[pointy, pointx] > 0:
                        z = depth_meters[pointy, pointx]
                    else:
                        if frame_i == 0:
                            print("Error, unconfident first frame")
                            continue
                        z = pos_array[frame_i - 1][2]
                    print(f"Depth at {part_name} (frame {frame_i}) at {pointx},{pointy}: {z}")
            else:
                print(f"No valid position for frame {frame_i}")
            x = (pointx - cx) * z / fx
            y = (pointy - cy) * z / fy    
            pos_array.append((x, y, z))
            # Increment frame index
            frame_i += 1

input1 = input("left knee, right knee, left elbow, or right elbow: ")
input2 = input("left hip, right hip, left shoulder, or right shoulder: ")
input3 = input("left ankle, right ankle, left wrist, or right wrist: ")

landmark1 = landmark_map[input1]
l1_arr = []
landmark2 = landmark_map[input2]
l2_arr = []
landmark3 = landmark_map[input3]
l3_arr = []

get_landmark_arr(landmark1, l1_arr, input1)
get_landmark_arr(landmark2, l2_arr, input2)
get_landmark_arr(landmark3, l3_arr, input3)
