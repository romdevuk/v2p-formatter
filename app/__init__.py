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
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp, url_prefix='/v2p-formatter')
    
    # Make BASE_DIR available to routes
    app.config['BASE_DIR'] = BASE_DIR
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Run on port 5000 - nginx will proxy port 80 to this
    app.run(debug=True, host='127.0.0.1', port=5000)

