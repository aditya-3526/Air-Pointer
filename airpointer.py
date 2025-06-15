import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
from gesture_recognizer import GestureRecognizer

class AirPointer:
    def __init__(self):
        # Configuration
        pyautogui.FAILSAFE = False
        self.screen_width, self.screen_height = pyautogui.size()
        
        # MediaPipe Hand Tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            max_num_hands=1)
        
        # Drawing Canvas Setup
        self.canvas = np.zeros((720, 1280, 3), dtype=np.uint8)  # Black canvas
        self.drawing_mode = False
        self.prev_drawing_point = None
        self.drawing_color = (0, 255, 0)  # Green
        self.brush_size = 5
        
        # Cursor Control
        self.gesture_recognizer = GestureRecognizer()
        self.smoothing_factor = 0.5
        self.prev_x, self.prev_y = 0, 0
        self.prev_landmarks = None
        self.last_click_time = 0
        self.click_cooldown = 0.3  # seconds

    def toggle_drawing_mode(self):
        """Switch between cursor and drawing modes"""
        self.drawing_mode = not self.drawing_mode
        self.prev_drawing_point = None  # Reset drawing point
        if not self.drawing_mode:
            self.canvas = np.zeros((720, 1280, 3), dtype=np.uint8)  # Clear canvas

    def draw_on_canvas(self, x, y):
        """Draw continuous line on canvas"""
        if self.prev_drawing_point:
            cv2.line(self.canvas, self.prev_drawing_point, (x, y), 
                    self.drawing_color, self.brush_size)
        self.prev_drawing_point = (x, y)

    def smooth_position(self, x, y):
        """Apply smoothing to cursor/drawing position"""
        smoothed_x = self.prev_x + self.smoothing_factor * (x - self.prev_x)
        smoothed_y = self.prev_y + self.smoothing_factor * (y - self.prev_y)
        self.prev_x, self.prev_y = smoothed_x, smoothed_y
        return int(smoothed_x), int(smoothed_y)

    def map_to_screen(self, x, y):
        """Convert normalized coordinates to screen pixels"""
        return int(x * self.screen_width), int(y * self.screen_height)

    def display_ui(self, frame, action):
        """Show status information on screen"""
        h, w = frame.shape[:2]
        
        # Action label
        cv2.putText(frame, action, (20, h - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Mode indicator
        mode_text = "DRAW MODE (Open palm to lift pen)" if self.drawing_mode \
                  else "POINTER MODE (Pinch to click)"
        cv2.putText(frame, mode_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        
        # Help text
        cv2.putText(frame, "'d' to toggle modes | 'c' to clear | 'q' to quit", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        print("AirPointer is running!")
        print("- Press 'd' to toggle drawing mode")
        print("- Open palm 🤚 to lift pen (draw mode)")
        print("- Pinch 🤏 to click (pointer mode)")
        print("- Two fingers ✌️ to scroll")
        print("- Press 'c' to clear canvas")
        print("- Press 'q' to quit")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Flip and process frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            action_text = "No hand detected"
            
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                landmarks = self.gesture_recognizer.get_landmark_coords(hand_landmarks)
                
                # Draw hand landmarks
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
                    mp.solutions.drawing_styles.get_default_hand_connections_style())
                
                # Get index finger tip coordinates
                index_tip = hand_landmarks.landmark[8]
                x, y = self.map_to_screen(index_tip.x, index_tip.y)
                x, y = self.smooth_position(x, y)
                
                if self.drawing_mode:
                    # Air Drawing Logic
                    if self.gesture_recognizer.is_open_palm(landmarks):
                        self.prev_drawing_point = None  # Lift pen
                        action_text = "Pen lifted (open palm)"
                    elif self.gesture_recognizer.is_index_pointing(landmarks):
                        self.draw_on_canvas(x, y)
                        action_text = "Drawing"
                else:
                    # Pointer Mode Logic
                    pyautogui.moveTo(x, y)
                    action_text = "Moving cursor"
                    
                    # Click on pinch (with cooldown)
                    current_time = time.time()
                    if (self.gesture_recognizer.is_pinch_gesture(landmarks) and 
                        current_time - self.last_click_time > self.click_cooldown):
                        pyautogui.click()
                        action_text = "Click (pinch)"
                        self.last_click_time = current_time
                    
                    # Scroll gesture
                    if self.gesture_recognizer.is_scroll_gesture(landmarks):
                        if self.prev_landmarks is not None:
                            scroll_amount = landmarks[12][1] - self.prev_landmarks[12][1]
                            if abs(scroll_amount) > 0.01:
                                pyautogui.scroll(int(-scroll_amount * 20))
                                action_text = "Scrolling"
                
                self.prev_landmarks = landmarks

            # Blend canvas with camera feed (semi-transparent)
            resized_canvas = cv2.resize(self.canvas, (frame.shape[1], frame.shape[0]))
            frame = cv2.addWeighted(frame, 0.8, resized_canvas, 0.2, 0)
            
            # Display UI
            self.display_ui(frame, action_text)
            cv2.imshow('AirPointer', frame)
            
            # Key controls
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                break
            elif key & 0xFF == ord('d'):
                self.toggle_drawing_mode()
            elif key & 0xFF == ord('c') and self.drawing_mode:  # Clear canvas
                self.canvas = np.zeros((720, 1280, 3), dtype=np.uint8)

        cap.release()
        cv2.destroyAllWindows()
        print("AirPointer session ended.")