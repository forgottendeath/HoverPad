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

mouse = MouseController()
keyboard_sim = KeyboardController()
screen_width, screen_height = pyautogui.size()

with open('gesture_model.pkl', 'rb') as f:
    model = pickle.load(f)

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
tracker = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

prev_x, prev_y = 0, 0
smooth = 5
margin = 0.05  # Lowered margin so the mouse is more precise

is_left_clicking = False
is_right_clicking = False
action_cooldown = 0  
is_tracking = True  

# NEW: Anchor variables for swiping!
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
    5: "Mission Control (Surfer)"
}

print("--- SMART MOUSE V4 (ANCHOR SWIPES) ONLINE ---")

while True:
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = tracker.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        
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
            cv2.putText(frame, f"AI Sees: {gesture_names[gesture]}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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

            # --- THE ANCHOR LOGIC ---
            # If the gesture just changed THIS FRAME, drop the anchor!
            if gesture != prev_gesture:
                gesture_start_x = curr_x

            if gesture == 0: 
                mouse.position = (int(curr_x), int(curr_y))
                
            elif gesture == 1: 
                mouse.position = (int(curr_x), int(curr_y)) 
                if not is_left_clicking:
                    mouse.click(Button.left, 1)
                    is_left_clicking = True
                    
            elif gesture == 2: 
                if not is_right_clicking:
                    mouse.click(Button.right, 1)
                    is_right_clicking = True
                    
            elif gesture == 3: 
                if abs(dy) > 1.0: 
                    mouse.scroll(0, dy / 5.0)
                    
            elif gesture == 4: 
                if time.time() > action_cooldown:
                    # Calculate how far you moved from the Anchor Point (150 pixels)
                    swipe_distance = curr_x - gesture_start_x
                    
                    if swipe_distance > 150:  
                        print(">>> SWIPED RIGHT <<<")
                        os.system('''osascript -e 'tell application "System Events" to key code 124 using control down' ''')
                        action_cooldown = time.time() + 1.0 
                        gesture_start_x = curr_x # Reset the anchor so it doesn't double-trigger!
                        
                    elif swipe_distance < -150: 
                        print(">>> SWIPED LEFT <<<")
                        os.system('''osascript -e 'tell application "System Events" to key code 123 using control down' ''')
                        action_cooldown = time.time() + 1.0
                        gesture_start_x = curr_x
                        
            elif gesture == 5: 
                if time.time() > action_cooldown:
                    os.system('open -a "Mission Control"')
                    action_cooldown = time.time() + 2.0 

            if gesture != 1: is_left_clicking = False
            if gesture != 2: is_right_clicking = False
            
            prev_x, prev_y = curr_x, curr_y
            prev_gesture = gesture # Save the gesture for the next frame
            
        else:
            cv2.putText(frame, "PAUSED (Press Ctrl+Shift+H)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    small_frame = cv2.resize(frame, (400, 250)) 
    cv2.imshow("Hand Mouse", small_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()