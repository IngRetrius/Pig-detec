import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Base Directory
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    BASE_DIR = os.path.dirname(os.path.dirname(APP_DIR))

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'

    # Model Configuration
    MODEL_PATH = os.path.join(BASE_DIR, 'yolov8x.pt')
    SELECTED_CLASSES = [18, 19]  # sheep (18), cow (19)
    MODEL_CONFIDENCE = float(os.getenv('MODEL_CONFIDENCE', '0.25'))

    # Folder Configuration
    UPLOAD_FOLDER = os.path.join(APP_DIR, 'uploads')
    PROCESSED_FOLDER = os.path.join(APP_DIR, 'processed')
    STATIC_FOLDER = os.path.join(APP_DIR, 'static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

    # File Upload Configuration
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 104857600))  # 100MB
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

    # Tracking Configuration
    TRACK_THRESH = float(os.getenv('TRACK_THRESH', '0.25'))
    TRACK_BUFFER = int(os.getenv('TRACK_BUFFER', '30'))
    MATCH_THRESH = float(os.getenv('MATCH_THRESH', '0.8'))
    FRAME_RATE = int(os.getenv('FRAME_RATE', '30'))