from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    Config.warn_insecure_defaults()

    db.init_app(app)

    from app.auth import auth_bp
    from app.doctor import doctor_bp
    from app.admin import admin_bp
    from app.patient import patient_bp
    from app.api_patient import api_patient_bp

    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(api_patient_bp, url_prefix='/api/patient')

    # Enable CORS for the mobile JSON API so the H5 front-end can call it
    CORS(app, resources={r'/api/*': {'origins': '*'}})

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
