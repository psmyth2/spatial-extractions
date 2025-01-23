from flask import Flask
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['UPLOAD_FOLDER'] = 'uploads'

    CORS(app)
    CSRFProtect(app)

    from app.routes import main
    app.register_blueprint(main)

    return app
