import os
import pygame
from src.config import AUDIO_DIR, INSTRUMENT_MAP, NOTE_MAP

class AudioPlayer:
    def __init__(self):
        """Inicializa Pygame Mixer y precarga todas las muestras de audio."""
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        self.sounds = {}
        self.active_channel = None
        self._load_sounds()

    def _load_sounds(self):
        """Carga en memoria todos los archivos de audio .wav del directorio configurado."""
        instruments = set(INSTRUMENT_MAP.values())
        notes = set(NOTE_MAP.values())
        
        print("Cargando archivos de audio...")
        missing_files = []
        
        for inst in instruments:
            self.sounds[inst] = {}
            for note in notes:
                filename = f"{inst}_{note}.wav"
                filepath = os.path.join(AUDIO_DIR, filename)
                if os.path.exists(filepath):
                    try:
                        self.sounds[inst][note] = pygame.mixer.Sound(filepath)
                    except Exception as e:
                        print(f"Error al cargar la muestra {filename}: {e}")
                else:
                    missing_files.append(filename)
                    
        if missing_files:
            print(f"Advertencia: Faltan archivos de audio: {missing_files}")
            print("Por favor, ejecuta 'python audio_generator.py' para crearlos.")
        else:
            print("¡Todos los archivos de audio se cargaron con éxito!")

    def play_sound(self, instrument, note, initial_volume=1.0):
        """Reproduce una muestra de audio específica con un volumen inicial y almacena el canal."""
        if instrument in self.sounds and note in self.sounds[instrument]:
            try:
                channel = self.sounds[instrument][note].play()
                if channel:
                    channel.set_volume(initial_volume)
                    print(f"[PLAY] {instrument.upper()} - {note.upper()} | Vol: {initial_volume:.2f}")
                    self.active_channel = channel
                    return channel
            except Exception as e:
                print(f"Error al reproducir sonido: {e}")
        return None

    def update_volume(self, volume):
        """Actualiza dinámicamente el volumen del canal activo en reproducción."""
        if self.active_channel and self.active_channel.get_busy():
            self.active_channel.set_volume(volume)

    def close(self):
        """Libera los recursos del mezclador de audio."""
        pygame.mixer.quit()
