import os
import wave
import struct
import math
import random

# Directorio de salida
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")

# Frecuencias de las notas musicales
# Do (C4), Re (D4), Mi (E4), Fa (F4), Sol (G4)
NOTE_FREQS = {
    "do": 261.63,
    "re": 293.66,
    "mi": 329.63,
    "fa": 349.23,
    "sol": 392.00
}

SAMPLE_RATE = 44100
DURATION = 1.2  # segundos por nota
NUM_SAMPLES = int(SAMPLE_RATE * DURATION)

def save_wav(filepath, samples):
    """Guarda una lista de valores float [-1.0, 1.0] en un archivo WAV de 16 bits mono."""
    with wave.open(filepath, 'w') as wav_file:
        nchannels = 1
        sampwidth = 2  # 16 bits = 2 bytes
        framerate = SAMPLE_RATE
        nframes = len(samples)
        
        # Configurar parámetros
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, "NONE", "not compressed"))
        
        for sample in samples:
            # Limitar y escalar a rango de enteros de 16 bits
            val = int(max(-32768, min(32767, sample * 32767)))
            wav_file.writeframesraw(struct.pack('<h', val))

def generate_piano(f):
    """Sintetiza un sonido similar a un piano usando armónicos y decaimiento exponencial."""
    samples = []
    tau = 0.35  # constante de tiempo de decaimiento
    for i in range(NUM_SAMPLES):
        t = i / SAMPLE_RATE
        # Mezcla de la frecuencia fundamental y armónicos superiores
        wave_val = (
            1.0 * math.sin(2 * math.pi * f * t) +
            0.5 * math.sin(2 * math.pi * 2 * f * t) +
            0.25 * math.sin(2 * math.pi * 3 * f * t) +
            0.1 * math.sin(2 * math.pi * 4 * f * t)
        )
        # Normalizar
        wave_val = wave_val / 1.85
        # Envolvente de volumen (decaimiento exponencial)
        envelope = math.exp(-t / tau)
        samples.append(wave_val * envelope)
    return samples

def generate_guitar(f):
    """Sintetiza una guitarra utilizando el algoritmo de Karplus-Strong (cuerda pulsada)."""
    N = int(SAMPLE_RATE / f)
    # Línea de retardo inicializada con ruido blanco aleatorio
    delay_line = [random.uniform(-1.0, 1.0) for _ in range(N)]
    samples = []
    decay = 0.996  # factor de atenuación por muestra
    ptr = 0
    
    # Envolvente de entrada/ataque rápida
    for i in range(NUM_SAMPLES):
        t = i / SAMPLE_RATE
        val = delay_line[ptr]
        samples.append(val)
        
        # Promedio del elemento actual y el siguiente en la línea de retardo (filtro de paso bajo)
        next_ptr = (ptr + 1) % N
        avg = 0.5 * (val + delay_line[next_ptr])
        
        # Retroalimentar amortiguado
        delay_line[ptr] = avg * decay
        ptr = next_ptr
        
    # Aplicar un pequeño fadeout al final para evitar clics
    fade_len = int(0.1 * SAMPLE_RATE)
    for i in range(fade_len):
        idx = NUM_SAMPLES - fade_len + i
        factor = (fade_len - i) / fade_len
        samples[idx] *= factor
        
    return samples

def generate_violin(f):
    """Sintetiza un violín utilizando una onda de sierra con vibrato y envolvente ADSR suave."""
    samples = []
    phase = 0.0
    
    # Parámetros del violín
    vibrato_freq = 5.5  # Hz
    vibrato_depth = 0.012  # profundidad de la variación de frecuencia
    
    # Tiempos de la envolvente
    attack_len = int(0.15 * SAMPLE_RATE)
    release_len = int(0.25 * SAMPLE_RATE)
    
    for i in range(NUM_SAMPLES):
        t = i / SAMPLE_RATE
        
        # Aplicar vibrato modulando la frecuencia
        inst_f = f * (1.0 + vibrato_depth * math.sin(2 * math.pi * vibrato_freq * t))
        phase += (2 * math.pi * inst_f) / SAMPLE_RATE
        
        # Onda de sierra (sawtooth) a partir de la fase acumulada
        normalized_phase = (phase % (2 * math.pi)) / (2 * math.pi)
        wave_val = 2.0 * normalized_phase - 1.0
        
        # Envolvente de volumen (ataque y relajación)
        if i < attack_len:
            env = i / attack_len
        elif i > NUM_SAMPLES - release_len:
            env = (NUM_SAMPLES - i) / release_len
        else:
            env = 1.0
            
        samples.append(wave_val * env)
        
    # Filtrar levemente con paso bajo para suavizar el sonido agudo de la sierra
    filtered = []
    prev = 0.0
    for s in samples:
        val = 0.25 * s + 0.75 * prev
        prev = val
        filtered.append(val)
        
    return filtered

