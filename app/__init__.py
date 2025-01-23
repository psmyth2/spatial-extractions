import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

log_file_path = "extraction.log"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    CORS(app)
    CSRFProtect(app)

    # ✅ Configure Logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),  # ✅ Save logs to file
            logging.StreamHandler()  # ✅ Print logs to console
        ]
    )

    from app.routes import main
    app.register_blueprint(main)

    return app
