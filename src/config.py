import os

# Configuración de Rutas de Archivos
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Frecuencias de las notas musicales (Do, Re, Mi, Fa, Sol)
NOTE_FREQS = {
    "do": 261.63,
    "re": 293.66,
    "mi": 329.63,
    "fa": 349.23,
    "sol": 392.00
}

# Parámetros del Generador de Audio
SAMPLE_RATE = 44100
DURATION = 1.2  # Duración del audio en segundos

# Mapeos de dedos (gestos) a Instrumentos y Notas
INSTRUMENT_MAP = {
    1: "piano",
    2: "guitar",
    3: "violin",
    4: "drums"
}

NOTE_MAP = {
    1: "do",
    2: "re",
    3: "mi",
    4: "fa",
    5: "sol"
}

# Colores en formato BGR para la interfaz OpenCV
COLOR_LEFT = (255, 100, 0)   # Azul/Cian para mano izquierda (Instrumento)
COLOR_RIGHT = (0, 200, 100)  # Verde para mano derecha (Nota)
COLOR_TEXT = (255, 255, 255) # Blanco para textos generales
COLOR_BG = (30, 30, 30)      # Gris oscuro para el fondo de paneles
