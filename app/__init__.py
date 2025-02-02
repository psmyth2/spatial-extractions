import logging
import os
import sys
from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

# ✅ Ensure logs directory exists
log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)

# ✅ Set log file path inside a writable directory
log_file_path = os.path.join(log_dir, "extraction.log")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    CORS(app)
    CSRFProtect(app)

    # ✅ Configure Logging to avoid permission issues
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            # ✅ Save logs to a writable directory
            logging.FileHandler(log_file_path),
            logging.StreamHandler(sys.stdout)   # ✅ Print logs to console
        ]
    )

    app.logger.info("Flask app is starting...")

    from app.routes import main
    app.register_blueprint(main)

    return app
