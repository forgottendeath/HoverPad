import cv2
import mediapipe as mp
import pyautogui
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
from pynput import keyboard
import pickle
import time
import os
import math 
import platform

CURRENT_OS = platform.system()

mouse = MouseController()
keyboard_sim = KeyboardController()
screen_width, screen_height = pyautogui.size()

# Ensure it always finds the model regardless of where the terminal is opened
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'gesture_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
tracker = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

prev_x, prev_y = 0, 0
smooth = 5
margin = 0.05

is_left_clicking = False
is_right_clicking = False
action_cooldown = 0  
is_tracking = True  
prev_gesture = -1
gesture_start_x = 0

def toggle_tracking():
    global is_tracking
    is_tracking = not is_tracking

listener = keyboard.GlobalHotKeys({'<ctrl>+<shift>+h': toggle_tracking})
listener.start()

gesture_names = {
    0: "Move (Open Hand)", 
    1: "Left Click (OK Sign)", 
    2: "Right Click (Fist)", 
    3: "Scroll (Peace)", 
    4: "Desktops (Thumbs Up)", 
    5: "Mission Control / Task View (Surfer)"
}

print("--- SMART MOUSE V6 (DRAG SUPPORT + CRASH SAFE) ONLINE ---")

try:
    while True:
        success, frame = cap.read()
        if not success: break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tracker.process(rgb_frame)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            
            cam_h, cam_w, _ = frame.shape
            box_x1, box_y1 = int(margin * cam_w), int(margin * cam_h)
            box_x2, box_y2 = int((1 - margin) * cam_w), int((1 - margin) * cam_h)
            cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (255, 0, 255), 2)
            
            if is_tracking:
                wrist_x = hand.landmark[0].x
                wrist_y = hand.landmark[0].y
                wrist_z = hand.landmark[0].z
                
                scale = math.hypot(hand.landmark[9].x - wrist_x, hand.landmark[9].y - wrist_y)
                if scale == 0: scale = 0.0001
                
                row = []
                for lm in hand.landmark:
                    row.extend([(lm.x - wrist_x) / scale, (lm.y - wrist_y) / scale, (lm.z - wrist_z) / scale])
                    
                gesture = model.predict([row])[0]
                cv2.putText(frame, f"AI Sees: {gesture_names.get(gesture, 'Unknown')}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                index_finger_tip = hand.landmark[8]
                x_percentage = max(0.0, min(1.0, (index_finger_tip.x - margin) / (1.0 - margin * 2)))
                y_percentage = max(0.0, min(1.0, (index_finger_tip.y - margin) / (1.0 - margin * 2)))

                target_x = x_percentage * screen_width
                target_y = y_percentage * screen_height
                
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = target_x, target_y
                    
                curr_x = prev_x + (target_x - prev_x) / smooth
                curr_y = prev_y + (target_y - prev_y) / smooth
                
                dy = prev_y - curr_y 

                if gesture != prev_gesture:
                    gesture_start_x = curr_x

                if gesture == 0: 
                    mouse.position = (int(curr_x), int(curr_y))
                    
                elif gesture == 1: 
                    mouse.position = (int(curr_x), int(curr_y)) 
                    if not is_left_clicking:
                        mouse.press(Button.left) # FIX: Holds the click down so you can drag!
                        is_left_clicking = True
                        
                elif gesture == 2: 
                    if not is_right_clicking:
                        mouse.click(Button.right, 1) # Right click doesn't need to drag
                        is_right_clicking = True
                        
                elif gesture == 3: 
                    if abs(dy) > 1.0: 
                        mouse.scroll(0, dy / 5.0)
                        
                elif gesture == 4: 
                    if time.time() > action_cooldown:
                        swipe_distance = curr_x - gesture_start_x
                        if swipe_distance > 150:  
                            if CURRENT_OS == "Darwin":
                                os.system('''osascript -e 'tell application "System Events" to key code 124 using control down' ''')
                            elif CURRENT_OS == "Windows":
                                pyautogui.hotkey('ctrl', 'win', 'right')
                            action_cooldown = time.time() + 1.0 
                            gesture_start_x = curr_x
                        elif swipe_distance < -150: 
                            if CURRENT_OS == "Darwin":
                                os.system('''osascript -e 'tell application "System Events" to key code 123 using control down' ''')
                            elif CURRENT_OS == "Windows":
                                pyautogui.hotkey('ctrl', 'win', 'left')
                            action_cooldown = time.time() + 1.0
                            gesture_start_x = curr_x
                            
                elif gesture == 5: 
                    if time.time() > action_cooldown:
                        if CURRENT_OS == "Darwin":
                            os.system('open -a "Mission Control"')
                        elif CURRENT_OS == "Windows":
                            pyautogui.hotkey('win', 'tab')
                        action_cooldown = time.time() + 2.0 

                # FIX: Release the mouse when you stop making the OK Sign!
                if gesture != 1 and is_left_clicking:
                    mouse.release(Button.left)
                    is_left_clicking = False
                    
                if gesture != 2 and is_right_clicking:
                    is_right_clicking = False
                
                prev_x, prev_y = curr_x, curr_y
                prev_gesture = gesture
                
            else:
                cv2.putText(frame, "PAUSED (Press Ctrl+Shift+H)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        small_frame = cv2.resize(frame, (400, 250)) 
        cv2.imshow("Hand Mouse", small_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

# FIX: No matter how it crashes, turn off the webcam!
finally:
    cap.release()
    cv2.destroyAllWindows()
