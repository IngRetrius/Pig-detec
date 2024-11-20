import os
import json
import time
import supervision as sv
from ultralytics import YOLO
import numpy as np
import cv2
import logging
from datetime import datetime, timedelta
from app.config import Config

logger = logging.getLogger(__name__)

# Initialize YOLO model
model = None

def get_model():
    """Get or initialize the YOLO model for inference"""
    global model
    if model is None:
        try:
            logger.info(f"Loading model from {Config.MODEL_PATH}")
            
            # Verificar que el archivo existe
            if not os.path.exists(Config.MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at: {Config.MODEL_PATH}")
                
            # Verificar que el archivo es accesible
            if not os.access(Config.MODEL_PATH, os.R_OK):
                raise PermissionError(f"Cannot read model file at: {Config.MODEL_PATH}")
                
            # Verificar el tamaño del archivo
            file_size = os.path.getsize(Config.MODEL_PATH)
            if file_size < 1000000:  # menos de 1MB probablemente no es un modelo válido
                raise ValueError(f"Model file seems too small: {file_size} bytes")
                
            logger.info(f"Model file verified: {Config.MODEL_PATH} ({file_size} bytes)")
            
            # Cargar el modelo
            model = YOLO(Config.MODEL_PATH)
            model.fuse()
            
            # Verificar que el modelo se cargó correctamente
            if not hasattr(model, 'predict'):
                raise ValueError("Model loaded but seems invalid (no predict method)")
                
            logger.info("Model loaded and verified successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    return model

def process_video(source_path, target_path):
    """Process video file and detect animals"""
    try:
        logger.info(f'Processing video: {source_path}')
        
        # Get video info
        cap = cv2.VideoCapture(source_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file")
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed_frames = 0
        cap.release()

        # Initialize detector
        model = get_model()
        byte_tracker = sv.ByteTrack()
        box_annotator = sv.BoxAnnotator(thickness=4)

        def process_callback(frame: np.ndarray, index: int) -> np.ndarray:
            nonlocal processed_frames
            processed_frames += 1
            
            # Update progress every few frames
            if processed_frames % 10 == 0:
                progress = min(95, (processed_frames / total_frames) * 100)
                save_progress(progress)
                logger.debug(f'Progress: {progress:.2f}%')

            try:
                # Model prediction
                results = model(frame, verbose=False)[0]
                
                # Convert results
                detections = sv.Detections(
                    xyxy=results.boxes.xyxy.cpu().numpy(),
                    confidence=results.boxes.conf.cpu().numpy(),
                    class_id=results.boxes.cls.cpu().numpy().astype(int)
                )
                
                # Filter detections
                mask = np.isin(detections.class_id, Config.SELECTED_CLASSES)
                detections = detections[mask]
                
                # Update tracking
                detections = byte_tracker.update_with_detections(detections)
                
                # Annotate frame
                annotated_frame = frame.copy()
                if len(detections) > 0:
                    labels = [f"Pig #{int(id)}" for id in detections.tracker_id]
                    annotated_frame = box_annotator.annotate(
                        scene=annotated_frame, 
                        detections=detections,
                        labels=labels
                    )
                
                return draw_text_annotations(annotated_frame, detections)
            
            except Exception as e:
                logger.error(f'Error processing frame {index}: {str(e)}')
                return frame

        # Process video
        sv.process_video(
            source_path=source_path,
            target_path=target_path,
            callback=process_callback
        )
        
        # Verify processing was successful
        if not os.path.exists(target_path):
            raise Exception("Processing failed - output file not created")
            
        logger.info('Video processing completed successfully')
        save_progress(100)
        
    except Exception as e:
        logger.error(f'Error processing video: {str(e)}')
        save_progress(0)
        raise

def save_progress(progress):
    """Save current processing progress to file"""
    try:
        progress_file = 'progress.json'
        progress = min(100, max(0, float(progress)))
        with open(progress_file, 'w') as f:
            json.dump({
                'progress': progress,
                'timestamp': time.time()
            }, f)
        logger.debug(f'Progress saved: {progress}%')
    except Exception as e:
        logger.error(f"Error saving progress: {str(e)}")

def get_progress():
    """Get current processing progress from file"""
    try:
        progress_file = 'progress.json'
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                data = json.load(f)
                return {'progress': data.get('progress', 0)}
        return {'progress': 0}
    except Exception as e:
        logger.error(f'Error reading progress: {str(e)}')
        return {'progress': 0}

def allowed_file(filename):
    """Check if a filename has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def draw_text_annotations(frame: np.ndarray, detections) -> np.ndarray:
    """Draw the current frame's animal count and individual labels"""
    try:
        # Draw total count
        position = (30, 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.5
        color = (0, 255, 0)
        thickness = 3

        current_count = len(detections.tracker_id) if len(detections) > 0 else 0
        text = f"Total Animals: {current_count}"
        cv2.putText(frame, text, position, font, scale, color, thickness)

        if len(detections) > 0:
            # Sort detections by x coordinate
            indices = np.argsort([box[0] for box in detections.xyxy])
            for idx in indices:
                x1, y1 = int(detections.xyxy[idx][0]), int(detections.xyxy[idx][1])
                label_position = (x1, y1 - 10)
                label_text = f"Pig #{int(detections.tracker_id[idx])}"
                
                # Add black background for better visibility
                (text_width, text_height), _ = cv2.getTextSize(
                    label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
                )
                cv2.rectangle(
                    frame,
                    (x1, y1 - 30),
                    (x1 + text_width, y1 - 10),
                    (0, 0, 0),
                    -1
                )
                
                cv2.putText(
                    frame,
                    label_text,
                    label_position,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

        return frame
    except Exception as e:
        logger.error(f"Error drawing annotations: {str(e)}")
        return frame

def process_video(source_path, target_path):
    """Process video file and detect animals"""
    logger.info(f'Starting video processing: {source_path} -> {target_path}')
    
    try:
        # Reset progress
        save_progress(0)
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f'Source file not found: {source_path}')
        
        # Get video info
        cap = cv2.VideoCapture(source_path)
        if not cap.isOpened():
            raise ValueError(f'Could not open video: {source_path}')
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        cap.release()

        if total_frames <= 0:
            raise ValueError('Invalid video file: no frames detected')

        # Initialize model and tracker
        model = get_model()
        byte_tracker = sv.ByteTrack(
            track_thresh=Config.TRACK_THRESH,
            track_buffer=Config.TRACK_BUFFER,
            match_thresh=Config.MATCH_THRESH,
            frame_rate=Config.FRAME_RATE
        )
        box_annotator = sv.BoxAnnotator(thickness=4)

        processed_frames = 0
        last_progress_update = time.time()

        def callback(frame: np.ndarray, index: int) -> np.ndarray:
            nonlocal processed_frames, last_progress_update
            processed_frames += 1
            
            # Update progress every second
            current_time = time.time()
            if current_time - last_progress_update >= 1.0:
                progress = min(95, (processed_frames / total_frames) * 100)
                save_progress(progress)
                last_progress_update = current_time
                logger.debug(f'Processing progress: {progress:.2f}%')
            
            try:
                # Model prediction
                results = model(frame, verbose=False)[0]
                
                # Convert results to detections
                detections = sv.Detections(
                    xyxy=results.boxes.xyxy.cpu().numpy(),
                    confidence=results.boxes.conf.cpu().numpy(),
                    class_id=results.boxes.cls.cpu().numpy().astype(int)
                )
                
                # Filter for selected classes (pigs)
                mask = np.isin(detections.class_id, Config.SELECTED_CLASSES)
                detections = detections[mask]
                
                # Update tracking
                detections = byte_tracker.update_with_detections(detections)
                
                # Annotate frame
                annotated_frame = frame.copy()
                if len(detections) > 0:
                    labels = [
                        f"Pig #{int(tracker_id)}"
                        for tracker_id in detections.tracker_id
                    ]
                    
                    annotated_frame = box_annotator.annotate(
                        scene=annotated_frame,
                        detections=detections,
                        labels=labels
                    )
                
                return draw_text_annotations(annotated_frame, detections)
            
            except Exception as e:
                logger.error(f"Error processing frame {index}: {str(e)}")
                return frame

        # Process video with supervision
        sv.process_video(
            source_path=source_path,
            target_path=target_path,
            callback=callback
        )
        
        # Verify the output file exists and has size
        if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
            raise Exception("Output video file is missing or empty")

        # Mark as complete
        save_progress(100)
        logger.info('Video processing completed successfully')

    except Exception as e:
        logger.error(f'Error during video processing: {str(e)}')
        save_progress(0)
        
        # Cleanup on error
        for path in [source_path, target_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    logger.info(f'Cleaned up file: {path}')
                except Exception as cleanup_error:
                    logger.error(f'Error cleaning up file {path}: {str(cleanup_error)}')
        
        raise

def cleanup_old_files(max_age_hours=None):
    """Clean up files older than specified hours"""
    if max_age_hours is None:
        max_age_hours = Config.CLEANUP_INTERVAL
        
    try:
        current_time = datetime.now()
        for folder in [Config.UPLOAD_FOLDER, Config.PROCESSED_FOLDER]:
            if not os.path.exists(folder):
                continue
            
            logger.info(f'Cleaning up folder: {folder}')
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                if current_time - file_modified > timedelta(hours=max_age_hours):
                    try:
                        os.remove(file_path)
                        logger.info(f'Removed old file: {file_path}')
                    except Exception as e:
                        logger.error(f'Error removing file {file_path}: {str(e)}')
                    
    except Exception as e:
        logger.error(f'Error during cleanup: {str(e)}')