from flask import Blueprint, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from app.utils import allowed_file, process_video, get_progress, save_progress, cleanup_old_files
from app.config import Config
import logging
from threading import Thread

# Initialize Blueprint
main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main.route('/')
@main.route('/index')
def index():
    """Render the main page"""
    return render_template('index.html')

@main.route('/progress')
def get_progress_status():
    """Get the current processing progress"""
    try:
        progress_data = get_progress()
        logger.debug(f'Progress data: {progress_data}')
        return jsonify(progress_data)
    except Exception as e:
        logger.error(f'Error getting progress: {str(e)}')
        return jsonify({'progress': 0})

def process_video_async(input_path, output_path):
    """Process video in a separate thread"""
    try:
        save_progress(0)  # Reset progress
        process_video(input_path, output_path)
        save_progress(100)  # Mark as complete
        logger.info('Video processing completed successfully')
        
        # Cleanup input file after successful processing
        if os.path.exists(input_path):
            os.remove(input_path)
            logger.info(f'Cleaned up input file: {input_path}')
    except Exception as e:
        logger.error(f'Error in async processing: {str(e)}')
        save_progress(0)  # Reset progress on error
        # Cleanup files in case of error
        for path in [input_path, output_path]:
            if os.path.exists(path):
                os.remove(path)
                logger.info(f'Cleaned up file after error: {path}')

@main.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        if 'video' not in request.files:
            logger.error('No file part in request')
            return jsonify({'error': 'No file found'}), 400
        
        file = request.files['video']
        if file.filename == '':
            logger.error('No file selected')
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            logger.error(f'Invalid file type: {file.filename}')
            return jsonify({'error': 'Unsupported file format'}), 400

        filename = secure_filename(file.filename)
        input_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        output_filename = f'processed_{filename}'
        output_path = os.path.join(Config.PROCESSED_FOLDER, output_filename)
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(input_path), exist_ok=True)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        logger.info(f'Saving uploaded file to: {input_path}')
        file.save(input_path)
        
        # Start processing in background thread
        processing_thread = Thread(
            target=process_video_async,
            args=(input_path, output_path)
        )
        processing_thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Processing started',
            'processed_video': f'/processed/{output_filename}'
        })

    except Exception as e:
        logger.error(f'Error in upload handler: {str(e)}')
        return jsonify({'error': str(e)}), 500

@main.route('/processed/<filename>')
def processed_file(filename):
    """Serve processed video files"""
    try:
        file_path = os.path.join(Config.PROCESSED_FOLDER, filename)
        logger.info(f'Attempting to serve file from: {file_path}')
        
        if not os.path.exists(file_path):
            logger.error(f'File not found at path: {file_path}')
            return jsonify({'error': 'File not found'}), 404
            
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='video/mp4'
        )
    except Exception as e:
        logger.error(f'Error sending file: {str(e)}')
        return jsonify({'error': str(e)}), 500