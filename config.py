import os
import warnings
from dotenv import load_dotenv

load_dotenv()

_DEFAULT_SECRET = 'change-me-in-production'
_DEFAULT_JWT_SECRET = 'jwt-secret-change-me-in-production'


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', _DEFAULT_SECRET)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/diabetes_system'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GLUCOSE_HIGH = float(os.environ.get('GLUCOSE_HIGH', 11.1))
    GLUCOSE_LOW = float(os.environ.get('GLUCOSE_LOW', 3.9))

    # JWT configuration for the mobile JSON API
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', _DEFAULT_JWT_SECRET)
    JWT_EXPIRE_DAYS = int(os.environ.get('JWT_EXPIRE_DAYS', 7))

    @classmethod
    def warn_insecure_defaults(cls):
        """Emit a warning when the default insecure SECRET_KEY is in use."""
        if cls.SECRET_KEY == _DEFAULT_SECRET:
            warnings.warn(
                "SECRET_KEY is using the insecure default value. "
                "Set the SECRET_KEY environment variable before deploying to production.",
                UserWarning,
                stacklevel=2,
            )
        if cls.JWT_SECRET_KEY == _DEFAULT_JWT_SECRET:
            warnings.warn(
                "JWT_SECRET_KEY is using the insecure default value. "
                "Set the JWT_SECRET_KEY environment variable before deploying to production.",
                UserWarning,
                stacklevel=2,
            )
