import cv2
import mediapipe as mp
from math import sqrt
import pyautogui
import pydirectinput

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
		model_complexity=0,
		min_detection_confidence=0.5,
		min_tracking_confidence=0.5) as hands:
	while cap.isOpened():
		success, image = cap.read()
		if not success:
			print("Ignoring empty camera frame.")
			# If loading a video, use 'break' instead of 'continue'.
			continue

		# To improve performance, optionally mark the image as not writeable to
		# pass by reference.
		image.flags.writeable = False
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		results = hands.process(image)

		# Draw the hand annotations on the image.
		image.flags.writeable = True
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		if results.multi_hand_landmarks:
			# Get size of image
			image_height, image_width, _ = image.shape

			# Main process
			for hand_landmarks in results.multi_hand_landmarks:
				point1 = (hand_landmarks.landmark[8].x,hand_landmarks.landmark[8].y)
				point2 = (hand_landmarks.landmark[4].x,hand_landmarks.landmark[4].y)
				dist = sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

				point2 = (hand_landmarks.landmark[4].x,hand_landmarks.landmark[4].y)
				point3 = (hand_landmarks.landmark[20].x,hand_landmarks.landmark[20].y)
				dist1 = sqrt((point2[0]-point3[0])**2 + (point2[1]-point3[1])**2)

				#print(dist) test khoang cach

				if dist < 0.05 :pydirectinput.click()
				if dist1 < 0.05 : mouse.press('esc')

				#print('hand_landmarks:', hand_landmarks) --x/y/z
				
				'''print(
						f'Index finger tip coordinates: (',
						f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
						f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
				)'''

				mp_drawing.draw_landmarks(
						image,
						hand_landmarks,
						mp_hands.HAND_CONNECTIONS,
						mp_drawing_styles.get_default_hand_landmarks_style(),
						mp_drawing_styles.get_default_hand_connections_style())
		# Flip the image horizontally for a selfie-view display.
		cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
		if cv2.waitKey(5) & 0xFF == 27:
			break
cap.release()