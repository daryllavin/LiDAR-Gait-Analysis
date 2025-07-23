import numpy as np
import os
import matplotlib.pyplot as plt
# Map pivot body part to the three landmarks to calculate angle
landmark_map = {
    "left elbow": ("left elbow", "left shoulder", "left wrist"),
    "right elbow": ("right elbow", "right shoulder", "right wrist"),
    "left hip": ("left hip", "left shoulder", "left knee"),
    "right hip": ("right hip", "right shoulder", "right knee"),
    "left knee": ("left knee", "left hip", "left ankle"),
    "right knee": ("right knee", "right hip", "right ankle")
}

# Takes in arrays of 3 3d points A, B, and C and calculates the angle at B
def calculate_angle(A, B, C):
    # Turn points into numpy arrays
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    # Get vectors BA and BC
    BA = A - B
    BC = C - B

    # Get magnitude of vectors BA and BC
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)

    # Ensure BA and BC are not 0 vectors
    if norm_BA == 0 or norm_BC == 0:
        return None

    # Get cosine of the angle using formula (BA * BC / (|BA| * |BC|))
    cosine_angle = np.dot(BA, BC) / (norm_BA * norm_BC)
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    # Get angle in radians then degrees
    angle_rad = np.arccos(cosine_angle)
    angle_deg = np.degrees(angle_rad)

    # Return angle in degrees
    return angle_deg

def plot_point_over_time(data, label, save_path):
    data = np.array(data)
    frames = np.arange(data.shape[0]) / 60
    plt.figure(figsize=(10, 6))
    plt.plot(frames, data[:, 2])
    plt.title(f'Z Distance Over Time ({label})')
    plt.xlabel('Time (s)')
    plt.ylabel('Z Distance (m)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_angle_over_time(angles, bp, save_path):
    frames = np.arange(len(angles)) / 60
    plt.figure(figsize=(10, 6))
    plt.plot(frames, angles, color='purple')
    plt.title(f'{bp.capitalize()} Angle Over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Angle (degrees)')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def main(folder=None, bp=None):
    # If not being used as module get the input folder and requested body part
    if folder is None:
        folder = input("Folder name: ")
    
    for bp in landmark_map:
        # Get the three landmarks based on the landmark at which angle is being calculated
        bp1, bp2, bp3 = landmark_map[bp]

        CACHE_FILE = f'{folder}/{bp}/landmark_cache.npz'

        # If pipelandmark has already been run, use the cache data
        if os.path.exists(CACHE_FILE):
            data = np.load(CACHE_FILE)
            l1 = data['l1']
            l2 = data['l2']
            l3 = data['l3']
            input1 = data['input1'].tolist()
            input2 = data['input2'].tolist()
            input3 = data['input3'].tolist()
            print("Loaded from cache")
        # If pipelandmark hasn't been run, run it
        else:
            print("Running pipelandmark...")
            from pipelandmark import extract_landmarks
            l1, l2, l3, input1, input2, input3 = extract_landmarks(folder, bp1, bp2, bp3)

            # Save cache file for this data so pipelandmark doesn't have to be run on it again
            np.savez(CACHE_FILE, l1=l1, l2=l2, l3=l3, input1=input1, input2=input2, input3=input3)

        l4 = []
        for i in range(len(l1)):
            l4.append(calculate_angle(l2[i], l1[i], l3[i]))

        # Save the x/y/z for each body part and the angle data as csv files
        save_dir = f'charts/{folder}/data'
        os.makedirs(save_dir, exist_ok=True)
        np.savetxt(f'charts/{folder}/data/{input1}.csv', l1, delimiter=',', fmt='%s')
        np.savetxt(f'charts/{folder}/data/{input2}.csv', l2, delimiter=',', fmt='%s')
        np.savetxt(f'charts/{folder}/data/{input3}.csv', l3, delimiter=',', fmt='%s')
        np.savetxt(f'charts/{folder}/data/{input1} angle.csv', l4, delimiter=',', fmt='%s')

        # Plot and save charts for each point's x, y, z over time
        os.makedirs(f"charts/{folder}/graphs", exist_ok=True)
        plot_point_over_time(l1, input1, f'charts/{folder}/graphs/{input1} distance.png')
        plot_point_over_time(l2, input2, f'charts/{folder}/graphs/{input2} distance.png')
        plot_point_over_time(l3, input3, f'charts/{folder}/graphs/{input3} distance.png')

        # Plot and save angle over time
        plot_angle_over_time(l4, input1, f'charts/{folder}/graphs/{input1} angle.png')

    return l4

if __name__ == '__main__':
    l4 = main()

    # If not being run as a module, print the angle at each frame
    for angle in l4:
        print(angle)