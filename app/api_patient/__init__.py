from flask import Blueprint

api_patient_bp = Blueprint('api_patient', __name__)

from app.api_patient import routes  # noqa: F401, E402
