#!/usr/bin/env python3
import os
from app import create_app
import logging
from dotenv import load_dotenv
import sys
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

def setup_logging():
    """Configure logging with both file and console handlers"""
    # Create logs directory if it doesn't exist
    logs_dir = 'logs'
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Get log level from environment variable
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_file = os.path.join(logs_dir, os.getenv('LOG_FILE', 'app.log'))

    # Configure logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10485760,  # 10MB
        backupCount=5,      # Keep 5 backup files
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Log startup information
    root_logger.info('Application startup')
    root_logger.info(f'Log level set to: {log_level}')

def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)

        # Create app
        app = create_app()

        # Get configuration from environment
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', '1') == '1'

        # Log startup configuration
        logger.info(f'Starting server on {host}:{port}')
        logger.info(f'Debug mode: {debug}')
        logger.info(f'Upload folder: {app.config["UPLOAD_FOLDER"]}')
        logger.info(f'Processed folder: {app.config["PROCESSED_FOLDER"]}')
        
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug
        )

    except Exception as e:
        logger.error(f'Failed to start application: {str(e)}', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()