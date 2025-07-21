import numpy as np
import os

folder = input("Folder name: ")
bp = input("Body part (left knee, right knee, left elbow, right elbow, left hip, right hip): ")
landmark_map = {
    "left elbow": ("left elbow", "left shoulder", "left wrist"),
    "right elbow": ("right elbow", "right shoulder", "right wrist"),
    "left hip": ("left hip", "left shoulder", "left knee"),
    "right hip": ("right hip", "right shoulder", "right knee"),
    "left knee": ("left knee", "left hip", "left ankle"),
    "right knee": ("right knee", "right hip", "right ankle")
}
bp1, bp2, bp3 = landmark_map[bp]
CACHE_FILE = f'{folder}/{bp}/landmark_cache.npz'

# Try to load from cache
if os.path.exists(CACHE_FILE):
    data = np.load(CACHE_FILE)
    l1 = data['l1']
    l2 = data['l2']
    l3 = data['l3']
    input1 = data['input1'].tolist()
    input2 = data['input2'].tolist()
    input3 = data['input3'].tolist()
    print("Loaded from cache")
else:
    print("Running pipelandmark...")
    from pipelandmark import extract_landmarks
    l1, l2, l3, input1, input2, input3 = extract_landmarks(folder, bp1, bp2, bp3)

    # Save to cache
    np.savez(CACHE_FILE, l1=l1, l2=l2, l3=l3, input1=input1, input2=input2, input3=input3)

def calculate_angle(A, B, C):
    # Turn tuples to numpy arrays
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)

    # Get vectors between the points (i.e. elbow to shoulder and elbow to wrist)
    BA = A - B
    BC = C - B

    # Normalize vectors
    norm_BA = np.linalg.norm(BA)
    norm_BC = np.linalg.norm(BC)
    
    if norm_BA == 0 or norm_BC == 0:
        return None  # Avoid division by zero

    # Find cosine of the elbow/knee angle
    cosine_angle = np.dot(BA, BC) / (norm_BA * norm_BC)
    # Clip cosine to avoid floating point errors outside [-1, 1]
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    # Get angle in radians
    angle_rad = np.arccos(cosine_angle)
    # Convert to degrees
    angle_deg = np.degrees(angle_rad)

    return angle_deg

# Add angle at each frame
l4 = []
for i in range(len(l1)):
    l4.append(calculate_angle(l2[i], l1[i], l3[i]))
    print(calculate_angle(l2[i], l1[i], l3[i]))

# Save the x,y,z data for each body part in csv files
save_dir = f'charts/{folder}'
os.makedirs(save_dir, exist_ok=True)
np.savetxt(f'charts/{folder}/{input1}.csv', l1, delimiter=',', fmt='%s')
np.savetxt(f'charts/{folder}/{input2}.csv', l2, delimiter=',', fmt='%s')
np.savetxt(f'charts/{folder}/{input3}.csv', l3, delimiter=',', fmt='%s')
np.savetxt(f'charts/{folder}/{input3} angle.csv', l4, delimiter=',', fmt='%s')
