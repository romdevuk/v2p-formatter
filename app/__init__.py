from flask import Flask
from pathlib import Path
from config import UPLOAD_FOLDER, MAX_CONTENT_LENGTH

# Get the root directory (parent of app directory)
BASE_DIR = Path(__file__).parent.parent

def create_app():
    import logging
    
    app = Flask(__name__, 
                template_folder=str(BASE_DIR / 'templates'),
                static_folder=str(BASE_DIR / 'static'))
    app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure media converter logging
    from pathlib import Path
    import logging.handlers
    
    # Create logs directory if it doesn't exist
    logs_dir = BASE_DIR / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Media converter logger with file handler
    media_converter_logger = logging.getLogger('media_converter')
    media_converter_logger.setLevel(logging.DEBUG)
    
    # File handler (rotating, max 10MB, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        str(logs_dir / 'media_converter.log'),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers if not already added
    if not media_converter_logger.handlers:
        media_converter_logger.addHandler(file_handler)
        media_converter_logger.addHandler(console_handler)
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp, url_prefix='/v2p-formatter')
    
    # Make BASE_DIR available to routes
    app.config['BASE_DIR'] = BASE_DIR
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Use port 5001 to avoid macOS AirPlay Receiver conflict on port 5000
    # Run on port 5001 - nginx will proxy port 80 to this
    app.run(debug=True, host='127.0.0.1', port=5001)

