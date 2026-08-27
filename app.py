import cv2
from src.config import NOTE_MAP, INSTRUMENT_MAP
from src.audio_player import AudioPlayer
from src.gesture_detector import GestureDetector
from src.gui_renderer import draw_hand_overlay, draw_hud

def main():
    # Inicializar captura de video
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara web.")
        return

    # Inicializar componentes modulares
    player = AudioPlayer()
    detector = GestureDetector()

    print("\n=== SINTETIZADOR MUSICAL POR GESTOS (MODULAR) ===")
    print("Instrucciones:")
    print("- Mano IZQUIERDA (Instrumento): 1=Piano, 2=Guitarra, 3=Violín, 4=Batería")
    print("- Mano DERECHA (Nota): 1=Do, 2=Re, 3=Mi, 4=Fa, 5=Sol")
    print("- Mueve la mano derecha verticalmente para regular el volumen de la nota.")
    print("- Cierra la mano (0 dedos) y ábrela de nuevo para repetir una nota.")
    print("- Presiona 'Q' en la ventana de video para salir.\n")

    # Registro de estados para evitar repeticiones de notas innecesarias
    last_instrument = None
    last_note = None

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # 1. Espejar la imagen horizontalmente para interacción intuitiva
        frame = cv2.flip(frame, 1)
        
        # 2. Procesar el frame con MediaPipe
        results = detector.process_frame(frame)
        hands_state = detector.interpret_hands(results)

        # Extraer variables del estado de las manos
        left = hands_state["left"]
        right = hands_state["right"]

        # Dibujar esqueletos y textos de guía sobre las manos detectadas
        if left["present"]:
            detail = f"INSTRUMENTO: {left['instrument'].upper() if left['instrument'] else '...'}"
            draw_hand_overlay(frame, left["landmarks"], "Left", left["fingers"], detail)
            
        if right["present"]:
            detail = f"NOTA: {right['note'].upper() if right['note'] else '...'}"
            draw_hand_overlay(frame, right["landmarks"], "Right", right["fingers"], detail)

        # Calcular volumen basado en la altura Y de la mano derecha [0.25, 0.75] -> [1.0, 0.0]
        current_volume = 0.8
        if right["present"] and right["wrist_y"] is not None:
            raw_vol = (0.75 - right["wrist_y"]) / 0.5
            current_volume = max(0.0, min(1.0, raw_vol))

        # 3. Lógica de Disparo (Trigger) para los sonidos
        if left["instrument"] and right["note"]:
            if left["instrument"] != last_instrument or right["note"] != last_note:
                player.play_sound(left["instrument"], right["note"], initial_volume=current_volume)
                last_instrument = left["instrument"]
                last_note = right["note"]
        else:
            # Reseteo de estados si soltamos el gesto
            if not right["note"]:
                last_note = None
            if not left["instrument"]:
                last_instrument = None

        # Actualizar volumen del canal activo en tiempo real
        player.update_volume(current_volume)

        # 4. Dibujar Interfaz de Usuario / Panel Superior y HUD
        draw_hud(frame, last_instrument, last_note, current_volume, right["present"], left["present"])

        # Mostrar el frame procesado en la ventana
        cv2.imshow('Sintetizador por Gestos', frame)

        # Salir al presionar 'q' o 'Q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    player.close()
    print("Aplicación cerrada correctamente.")

if __name__ == "__main__":
    main()
