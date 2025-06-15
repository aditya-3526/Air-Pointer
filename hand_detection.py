import cv2
import mediapipe as mp

def detect_hands():
    
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    
    
    cap = cv2.VideoCapture(0)
        
    
    with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=1) as hands:
        
        while cap.isOpened():
            
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            
            frame = cv2.flip(frame, 1)
            
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
                    
                    
                    for id, lm in enumerate(hand_landmarks.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_PLAIN,
                                   1, (0, 255, 0), 1)
            
            
            cv2.putText(frame, "Press 'q' to quit", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            
            cv2.imshow('Hand Detection Test', frame)
            
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_hands()