def generate_drums(note_name):
    """Genera sonidos de batería correspondientes a 5 piezas de percusión distintas según la nota."""
    samples = []
    
    if note_name == "do":
        # Bombo (Kick Drum): Caída rápida de frecuencia y decaimiento rápido de amplitud
        phase = 0.0
        for i in range(NUM_SAMPLES):
            t = i / SAMPLE_RATE
            freq = 40.0 + 120.0 * math.exp(-70.0 * t)
            phase += (2 * math.pi * freq) / SAMPLE_RATE
            wave_val = math.sin(phase)
            env = math.exp(-18.0 * t)
            samples.append(wave_val * env)
            
    elif note_name == "re":
        # Tarola (Snare Drum): Mezcla de un tono fundamental y ruido blanco
        for i in range(NUM_SAMPLES):
            t = i / SAMPLE_RATE
            tone = math.sin(2 * math.pi * 180.0 * t) * math.exp(-35.0 * t)
            noise = random.uniform(-1.0, 1.0) * math.exp(-15.0 * t)
            val = 0.35 * tone + 0.65 * noise
            samples.append(val)
            
    elif note_name == "mi":
        # Platillo Cerrado (Closed Hi-Hat): Ruido filtrado con paso alto y decaimiento muy rápido
        prev = 0.0
        for i in range(NUM_SAMPLES):
            t = i / SAMPLE_RATE
            noise = random.uniform(-1.0, 1.0)
            # Filtro paso alto simple: y[n] = x[n] - x[n-1]
            hp_noise = noise - prev
            prev = noise
            env = math.exp(-95.0 * t)
            samples.append(hp_noise * 0.4 * env)
            
    elif note_name == "fa":
        # Platillo Abierto (Open Hi-Hat): Similar a cerrado pero con decaimiento más lento
        prev = 0.0
        for i in range(NUM_SAMPLES):
            t = i / SAMPLE_RATE
            noise = random.uniform(-1.0, 1.0)
            hp_noise = noise - prev
            prev = noise
            env = math.exp(-12.0 * t)
            samples.append(hp_noise * 0.35 * env)
            
    elif note_name == "sol":
        # Rimshot / Bloque de madera (Woodblock): Frecuencia alta con decaimiento percusivo rápido
        for i in range(NUM_SAMPLES):
            t = i / SAMPLE_RATE
            wave_val = math.sin(2 * math.pi * 850.0 * t)
            env = math.exp(-45.0 * t)
            samples.append(wave_val * env)
            
    return samples

def main():
    print("Iniciando generación de muestras de audio...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    instruments = ["piano", "guitar", "violin", "drums"]
    
    for inst in instruments:
        for note, freq in NOTE_FREQS.items():
            filename = f"{inst}_{note}.wav"
            filepath = os.path.join(OUTPUT_DIR, filename)
            print(f"Generando {filename}...", end="", flush=True)
            
            if inst == "piano":
                samples = generate_piano(freq)
            elif inst == "guitar":
                samples = generate_guitar(freq)
            elif inst == "violin":
                samples = generate_violin(freq)
            elif inst == "drums":
                samples = generate_drums(note)
                
            save_wav(filepath, samples)
            print(" [OK]")
            
    print("\n¡Generación de audio completada con éxito!")
    print(f"Archivos guardados en: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
