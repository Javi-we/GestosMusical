import cv2
import mediapipe as mp
from src.config import INSTRUMENT_MAP, NOTE_MAP

class GestureDetector:
    def __init__(self, min_detection_confidence=0.75, min_tracking_confidence=0.75):
        """Inicializa el modelo de detección de manos de MediaPipe."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process_frame(self, frame_bgr):
        """Procesa una imagen BGR y devuelve los landmarks de las manos detectadas."""
        # MediaPipe utiliza imágenes en formato RGB
        rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb_frame)

    def count_fingers(self, hand_landmarks, hand_label):
        """
        Determina cuántos dedos de la mano están extendidos.
        Lógica especial para el pulgar dependiendo de si es mano izquierda o derecha.
        """
        fingers = []
        
        # Pulgar (Thumb): Landmark 4 (Tip), Landmark 3 (IP Joint)
        # MediaPipe clasifica las manos de forma absoluta ('Left' o 'Right')
        if hand_label == "Right":
            # Mano derecha: el pulgar extendido apunta a la izquierda (X menor)
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            # Mano izquierda: el pulgar extendido apunta a la derecha (X mayor)
            if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)
                
        # Dedos restantes: Índice (8), Medio (12), Anular (16), Meñique (20)
        # Comparación contra su nodo PIP de articulación correspondiente
        tips = [8, 12, 16, 20]
        joints = [6, 10, 14, 18]
        
        for tip, joint in zip(tips, joints):
            # En coordenadas OpenCV, Y aumenta hacia abajo.
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[joint].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers.count(1)

    def interpret_hands(self, results):
        """
        Interpreta los resultados y los estructura en un diccionario amigable.
        Identifica instrumentos (mano izquierda) y notas/volumen (mano derecha).
        """
        hands_state = {
            "left": {
                "present": False,
                "fingers": 0,
                "instrument": None,
                "landmarks": None
            },
            "right": {
                "present": False,
                "fingers": 0,
                "note": None,
                "wrist_y": None,
                "landmarks": None
            }
        }
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = handedness.classification[0].label  # "Left" o "Right"
                num_fingers = self.count_fingers(hand_landmarks, label)
                
                if label == "Left":
                    hands_state["left"]["present"] = True
                    hands_state["left"]["fingers"] = num_fingers
                    hands_state["left"]["instrument"] = INSTRUMENT_MAP.get(num_fingers)
                    hands_state["left"]["landmarks"] = hand_landmarks
                elif label == "Right":
                    hands_state["right"]["present"] = True
                    hands_state["right"]["fingers"] = num_fingers
                    hands_state["right"]["note"] = NOTE_MAP.get(num_fingers)
                    hands_state["right"]["wrist_y"] = hand_landmarks.landmark[0].y
                    hands_state["right"]["landmarks"] = hand_landmarks
                    
        return hands_state
