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
    from pathlib import Path
    import logging.handlers
    
    # Create logs directory if it doesn't exist
    logs_dir = BASE_DIR / 'logs'
    logs_dir.mkdir(exist_ok=True)
    
    # Configure root logger with file handler
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()
    
    # File handler for all logs (including Flask/Werkzeug)
    app_log_file = logs_dir / 'app.log'
    file_handler = logging.handlers.RotatingFileHandler(
        str(app_log_file),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Console handler for important messages
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Configure Flask/Werkzeug logging
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)
    werkzeug_logger.addHandler(file_handler)
    
    # Configure media converter logging
    # Media converter logger with file handler
    media_converter_logger = logging.getLogger('media_converter')
    media_converter_logger.setLevel(logging.DEBUG)
    
    # File handler for media converter (separate from app log)
    media_converter_file_handler = logging.handlers.RotatingFileHandler(
        str(logs_dir / 'media_converter.log'),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    media_converter_file_handler.setLevel(logging.DEBUG)
    media_converter_file_handler.setFormatter(file_formatter)
    
    # Media converter console handler
    media_converter_console_handler = logging.StreamHandler()
    media_converter_console_handler.setLevel(logging.INFO)
    media_converter_console_handler.setFormatter(console_formatter)
    
    # Add handlers if not already added
    if not media_converter_logger.handlers:
        media_converter_logger.addHandler(media_converter_file_handler)
        media_converter_logger.addHandler(media_converter_console_handler)
    
    # Deface module logger (app.routes) will use root logger handlers
    # But we can add a specific file handler if needed
    deface_logger = logging.getLogger('app.routes')
    deface_logger.setLevel(logging.DEBUG)
    
    # File handler for deface logs
    deface_file_handler = logging.handlers.RotatingFileHandler(
        str(logs_dir / 'deface.log'),
        maxBytes=10*1024*1024,
        backupCount=5
    )
    deface_file_handler.setLevel(logging.DEBUG)
    deface_file_handler.setFormatter(file_formatter)
    
    # Add file handler if not already added
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) and hasattr(h, 'baseFilename') and h.baseFilename == str(logs_dir / 'deface.log') for h in deface_logger.handlers):
        deface_logger.addHandler(deface_file_handler)
    
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

