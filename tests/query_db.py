from takehome_api.src.config.database import db
from takehome_api.src.models.model import Patient, Provider, Appointment
from takehome_api.src.config.config import get_logger
from takehome_api.src.models.response_model import ProviderResponse, PatientResponse
from rich import print

logger = get_logger("query_db")


def query_db():
    providers = db.session.query(Provider).all()
    patients = db.session.query(Patient).all()
    appointments = db.session.query(Appointment).all()

    provider_responses = [ProviderResponse(
        first_name=provider.first_name,
        last_name=provider.last_name,
        title=provider.title,
        states=[state.state for state in provider.states],
        insurances=[insurance.name for insurance in provider.insurances],
        appointment_times=[
            appointment.time.strftime("%Y-%m-%d %H:%M:%S") for appointment in appointments if appointment.provider_id == provider.id]
    ) for provider in providers]

    patient_responses = [PatientResponse(
        first_name=patient.first_name,
        last_name=patient.last_name,
        email=patient.email,
        state=patient.state,
        insurance=patient.insurance,
        appointment_times=[
            appointment.time.strftime("%Y-%m-%d %H:%M:%S") for appointment in appointments if appointment.patient_id == patient.id]
    ) for patient in patients]

    print("Providers:")
    for provider in provider_responses:
        print(provider.model_dump_json())

    print("Patients:")
    for patient in patient_responses:
        print(patient.model_dump_json())
