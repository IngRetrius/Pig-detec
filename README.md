# Pig Detection System

Web system that uses artificial intelligence to detect and track pigs in videos.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

## Virtual Environment Setup

1. Create virtual environment:
```powershell
python -m venv venv
```

2. Activate virtual environment:
```powershell
venv\Scripts\activate
```

## Installation

1. Clone repository:
```bash
git clone https://github.com/IngRetrius/Pig-detec.git
cd Pig-detec
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Note: The YOLOv8 model will be downloaded automatically when you first run the application.

## Configuration

Create `.env` file in project root:
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

## Running the Application

1. Activate virtual environment:
```bash
venv\Scripts\activate
```

2. Start server:
```bash
flask run
```

3. Access application:
- Open web browser
- Go to `http://localhost:5000`

## Usage

1. Open web interface
2. Select video file
3. Wait for processing
4. Download processed video with pig detection

Supported formats:
- MP4
- AVI
- MOV
- WMV

Maximum file size: 100MB

## Main Dependencies

- flask==3.0.2
- ultralytics==8.1.28
- supervision==0.19.0
- opencv-python-headless>=4.9.0.80
- torch>=2.1.0

## Troubleshooting

If there's an error activating virtual environment:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

# Sistema de Detección de Cerdos

Sistema web que utiliza inteligencia artificial para detectar y rastrear cerdos en videos.

## Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git

## Configuración del Entorno Virtual

1. Crear entorno virtual:
```powershell
python -m venv venv
```

2. Activar entorno virtual:
```powershell
venv\Scripts\activate
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/IngRetrius/Pig-detec.git
cd Pig-detec
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

Nota: El modelo YOLOv8 se descargará automáticamente la primera vez que ejecutes la aplicación.

## Configuración

Crear archivo `.env` en la raíz del proyecto:
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

## Ejecutar la Aplicación

1. Activar entorno virtual:
```bash
venv\Scripts\activate
```

2. Iniciar servidor:
```bash
flask run
```

3. Acceder a la aplicación:
- Abrir navegador web
- Ir a `http://localhost:5000`

## Uso

1. Abrir interfaz web
2. Seleccionar archivo de video
3. Esperar procesamiento
4. Descargar video procesado con detección de cerdos

Formatos soportados:
- MP4
- AVI
- MOV
- WMV

Tamaño máximo: 100MB

## Dependencias Principales

- flask==3.0.2
- ultralytics==8.1.28
- supervision==0.19.0
- opencv-python-headless>=4.9.0.80
- torch>=2.1.0

## Solución de Problemas

Si hay error al activar el entorno virtual:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```