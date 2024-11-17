from flask import Flask
from app.config import Config
import os
import logging

def create_app(config_class=Config):
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload and processed folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    logger.info('Application initialized')
    logger.info(f"Model path: {app.config['MODEL_PATH']}")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Processed folder: {app.config['PROCESSED_FOLDER']}")

    return app