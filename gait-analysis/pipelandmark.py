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

# LiDAR video dimensions
width, height = 192, 256

def extract_landmarks(folder, input1, input2, input3):
    # Paths
    video_path = os.path.join(folder, "rgb.mp4")
    depth_folder = os.path.join(folder, "depth")
    conf_folder = os.path.join(folder, "confidence")
    depth_files = sorted(os.listdir(depth_folder))
    conf_files = sorted(os.listdir(conf_folder))

    # Load and scale intrinsics
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

    # Landmark indices
    idx1, idx2, idx3 = landmark_map[input1], landmark_map[input2], landmark_map[input3]

    # Output arrays
    l1_arr, l2_arr, l3_arr = [], [], []

    # Pose estimation setup
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(video_path)
    with mp_pose.Pose(static_image_mode=False, model_complexity=2,
                      enable_segmentation=False,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        frame_i = 0
        prev = {idx1: None, idx2: None, idx3: None}

        # Read frames
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Orient frame and change to RGB for mediapipe
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            frame = cv2.resize(frame, (width, height))
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = pose.process(rgb_frame)

            if frame_i == 0:
                print("Loading...")

            # Load depth/confidence once per frame
            depth_mm = cv2.imread(os.path.join(depth_folder, depth_files[frame_i]), cv2.IMREAD_UNCHANGED)
            conf = cv2.imread(os.path.join(conf_folder, conf_files[frame_i]), cv2.IMREAD_UNCHANGED)
            if depth_mm is None or conf is None:
                print(f"Missing depth/confidence at frame {frame_i}")
                break

            # Orient/convert depth and confidence data
            depth_mm = cv2.rotate(depth_mm, cv2.ROTATE_90_CLOCKWISE)
            conf = cv2.rotate(conf, cv2.ROTATE_90_CLOCKWISE)
            depth_meters = depth_mm / 1000.0

            # Takes in a landmark index and array label and returns the 3d coordinate of the point if it is confident enough, otherwise defaulting back to that of the previous frame
            def extract_one(idx, label):
                if results.pose_landmarks:
                    lm = results.pose_landmarks.landmark[idx]
                    pos = (int(lm.x * width), int(lm.y * height))
                    prev[idx] = pos
                else:
                    pos = prev[idx]

                if pos:
                    pointx = np.clip(pos[0], 0, width - 1)
                    pointy = np.clip(pos[1], 0, height - 1)
                    if frame_i == 0 or conf[pointy, pointx] > 0:
                        z = depth_meters[pointy, pointx]
                    else:
                        # Fallback to previous z
                        z = {'l1': l1_arr, 'l2': l2_arr, 'l3': l3_arr}[label][frame_i - 1][2]
                    x = (pointx - cx) * z / fx
                    y = (pointy - cy) * z / fy
                    return (x, y, z)
                else:
                    print(f"No position for {label} at frame {frame_i}")
                    return (0, 0, 0)

            # Add the 3d coordinates to the arrays
            l1_arr.append(extract_one(idx1, 'l1'))
            l2_arr.append(extract_one(idx2, 'l2'))
            l3_arr.append(extract_one(idx3, 'l3'))

            frame_i += 1

    # Save to cache
    save_dir = os.path.join(folder, input1)
    os.makedirs(save_dir, exist_ok=True)
    np.savez(os.path.join(save_dir, "landmark_cache.npz"),
             l1=l1_arr, l2=l2_arr, l3=l3_arr,
             input1=input1, input2=input2, input3=input3)

    return l1_arr, l2_arr, l3_arr, input1, input2, input3

if __name__ == '__main__':
    folder = input("Folder name: ")
    input1 = input("left knee, right knee, left elbow, or right elbow: ")
    input2 = input("left hip, right hip, left shoulder, or right shoulder: ")
    input3 = input("left ankle, right ankle, left wrist, or right wrist: ")
    extract_landmarks(folder, input1, input2, input3)
