# LiDAR Gait Analysis

Analyze human gait using RGB-D LiDAR video with 3D pose estimation and angle computation powered by MediaPipe and OpenCV. 

## Overview

This project aims to utilize iPad/iPhone LiDAR recording capabilities to analyze gait through 3d position tracking, specifically aimed to track and detect patterns in parkinsonian gait. The repository has two main folders, general-lidar and gait-analysis. 

The general-lidar folder contains 5 programs that are targeted towards more general LiDAR analysis applications, with functionalities such as creating depth maps of videos and/or individual frames, as well as 3d point cloud video/image recreations. You can read more about these programs in the General-LiDAR section below.

The gait-analysis folder contains 4 programs which are targeted towards position tracking and gait analysis. It utilizes the Mediapipe pose estimation model to map joint locations to the LiDAR data, which allows for data such as joint location over time and joint angles to be calculated and plotted. You can read more about the specific functionalities in the Gait-Analysis section below.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/daryllavin/LiDAR-Gait-Analysis.git
   cd LiDAR-Gait-Analysis
   ```
   
2. Create the environment:
   ```bash
   conda env create -f env.yaml
   conda activate lidar-gait-analysis
   ```

## Usage

To utilize the LiDAR capabilities of the iPhone/iPad, you must have a LiDAR-equipped device (including the iPhone 12+ Pro/Pro Max, or an iPad Pro). You should then download the Stray Scanner app from the app store which is used to record the LiDAR videos. When recording a Stray Scanner video for gait analysis, you should record in 60fps. The video data is saved to the files app in a folder which contains camera intrinsic data (camera_matrix.csv, imu.csv, odometry.csv), the original rgb video (rgb.mp4), and folders of depth and confidence frames (depth, confidence) which should contain a png file for each frame of the video. This folder should be renamed and uploaded to the LiDAR-Gait-Analysis folder created from cloning this repository, and the programs can now run the analysis using this folder.

## General-LiDAR

To use the general-lidar folder, change your directory to general-lidar
  ```bash
  cd general-lidar
  ```

The general-lidar folder contains 5 programs whose functionalities are described below. These programs are general-purpose LiDAR data analysis and visualization tools as opposed to specific tools targeted for gait analysis.

**png2realdepth.py**: This program prompts the user to input their LiDAR data folder name and an output file name (which should be in a .png format). It then prints the number of total frames in the input video, and asks the user to pick a valid frame number (frames start from 000000 and should all be 6 digits). It then prompts the user to choose an x and y pixel coordinate at which the real distance from that point to the camera is printed, and a depth map of all points is also saved to the output file. It also opens a visualizer window showing the depth map, and depth values in the visualizer can be viewed by hovering the cursor over pixels. 

**distancefrompoints.py**: This program prompts the user to input their LiDAR data folder name and an output file name (which should be in a .png format). It then prints the number of total frames in the input video, and asks the user to pick a valid frame number (frames start from 000000 and should all be 6 digits). It then prompts the user to choose two sets of x and y pixel coordinates. The first coordinate location inputted by the user will be the reference coordinates from which the distance map data will be based on (it will be a map of the distances from this point to all other points). The second coordinate location will be the point from which a distance will be printed, allowing the user to print distances between these two exact pixel locations. The distance map is then saved to the output file. It also opens a visualizer window showing the distance map, and each distance can be viewed by hovering the cursor over each pixel. 

**makevideo.py**: This program prompts the user to input their LiDAR data folder name, then asks if they want a depth map or a confidence map. It then asks for two output file names, one for the standalone depth/confidence video, and one for the comparative video (these should both be in .mp4 file formats). It then outputs one standalone video in the first output file which shows the depth/confidence version of the original video, and also a comparative side-by-side video in the second output file of the depth/confidence video next to the original rgb video.

**3dframe.py**: This program prompts the user to input their LiDAR data folder name and an output file name (which should be in .ply file format). It then prints the number of total frames in the input video, and asks the user to pick a valid frame number (frames start from 000000 and should all be 6 digits). It then creates a 3d point cloud representation of the LiDAR data, shows the point cloud in an open3d window, and saves the result to the output file.

**3dvid.py**: This program prompts the user to input their LiDAR data folder name, as well as an output file name (which should be in .mp4 format) then opens an open3d visualizer window in which the 3d point cloud video plays. The result of this 3d visualizer is saved to the output file.

## Gait-Analysis

To use the gait-analysis folder, change your directory to gait-analysis
  ```bash
  cd gait-analysis
  ```

The gait-analysis folder contains 4 programs whose functionalities are described below. These programs utilize the Mediapipe pose estimation model to track joint locations over time, and map the joints to the LiDAR depth data which allows for analysis of gait through 3d pose tracking.

**visualize.py**: This program prompts the user to input their LiDAR data folder name as well as an output file name (which should be in .mp4 format). It then plays the original rgb video with pose estimation joint landmarks from Mediapipe drawn onto the video, saving this to the output file.

**calculateangle.py**: This program prompts the user to input their LiDAR data folder name as well as a body part which should be either left knee, right knee, left elbow, right elbow, left hip, or right hip. It then prints out the angle of that body part (i.e. left elbow angle) for each frame in the video. Additionally, in the charts folder (which it creates if it doesn't already exist), it creates csv files for the 3d location for each of the 3 body parts used to calculate that angle (i.e. left elbow, left shoulder, and left wrist to calculate the left elbow angle), as well as a csv file containing the angle data for each frame. It also creates graphs in .png format to visualize the distance of each of these 3 body parts from the camera over time as well as a graph for the angle over time.

**detrend.py**: This program prompts the user to input their LiDAR data folder name as well as a body part (which should be either left elbow, left shoulder, left wrist, left knee, left hip, left ankle, right elbow, right shoulder, right wrist, right knee, right hip, or right ankle). It then creates a .png graph of the distance of that body part from the camera over time along with a trendline. It also plots a detrended line by plotting the difference between the actual distance and the trendline over time.

**pipelandmark**: This program is used for both the calculateangle.py and detrend.py program, but doesn't have any use of its own.
