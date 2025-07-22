# LiDAR Gait Analysis

This project analyzes human gait using RGB-D video from LiDAR-enabled iPhones/iPads, combining 3D pose estimation with depth data to detect trends in Parkinsonian gait.

## Contents
- [Overview](#overview)
- [Results](#results)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [General-LiDAR](#general-lidar)
- [Gait-Analysis](#gait-analysis)

## Overview

This project aims to utilize iPad/iPhone LiDAR recording capabilities to analyze gait through 3D position tracking, specifically aimed to track and detect patterns in Parkinsonian gait. The repository has two main folders, general-lidar and gait-analysis. 

The general-lidar folder contains 5 programs designed for general-purpose LiDAR analysis applications, with functionalities such as creating depth maps of videos and/or individual frames, as well as 3D point cloud video/image recreations. You can read more about these programs in the [General-LiDAR](#general-lidar) section below.

The gait-analysis folder includes 4 programs for pose tracking and gait analysis. It utilizes the MediaPipe pose estimation model to map joint locations to the LiDAR data, which allows for data such as joint location over time and joint angles to be calculated and plotted. You can read more about the specific functionalities in the [Gait-Analysis](#gait-analysis) section below.

## Results

Participants were asked to stand up from a chair around five meters away from the camera and walk towards it. From this data, depth maps, 3D point cloud videos, and charts of joint angles and joint positions were generated. See below for some of the results.

Using LiDAR data, depth maps of euclidean distance from the camera at every pixel are generated from single frames of a video. By combining the depth maps from each frame of the video, a full LiDAR depth video is created:

<img src=sample-results/frame.png height="300"> <img src=sample-results/depthvid.gif height="290">

By using Open3D to visualize the 3D point clouds, interactive 3D frame-by-frame videos are created:

<img src=sample-results/3dvid.gif width="500">

For gait analysis, MediaPipe is used to track joint locations which can be mapped to the LiDAR depth data. Here is a visualization of MediaPipe pose tracking:

<img src=sample-results/mediapipe.gif width="300">

Using the MediaPipe pose tracking along with LiDAR data, graphs are generated like the ones below (similar graphs can be created for different human joints). The first graph displays the right knee angle over time which documents the transition from sitting to walking (fluctuations at the end reflect the knee leaving frame). The second graph shows the movement of the right knee's position over time compared to a trendline, and creates a detrended line which provides insights into how the knee is moving over time:

<img src=sample-results/rightkneeangle.png width="500"> <img src=sample-results/Rightkneedetrended.png width="500">

## Requirements
- Python 3.10 (recommended, as specified in env.yaml)
- [Anaconda](https://www.anaconda.com/)
- iPhone 12 Pro+ or iPad Pro with LiDAR
- [Stray Scanner](https://apps.apple.com/us/app/stray-scanner/id1564126243) app to record LiDAR data

## Installation

Make sure you have [Anaconda](https://www.anaconda.com/) installed.

1. Clone this repository:

   ```bash
   git clone https://github.com/daryllavin/LiDAR-Gait-Analysis.git
   cd LiDAR-Gait-Analysis
   ```
   
2. Create and activate the Conda environment:

   ```bash
   conda env create -f env.yaml
   conda activate lidar-gait-analysis
   ```

## Usage

To utilize the LiDAR capabilities of the iPhone/iPad, you must have a LiDAR-equipped device (iPhone 12+ Pro/Pro Max, or iPad Pro).

The **Stray Scanner** app (available on the App Store) should be used to record LiDAR videos. When recording for gait analysis, ensure the video is recorded at **60 FPS** for accurate joint tracking and analysis.

Each recording session is saved as a folder in the Files app. This folder includes:
- Camera intrinsic files (camera_matrix.csv, imu.csv, odometry.csv)
- The original RGB video (rgb.mp4)
- Folders for depth and confidence frames (depth/, confidence/) as PNGs

Rename this folder and move it into your cloned LiDAR-Gait-Analysis repository. Once placed there, the programs can process and analyze the video.

To run a general-lidar program, see [General-LiDAR](#general-lidar)

To run a gait-analysis program, see [Gait-Analysis](#gait-analysis)

## General-LiDAR

### Running a General-LiDAR Script

Ex. run makevideo.py:

   ```bash
   python3 general-lidar/makevideo.py
   ```

### Purpose

The general-lidar folder contains 5 programs whose functionalities are described below. These programs are general-purpose LiDAR data analysis and visualization tools as opposed to specific tools targeted for gait analysis.

**Note: The video dimensions are 192x256, so x-coordinates range from 0-191 and y-coordinates range from 0-255**

### General-LiDAR Summary

| Script                | Description                                                         |
|------------------------|---------------------------------------------------------------------|
| png2realdepth.py     | Converts a single video frame to a depth map and outputs distance from the camera |
| distancefrompoints.py| Creates a depth map from a user-defined point; computes distance between any two pixels |
| makevideo.py         | Generates a LiDAR-based depth/confidence video and a side-by-side comparison with the RGB video |
| 3dframe.py           | Creates and saves a 3D point cloud of a single frame as a PLY file |
| 3dvid.py             | Creates and plays an interactive 3D point cloud video; saves it as MP4 |


**png2realdepth.py**: This program converts a frame from a video into a depth map of euclidean distances from the camera, and can display the distance value in meters from any point in the frame.

It first prompts the user to input their LiDAR data folder name and an output file name (which should be in PNG format). It then prints the number of total frames in the input video, and asks the user to pick a valid frame number (frames start from 000000 and should be exactly 6 digits). It then prompts the user to choose an x and y pixel coordinate at which the real distance from that point to the camera is printed, and a depth map of all points is also saved to the output file. It also opens a visualizer window showing the depth map, and depth values in the visualizer can be viewed by hovering the cursor over pixels. 

**distancefrompoints.py**: This program creates a depth map of distances from a specific point in the frame that the user inputs, also with the ability to print the distance between any two points in the frame.

It first prompts the user to input their LiDAR data folder name and an output file name (which should be in PNG format). It then prints the number of total frames in the input video, and asks the user to pick a valid frame number (frames start from 000000 and should be exactly 6 digits). It then prompts the user to choose two sets of x and y pixel coordinates. The first coordinate location input by the user will be the reference coordinate from which the distance map data will be based on (it will be a map of the distances from this point to all other points). The second coordinate location will be the point from which a distance will be printed, allowing the user to print distances between these two exact pixel locations. The distance map is then saved to the output file. It also opens a visualizer window showing the distance map, and each distance can be viewed by hovering the cursor over each pixel. 

**makevideo.py**: This program creates either a depth or confidence map recreation of the video based on LiDAR data. It also creates a video with the depth/confidence video side-by-side with the original.

It first prompts the user to input their LiDAR data folder name, then asks if they want a depth map or a confidence map. It then asks for two output file names, one for the standalone depth/confidence video, and one for the comparative video (these should both be in MP4 formats). It then outputs one standalone video in the first output file which shows the depth/confidence version of the original video, and also a comparative side-by-side video in the second output file of the depth/confidence video next to the original RGB video.

**3dframe.py**: This program opens an Open3D window with and interactive 3D point cloud model of a single frame of a video, and saves it as a PLY file.

It first prompts the user to input their LiDAR data folder name and an output file name (which should be in PLY file format). It then prints the number of total frames in the input video, and asks the user to pick a valid frame number (frames start from 000000 and should be exactly 6 digits). It then creates a 3D point cloud representation of the LiDAR data, shows the point cloud in an open3D window, and saves the result to the output file.

**3dvid.py**: This program opens an Open3D window where an interactive 3D point cloud recreation of the video plays. The result of this video is saved to an MP4 file.

It first prompts the user to input their LiDAR data folder name, as well as an output file name (which should be in .mp4 format) then opens an open3D visualizer window in which the 3D point cloud video plays. The result of this 3D visualizer is saved to the output file.

## Gait-Analysis

### Running a Gait-Analysis Script

Ex. run calculateangle.py:

   ```bash
   python3 gait-analysis/calculateangle.py
   ```

### Purpose

The gait-analysis folder contains 4 programs whose functionalities are described below. These programs utilize the MediaPipe pose estimation model to track joint locations over time, and map the joints to the LiDAR depth data which allows for analysis of gait through 3D pose tracking.

### Gait-Analysis Summary

| Script              | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| visualize.py      | Overlays MediaPipe pose landmarks on the video and saves it as an MP4       |
| calculateangle.py | Calculates joint angles (e.g., knees, elbows); saves CSV + graphs           |
| detrend.py        | Plots joint movement over time, removes trendline for better insight        |
| pipelandmark.py   | Helper module for joint location extraction (not used on its own)         |

**visualize.py**: This program displays the MediaPipe joint landmarks drawn onto the video, and saves it as an MP4.

It first prompts the user to input their LiDAR data folder name as well as an output file name (which should be in MP4 format). It then plays the original RGB video with pose estimation joint landmarks from MediaPipe drawn onto the video, saving this to the output file.

**calculateangle.py**: This program computes and prints the angle at a specific joint over time. It saves this data as well as the location data for the three joints used to calculate this angle as CSV files, and also generates graphs of the data over time.

It first prompts the user to input their LiDAR data folder name as well as a body part which should be either left knee, right knee, left elbow, right elbow, left hip, or right hip. It then prints the computed angle at that joint (e.g., left elbow angle) for each frame in the video. Additionally, in the charts folder (which it creates if it doesn't already exist), it creates CSV files for the 3D location of each of the 3 body parts used to calculate that angle (i.e. left elbow, left shoulder, and left wrist to calculate the left elbow angle), as well as a CSV file containing the angle data for each frame. It also creates graphs in PNG format to visualize the distance of each of these 3 body parts from the camera over time and a graph for the angle over time.

**detrend.py**: This program creates a PNG graph of the distance of a body part from the camera over time. This data is plotted alongside a trendline, and a detrended line is generated.

It first prompts the user to input their LiDAR data folder name as well as a body part (which should be either left elbow, left shoulder, left wrist, left knee, left hip, left ankle, right elbow, right shoulder, right wrist, right knee, right hip, or right ankle). It then creates a PNG graph of the distance of that body part from the camera over time along with a trendline. It also plots a detrended line by plotting the difference between the actual distance and the trendline over time.

**pipelandmark**: This program is a helper module and not meant to be executed directly. It is automatically imported by calculateangle.py and detrend.py which require joint landmark extraction.
