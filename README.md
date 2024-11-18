# RanchTrack AI - Pig Video Detector

RanchTrack AI is a web application that uses artificial intelligence to detect and track pigs in videos. The system processes uploaded videos and provides tracking information for livestock management.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Virtual Environment Setup](#virtual-environment-setup)
- [Installation](#installation)
- [Project Setup](#project-setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or higher
- pip (Python package manager)
- Git

## Virtual Environment Setup

If you encounter the following error when trying to activate the virtual environment:
```
cannot be loaded because running scripts is disabled on this system
```

Open PowerShell as Administrator and run:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Type 'Y' when prompted for confirmation.

### Creating and Activating Virtual Environment

1. Create virtual environment:
```powershell
python -m venv venv
```

2. Activate virtual environment:
```powershell
venv\Scripts\activate
```

3. To deactivate when finished:
```powershell
deactivate
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ranchtrack-ai.git
cd ranchtrack-ai
```

2. With virtual environment activated, install dependencies:
```bash
pip install -r requirements.txt
```

## Project Setup

1. Create a .env file in the project root:
```bash
# Flask Configuration
FLASK_APP=run.py
FLASK_DEBUG=1
SECRET_KEY=your-super-secret-key-change-this

# Model Configuration
MODEL_CONFIDENCE=0.25

# Tracking Configuration
TRACK_THRESH=0.25
TRACK_BUFFER=30
MATCH_THRESH=0.8
FRAME_RATE=30

# File Limits
MAX_CONTENT_LENGTH=104857600  # 100MB
```

2. Download the YOLOv8 model:
- The model will be downloaded automatically on first run, or
- Download manually from https://github.com/ultralytics/assets/releases/
- Place the downloaded model in the project root directory as `yolov8x.pt`

## Project Structure
```
ranchtrack-ai/
├── app/
│   ├── static/
│   │   └── css/
│   ├── templates/
│   ├── uploads/
│   ├── processed/
│   ├── __init__.py
│   ├── config.py
│   ├── routes.py
│   └── utils.py
├── venv/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Running the Application

1. Ensure your virtual environment is activated:
```bash
venv\Scripts\activate
```

2. Start the Flask development server:
```bash
flask run
```

3. Access the application:
- Open your web browser
- Navigate to `http://localhost:5000`

## Usage

1. Open the web interface
2. Click "Select a file" or drag and drop a video file
3. Wait for the processing to complete
4. Download the processed video with pig detection and tracking

Supported video formats:
- MP4
- AVI
- MOV
- WMV

Maximum file size: 100MB

## Configuration

Key configuration parameters in .env file:

- `MODEL_CONFIDENCE`: Detection confidence threshold (0.0-1.0)
- `TRACK_THRESH`: Tracking threshold for ByteTrack
- `TRACK_BUFFER`: Number of frames to keep track of objects
- `MATCH_THRESH`: Threshold for matching tracked objects
- `FRAME_RATE`: Video processing frame rate

## Troubleshooting

Common issues and solutions:

1. **ModuleNotFoundError**:
   ```bash
   # Verify virtual environment is activated
   venv\Scripts\activate

   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **CUDA/GPU Issues**:
   ```bash
   # Verify CUDA availability
   python -c "import torch; print(torch.cuda.is_available())"
   ```

3. **Memory Issues**:
   - Reduce video resolution before uploading
   - Increase system swap space
   - Process shorter video segments

## Requirements

```txt
flask==3.0.2
ultralytics==8.1.28
supervision==0.19.0
numpy>=1.26.4
opencv-python-headless>=4.9.0.80
python-dotenv==1.0.1
gunicorn==21.2.0
Pillow>=10.0.0
torch>=2.1.0
```

For additional support, please create an issue in the repository.

---
Created by RanchTrack AI Team
