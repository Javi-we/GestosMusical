import cv2
import mediapipe as mp
from src.config import (
    COLOR_LEFT, COLOR_RIGHT, COLOR_TEXT, COLOR_BG
)

# Inicializar Drawing Utils de MediaPipe
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def draw_instrument_icon(img, instrument, x, y, size=60):
    """Dibuja un icono vectorial estilizado en pantalla basado en el instrumento activo."""
    # Fondo del icono
    cv2.rectangle(img, (x, y), (x + size, y + size), (50, 50, 50), -1)
    cv2.rectangle(img, (x, y), (x + size, y + size), (150, 150, 150), 1)
    
    center_x = x + size // 2
    center_y = y + size // 2
    
    if instrument == "piano":
        # Teclado de Piano
        ky_start = y + size // 4
        ky_end = y + (3 * size) // 4
        kx_start = x + 8
        kx_end = x + size - 8
        
        # Fondo blanco para teclas
        cv2.rectangle(img, (kx_start, ky_start), (kx_end, ky_end), (255, 255, 255), -1)
        
        # Líneas divisorias de teclas blancas (5 teclas blancas)
        width_k = (kx_end - kx_start) // 5
        for i in range(1, 5):
            cv2.line(img, (kx_start + i * width_k, ky_start), (kx_start + i * width_k, ky_end), (0, 0, 0), 1)
            
        # Teclas negras (3 teclas negras en posiciones específicas)
        black_w = max(2, width_k // 2)
        black_h = (ky_end - ky_start) // 2
        for i in [1, 2, 4]:
            bx = kx_start + i * width_k - black_w // 2
            cv2.rectangle(img, (bx, ky_start), (bx + black_w, ky_start + black_h), (0, 0, 0), -1)
            
    elif instrument == "guitar":
        # Cuerpo y mástil de la Guitarra (Marrón y Celeste)
        # Mástil (línea gruesa diagonal)
        cv2.line(img, (x + 12, y + size - 12), (x + size - 15, y + 15), (100, 150, 200), 3)
        # Cuerpo (Elipse marrón)
        cv2.ellipse(img, (x + size - 18, y + size - 18), (12, 9), -45, 0, 360, (30, 60, 140), -1)
        # Agujero de sonido
        cv2.circle(img, (x + size - 18, y + size - 18), 3, (0, 0, 0), -1)
        # Clavijero
        cv2.circle(img, (x + 10, y + 10), 3, (100, 150, 200), -1)
        
    elif instrument == "violin":
        # Violín (doble elipse y arco)
        # Cuerpo
        cv2.ellipse(img, (x + 18, y + size - 18), (11, 7), 45, 0, 360, (20, 45, 110), -1)
        cv2.ellipse(img, (x + 28, y + size - 28), (8, 5), 45, 0, 360, (20, 45, 110), -1)
        # Mástil
        cv2.line(img, (x + 12, y + size - 12), (x + size - 15, y + 15), (20, 20, 20), 2)
        # Arco (Línea gris muy fina diagonal cruzando)
        cv2.line(img, (x + 10, y + 22), (x + size - 10, y + size - 12), (220, 220, 220), 1)
        
    elif instrument == "drums":
        # Tambor de Batería con baquetas cruzadas
        # Cuerpo azul/rojo
        cv2.rectangle(img, (x + 12, y + 24), (x + size - 12, y + size - 14), (180, 50, 50), -1)
        # Parche / Aro superior (elipse gris y blanca)
        cv2.ellipse(img, (center_x, y + 24), (size // 2 - 12, 5), 0, 0, 360, (200, 200, 200), -1)
        cv2.ellipse(img, (center_x, y + 24), (size // 2 - 14, 3), 0, 0, 360, (240, 240, 240), -1)
        # Baquetas cruzadas (amarillas/madera)
        cv2.line(img, (x + 6, y + 12), (x + size - 16, y + 26), (50, 200, 240), 2)
        cv2.line(img, (x + size - 6, y + 12), (x + 16, y + 26), (50, 200, 240), 2)
        
    else:
        # Signo de interrogación cuando no hay instrumento seleccionado
        cv2.putText(img, "?", (center_x - 8, center_y + 9), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (150, 150, 150), 2)

def draw_hand_overlay(frame, hand_landmarks, hand_label, count, detail_text):
    """Dibuja el esqueleto de la mano en pantalla y su texto informativo."""
    w, h = frame.shape[1], frame.shape[0]
    
    # Determinar color según lateralidad
    color = COLOR_RIGHT if hand_label == "Right" else COLOR_LEFT
    label_es = "Mano Der (Nota)" if hand_label == "Right" else "Mano Izq (Inst)"
    
    # Dibujar esqueleto MediaPipe
    mp_draw.draw_landmarks(
        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
        mp_draw.DrawingSpec(color=color, thickness=2, circle_radius=2),
        mp_draw.DrawingSpec(color=COLOR_TEXT, thickness=2)
    )
    
    # Colocar texto informativo sobre la muñeca
    wrist = hand_landmarks.landmark[0]
    cx, cy = int(wrist.x * w), int(wrist.y * h)
    
    cv2.putText(frame, label_es, (cx - 80, cy + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, f"Dedos: {count}", (cx - 80, cy + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
    cv2.putText(frame, detail_text, (cx - 80, cy + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

def draw_hud(frame, last_instrument, last_note, current_volume, right_hand_present, left_hand_present):
    """Renderiza toda la interfaz de usuario en pantalla (HUD)."""
    w, h = frame.shape[1], frame.shape[0]
    
    # 1. Barra de estado superior
    cv2.rectangle(frame, (0, 0), (w, 80), COLOR_BG, -1)
    
    # Dibujar el Icono del Instrumento
    draw_instrument_icon(frame, last_instrument, 20, 10, 60)
    
    # Etiquetas de Instrumento y Nota
    inst_text = f"Inst: {last_instrument.upper() if last_instrument else 'NINGUNO'}"
    cv2.putText(frame, inst_text, (95, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_LEFT, 2)
    
    note_text = f"Nota: {last_note.upper() if last_note else 'NINGUNA'}"
    cv2.putText(frame, note_text, (300, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_RIGHT, 2)
    
    # Instrucciones rápidas
    cv2.putText(frame, "Teclas: [Q] Salir | Izq = Inst (1-4) | Der = Nota (1-5) + Altura (Vol)", 
                (95, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_TEXT, 1)
    
    status_text = "Sube/baja mano Der para volumen"
    cv2.putText(frame, status_text, (w - 320, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
    
    # Indicador de detección activo (Círculo Verde/Rojo)
    any_hand = left_hand_present or right_hand_present
    cv2.circle(frame, (w - 20, 60), 6, (0, 255, 0) if any_hand else (0, 0, 255), -1)

    # 2. Barra lateral de volumen (si la mano de nota está en pantalla)
    if right_hand_present:
        bar_x = w - 40
        bar_y_start = 120
        bar_y_end = 360
        bar_height = bar_y_end - bar_y_start
        
        # Fondo (Gris)
        cv2.rectangle(frame, (bar_x, bar_y_start), (bar_x + 15, bar_y_end), (60, 60, 60), -1)
        # Relleno de volumen
        fill_y = int(bar_y_end - (current_volume * bar_height))
        cv2.rectangle(frame, (bar_x, fill_y), (bar_x + 15, bar_y_end), COLOR_RIGHT, -1)
        # Borde blanco
        cv2.rectangle(frame, (bar_x, bar_y_start), (bar_x + 15, bar_y_end), COLOR_TEXT, 1)
        
        # Porcentaje del volumen
        pct = int(current_volume * 100)
        cv2.putText(frame, f"{pct}%", (bar_x - 45, fill_y + 5 if fill_y < bar_y_end - 10 else bar_y_end - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXT, 1)
        cv2.putText(frame, "VOL", (bar_x - 8, bar_y_start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_RIGHT, 1)
