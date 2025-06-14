from takehome_api.src.config.database import db
from instance.config import APP_CONFIG
from flask_cors import CORS
from flask import Flask, Response, request
from takehome_api.src.core.core import schedule_appointment
from takehome_api.src.config.config import get_logger

logger = get_logger("main")


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(APP_CONFIG[config_name])

    db.init_db(app)

    @app.route("/")
    def home():
        return str(Response.default_status) + " OK"

    @app.route("/appointment", methods=["POST"])
    def book_appointment():
        data = request.get_json()

        try:
            patient_data = data["patient"]
            appointment_response, success = schedule_appointment(
                db.session, patient_data)

            if success:
                return appointment_response.model_dump_json(), 200
            return {"success": False, "error": f"There are no available appointments for: {patient_data['first_name']} {patient_data['last_name']}"}, 404
        except Exception as e:
            logger.error("Error scheduling appointment: %s", e)
            return {"success": False, "error": f"Error scheduling appointment: {str(e)}"}, 400

    return app
