import cv2
import cv2.aruco as aruco
import socket

# ===============================
# Socket Configuration
# ===============================
HOST = "127.0.0.1"
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# ===============================
# Camera Setup (Windows)
# ===============================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("[ERROR] Camera could not be opened")
    exit()

print("[CAMERA] Running marker detection")

# ===============================
# ArUco Setup (DICT_4X4_50)
# ===============================
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

parameters = aruco.DetectorParameters()
parameters.adaptiveThreshWinSizeMin = 5
parameters.adaptiveThreshWinSizeMax = 50
parameters.adaptiveThreshWinSizeStep = 5
parameters.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
parameters.minMarkerPerimeterRate = 0.03
parameters.maxMarkerPerimeterRate = 4.0

detector = aruco.ArucoDetector(aruco_dict, parameters)

# ===============================
# Allowed Marker IDs
# ===============================
ALLOWED_MARKERS = {0, 1, 2, 3, 4, 5}

# ===============================
# Main Loop
# ===============================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        for marker_id in ids.flatten():
            if marker_id in ALLOWED_MARKERS:
                msg = f"MARKER:{marker_id}\n"
                sock.sendall(msg.encode())
                print(f"[VALID] MARKER:{marker_id}")
            else:
                print(f"[IGNORED] Marker {marker_id}")

        aruco.drawDetectedMarkers(frame, corners, ids)

    cv2.imshow("TUIO Marker Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ===============================
# Cleanup
# ===============================
cap.release()
sock.close()
cv2.destroyAllWindows()
