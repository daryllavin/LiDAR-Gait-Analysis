import numpy as np
from pipelandmark import l1_arr as l1
from pipelandmark import l2_arr as l2
from pipelandmark import l3_arr as l3
from pipelandmark import input1, input2, input3

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

# Print out angle at each frame
for i in range(len(l1)):
    print(calculate_angle(l2[i], l1[i], l3[i]))

# Save the x,y,z data for each body part in csv files
np.savetxt(f'{input1}.csv', l1, delimiter=',', fmt='%s')
np.savetxt(f'{input2}.csv', l2, delimiter=',', fmt='%s')
np.savetxt(f'{input3}.csv', l3, delimiter=',', fmt='%s')

