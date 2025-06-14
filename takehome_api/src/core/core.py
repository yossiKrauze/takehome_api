from takehome_api.src.config.config import get_logger
from sqlalchemy.orm import Session
import uuid

from takehome_api.src.models.model import Patient, Provider, Appointment, State, Insurance, db
from takehome_api.src.models.response_model import AppointmentResponse

logger = get_logger("core")


class Scheduler:
    def __init__(self, session: Session):
        self.session = session

    def _look_up_patient(self, patient_first_name: str, patient_last_name: str) -> Patient:
        return Patient.query.where(
            Patient.first_name == patient_first_name,
            Patient.last_name == patient_last_name
        ).first()

    def _get_available_providers_per_state_and_insurance(self, state: str, insurance: str) -> list[Provider]:
        return Provider.query.where(
            Provider.states.any(State.state == state),
            Provider.insurances.any(Insurance.name == insurance)).all()

    def _get_available_appointments(self, providers: list[Provider], patient: Patient) -> AppointmentResponse:
        # Hack - get the first available appointment
        first_available_appointment = Appointment.query.where(
            Appointment.provider_id.in_([provider.id for provider in providers])).where(Appointment.patient_id.is_(None)).first()

        if not first_available_appointment:
            logger.error(
                f"No available appointments found for providers: {providers} and patient: {patient}")
            return None

        available_provider = Provider.query.where(
            Provider.id == first_available_appointment.provider_id).first()

        return AppointmentResponse(
            patient=patient.first_name + " " + patient.last_name,
            scheduled=True,
            appointment_id=str(first_available_appointment.id),
            provider=f"{available_provider.title} {available_provider.first_name} {available_provider.last_name}",
            time=first_available_appointment.time.strftime("%Y-%m-%d %H:%M:%S")
        )

    def _set_appointment(self, appointment_id: str, patient_id: str) -> bool:
        try:
            appointment_uuid = uuid.UUID(appointment_id)
            patient_uuid = uuid.UUID(str(patient_id))

            logger.debug(
                f"Looking for appointment with ID: {appointment_uuid}")
            appointment = Appointment.query.where(
                Appointment.id == appointment_uuid).first()

            if not appointment:
                raise Exception(f"Appointment {appointment_id} not found")

            logger.debug(f"Setting patient ID to: {patient_uuid}")
            appointment.patient_id = patient_uuid
            return True
        except Exception as e:
            logger.error("Error setting appointment: %s", e)
            raise e

    def _create_patient(self, patient_data: dict) -> Patient:
        patient = Patient(
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
            email=patient_data["email"],
            state=patient_data["state"],
            insurance=patient_data["insurance"]
        )
        self.session.add(patient)
        self.session.flush()
        return patient

    def schedule_appointment(self, patient_data: dict) -> tuple[AppointmentResponse, bool]:
        try:
            patient = self._look_up_patient(
                patient_data["first_name"], patient_data["last_name"])

            if not patient:
                patient = self._create_patient(patient_data)
                logger.info("Created patient: %s", patient)

            logger.info("Found patient: %s", patient)

            providers = self._get_available_providers_per_state_and_insurance(
                patient.state, patient.insurance)
            logger.info(
                "Found providers for the state and insurance: %s", providers)

            appointment_response = self._get_available_appointments(
                providers, patient)

            if not appointment_response:
                return None, False

            self.session.flush()

            logger.info("Found available appointment: %s",
                        appointment_response.model_dump_json())

            success = self._set_appointment(
                appointment_response.appointment_id, patient.id)
            self.session.commit()
            logger.info(
                f"Appointment set successfully: {success}; for patient: {patient.first_name} {patient.last_name}; appointment ID: {appointment_response.appointment_id}")

            return appointment_response, success
        except Exception as e:
            logger.error("Error looking up patient: %s", e)
            raise e
