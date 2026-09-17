import cv2
import numpy as np


# ============================================================
# ESP32-CAM STREAM
# ============================================================

STREAM_URL = "http://192.168.186.122/stream"


# ============================================================
# YOLO MODEL
# ============================================================

weights_path = r"./YOLO/yolov3.weights"
config_path = r"./YOLO/yolov3.cfg"
names_path = r"./YOLO/coco.names"


# Load YOLO
print("Loading YOLO...")

net = cv2.dnn.readNet(
    weights_path,
    config_path
)


# Load class names
with open(names_path, "r") as f:

    classes = [
        line.strip()
        for line in f.readlines()
    ]


# ============================================================
# YOLO OUTPUT LAYERS
# ============================================================

layer_names = net.getLayerNames()

out_layers = net.getUnconnectedOutLayers()

output_layers = []

for i in out_layers:

    if isinstance(
        i,
        (list, tuple, np.ndarray)
    ):

        output_layers.append(
            layer_names[int(i[0]) - 1]
        )

    else:

        output_layers.append(
            layer_names[int(i) - 1]
        )


# ============================================================
# COLORS
# ============================================================

colors = np.random.uniform(
    0,
    255,
    size=(len(classes), 3)
)


# ============================================================
# OBJECT DETECTION
# ============================================================

def detect_objects(frame):

    height, width = frame.shape[:2]


    # Create YOLO blob
    blob = cv2.dnn.blobFromImage(
        frame,
        1 / 255.0,
        (416, 416),
        swapRB=True,
        crop=False
    )


    # Send image to YOLO
    net.setInput(blob)


    # Run detection
    layer_outputs = net.forward(
        output_layers
    )


    boxes = []
    confidences = []
    class_ids = []


    # ========================================================
    # PROCESS DETECTIONS
    # ========================================================

    for output in layer_outputs:

        for detection in output:

            scores = detection[5:]

            class_id = np.argmax(scores)

            confidence = scores[class_id]


            if confidence > 0.3:

                center_x = int(
                    detection[0] * width
                )

                center_y = int(
                    detection[1] * height
                )

                w = int(
                    detection[2] * width
                )

                h = int(
                    detection[3] * height
                )


                x = int(
                    center_x - w / 2
                )

                y = int(
                    center_y - h / 2
                )


                boxes.append([
                    x,
                    y,
                    w,
                    h
                ])

                confidences.append(
                    float(confidence)
                )

                class_ids.append(
                    class_id
                )


    # ========================================================
    # NON-MAXIMUM SUPPRESSION
    # ========================================================

    indexes = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        0.3,
        0.4
    )


    if len(indexes) > 0:

        indexes = np.array(
            indexes
        ).flatten()


        for i in indexes:

            x, y, w, h = boxes[i]

            label = classes[
                class_ids[i]
            ]

            confidence = confidences[i]

            color = colors[
                class_ids[i]
            ]


            print(
                f"Detected: {label} "
                f"{confidence:.2f}"
            )


            # Draw box
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                2
            )


            # Draw label
            cv2.putText(
                frame,
                f"{label} {confidence:.2f}",
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )


    return frame


# ============================================================
# OPEN ESP32 STREAM
# ============================================================

print("Connecting to ESP32-CAM...")

cap = cv2.VideoCapture(
    STREAM_URL
)


if not cap.isOpened():

    print(
        "ERROR: Could not open ESP32-CAM stream"
    )

    exit()


print("ESP32-CAM connected")
print("YOLO detection started")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = cap.read()


    if not ret:

        print(
            "ERROR: Could not receive frame"
        )

        break


    # Run YOLO
    frame = detect_objects(
        frame
    )


    # Display
    cv2.imshow(
        "YOLO ESP32-CAM",
        frame
    )


    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()