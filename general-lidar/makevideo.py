import cv2
import os
import numpy as np

folder = input("Folder name: ")
dorc = input("depth or confidence? ")
output = input("Output video filename: ")
fps = 60

paths = sorted([os.path.join(folder, dorc, f) for f in os.listdir(folder + "/" + dorc) if f.endswith(".png")])

if not paths:
    raise RuntimeError("No PNG files found in folder.")

first = cv2.imread(paths[0], cv2.IMREAD_UNCHANGED)
if first is None:
    raise RuntimeError("Failed to read first frame.")

h, w = first.shape if len(first.shape) == 2 else first.shape[:2]

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output, fourcc, fps, (h, w), isColor=True)

for path in paths:
    frame = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if frame is None:
        print(f"Warning: Failed to read {path}")
        continue

    norm = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
    norm = norm.astype(np.uint8)

    rgb_frame = cv2.applyColorMap(norm, cv2.COLORMAP_JET)

    if rgb_frame.dtype != np.uint8:
        rgb_frame = cv2.convertScaleAbs(rgb_frame, alpha=255.0/rgb_frame.max())

    if rgb_frame.shape[:2] != (h, w):
        rgb_frame = cv2.resize(rgb_frame, (w, h))

    rgb_frame = cv2.rotate(rgb_frame, cv2.ROTATE_90_CLOCKWISE)

    out.write(rgb_frame)

out.release()

depth_cap = cv2.VideoCapture(output) 
rgb_cap = cv2.VideoCapture(folder + "/rgb.mp4")

cmb_output = input("Comparative video filename: ")

output_size = (192 * 2, 256)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(cmb_output, fourcc, 60.0, output_size)

while True:
    ret_d, depth_frame = depth_cap.read()
    ret_rgb, rgb_frame = rgb_cap.read()

    if not ret_d or not ret_rgb:
        break

    rgb_resized = cv2.resize(rgb_frame, (256, 192))
    rgb_resized = cv2.rotate(rgb_resized, cv2.ROTATE_90_CLOCKWISE)

    combined = np.hstack((rgb_resized, depth_frame))

    out.write(combined)

depth_cap.release()
rgb_cap.release()
out.release

print(f"Videos saved: {output}, {cmb_output}")