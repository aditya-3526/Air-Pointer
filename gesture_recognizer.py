import numpy as np

class GestureRecognizer:
    def __init__(self):
        # Thresholds
        self.pinch_threshold = 0.05
        self.click_debounce_frames = 7
        self.scroll_debounce_frames = 7
        
        # State variables
        self.pinch_active = False
        self.pinch_counter = 0
        self.scroll_active = False
        self.scroll_counter = 0

    def get_landmark_coords(self, hand_landmarks):
        """Convert landmarks to numpy array"""
        return np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])

    def distance(self, point1, point2):
        """Euclidean distance between two points"""
        return np.sqrt(np.sum((point1 - point2) ** 2))

    def is_index_pointing(self, landmarks):
        """Index up, others down"""
        return (landmarks[8][1] < landmarks[6][1] and  # Index
                landmarks[12][1] > landmarks[10][1] and  # Middle
                landmarks[16][1] > landmarks[14][1] and  # Ring
                landmarks[20][1] > landmarks[18][1])     # Pinky

    def is_pinch_gesture(self, landmarks):
        """Thumb tip close to index tip"""
        distance = self.distance(landmarks[4], landmarks[8])
        if distance < self.pinch_threshold:
            self.pinch_counter += 1
            if self.pinch_counter >= self.click_debounce_frames:
                if not self.pinch_active:
                    self.pinch_active = True
                    return True
        else:
            self.pinch_active = False
            self.pinch_counter = 0
        return False

    def is_open_palm(self, landmarks):
        """All fingers extended (for lifting pen)"""
        return (landmarks[8][1] < landmarks[6][1] and   # Index
                landmarks[12][1] < landmarks[10][1] and  # Middle
                landmarks[16][1] < landmarks[14][1] and  # Ring
                landmarks[20][1] < landmarks[18][1])     # Pinky

    def is_scroll_gesture(self, landmarks):
        """Index+middle extended, others curled"""
        return (landmarks[8][1] < landmarks[6][1] and   # Index
                landmarks[12][1] < landmarks[10][1] and  # Middle
                landmarks[16][1] > landmarks[14][1] and  # Ring
                landmarks[20][1] > landmarks[18][1])    # Pinky