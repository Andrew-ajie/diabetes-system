from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)

    from app.auth import auth_bp
    from app.doctor import doctor_bp
    from app.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
