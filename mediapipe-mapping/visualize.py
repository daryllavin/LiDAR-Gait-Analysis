import os
import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe pose class and drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Load video
video_path = 'lowframes/rgb.mp4'
cap = cv2.VideoCapture(video_path)

width = 192
height = 256

# Set up Pose estimator
with mp_pose.Pose(static_image_mode=False,
                  model_complexity=2,
                  enable_segmentation=False,
                  min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    prev = None
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.resize(frame, (192,256))
        # Convert the BGR image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Perform pose detection
        results = pose.process(image)

        # Draw the pose annotation on the image
        image.flags.writeable = True
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()