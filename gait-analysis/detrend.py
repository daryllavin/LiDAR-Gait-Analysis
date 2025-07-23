import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import calculateangle

# Get folder
folder = input("Folder name: ")
for bp in ('left elbow', 'left shoulder', 'left wrist', 'left knee', 'left hip', 'left ankle', 'right elbow', 'right shoulder', 'right wrist', 'right knee', 'right hip', 'right ankle'):
    if not os.path.exists(f"charts/{folder}/data/{bp}.csv"):
        calculateangle.main(folder, bp)

    # Read z data from csv file for that body part
    df = pd.read_csv(f"charts/{folder}/data/{bp}.csv", usecols=[2])
    df.columns = [bp]

    # Align time data (assuming video is 60 fps)
    df['Time'] = df.index / 60
    df = df[['Time', bp]]

    # Get arrays of time and distance data
    x = df['Time'].values
    y = df[bp].values

    # Create trendline
    degree = 2 
    coeffs = np.polyfit(x, y, degree)
    trend = np.polyval(coeffs, x)

    # Get detrended data by finding difference between actual and trend data
    df['Detrended'] = y - trend

    # Create plot with distance, trend, and detrended data over time
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='Original')
    plt.plot(x, trend, label='Trend', linestyle='--')
    plt.plot(x, df['Detrended'], label='Detrended', linestyle=':')
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel(f"{bp.capitalize()} Value")
    plt.title(f"Polynomial Detrending - {bp.capitalize()}")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs(f"charts/{folder}/detrended", exist_ok=True)
    plt.savefig(f"charts/{folder}/detrended/{bp} Detrended.png")
