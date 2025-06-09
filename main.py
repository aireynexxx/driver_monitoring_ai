# Import required libraries
from picamera2 import Picamera2, Preview
import time
import cv2
import numpy as np
import mediapipe as mp
import tkinter as tk
from tkinter import messagebox
import threading
import tflite_runtime.interpreter as tflite

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
	static_image_mode=False,
	max_num_faces=1,
	refine_landmarks=True,
	min_detection_confidence=0.5,
	min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Calculate Eye Aspect Ratio (EAR) to detect if eyes are closed
def eye_aspect_ratio(landmarks, eye_indices):
	def dist(a, b):
		return np.linalg.norm(np.array(a) - np.array(b))
	p1 = landmarks[eye_indices[0]]
	p2 = landmarks[eye_indices[1]]
	p3 = landmarks[eye_indices[2]]
	p4 = landmarks[eye_indices[3]]
	p5 = landmarks[eye_indices[4]]
	p6 = landmarks[eye_indices[5]]
	vertical = (dist(p2, p6) + dist(p3, p5)) / 2.0
	horizontal = dist(p1, p4)
	return vertical / horizontal

# Flags to track alert state
alert_shown = False
tired_shown = False

# Alert popups using tkinter
def message_alert():
	messagebox.showinfo('Alert', 'Sleeping')
	return False

def tired_alert():
	messagebox.showinfo('Alert', 'Tired')
	return False

# Load labels for TFLite object detection model
def load_labels(path):
	with open(path, 'r') as f:
		return [line.strip() for line in f.readlines()]

# Alert for phone detection
def phone_message_alert():
	global phone_alert_shown, phone_frames, no_phone_frames
	messagebox.showinfo('Alert', 'Phone out')
	phone_alert_shown = False 

# Load TFLite object detection model
interpreter = tflite.Interpreter(model_path='detect.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_shape = input_details[0]['shape']
input_dtype = input_details[0]['dtype']
labels = load_labels('labelmap.txt')

# Phone detection state
phone_alert_shown = False
phone_frames = 0
no_phone_frames = 0

# Facial landmark indices
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 273, 380]
UPPER_LIP_IDX = 13
LOWER_LIP_IDX = 14

# Fatigue detection counters
timer = 90
yawns = 0
eyes_closed = 0
mouth_open = 0

# Initialize PiCamera
cam = Picamera2()
config = cam.create_preview_configuration(main={'format': 'RGB888', 'size': (640, 480)})
cam.configure(config)
cam.start()
print('Camera started')
time.sleep(2)
print('Initialization complete')

try:
	while True:
		# Capture frame from camera
		frame = cam.capture_array('main')
		img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# Run face mesh detection
		results = face_mesh.process(img_rgb)
		if results.multi_face_landmarks:
			for face_landmarks in results.multi_face_landmarks:
				h, w, _ = frame.shape
				landmarks = [(lm.x * w, lm.y * h) for lm in face_landmarks.landmark]

				# EAR Calculation for both eyes
				left_ear = eye_aspect_ratio(landmarks, LEFT_EYE_IDX)
				right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE_IDX)
				avg_ear = (left_ear + right_ear) / 2.0

				eye_closed_thresh = 0.85
				if avg_ear < eye_closed_thresh:
					status = 'Eyes closed'
					color = (0, 0, 255)
					eyes_closed += 1
				else:
					status = 'Eyes open'
					color = (0, 255, 0)
					eyes_closed = 0
					alert_shown = False

				# Alert if eyes have been closed too long
				if eyes_closed > 70 and not alert_shown:
					alert_shown = True
					threading.Thread(target=message_alert).start()

				cv2.putText(frame, status, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

				# Mouth open/yawn detection
				upper_lip = landmarks[UPPER_LIP_IDX]
				lower_lip = landmarks[LOWER_LIP_IDX]
				mouth_open_dist = np.linalg.norm(np.array(upper_lip) - np.array(lower_lip))
				yawn_thresh = 20

				if mouth_open_dist > yawn_thresh and mouth_open < 50:
					yawn_status = 'Not Yawning'
					yawn_color = (255, 0, 0)

				if mouth_open_dist > yawn_thresh:
					mouth_open += 1
					mouth_status = 'Mouth Open'
					mouth_color = (255, 255, 0)
				else:
					mouth_status = 'Mouth Closed'
					mouth_color = (0, 255, 255)
					mouth_open = 0
					timer -= 2
					yawn_status = 'Not Yawning'
					yawn_color = (255, 0, 0)

				if mouth_open == 30:
					yawn_status = 'Yawning'
					yawn_color = (255, 0, 0)
					yawns += 1
					timer = 90

				if yawns >= 3 and timer != 0 and not tired_shown:
					tired_shown = True
					threading.Thread(target=tired_alert).start()
				elif timer == 0:
					tired_shown = False
					yawns = 0

				cv2.putText(frame, mouth_status, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, mouth_color, 2)
				cv2.putText(frame, yawn_status, (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, yawn_color, 2)

		# Prepare input for TFLite phone detection
		input_frame = cv2.resize(frame, (input_shape[2], input_shape[1]))
		if input_dtype == np.float32:
			input_tensor = np.expand_dims(input_frame.astype(np.float32), axis=0)
			input_tensor = (input_tensor - 127.5) / 127.5  # normalize to [-1, 1]
		else:
			input_tensor = np.expand_dims(input_frame.astype(np.uint8), axis=0)

		interpreter.set_tensor(input_details[0]['index'], input_tensor)
		interpreter.invoke()

		# Get TFLite model output
		boxes = interpreter.get_tensor(output_details[0]['index'])[0]
		classes = interpreter.get_tensor(output_details[1]['index'])[0]
		scores = interpreter.get_tensor(output_details[2]['index'])[0]

		# Loop through detected objects
		h, w, _ = frame.shape
		for i in range(len(scores)):
			if scores[i] > 0.45:
				class_id = int(classes[i])
				label_index = class_id - 1 if class_id > 0 else 0
				label = labels[label_index] if 0 <= label_index < len(labels) else 'N/A'

				if label == 'cell phone':
					# Draw bounding box for phone
					ymin, xmin, ymax, xmax = boxes[i]
					left = int(xmin * w)
					top = int(ymin * h)
					right = int(xmax * w)
					bottom = int(ymax * h)
					phone_frames += 1
					no_phone_frames = 0
					print(phone_frames)
					cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
					cv2.putText(frame, f"{label}: {scores[i]:.2f}", (left, max(top - 10, 10)),
								cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

					if phone_frames > 100 and not phone_alert_shown:
						phone_alert_shown = True
						threading.Thread(target=phone_message_alert).start()
				else:
					no_phone_frames += 1
					if no_phone_frames > 50:
						phone_frames = 0
						phone_alert_shown = False

		# Show the live video feed
		cv2.imshow('feed', frame)
		key = cv2.waitKey(10)
		if key == ord('q'):
			break
finally:
	cv2.destroyAllWindows()
	face_mesh.close()
