import os
import sys
import logging
from flask import Flask, render_template, send_from_directory

# Add parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  

from config.config import Config  
from database.operations.queries import get_all_messages  
from database.db_session import db

# Set up the absolute path for logs
LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_logging(app)
    
    @app.route('/')
    def index():
        app.logger.info("Endpoint '/' accessed.")
        messages, columns = get_all_messages()
        
        if messages is None or columns is None:
            app.logger.error("Problem retrieving messages or columns from the database.")
            return "There was an issue retrieving data from the database.", 500

        return render_template('index.html', messages=messages, db_path=app.config['DATABASE_URL'], headers=columns)

    @app.route('/logs/<filename>')
    def serve_log_file(filename):
        app.logger.info(f"Endpoint '/logs/{filename}' accessed.")
        try:
            return send_from_directory(LOGS_DIR, filename)
        except FileNotFoundError:
            app.logger.error(f"Log file {filename} not found.")
            return "Log file not found.", 404

    @app.route('/log_files')
    def list_log_files():
        app.logger.info("Endpoint '/log_files' accessed.")
        log_files = os.listdir(LOGS_DIR)
        return render_template('log_files.html', log_files=log_files)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()

    return app



def setup_logging(app):
    log_file_path = os.path.join(LOGS_DIR, 'app.log')
    
    if not os.path.exists(log_file_path):
        os.makedirs(LOGS_DIR, exist_ok=True)
        with open(log_file_path, 'w') as f:  # Create an empty 'app.log' file.
            f.write('')

    logging.basicConfig(filename=log_file_path, 
                        level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

app = create_app()

if __name__ == '__main__':
    app.logger.info("Starting the server.")
    app.run(debug=app.config['DEBUG'])
    app.logger.info("Server stopped.")
