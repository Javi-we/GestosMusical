# Sintetizador Musical Controlado por Gestos en Tiempo Real

Este proyecto es una aplicación interactiva que transforma la cámara web de tu computadora en un sintetizador de música inteligente. Utiliza visión artificial para reconocer los gestos de tus manos en tiempo real, permitiéndote seleccionar instrumentos con la mano izquierda, tocar notas con la mano derecha y controlar la expresión/volumen de cada nota moviéndola verticalmente.

---

## 🚀 Características Principales

*   **Detección Bi-Manual en Tiempo Real:** Seguimiento de landmarks y articulaciones mediante MediaPipe Hands.
*   **4 Instrumentos Sintetizados:** Piano, Guitarra acústica (Karplus-Strong), Violín (con vibrato) y Batería (5 piezas de percusión).
*   **Expresión Dinámica (Volumen):** Control del volumen en tiempo real basado en la altura física de tu mano derecha (eje vertical Y).
*   **Lógica de Disparo Inteligente (Trigger):** Evita la reproducción repetitiva y molesta; la nota se dispara una sola vez y se puede re-disparar cerrando y abriendo la mano ("plucking").
*   **Mapeo de Audio Sintético Autónomo:** No requiere descargas de sonidos externos; incluye un generador que crea muestras matemáticas en formato `.wav` de 16 bits.
*   **Interfaz HUD Interactiva:** Visualización del esqueleto de las manos, barra gráfica de volumen y elegantes iconos vectoriales dinámicos para los instrumentos.

---

## 📂 Estructura del Proyecto

El código está estructurado de manera modular siguiendo buenas prácticas de desarrollo:

```text
gesture_synth/
├── audio/                   # Almacena las muestras de audio generadas (.wav)
├── src/                     # Código fuente del módulo de control
│   ├── __init__.py          # Define la carpeta como paquete de Python
│   ├── config.py            # Constantes globales, colores BGR y mapeos de gestos
│   ├── audio_player.py      # Gestor de Pygame Mixer (reproducción y volumen continuo)
│   ├── gesture_detector.py  # Pipeline de MediaPipe (análisis de manos y conteo de dedos)
│   └── gui_renderer.py      # Dibujo HUD, esqueletos e iconos vectoriales interactivos
├── audio_generator.py       # Sintetiza matemáticamente los archivos .wav
├── app.py                   # Orquestador del bucle principal y cámara (Punto de entrada)
└── README.md                # Esta documentación detallada
```

---

## 🛠️ Requisitos e Instalación

### 1. Requisitos del Sistema
*   **Python 3.11** o superior.
*   Una cámara web integrada o externa.
*   Altavoces o auriculares conectados.

### 2. Instalación de Dependencias
Asegúrate de instalar las librerías necesarias mediante tu consola de comandos:
```bash
pip install opencv-python mediapipe pygame
```

---

## 🎹 Guía de Uso y Control Gestual

La aplicación divide la pantalla en dos zonas lógicas basadas en la lateralidad absoluta de tus manos detectada por MediaPipe (en modo espejo):

| Mano | Función Principal | Control Adicional |
| :--- | :--- | :--- |
| **Mano Izquierda** | **Seleccionar Instrumento** | Gestos del 1 al 4 (dedos extendidos) |
| **Mano Derecha** | **Disparar / Tocar Nota** | Gestos del 1 al 5 (dedos extendidos) |
| **Mano Derecha (Altura)** | **Control de Volumen** | Movimiento vertical (Arriba = Fuerte, Abajo = Suave) |

### 1. Gestos de la Mano Izquierda (Instrumentos)
Extiende los dedos correspondientes de tu mano izquierda para cambiar el timbre de la música:

*   🖐️ **1 dedo:** **Piano** 🎹 (Timbre clásico con decaimiento exponencial).
*   🖐️ **2 dedos:** **Guitarra** 🎸 (Simulación física de cuerda pulsada mediante Karplus-Strong).
*   🖐️ **3 dedos:** **Violín** 🎻 (Onda de sierra filtrada con vibrato y envolvente de ataque lento).
*   🖐️ **4 dedos:** **Batería** 🥁 (Percusión directa sin afinación tonal).

### 2. Gestos de la Mano Derecha (Notas Musicales)
Extiende los dedos correspondientes de tu mano derecha para tocar la melodía:

*   🖐️ **1 dedo:** **Do** (C4 - 261.63 Hz) / *Bajo (Bombo)* en batería.
*   🖐️ **2 dedos:** **Re** (D4 - 293.66 Hz) / *Tarola (Snare)* en batería.
*   🖐️ **3 dedos:** **Mi** (E4 - 329.63 Hz) / *Hi-hat cerrado* en batería.
*   🖐️ **4 dedos:** **Fa** (F4 - 349.23 Hz) / *Hi-hat abierto* en batería.
*   🖐️ **5 dedos:** **Sol** (G4 - 392.00 Hz) / *Rimshot (Woodblock)* en batería.

### 3. Control de Volumen Dinámico (Expresión)
La altura de la muñeca de tu mano derecha determina la presión o intensidad:
*   **Subir la mano:** Mapea el volumen hasta el **100%** (indicado en la barra verde lateral).
*   **Bajar la mano:** Atenúa el volumen linealmente hasta llegar al **0%** (silencio).
*   *El volumen se ajusta dinámicamente sobre la nota que ya está sonando.*

---

## ⚡ Consejos de Interpretación Musical

*   **Pulsación de Notas (Plucking):** Para repetir la misma nota (por ejemplo, tocar "Do" tres veces seguidas), simplemente **cierra el puño derecho (0 dedos)** para liberar el disparador y vuelve a abrirlo con 1 dedo.
*   **Ligados rápidos:** Puedes deslizarte entre notas cambiando directamente el número de dedos (por ejemplo, pasar de 1 dedo a 3 dedos). La nueva nota sonará de forma inmediata.
*   **Espejo e Iluminación:** La cámara está configurada con efecto espejo para que mover la mano derecha se sienta natural. Procura tener buena iluminación de fondo para que MediaPipe no pierda el rastreo de tus dedos.

---

## 🔧 Solución de Problemas

> [!WARNING]
> **"Error: No se pudo abrir la cámara web."**
> *   Asegúrate de que ninguna otra aplicación (como Zoom, Teams, Skype, OBS o la cámara de Windows) esté utilizando la cámara web. Cierra esas aplicaciones y vuelve a ejecutar `app.py`.

> [!IMPORTANT]
> **No se escucha sonido al tocar**
> *   Verifica que los archivos de audio se hayan generado correctamente ejecutando `python audio_generator.py`. Deberías ver la creación de 20 archivos `.wav` dentro de la carpeta `audio/`.
> *   Sube el volumen del sistema y asegúrate de que el indicador de volumen del HUD de la aplicación no marque `0%` (sube la mano derecha).

> [!TIP]
> **La detección de manos es inestable**
> *   Mantén tus manos a una distancia cómoda de la cámara (aproximadamente entre 50 cm y 1 metro).
> *   Evita fondos con colores demasiado similares a tu tono de piel o luces directas brillantes detrás de ti.

---

## ⌨️ Comandos del Teclado

*   `Q` o `q`: Presiona esta tecla con la ventana del video activa para cerrar el sintetizador de forma segura y liberar los recursos del sistema.
