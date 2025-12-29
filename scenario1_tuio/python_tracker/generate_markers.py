import cv2
import cv2.aruco as aruco

# ===============================
# Use AVAILABLE dictionary
# ===============================
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# ===============================
# Generate ONLY markers 0–5
# ===============================
for i in range(6):
    marker = aruco.generateImageMarker(aruco_dict, i, 300)
    cv2.imwrite(f"marker_{i}.png", marker)
    print(f"[GENERATED] marker_{i}.png")
