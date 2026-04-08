import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/diabetes_system'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GLUCOSE_HIGH = float(os.environ.get('GLUCOSE_HIGH', 11.1))
    GLUCOSE_LOW = float(os.environ.get('GLUCOSE_LOW', 3.9))
