# Pig Detection System

Web application using artificial intelligence to detect, track, and count pigs in videos.

## 🌟 Key Features
- AI-powered pig detection and tracking
- Support for YOLOv8x and YOLOv8s models
- Web interface for easy video processing
- Comparative model testing via console
- Supports multiple video formats

## 📋 Prerequisites

- Python 3.10+
- pip
- Git

## 🚀 Installation

### 1. Clone Repository
```bash
git clone https://github.com/IngRetrius/Pig-detec.git
cd Pig-detec
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

> **Note:** YOLOv8 models are automatically downloaded. Manual download links:
> - [YOLOv8s Model](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt)
> - [YOLOv8x Model](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt)

## 🔧 Virtual Environment Setup

```powershell
python -m venv venv
```

## ⚙️ Configuration

Create `.env` file with the following configuration:
```bash
FLASK_APP=run.py
FLASK_DEBUG=1
SECRET_KEY=your-super-secret-key

MODEL_CONFIDENCE=0.25
TRACK_THRESH=0.25
TRACK_BUFFER=30
MATCH_THRESH=0.8
FRAME_RATE=30

MAX_CONTENT_LENGTH=104857600  # 100MB
```

> **Tip:** To change models, modify `config.py`:
> ```python
> MODEL_PATH = os.path.join(BASE_DIR, 'yolov8x.pt')
> ```

## 🖥️ Running the Application

1. Activate virtual environment:
```bash
venv\Scripts\activate
```

2. Start server:
```bash
flask run
```
Or run `run.py`

3. Access application:
- Open web browser
- Navigate to `http://localhost:5000`

## 🎬 Usage

1. Open web interface
2. Select video file
3. Wait for processing
4. Download processed video with pig detection

### Model Comparison Testing (Console)
The application includes a console-based model comparison system between YOLOv8x and YOLOv8s. This feature allows developers to compare model performance directly via command-line interface.

### Supported Video Formats
- MP4
- AVI
- MOV
- WMV

**Maximum file size:** 100MB

## 📦 Main Dependencies

- Flask 3.0.2
- Ultralytics 8.1.28
- Supervision 0.19.0
- OpenCV Python Headless ≥4.9.0.80
- PyTorch ≥2.1.0

## 🛠️ Troubleshooting

### Virtual Environment Activation
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### VS Code Virtual Environment Setup
1. Ctrl + Shift + P
2. Type "Python: Select Interpreter"
3. Create Virtual Environment
4. Select Venv
5. Delete and Recreate
6. Enter interpreter path
7. Paste virtual environment's python.exe path

# Sistema de Detección de Cerdos

Aplicación web que utiliza inteligencia artificial para detectar, rastrear y contar cerdos en videos.

## 🌟 Características Principales
- Detección y seguimiento de cerdos con IA
- Soporte para modelos YOLOv8x y YOLOv8s
- Interfaz web para procesamiento de videos
- Pruebas comparativas de modelos por consola
- Soporta múltiples formatos de video

## 📋 Requisitos Previos

- Python 3.10+
- pip
- Git

## 🚀 Instalación

### 1. Clonar Repositorio
```bash
git clone https://github.com/IngRetrius/Pig-detec.git
cd Pig-detec
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

> **Nota:** Los modelos YOLOv8 se descargan automáticamente. Enlaces de descarga manual:
> - [Modelo YOLOv8s](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt)
> - [Modelo YOLOv8x](https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8x.pt)

## 🔧 Configuración de Entorno Virtual

```powershell
python -m venv venv
```

## ⚙️ Configuración

Crea un archivo `.env` con la siguiente configuración:
```bash
FLASK_APP=run.py
FLASK_DEBUG=1
SECRET_KEY=tu-clave-secreta-super-segura

MODEL_CONFIDENCE=0.25
TRACK_THRESH=0.25
TRACK_BUFFER=30
MATCH_THRESH=0.8
FRAME_RATE=30

MAX_CONTENT_LENGTH=104857600  # 100MB
```

> **Consejo:** Para cambiar modelos, modifica `config.py`:
> ```python
> MODEL_PATH = os.path.join(BASE_DIR, 'yolov8x.pt')
> ```

## 🖥️ Ejecutar la Aplicación

1. Activar entorno virtual:
```bash
venv\Scripts\activate
```

2. Iniciar servidor:
```bash
flask run
```
O ejecutar `run.py`

3. Acceder a la aplicación:
- Abrir navegador web
- Navegar a `http://localhost:5000`

## 🎬 Uso

1. Abrir interfaz web
2. Seleccionar archivo de video
3. Esperar procesamiento
4. Descargar video procesado con detección de cerdos

### Pruebas de Comparación de Modelos (Consola)
La aplicación incluye un sistema de comparación de modelos por consola entre YOLOv8x y YOLOv8s. Esta característica permite a los desarrolladores comparar el rendimiento de los modelos directamente a través de la interfaz de línea de comandos.

### Formatos de Video Soportados
- MP4
- AVI
- MOV
- WMV

**Tamaño máximo de archivo:** 100MB

## 📦 Dependencias Principales

- Flask 3.0.2
- Ultralytics 8.1.28
- Supervision 0.19.0
- OpenCV Python Headless ≥4.9.0.80
- PyTorch ≥2.1.0

## 🛠️ Resolución de Problemas

### Activación de Entorno Virtual
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Configuración de Entorno Virtual en VS Code
1. Ctrl + Shift + P
2. Escribir "Python: Select Interpreter"
3. Crear Entorno Virtual
4. Seleccionar Venv
5. Eliminar y Recrear
6. Ingresar ruta del intérprete
7. Pegar ruta de python.exe del entorno virtual