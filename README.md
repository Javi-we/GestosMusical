# Sintetizador Musical por Gestos en Tiempo Real

Este proyecto consiste en una aplicación interactiva que utiliza la cámara del dispositivo para interpretar gestos de las manos en tiempo real y reproducir notas musicales con diferentes instrumentos.

## Requisitos Previos

Las dependencias principales ya están instaladas en tu entorno:
- **Python 3.11+**
- **OpenCV** (para la captura y procesamiento de video)
- **MediaPipe** (para la detección y seguimiento de landmarks de las manos)
- **Pygame** (para la mezcla y reproducción de audio de baja latencia)

## Estructura del Proyecto

El código está organizado de manera modular en las siguientes carpetas y archivos:
```text
gesture_synth/
├── audio/                   # Muestras generadas (.wav)
├── src/                     # Código fuente modular
│   ├── __init__.py          # Define la carpeta como paquete Python
│   ├── config.py            # Constantes, colores y mapeo de gestos
│   ├── audio_player.py      # Gestión y reproducción de audio (Pygame)
│   ├── gesture_detector.py  # Detección y conteo de dedos (MediaPipe)
│   └── gui_renderer.py      # Dibujo de HUD, volumen e iconos vectoriales
├── audio_generator.py       # Generador de sonidos matemáticos
├── app.py                   # Orquestador y punto de entrada principal
└── README.md                # Esta guía de usuario
```

## Cómo Ejecutar la Aplicación

1. **Generar los Archivos de Audio (Opcional, ya completado):**
   Si necesitas regenerar las muestras de audio sintéticas, corre:
   ```bash
   python audio_generator.py
   ```
   Esto creará o actualizará la carpeta `audio/` con 20 archivos `.wav` correspondientes a las combinaciones de instrumentos y notas.

2. **Iniciar la Aplicación Principal:**
   Ejecuta el siguiente comando para abrir el sintetizador por cámara:
   ```bash
   python app.py
   ```

## Cómo Jugar y Controlar los Instrumentos

La aplicación detecta las dos manos de manera independiente frente a la cámara web. Asegúrate de tener una buena iluminación.

### 1. Mano Izquierda (Selección de Instrumento)
Muestra tu mano izquierda a la pantalla y extiende los dedos para elegir el instrumento musical:
- 🖐️ **1 dedo extendido:** Piano 🎹
- 🖐️ **2 dedos extendidos:** Guitarra 🎸
- 🖐️ **3 dedos extendidos:** Violín 🎻
- 🖐️ **4 dedos extendidos:** Batería (Percusión) 🥁

### 2. Mano Derecha (Selección, Reproducción y Volumen)
Muestra tu mano derecha a la pantalla:
- **Notas (dedos extendidos):**
  - 🖐️ **1 dedo extendido:** Do (C4)
  - 🖐️ **2 dedos extendidos:** Re (D4)
  - 🖐️ **3 dedos extendidos:** Mi (E4)
  - 🖐️ **4 dedos extendidos:** Fa (F4)
  - 🖐️ **5 dedos extendidos:** Sol (G4)
- **Volumen (posición vertical):**
  - **Sube la mano** (hacia la parte superior de la pantalla) para aumentar el volumen.
  - **Baja la mano** (hacia la parte inferior de la pantalla) para atenuar o silenciar la nota.
  - La barra de volumen verde en el extremo derecho de la pantalla te dará retroalimentación visual en tiempo real.

---

### 💡 Tips para una mejor experiencia:
- **Iconos Visuales:** En la esquina superior izquierda verás un icono dibujado en tiempo real que cambiará según el instrumento seleccionado (un piano 🎹, una guitarra 🎸, un violín 🎻 o una batería 🥁). Si no hay mano izquierda detectada, se mostrará un signo de interrogación `?`.
- **Disparo único:** La aplicación está diseñada para que la nota suene una sola vez cuando haces el gesto (evitando que se repita 30 veces por segundo).
- **Repetición de nota (Plucking):** Para volver a tocar la misma nota, simplemente **cierra tu mano derecha (0 dedos)** y vuelve a hacer el gesto. Esto actúa como un gatillo o "plucking" de la cuerda.
- **Transición rápida:** Puedes cambiar de nota directamente levantando más o menos dedos (por ejemplo, pasar de 1 dedo a 3 dedos) y la nueva nota se disparará inmediatamente.
- **Salir:** Presiona la tecla **`Q`** en tu teclado con la ventana del video activa para cerrar el programa de forma segura.
