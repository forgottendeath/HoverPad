import cv2
import mediapipe as mp
import csv
import math

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
tracker = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

csv_file = open('gesture_data.csv', 'a', newline='')
writer = csv.writer(csv_file)

print("--- V2 ANTI-HALLUCINATION COLLECTOR ---")
print("Press '0' -> Open Hand (Move)")
print("Press '1' -> OK Sign (Left Click)")
print("Press '2' -> Fist (Right Click)")
print("Press '3' -> Peace Sign (Scroll)")
print("Press '4' -> Thumbs Up (Desktops)")
print("Press '5' -> Surfer Sign (Mission Control)")
print("Press 'q' -> Quit and Save")

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = tracker.process(rgb_frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        
        if key in [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            wrist_x = hand.landmark[0].x
            wrist_y = hand.landmark[0].y
            wrist_z = hand.landmark[0].z
            
            # THE MAGIC SCALE MATH!
            scale = math.hypot(hand.landmark[9].x - wrist_x, hand.landmark[9].y - wrist_y)
            if scale == 0: scale = 0.0001
            
            row = []
            if key == ord('0'): row.append(0); print("0 - Move")
            elif key == ord('1'): row.append(1); print("1 - Left Click")
            elif key == ord('2'): row.append(2); print("2 - Right Click")
            elif key == ord('3'): row.append(3); print("3 - Scroll")
            elif key == ord('4'): row.append(4); print("4 - Desktops")
            elif key == ord('5'): row.append(5); print("5 - Mission Control")
                
            for lm in hand.landmark:
                # Divide by scale so the model understands distance!
                row.append((lm.x - wrist_x) / scale)
                row.append((lm.y - wrist_y) / scale)
                row.append((lm.z - wrist_z) / scale)
                
            writer.writerow(row)
            
    cv2.imshow("Data Collector", frame)

csv_file.close()
cap.release()
cv2.destroyAllWindows()